@echo off
echo ========================================
echo Updating Gemini Package
echo ========================================
echo.

echo Uninstalling old package...
pip uninstall -y google-generativeai

echo.
echo Installing new package...
pip install google-genai

echo.
echo ========================================
echo Update Complete!
echo ========================================
echo.
echo Please restart your backend server.
pause
