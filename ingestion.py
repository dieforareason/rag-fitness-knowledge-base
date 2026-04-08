import os
import glob
import logging
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
from qdrant_store import QdrantStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeIngestor:
    def __init__(self, data_dir="data/pdfs"):
        self.data_dir = data_dir
        self.store = QdrantStore()

    def process_folder(self):
        pdf_files = glob.glob(os.path.join(self.data_dir, "*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.data_dir}")
            return

        for pdf_path in pdf_files:
            logger.info(f"Processing {pdf_path}...")
            self._process_single_pdf(pdf_path)

    def _process_single_pdf(self, pdf_path):
        try:
            # Parse text from PDF using unstructured
            elements = partition_pdf(filename=pdf_path)
            
            # Semantic chunking by title, suitable for research papers
            # Trying to keep chunk size around 300-800 tokens logically
            chunks = chunk_by_title(
                elements,
                max_characters=2500,
                new_after_n_chars=1500,
                combine_text_under_n_chars=500
            )
            
            texts = []
            metadatas = []
            
            for chunk in chunks:
                text = chunk.text
                if not text.strip():
                    continue
                
                texts.append(text)
                
                # Assign metadata payload
                metadata = {
                    "source_file": os.path.basename(pdf_path),
                    "title": chunk.metadata.to_dict().get("title", "Unknown"),
                }
                metadatas.append(metadata)

            if texts:
                self.store.store_chunks(texts, metadatas)
                logger.info(f"Successfully ingested {len(texts)} chunks from {pdf_path}")
                
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")

if __name__ == "__main__":
    if not os.path.exists("data/pdfs"):
        os.makedirs("data/pdfs")
        logger.info("Created data/pdfs folder. Please place your PDFs there and run again.")
    else:
        ingestor = KnowledgeIngestor()
        ingestor.process_folder()
