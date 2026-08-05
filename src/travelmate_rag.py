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

question = "what park can i visit in Tokyo?"

#Create embedding for the question

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

query_vector = np.array([response.data[0].embedding]).astype("float32")

#search the index for the most similar chunks

distances, indices = index.search(query_vector, k=5)

context = ""
for idx in indices[0]:
    context += chunks[idx]
    context += "\n\n"

prompt = f"""
You are a TravelMate AI.

Answer the user's question using ONLY
the information provided in the context.

If the answer cannot be found in the context,
say:
'I could not find that information in the travel guide.'

Context: {context}

Question: {question}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }])

print("Question:")
print(question)
print()

print("Answer:")
print(response.choices[0].message.content)

sources = []

for idx in indices[0]:
    sources.append(chunks[idx])

print()
print("Sources:")
print("-" * 50)

for source in sources:
    print(source)
    print("-" * 50)  # Separator for readability

    