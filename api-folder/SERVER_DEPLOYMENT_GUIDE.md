# Server Configuration and Deployment Guide

## System Requirements
- 8GB+ RAM recommended (more for larger models)
- Modern CPU (4+ cores recommended)
- 20GB+ free disk space for model storage
- Linux or Windows server

## Setup Instructions

### Installing Dependencies
1. Install Python 3.8 or newer
2. Install Ollama from https://ollama.com/download
3. Install required Python packages:
   ```
   pip install -r requirements.txt
   pip install gunicorn uvicorn
   ```

### Starting the Server
#### On Linux:
1. Make the start script executable:
   ```
   chmod +x start_server.sh
   ```
2. Run the script:
   ```
   ./start_server.sh
   ```

#### On Windows:
1. Double-click `start_server.bat` or run from command prompt

### Server Configuration
- Edit `gunicorn_config.py` to adjust workers, timeout, etc.
- Default port is 8080, change in the config file if needed

### Firewall Configuration
- Ensure port 8080 (or your custom port) is open on the server firewall
- For internal use only, restrict access to your company network

### Production Deployment Tips
1. Use a process manager like systemd or supervisord to keep the service running
2. Set up a reverse proxy with Nginx or Apache for SSL and load balancing
3. Implement proper authentication for production
4. Set up monitoring and logging

### Example systemd Service (Linux)
Create file `/etc/systemd/system/ai-chatbot.service`:
```
[Unit]
Description=AI Troubleshooting Chatbot
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/ollamachatbot
ExecStart=/path/to/ollamachatbot/start_server.sh
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Then enable and start:
```
sudo systemctl enable ai-chatbot
sudo systemctl start ai-chatbot
```

### Accessing the Chatbot
- Web Interface: http://your-server-ip:8080
- API Endpoint: http://your-server-ip:8080/api/ask

### Monitoring and Maintenance
- Check logs in `access.log` and `error.log`
- Monitor server resources with tools like htop or Windows Task Manager
- Periodically update the model with: `ollama pull llama3.2`
