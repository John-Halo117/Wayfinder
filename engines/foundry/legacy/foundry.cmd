@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "ROOT_ARG=%ROOT_DIR:~0,-1%"
set "ARK_LEGACY_ROOT=%ROOT_DIR%..\..\..\engines\ark\legacy"
if exist "%ARK_LEGACY_ROOT%" set "PYTHONPATH=%ARK_LEGACY_ROOT%;%PYTHONPATH%"
set "FOUNDRY_PORT=%FOUNDRY_DESKTOP_PORT%"
if not defined FOUNDRY_PORT set "FOUNDRY_PORT=%FORGE_DESKTOP_PORT%"
if not defined FOUNDRY_PORT set "FOUNDRY_PORT=4765"
set "FOUNDRY_URL=http://127.0.0.1:%FOUNDRY_PORT%/"

if /I "%~1"=="--desktop-server" goto desktop_server
if /I "%~1"=="--status" goto status
if /I "%~1"=="--stop" goto stop_desktop
if /I "%~1"=="--cleanup" goto cleanup
if "%~1"=="" goto launch_desktop
goto run

:launch_desktop
call :resolve_python
if errorlevel 1 exit /b 1
call :stop_desktop_listener
start "Foundry" /min "%PYTHON_BIN%" "%ROOT_DIR%ark-core\scripts\ai\forge.py" --repo-root "%ROOT_ARG%" --desktop --no-browser --desktop-port %FOUNDRY_PORT%
set /a ATTEMPT=0
:wait_for_foundry
set /a ATTEMPT+=1
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ProgressPreference = 'SilentlyContinue';" ^
  "$url = '%FOUNDRY_URL%api/state';" ^
  "try { Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 -Uri $url | Out-Null; exit 0 } catch { exit 1 }"
if not errorlevel 1 (
  start "" "%FOUNDRY_URL%"
  exit /b 0
)
if %ATTEMPT% GEQ 40 goto desktop_failed
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Start-Sleep -Seconds 1" >nul 2>nul
goto wait_for_foundry

:desktop_failed
echo Foundry started but the browser app did not become ready at %FOUNDRY_URL%.
echo Retry in a few seconds, or run: "%ROOT_DIR%foundry.cmd --status"
exit /b 1

:stop_desktop_listener
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
  "$port = %FOUNDRY_PORT%;" ^
  "$pids = @(Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique);" ^
  "$foundry = @(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'forge.py' -and $_.CommandLine -match '--desktop-port %FOUNDRY_PORT%' } | Select-Object -ExpandProperty ProcessId);" ^
  "foreach ($procId in @($pids + $foundry | Select-Object -Unique)) { Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue }" >nul 2>nul
exit /b 0

:status
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
  "$url = '%FOUNDRY_URL%api/state';" ^
  "try { Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 -Uri $url | Out-Null; Write-Host 'Foundry is running at %FOUNDRY_URL%'; exit 0 } catch { Write-Host 'Foundry is not running.'; exit 1 }"
exit /b %errorlevel%

:stop_desktop
call :stop_desktop_listener
echo Stopped Foundry browser app if it was running.
exit /b 0

:cleanup
call :stop_desktop_listener
echo Cleaned Foundry desktop listener on %FOUNDRY_PORT%.
exit /b 0

:desktop_server
call :resolve_python
if errorlevel 1 exit /b 1
"%PYTHON_BIN%" "%ROOT_DIR%ark-core\scripts\ai\forge.py" --repo-root "%ROOT_ARG%" --desktop --no-browser --desktop-port %FOUNDRY_PORT%
exit /b %errorlevel%

:run
call :resolve_python
if errorlevel 1 exit /b 1
"%PYTHON_BIN%" "%ROOT_DIR%ark-core\scripts\ai\forge.py" --repo-root "%ROOT_ARG%" %*
exit /b %errorlevel%

:resolve_python
set "PYTHON_BIN=%ROOT_DIR%ark-core\.venv\Scripts\python.exe"
if exist "%PYTHON_BIN%" exit /b 0

where py >nul 2>nul
if not errorlevel 1 (
  for /f "usebackq delims=" %%I in (`py -3 -c "import sys; print(sys.executable)" 2^>nul`) do (
    set "PYTHON_BIN=%%I"
  )
  if defined PYTHON_BIN if exist "%PYTHON_BIN%" exit /b 0
)

where python >nul 2>nul
if not errorlevel 1 (
  for /f "usebackq delims=" %%I in (`where python 2^>nul`) do (
    if not defined PYTHON_BIN if exist "%%I" set "PYTHON_BIN=%%I"
  )
  if defined PYTHON_BIN if exist "%PYTHON_BIN%" exit /b 0
  set "PYTHON_BIN="
)

where python3 >nul 2>nul
if not errorlevel 1 (
  for /f "usebackq delims=" %%I in (`where python3 2^>nul`) do (
    if not defined PYTHON_BIN if exist "%%I" set "PYTHON_BIN=%%I"
  )
  if defined PYTHON_BIN if exist "%PYTHON_BIN%" exit /b 0
  set "PYTHON_BIN="
)

echo Foundry could not find a usable Python interpreter.
exit /b 1
