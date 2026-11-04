@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
    python python\visualizer.py %*
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        py -3 python\visualizer.py %*
    ) else (
        echo Python 3 was not found. Install Python and add it to PATH.
        pause
        exit /b 1
    )
)
echo.
pause
