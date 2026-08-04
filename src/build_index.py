from openai import OpenAI
from dotenv import load_dotenv
import os
import faiss
import numpy as np
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Load document 
with open("data/tokyo.txt", "r", encoding="utf-8") as file:
    content = file.read()

    # Split by double newlines for paragraphs
    chunks = content.split("\n\n")  

    #generate embeddings for each chunk
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
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

    print(f"Number of vectors stored: {index.ntotal}")

    faiss.write_index(index, "index/travel_index.faiss")
    print("Index created successfully!")
 
with open("index/chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)
    print("Chunks saved to chunks.json successfully!")
