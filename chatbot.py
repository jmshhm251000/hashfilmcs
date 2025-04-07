from typing import List, Any
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.schema import NodeWithScore, QueryBundle


class chatbot(BaseQueryEngine):
    """
    Custom query engine that retrieves relevant nodes and synthesizes a response based on the user query.
    """

    def __init__(self, index: VectorStoreIndex, model_name: str, custom_qa_template):
        self.index = index
        self.retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=3,
        )
        self.llm = Ollama(model=model_name, request_timeout=120.0)
        self.response_synthesizer = get_response_synthesizer(llm=self.llm, text_qa_template=custom_qa_template)


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