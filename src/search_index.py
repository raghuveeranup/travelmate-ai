from openai import OpenAI
from dotenv import load_dotenv
import os
import faiss
import numpy as np

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load document
with open("data/tokyo.txt", "r", encoding="utf-8") as file:
    content = file.read()

    # Split by double newlines for paragraphs
    chunks = content.split("\n\n")  

    # Generate embeddings for each chunk
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        embedding = response.data[0].embedding
        embeddings.append(embedding)

    # Build FAISS index
    vectors = np.array(embeddings).astype("float32")

    # Create a FAISS index
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)

    # Add vectors to the index
    index.add(vectors)

    #user question

    question = "Which market is know for street food in Tokyo?"

    #create embedding for the question
    question_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )
    question_vector = np.array([question_embedding.data[0].embedding]).astype("float32")

    #search

    distances, indices = index.search(question_vector, k=3)

    best_match_index = indices[0][0]

    print(indices)
    print(distances)

    for idx in indices[0]:
        print(idx)
        print(chunks[idx])
        print("_" * 50)

    print("Question:")

    print(question)
    print()

    print("Best matching chunk:")
    print(chunks[best_match_index])