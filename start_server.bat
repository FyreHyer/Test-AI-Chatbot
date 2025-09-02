@echo off
REM Windows batch script to start the AI Chatbot Server in production mode

REM Check if Ollama is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo Ollama is not running. Please start Ollama and try again.
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt gunicorn uvicorn

REM Start the server using Uvicorn (Windows version of production server)
echo Starting AI Chatbot Server...
python -m uvicorn app_check_ollama:app --host 0.0.0.0 --port 8080 --workers 4

pause
