@echo off
echo ========================================
echo KILLING ALL CHROME PROCESSES
echo ========================================
echo.

taskkill /F /IM chrome.exe /T 2>nul
if %errorlevel% equ 0 (
    echo [OK] Chrome processes killed
) else (
    echo [INFO] No Chrome processes found
)

echo.
taskkill /F /IM chromedriver.exe /T 2>nul
if %errorlevel% equ 0 (
    echo [OK] ChromeDriver processes killed
) else (
    echo [INFO] No ChromeDriver processes found
)

echo.
echo ========================================
echo DONE!
echo ========================================
echo.
echo You can now run the backend again.
echo.
pause
