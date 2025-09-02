# Production deployment configuration for your AI Chatbot

# Install these packages for production:
# pip install gunicorn uvicorn fastapi

# Directory structure:
# /app
#   /app_check_ollama.py  # Your main app
#   /templates/           # Your templates
#   /static/              # Static files (if any)
#   /gunicorn_config.py   # This file
#   /start_server.sh      # Script to start the server

# Gunicorn configuration for high performance
workers = 4  # Number of worker processes (2-4 x num_cores is recommended)
worker_class = 'uvicorn.workers.UvicornWorker'  # Use Uvicorn's worker class for ASGI
bind = '0.0.0.0:8080'  # Bind to all network interfaces, port 8080
timeout = 120  # Increase timeout for LLM responses which can be slow
keepalive = 5  # Keep connections alive for 5 seconds
accesslog = 'access.log'  # Access log file
errorlog = 'error.log'  # Error log file
loglevel = 'info'  # Log level

# Recommended worker processes calculation
# import multiprocessing
# workers = multiprocessing.cpu_count() * 2 + 1
