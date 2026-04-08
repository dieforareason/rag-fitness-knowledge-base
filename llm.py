from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, base_url="http://172.24.112.1:1234/v1", api_key="lm-studio", model="qwen-3.5-4b"):
        self.model = model
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

    def generate_answer(self, query, context_chunks):
        context_text = "\n\n---\n\n".join(context_chunks)
        
        prompt = f"""You are a helpful fitness AI assistant.
Answer the user's question ONLY using the provided retrieved context.
If the answer is not in the context, politely state that you do not know.
Avoid hallucination. Provide clear reasoning and reference findings when possible. Keep your answer concise.

CONTEXT:
{context_text}

USER QUESTION:
{query}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior AI engineer specializing in building production-ready RAG systems."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            return "Error: Could not generate an answer from the LLM. Ensure LM Studio is running correctly on http://localhost:1234/v1."
