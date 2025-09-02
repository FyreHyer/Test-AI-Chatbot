@echo off
echo Installing requirements...
pip install -r requirements.txt requests
echo.
echo Checking if Ollama is installed...
where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Ollama is not installed or not in your PATH.
    echo Please install Ollama from https://ollama.com/download
    echo.
    pause
    exit /b 1
)

echo Running the app with Ollama check...
python app_check_ollama.py
pause
