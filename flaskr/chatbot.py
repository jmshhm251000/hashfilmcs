from typing import List, Any
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.core.prompts import PromptTemplate


class Chatbot(BaseQueryEngine):
    """
    Custom query engine that retrieves relevant nodes and synthesizes a response based on the user query.
    """

    def __init__(self, index: VectorStoreIndex, model_name: str):
        self.custom_qa_template = (
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
        self.qa_template = PromptTemplate(self.custom_qa_template)
        self.index = index
        self.retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=3,
        )
        self.llm = Ollama(model=model_name, request_timeout=120.0)
        self.response_synthesizer = get_response_synthesizer(llm=self.llm, text_qa_template=self.qa_template)


    def _query(self, query_str: str) -> Any:
        nodes: List[NodeWithScore] = self.retriever.retrieve(query_str)

        for node in nodes:
            print(node)
        response = self.response_synthesizer.synthesize(query_str, nodes)

        return response


    async def _aquery(self, query_bundle: QueryBundle) -> Any:
        return self._query(query_bundle)


    def _get_prompt_modules(self) -> dict:
        return {}