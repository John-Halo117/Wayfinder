$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Launcher = Join-Path $RootDir "foundry.ps1"

if (-not (Test-Path $Launcher)) {
    Write-Error "Foundry launcher is missing: $Launcher"
    exit 1
}

& $Launcher @args
exit $LASTEXITCODE
