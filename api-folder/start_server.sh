#!/bin/bash
# Script to start the AI Chatbot Server in production mode

# Activate virtual environment if using one
# source /path/to/venv/bin/activate

# Make sure Ollama is running
if ! pgrep -x "ollama" > /dev/null
then
    echo "Ollama is not running. Starting Ollama..."
    # Uncomment and adjust if you have a way to start Ollama automatically
    # systemctl start ollama || service ollama start
    
    echo "Please start Ollama manually and then restart this script"
    exit 1
fi

# Check if the model exists
echo "Checking for LLaMA model..."
if ! ollama list | grep -q "llama3.2"
then
    echo "LLaMA 3.2 model not found. Pulling model (this may take a while)..."
    ollama pull llama3.2
fi

# Start the server using Gunicorn
echo "Starting AI Chatbot Server..."
gunicorn app_check_ollama:app -c gunicorn_config.py

# For Windows, you would use:
# python -m uvicorn app_check_ollama:app --host 0.0.0.0 --port 8080 --workers 4
