from openai import OpenAI
from dotenv import load_dotenv
import os
import faiss
import numpy as np
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

all_chunks = []
embeddings = []

for filename in os.listdir("data"):
    if not filename.endswith(".txt"):
        continue

    city = filename.replace(".txt", "")

    with open(f"data/{filename}", "r", encoding="utf-8") as file:
        content = file.read()
        chunks = content.split("\n\n")  # Split by double newlines for paragraphs

        for chunk in chunks:

            all_chunks.append({
                "city": city,
                "source": filename,
                "text": chunk
            })
print(f"Total chunks created: {len(all_chunks)}")

for chunk in all_chunks:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk["text"]
    )
    embedding = response.data[0].embedding
    embeddings.append(embedding)
    #convert embeddings to numpy array
    vectors = np.array(embeddings).astype("float32")
    #create a FAISS index
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)

    #add vectors to the index
    index.add(vectors)

    faiss.write_index(index, "index/travel_index.faiss")

with open("index/chunks.json", "w", encoding="utf-8") as file:
    json.dump(all_chunks, file, ensure_ascii=False, indent=2)
    print("Chunks saved to chunks.json successfully!")
    