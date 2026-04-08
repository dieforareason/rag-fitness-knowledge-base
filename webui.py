import logging
from flask import Flask, render_template, request, jsonify
from retriever import Retriever
from llm import LLMClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

logger.info("Initializing RAG backend...")
try:
    retriever = Retriever()
    llm = LLMClient()
except Exception as e:
    logger.error(f"Failed to initialize RAG backend: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        logger.info(f"UI Query received: {query}")
        
        # 1. Retrieve the context from Qdrant
        search_results, contexts = retriever.retrieve(query, top_k=5)
        
        if not contexts:
            return jsonify({
                "answer": "No relevant context found in your fitness documents. Please try rephrasing or ingesting more files.",
                "context_count": 0
            })

        # 2. Get the answer from the local LLM
        answer = llm.generate_answer(query, contexts)
        
        return jsonify({
            "answer": answer,
            "context_count": len(contexts)
        })
        
    except Exception as e:
        logger.error(f"Error during chat interaction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Premium AI Chat Interface on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
