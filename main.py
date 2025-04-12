from flaskr.chatbot import Chatbot
import os

if __name__ == "__main__":
    DOCUMENT_ID=os.getenv("DOCUMENT_ID")
    SCOPES=['https://www.googleapis.com/auth/documents.readonly']
    chatbot = Chatbot("deepseek-r1:8b", DOCUMENT_ID=DOCUMENT_ID, SCOPES=SCOPES)

    response = chatbot._query("사진이 안나와요.")
    
    node_metadata = response.source_nodes[0].node.metadata
    node_text = response.source_nodes[0].node.text
    node_score = response.source_nodes[0].score
    print("Response.response: ")
    print(response.response)
    print("Node_metadata: ")
    print(node_metadata)
    print("Node_text: ")
    print(node_text)
    print("Node_score: ")
    print(node_score)