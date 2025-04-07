from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.prompts import PromptTemplate
from data_processing import get_document_text, create_index
from chatbot import chatbot


def main():
    pass
if __name__ == "__main__":
    qa_template_str = (
        "You are a helpful customer support assistant for HashFilm (인생네컷).\n"
        "Use the following Q&A document context to accurately answer the user's question.\n"
        "If the user's question is written in Korean, respond in Korean. If it's in any other language, respond in English.\n"
        "If multiple context entries are provided, choose the one that best matches the question.\n"
        "If the user's question is irrelevant to the context (i.e., it cannot be answered based on the Q&A information), "
        "respond politely with: '죄송합니다. 해당 문의에 대한 정보를 찾을 수 없습니다.' for Korean queries or "
        "'I'm sorry, but I don't have information regarding your question.' for non-Korean queries.\n\n"
        "Context:\n{context_str}\n\n"
        "User question: {query_str}\n"
        "Answer:"
    )

    custom_qa_template = PromptTemplate(qa_template_str)

    query_str = "갈비찜 레시피 알려줘"

    index = create_index(get_document_text())

    chatbot = chatbot(index, "deepseek-r1:8b", custom_qa_template)

    print(chatbot._query(query_str))