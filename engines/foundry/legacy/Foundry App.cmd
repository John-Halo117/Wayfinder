@echo off
setlocal

set "ROOT_DIR=%~dp0"
call "%ROOT_DIR%foundry.cmd" %*
exit /b %errorlevel%
