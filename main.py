from flaskr.chatbot.chatbot import Chatbot
import os

if __name__ == "__main__":
    DOCUMENT_ID=os.getenv("DOCUMENT_ID")
    SCOPES=['https://www.googleapis.com/auth/documents.readonly']
    chatbot = Chatbot("deepseek-r1:8b", DOCUMENT_ID=DOCUMENT_ID, SCOPES=SCOPES)

    response = chatbot._query("사진이 안나와요.")
    print("Response.response: ")
    print(response)