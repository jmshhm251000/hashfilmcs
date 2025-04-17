from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import SummaryExtractor, QuestionsAnsweredExtractor
from llama_index.core.schema import MetadataMode
from ..data_processing import Document, VectorStoreIndex


def prepare_documents(documents, extractor_llm, embed_model):
    node_parser = TokenTextSplitter(separator=" ", chunk_size=256)
    extractors = [
        QuestionsAnsweredExtractor(questions=1, llm=extractor_llm, metadata_mode=MetadataMode.EMBED),
        SummaryExtractor(summaries=["self"], llm=extractor_llm)
    ]
    pipeline = IngestionPipeline(transformations=[node_parser, *extractors])
    processed = pipeline.run(documents=documents, in_place=False, show_progress=True)
    
    return VectorStoreIndex(processed, embed_model=embed_model)
