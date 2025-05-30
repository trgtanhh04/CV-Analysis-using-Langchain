from openai import OpenAI
from config.config import OPENAI_API_KEY, EMBEDDING_MODEL_NAME

def get_embedding(text: str) -> list:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL_NAME
    )
    return response.data[0].embedding if response.data else []