from openai import OpenAI
from dotenv import load_dotenv
import os
import faiss
import numpy as np
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Load FAISS index
index = faiss.read_index("index/travel_index.faiss")

# Load chunks from JSON file
with open("index/chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

question = "Which market is know for street food ?"

#Create embedding for the question

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

query_vector = np.array([response.data[0].embedding]).astype("float32")

#search the index for the most similar chunks

distances, indices = index.search(query_vector, k=3)

print("Top Results")
print()

for idx in indices[0]:
    print(chunks[idx])
    print("-" * 50)  # Separator for readability)
