from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from typing import List, Optional
import requests
import sys

# Initialize FastAPI
app = FastAPI(title="Troubleshooting AI Assistant")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Create directories for static files and templates
import os
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Check if Ollama is running
def check_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = [model["name"] for model in response.json().get("models", [])]
            if not models:
                print("No models found in Ollama. Please run: ollama pull llama3.2")
                return False
            
            if "llama3.2" not in models and "llama3.2:latest" not in models:
                print("LLaMA 3.2 model not found. Please run: ollama pull llama3.2")
                return False
            
            print(f"Ollama is running with models: {', '.join(models)}")
            return True
    except requests.exceptions.ConnectionError:
        print("Ollama is not running. Please start Ollama first.")
        return False
    except Exception as e:
        print(f"Error checking Ollama: {e}")
        return False

# Initialize model only if Ollama is running
model = None
chat_history = []

if check_ollama():
    try:
        from langchain_ollama.llms import OllamaLLM
        from langchain_core.prompts import ChatPromptTemplate
        
        # Set up the model and chain
        model = OllamaLLM(model="llama3.2")
        template = """
        You are an expert of troubleshooting software and hardware issues and provide information related to the company

        Here are some solutions: {solutions}

        Here is the question to the answer: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        print("LLM setup successful!")
    except Exception as e:
        print(f"Error initializing LLM: {e}")
else:
    print("Exiting due to Ollama issues.")

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse(
        "chat.html", {"request": request, "chat_history": chat_history, "ollama_running": model is not None}
    )

@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, question: str = Form(...)):
    if model is None:
        result = "Error: Ollama is not running or LLaMA 3.2 model is not available. Please start Ollama and make sure the LLaMA 3.2 model is installed."
    else:
        # Get AI response
        try:
            result = chain.invoke({"solutions": [], "question": question})
        except Exception as e:
            result = f"Error getting response: {str(e)}"
    
    # Add to chat history
    chat_history.append({"question": question, "answer": result})
    
    return templates.TemplateResponse(
        "chat.html", {"request": request, "chat_history": chat_history, "ollama_running": model is not None}
    )

# For API usage
@app.post("/api/ask")
async def ask_question(question: str, solutions: Optional[List[str]] = None):
    if model is None:
        return {"error": "Ollama is not running or LLaMA 3.2 model is not available"}
    
    if solutions is None:
        solutions = []
    
    try:
        result = chain.invoke({"solutions": solutions, "question": question})
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting server... Navigate to http://localhost:8080 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8080)
