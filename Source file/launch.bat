@echo off
set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%sys_inspector.py
set LOG_FILE=%SCRIPT_DIR%sys_inspector_log.txt
set ARGS=--basic --network --memory --disk

where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed or not added to PATH. Please install Python and add it to PATH.
    pause
    exit /b 1
)

if not exist "%SCRIPT_PATH%" (
    echo The script "%SCRIPT_PATH%" does not exist. Please make sure the script is in the same directory as this batch file.
    pause
    exit /b 1
)

echo Running Python script: %SCRIPT_PATH% %ARGS%
echo ======================== >> "%LOG_FILE%"
echo Running Python script: %SCRIPT_PATH% %ARGS% >> "%LOG_FILE%"
python "%SCRIPT_PATH%" %ARGS% >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    echo Python script encountered an error. Check "%LOG_FILE%" for details.
) else (
    echo Python script executed successfully. Check "%LOG_FILE%" for details.
)

pause
