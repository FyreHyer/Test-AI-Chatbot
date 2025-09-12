import re
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import os

# Set environment variables for performance
os.environ["OMP_NUM_THREADS"] = "12"
os.environ["MKL_NUM_THREADS"] = "12"

# Initialize the chatbot components
model = OllamaLLM(model="mistral")

template = """
You are REMABot, an IT support assistant. Use the information provided in the context to help troubleshoot user problems step by step.

CONTEXT FROM KNOWLEDGE BASE:
{solutions}

INSTRUCTIONS:
1. If the question "{question}" is clearly about IT/technical issues and the context contains relevant information, provide a helpful, interactive response.
2. If the question is in a non-English language, politely ask the user to ask in English for better assistance.
3. If the question is about HR, administrative, or non-IT matters (like intern schedules, payroll, workplace concerns), acknowledge their feelings and politely redirect: "I understand this might be challenging. While I'm an IT support assistant and specialize in technical issues, I want to make sure you get the right help. For HR or administrative questions, please contact the HR department. If there are any technical frustrations contributing to your concerns, I'm here to help with those."
4. For short responses like "no", "yes", "no I haven't", "tried that", assume they are responding to common troubleshooting steps and provide the next logical step.
5. For login/access problems to internal systems (rwem.local), first confirm the user is physically in the office or connected to the company network, as these systems cannot be accessed remotely.
6. If the context doesn't contain relevant information for IT questions, say: "I don't have specific information about that in my knowledge base. Please contact ISD support for assistance."
7. Be conversational and helpful - guide the user through troubleshooting.

Common follow-up responses and next steps:
- If user says "no" or "no I haven't" about clearing cache: Provide steps to clear browser cache
- If user says "tried that" or "doesn't work": Ask for specific error messages or try alternative browser
- If user says "yes" to being in office: Proceed with technical troubleshooting steps
- If user says "no" to being in office: Explain they need to be on company network

Answer the question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def get_bot_response(question: str):
    def format_solution_html(text):
        """Auto-format plain text troubleshooting steps as organized HTML."""
        # Add bold to section headers (lines ending with ':')
        text = re.sub(r'^(.*:)$', r'<strong>\1</strong>', text, flags=re.MULTILINE)
        # Convert numbered steps to ordered list
        steps = re.findall(r'\d+\.\s.*', text)
        if steps:
            ol = '<ol>' + ''.join(f'<li>{step[3:]}</li>' for step in steps) + '</ol>'
            text = re.sub(r'(\d+\.\s.*(?:\n\d+\.\s.*)*)', ol, text, flags=re.DOTALL)
        # Convert bullet points to unordered list
        bullets = re.findall(r'^[-*]\s.*', text, flags=re.MULTILINE)
        if bullets:
            ul = '<ul>' + ''.join(f'<li>{b[2:]}</li>' for b in bullets) + '</ul>'
            text = re.sub(r'(^[-*]\s.*(?:\n[-*]\s.*)*)', ul, text, flags=re.MULTILINE)
        # Add line breaks for paragraphs
        text = text.replace('\n', '<br>')
        return text
    """Function to get chatbot response"""
    try:
        docs = retriever.invoke(question)
        solutions = "\n\n".join([doc.page_content for doc in docs])
        
        # If no relevant docs found and question is about REMA Portal, search manually
        if not solutions.strip() and any(term in question.lower() for term in ['rema', 'portal', 'remaportal', 'login', 'access', 'cannot']):
            # Load PDF directly for troubleshooting questions
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader("troubleshooting.pdf")
            pdf_docs = loader.load()
            full_content = '\n'.join([doc.page_content for doc in pdf_docs])
            
            # Extract relevant sections based on keywords
            import re
            patterns = [
                r'Problem: How to access REMA Portal.*?(?=Problem:|$)',
                r'Problem:.*?login.*?(?=Problem:|$)',
                r'Problem:.*?access.*?(?=Problem:|$)',
                r'Problem:.*?cannot.*?(?=Problem:|$)'
            ]
            
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, full_content, re.DOTALL | re.IGNORECASE)
                matches.extend(found)
            
            if matches:
                solutions = '\n\n'.join(matches[:3])  # Limit to 3 most relevant
        
        # Always auto-format the solution as HTML if it looks like a troubleshooting answer
        result = chain.invoke({"solutions": solutions, "question": question})
        # Only format if result is a string (not a dict or error)
        if isinstance(result, str):
            return format_solution_html(result)
        return result
    except Exception as e:
        print(f"Error in get_bot_response: {e}")
        return f"I apologize, but I'm having technical difficulties right now. Error: {str(e)}"
