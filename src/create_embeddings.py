from openai import OpenAI
from dotenv import load_dotenv
import os   

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("data/tokyo.txt", "r", encoding="utf-8") as file:
    content = file.read()

    chunks = content.split("\n\n")  # Split by double newlines for paragraphs
    print(f"Total chunks created: {len(chunks)}")
    print()

for i, chunk in enumerate(chunks, start=1):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    embedding = response.data[0].embedding

    print(f"Chunk {i}:")
    print(chunk)
    print("Embedding vector length:", len(embedding))
    print("First 10 elements of the embedding vector:", embedding[:10])
    print("-" * 50)  # Separator for readability