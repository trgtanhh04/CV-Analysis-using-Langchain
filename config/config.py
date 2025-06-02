import os

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_cvs")

# Config database
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "cvdb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Local database URL
# DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Render database URL (for production)
DATABASE_URL = f"postgresql://postgres123:saW3kXjXXHZT3xni4cVCkM0tBQJpuKP2@dpg-d0ujljmmcj7s739op7og-a.oregon-postgres.render.com:5432/cvdb_65c9"


# API Key và loại Embedding
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-ada-002")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-3.5-turbo")

