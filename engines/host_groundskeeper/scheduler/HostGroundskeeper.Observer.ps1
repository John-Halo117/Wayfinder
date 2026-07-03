<#
.SYNOPSIS
Minimal Windows-native Host Groundskeeper observer.

.DESCRIPTION
Installs, uninstalls, or runs a bounded observation pass. The script uses
Task Scheduler, Windows Event Log, powercfg, CIM/performance counters, and
standard Windows APIs. It does not change power plans, inspect process contents,
optimize hardware, run AI, or install a Windows service.
#>

[CmdletBinding()]
param(
    [ValidateSet("Install", "Uninstall", "RunOnce")]
    [string] $Mode = "RunOnce",
    [string] $StatePath = "$env:ProgramData\Wayfinder\HostGroundskeeper\state.json",
    [string] $TelemetryPath = "$env:ProgramData\Wayfinder\HostGroundskeeper\observations.jsonl",
    [int] $CpuUtilizationThreshold = 2,
    [int] $MemoryMbThreshold = 256,
    [int] $DiskFreeMbThreshold = 1024,
    [int] $CoalesceSeconds = 5
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$EventSource = "WayfinderHostGroundskeeper"
$EventLog = "Application"
$TaskName = "Wayfinder Host Groundskeeper Observer"
$MaxProcesses = 512
$MaxDisks = 32
$MaxCounters = 32

function Ensure-EventSource {
    if (-not [System.Diagnostics.EventLog]::SourceExists($EventSource)) {
        New-EventLog -LogName $EventLog -Source $EventSource
    }
}

function Write-GroundskeeperLog {
    param([string] $Message, [int] $EventId = 4200)
    Ensure-EventSource
    Write-EventLog -LogName $EventLog -Source $EventSource -EventId $EventId -EntryType Information -Message $Message
}

function Ensure-ParentDirectory {
    param([string] $Path)
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
}

function Read-State {
    if (-not (Test-Path -LiteralPath $StatePath)) {
        return @{}
    }
    $json = Get-Content -LiteralPath $StatePath -Raw
    if ([string]::IsNullOrWhiteSpace($json)) {
        return @{}
    }
    $state = ConvertFrom-Json -InputObject $json -AsHashtable
    if ($null -eq $state) {
        return @{}
    }
    return $state
}

function Write-State {
    param([hashtable] $State)
    Ensure-ParentDirectory -Path $StatePath
    $State | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $StatePath -Encoding UTF8
}

function Get-ActivePowerPlan {
    $output = powercfg /GETACTIVESCHEME
    return ($output -join " ").Trim()
}

function Get-ForegroundProcessName {
    Add-Type -ErrorAction SilentlyContinue -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class WfForegroundWindow {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
}
"@
    $processId = 0
    $handle = [WfForegroundWindow]::GetForegroundWindow()
    [WfForegroundWindow]::GetWindowThreadProcessId($handle, [ref] $processId) | Out-Null
    if ($processId -le 0) {
        return "unknown"
    }
    try {
        return (Get-Process -Id $processId -ErrorAction Stop).ProcessName
    } catch {
        return "unknown"
    }
}

function Get-ProcessSnapshot {
    $items = Get-Process | Select-Object -First $MaxProcesses -Property ProcessName, Id
    $names = @()
    foreach ($item in $items) {
        if ($names.Count -ge $MaxProcesses) { break }
        $names += "$($item.ProcessName):$($item.Id)"
    }
    return $names
}

function Get-HostSnapshot {
    $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
    $os = Get-CimInstance Win32_OperatingSystem | Select-Object -First 1
    $disks = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Select-Object -First $MaxDisks
    $gpuCounters = @()
    try {
        $gpuCounters = Get-Counter '\GPU Engine(*)\Utilization Percentage' -ErrorAction Stop |
            Select-Object -ExpandProperty CounterSamples |
            Select-Object -First $MaxCounters
    } catch {
        $gpuCounters = @()
    }

    $diskValues = @()
    foreach ($disk in $disks) {
        if ($diskValues.Count -ge $MaxDisks) { break }
        $freeMb = [math]::Round(($disk.FreeSpace / 1MB), 0)
        $sizeMb = [math]::Round(($disk.Size / 1MB), 0)
        $diskValues += "$($disk.DeviceID):$freeMb/$sizeMb"
    }

    $gpuUtil = 0
    foreach ($counter in $gpuCounters) {
        if ($gpuUtil -lt $counter.CookedValue) {
            $gpuUtil = [math]::Round($counter.CookedValue, 2)
        }
    }

    return @{
        Cpu = @{
            utilization_percent = [int] $cpu.LoadPercentage
            frequency_mhz = [int] $cpu.CurrentClockSpeed
            logical_count = [int] $cpu.NumberOfLogicalProcessors
            core_count = [int] $cpu.NumberOfCores
            package_temperature_celsius = $null
        }
        Gpu = @{
            utilization_percent = $gpuUtil
            vram_megabytes = $null
            temperature_celsius = $null
        }
        Memory = @{
            total_megabytes = [math]::Round($os.TotalVisibleMemorySize / 1024, 0)
            available_megabytes = [math]::Round($os.FreePhysicalMemory / 1024, 0)
            used_megabytes = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1024, 0)
            committed_megabytes = [math]::Round($os.TotalVirtualMemorySize / 1024, 0)
        }
        Storage = @{
            disks = $diskValues
        }
        Process = @{
            foreground_application = Get-ForegroundProcessName
            processes = Get-ProcessSnapshot
        }
        Windows = @{
            active_power_plan = Get-ActivePowerPlan
            monitor_state = "unknown"
            sleep_state = "unknown"
        }
    }
}

function Get-Delta {
    param([object] $Previous, [object] $Current, [int] $NumericThreshold)
    if ($null -eq $Previous) {
        return $Current
    }
    if (($Previous -is [int] -or $Previous -is [double]) -and ($Current -is [int] -or $Current -is [double])) {
        if ([math]::Abs([double] $Current - [double] $Previous) -ge $NumericThreshold) {
            return $Current
        }
        return $null
    }
    if (($Previous | ConvertTo-Json -Depth 8 -Compress) -ne ($Current | ConvertTo-Json -Depth 8 -Compress)) {
        return $Current
    }
    return $null
}

function Publish-Observation {
    param([hashtable] $Observation)
    Ensure-ParentDirectory -Path $TelemetryPath
    $line = $Observation | ConvertTo-Json -Depth 8 -Compress
    Add-Content -LiteralPath $TelemetryPath -Value $line -Encoding UTF8
    Write-GroundskeeperLog -Message $line -EventId 4201
}

function Invoke-RunOnce {
    $state = Read-State
    $snapshot = Get-HostSnapshot
    $timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $changed = 0

    $observationNames = @{
        Cpu = "HostCpuChanged"
        Gpu = "HostGpuChanged"
        Memory = "MemoryChanged"
        Storage = "DiskUsageChanged"
        Process = "ForegroundApplicationChanged"
        Windows = "PowerPlanChanged"
    }

    foreach ($name in @("Cpu", "Gpu", "Memory", "Storage", "Process", "Windows")) {
        $previous = $state[$name]
        $current = $snapshot[$name]
        $threshold = 1
        if ($name -eq "Cpu") { $threshold = $CpuUtilizationThreshold }
        if ($name -eq "Memory") { $threshold = $MemoryMbThreshold }
        if ($name -eq "Storage") { $threshold = $DiskFreeMbThreshold }
        $delta = Get-Delta -Previous $previous -Current $current -NumericThreshold $threshold
        if ($null -ne $delta) {
            $observation = @{
                timestamp = $timestamp
                observation = $observationNames[$name]
                source = "windows.powershell"
                confidence = 0.8
                delta = $delta
                values = $current
            }
            Publish-Observation -Observation $observation
            $changed += 1
        }
        $state[$name] = $current
    }

    $previousProcesses = @()
    if ($null -ne $state["LastProcesses"]) { $previousProcesses = @($state["LastProcesses"]) }
    $currentProcesses = @($snapshot["Process"]["processes"])
    $started = @($currentProcesses | Where-Object { $previousProcesses -notcontains $_ } | Select-Object -First 128)
    $exited = @($previousProcesses | Where-Object { $currentProcesses -notcontains $_ } | Select-Object -First 128)
    foreach ($process in $started) {
        Publish-Observation -Observation @{ timestamp = $timestamp; observation = "ProcessStarted"; source = "windows.powershell"; confidence = 0.9; delta = @{ process = $process }; values = @{ process = $process } }
        $changed += 1
    }
    foreach ($process in $exited) {
        Publish-Observation -Observation @{ timestamp = $timestamp; observation = "ProcessExited"; source = "windows.powershell"; confidence = 0.9; delta = @{ process = $process }; values = @{ process = $process } }
        $changed += 1
    }
    $state["LastProcesses"] = $currentProcesses

    Write-State -State $state
    Write-GroundskeeperLog -Message "Host observer completed; observations=$changed; no optimization actions performed." -EventId 4202
}

function Install-Observer {
    Ensure-EventSource
    Ensure-ParentDirectory -Path $StatePath
    $script = $PSCommandPath
    $argument = "-NoProfile -ExecutionPolicy Bypass -File `"$script`" -Mode RunOnce"
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $argument
    $logon = New-ScheduledTaskTrigger -AtLogOn
    $startup = New-ScheduledTaskTrigger -AtStartup
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 2)
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($logon, $startup) -Settings $settings -Description "Wayfinder Host Groundskeeper observation pass; no optimization actions." -Force | Out-Null
    Write-GroundskeeperLog -Message "Installed Host Groundskeeper observer scheduled task." -EventId 4203
}

function Uninstall-Observer {
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }
    if (Test-Path -LiteralPath $StatePath) {
        Remove-Item -LiteralPath $StatePath -Force
    }
    Write-GroundskeeperLog -Message "Uninstalled Host Groundskeeper observer scheduled task and state." -EventId 4204
}

if ($Mode -eq "Install") {
    Install-Observer
} elseif ($Mode -eq "Uninstall") {
    Uninstall-Observer
} else {
    Invoke-RunOnce
}
