from llama_index.core.response_synthesizers import get_response_synthesizer
from flaskr.data_processing import get_document_text, create_index
from flaskr.chatbot import Chatbot


def main():
    pass
if __name__ == "__main__":

    query_str = "갈비찜 레시피 알려줘"

    index = create_index(get_document_text())

    chatbot = Chatbot(index, "deepseek-r1:8b")

    print(chatbot._query(query_str))