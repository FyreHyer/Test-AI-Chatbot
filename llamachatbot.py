from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

template = """
You are an expert of providing solutions for software and hardware problems and provide information regarding ROHM company
Here are some solutions: {solutions}
Here are some information:{information}

Here is the question to the answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain  = prompt | model

result = chain.invoke({"solutions": [],"information": [], "question": "Who is the president of ROHM?"})

print(result)




