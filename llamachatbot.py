from langchain_community.document_loaders import PyPDFLoader 
from chatbot_core import get_bot_response

print("---------------------------------------------------------------------")
question = input("Enter your question (type 'q' to quit): ")
print("---------------------------------------------------------------------")
if question.lower() == 'q':
    print("Exiting chatbot.")

result = get_bot_response(question)
print(result)

while True:
    print("---------------------------------------------------------------------")
    question = input("Enter your question (type 'q' to quit): ")
    print("---------------------------------------------------------------------")
    if question.lower() == 'q':
        print("Exiting chatbot.")
        break

    result = get_bot_response(question)
    print(result)











