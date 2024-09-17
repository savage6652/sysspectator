@echo off
setlocal

set SCRIPT_NAME=sys_inspector.py
set EXE_NAME=sys_inspector.exe
set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%%SCRIPT_NAME%
set DIST_DIR=%SCRIPT_DIR%dist
set EXE_PATH=%DIST_DIR%\%EXE_NAME%

if not exist "%SCRIPT_PATH%" (
    echo The script "%SCRIPT_PATH%" does not exist. Please make sure the script is in the same directory as this batch file.
    pause
    exit /b 1
)

python -m PyInstaller --onefile --name %EXE_NAME% "%SCRIPT_PATH%"

if exist "%EXE_PATH%" (
    echo Executable created successfully: %EXE_PATH%
) else (
    echo Failed to create executable. Check the output for errors.
)

pause
