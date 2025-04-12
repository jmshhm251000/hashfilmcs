import nest_asyncio
nest_asyncio.apply()

import logging
import time
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("chatbot_logger")
logger.setLevel(logging.INFO)

log_handler = logging.FileHandler("chatbot_queries.json")
formatter = jsonlogger.JsonFormatter()
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

import asyncio
from typing import List, Any
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.schema import NodeWithScore, QueryBundle, MetadataMode
from llama_index.core.prompts import PromptTemplate
from llama_index.core.extractors import SummaryExtractor, QuestionsAnsweredExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from .data_processing import get_document_text, VectorStoreIndex, Document
from llama_index.core.node_parser import TokenTextSplitter


class Chatbot(BaseQueryEngine):
    """
    Custom query engine that retrieves relevant nodes and synthesizes a response based on the user query.
    """
    def __init__(self, model_name: str, DOCUMENT_ID, SCOPES):
        # Retrieve documents from Google Docs API using provided document ID and scopes
        self.document = get_document_text(DOCUMENT_ID, SCOPES)
        self.llm = Ollama(model=model_name, request_timeout=120.0)
        self.extractor_llm = Ollama(model="llama3.2", request_timeout=120.0)
        self.node_parser = TokenTextSplitter(separator=" ", chunk_size=256, chunk_overlap=0)
        self.embed_model = HuggingFaceEmbedding(model_name="jhgan/ko-sbert-nli")
        
        # Set up metadata extractors
        self.extractors = (
            QuestionsAnsweredExtractor(questions=1, llm=self.extractor_llm, metadata_mode=MetadataMode.EMBED),
            SummaryExtractor(summaries=["self"], llm=self.extractor_llm)
        )
        self.pipeline = IngestionPipeline(transformations=[self.node_parser, *self.extractors])
        
        if self.document:
            #self.processed_documents = asyncio.run(self.process_all_documents(self.document))
            self.processed_documents = self.pipeline.run(documents=self.document, in_place=False, show_progress=False)
            #combined_docs = self.document + self.processed_documents if self.processed_documents else self.document
            self.index = VectorStoreIndex(self.processed_documents, embed_model=self.embed_model)
        else:
            self.processed_documents = None
            self.index = VectorStoreIndex([], embed_model=self.embed_model)
        
        self.custom_qa_template = (
            "You are a helpful customer support assistant for HashFilm (인생네컷).\n"
            "Use the following Q&A document context to accurately answer the user's question.\n"
            "If the user's question is written in Korean, respond in Korean. If it's in any other language, respond in English.\n"
            "If multiple context entries are provided, choose the one that best matches the question.\n"
            "If the user's question is irrelevant to the context (i.e., it cannot be answered based on the Q&A information),"
            "respond politely with: '해당 문의에 대한 정보를 찾을 수 없습니다.' for Korean queries or "
            "'I'm sorry, but I don't have information regarding your question.' for non-Korean queries.\n"
            "Context:\n{context_str}\n\n"
            "Context Metadata:\n{metadata_str}\n\n"
            "User question: {query_str}\n"
            "Answer:"
        )
        self.qa_template = PromptTemplate(self.custom_qa_template)
        self.retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=3,
        )
        self.response_synthesizer = get_response_synthesizer(llm=self.llm, text_qa_template=self.qa_template)


    def _query(self, query_str: str) -> Any:
        start_time = time.perf_counter()

        nodes: List[NodeWithScore] = self.retriever.retrieve(query_str)
        response = self.response_synthesizer.synthesize(query_str, nodes)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            "query": query_str,
            "response": str(response),
            "elapsed_time_sec": round(elapsed_time, 4),
            "retrieved_nodes": [
                {
                    "node_id": node.node.node_id,
                    "score": node.score,
                    "metadata": node.node.metadata
                }
                for node in nodes
            ]
        }

        logger.info(log_entry)

        return response


    async def _aquery(self, query_bundle: QueryBundle) -> Any:
        return self._query(query_bundle.query_str)


    def _get_prompt_modules(self) -> dict:
        return {}
    

    def process_document(self, document: Document) -> List:
        # Run the pipeline synchronously on a single document (wrapped in a list)
        return self.pipeline.run(documents=[document], in_place=False, show_progress=False)


    async def process_all_documents(self, documents: List[Document], max_concurrent_tasks: int = 10) -> List:
        # Limit the number of concurrent tasks using a semaphore.
        sem = asyncio.Semaphore(max_concurrent_tasks)
        
        async def limited_process_document(doc: Document) -> List:
            async with sem:
                return await asyncio.to_thread(self.process_document, doc)
        
        tasks = [limited_process_document(doc) for doc in documents]
        results = await asyncio.gather(*tasks)
        # Flatten the list of lists
        flat_results = [node for sublist in results for node in sublist]
        return flat_results