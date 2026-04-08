import argparse
import sys
import logging
from retriever import Retriever
from llm import LLMClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Fitness Knowledge Base RAG System")
    parser.add_argument("query", type=str, nargs="?", help="Your fitness-related question")
    args = parser.parse_args()

    if not args.query:
        print("Usage: python app.py \"your question\"")
        sys.exit(1)

    query = args.query
    logger.info(f"Question: {query}")

    logger.info("Retrieving relevant context from Vector DB...")
    retriever = Retriever()
    search_results, contexts = retriever.retrieve(query, top_k=5)

    if not contexts:
        logger.warning("No relevant context found in the vector database. Did you ingest documents?")
    else:
        logger.info(f"Found {len(contexts)} relevant chunks.")

    logger.info("Generating answer with local LLM (Qwen)...")
    llm = LLMClient(model="qwen-3.5-0.8b")
    answer = llm.generate_answer(query, contexts)

    print("\n" + "="*50)
    print("ANSWER:")
    print("="*50)
    print(answer)
    print("="*50)

if __name__ == "__main__":
    main()
