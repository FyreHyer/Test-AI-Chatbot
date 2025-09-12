from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from chatbot_core import get_bot_response

app = FastAPI(title="REMABot API", description="AI Chatbot for IT Support")

# Mount static files to serve images and other assets
app.mount("/static", StaticFiles(directory="."), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the HTML file at the root URL
@app.get("/")
def serve_chat_ui():
    return FileResponse("chat_ui.html")

#API endpoint for chat
@app.post("/chat")
def chat(message: dict):
    import time
    start_time = time.time()
    try:
        print(f"Received chat request: {message}")
        user_question = message.get("question")
        if not user_question:
            return {"error": "No question provided"}
        
        print(f"Processing question: '{user_question}'")
        response = get_bot_response(user_question)
        
        elapsed_time = time.time() - start_time
        print(f"Response generated in {elapsed_time:.2f} seconds")
        
        return {"response": response}
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_msg = f"API Error after {elapsed_time:.2f}s: {e}"
        print(error_msg)
        return {"error": f"Server error: {str(e)}"}

#API endpoint for health check
@app.get("/health")
def health_check():
    return {"status": "REMABot is running smoothly."}

