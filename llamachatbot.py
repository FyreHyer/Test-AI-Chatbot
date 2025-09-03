from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader 
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in providing solutions for software and hardware problems, but you can also answer other questions. Use the following context if it is relevant: {solutions}

If the context is not related to the question, ignore it and answer naturally or say there is no information available.

Answer the question: {question}
Do not repeat answers. If the user wants to talk about something else, change the topic.
If all solutions have been used and none worked, tell the user to contact ISD support.
"""

prompt = ChatPromptTemplate.from_template(template)
chain  = prompt | model

print("---------------------------------------------------------------------")
question = input("Enter your question (type 'q' to quit): ")
print("---------------------------------------------------------------------")
if question.lower() == 'q':
    print("Exiting chatbot.")

 # Retrieve context and get answer
docs = retriever.get_relevant_documents(question)
solutions = "\n\n".join([doc.page_content for doc in docs])

print("\n--- Retrieved Context ---\n")
print(solutions)
print("\n--- End of Context ---\n")

result = chain.invoke({"solutions": solutions, "question": question})
print(result)

while True:
    

    print("---------------------------------------------------------------------")
    question = input("Enter your question (type 'q' to quit): ")
    print("---------------------------------------------------------------------")
    if question.lower() == 'q':
        print("Exiting chatbot.")
        break
    docs = retriever.get_relevant_documents(question)
    solutions = "\n\n".join([doc.page_content for doc in docs])

    print("\n--- Retrieved Context ---\n")
    print(solutions)
    print("\n--- End of Context ---\n")

    result = chain.invoke({"solutions": solutions,"question": question})
    print(result)


print(result)











