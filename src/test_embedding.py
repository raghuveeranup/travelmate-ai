from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Ameyoko Market is known for street food."
)

embedding = response.data[0].embedding

print("Embedding vector length:", len(embedding))
print()
print("First 10 elements of the embedding vector:", embedding[:10])