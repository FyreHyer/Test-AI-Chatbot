from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from typing import List, Optional

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize FastAPI
app = FastAPI(title="Troubleshooting AI Assistant")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Create directories for static files and templates
import os
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Set up the model and chain
model = OllamaLLM(model="llama3.2")
template = """
You are an expert of troubleshooting software and hardware issues and provide information related to the company

Here are some solutions: {solutions}

Here is the question to the answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Store chat history (in a real app, use a database)
chat_history = []

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse(
        "chat.html", {"request": request, "chat_history": chat_history}
    )

@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, question: str = Form(...)):
    # Get AI response
    result = chain.invoke({"solutions": [], "question": question})
    
    # Add to chat history
    chat_history.append({"question": question, "answer": result})
    
    return templates.TemplateResponse(
        "chat.html", {"request": request, "chat_history": chat_history}
    )

# For API usage
@app.post("/api/ask")
async def ask_question(question: str, solutions: Optional[List[str]] = None):
    if solutions is None:
        solutions = []
    
    result = chain.invoke({"solutions": solutions, "question": question})
    return {"response": result}

if __name__ == "__main__":
    print("Starting server... Navigate to http://localhost:8080 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8080)
