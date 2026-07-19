$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Launcher = Join-Path $RootDir "foundry.cmd"

if (-not (Test-Path $Launcher)) {
    Write-Error "Foundry launcher is missing: $Launcher"
    exit 1
}

& $Launcher @args
exit $LASTEXITCODE
