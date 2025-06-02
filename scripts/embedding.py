from openai import OpenAI
from config.config import OPENAI_API_KEY, EMBEDDING_MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text: str) -> list:
    try:
        response = client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL_NAME
        )
        return response.data[0].embedding if response.data else []
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []
    
    