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


def ask_travelmate(question, chat_history):
    # Create embedding for the question
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    query_vector = np.array([response.data[0].embedding]).astype("float32")

    # Search the index for the most similar chunks
    distances, indices = index.search(query_vector, k=7)

    context = ""
    for idx in indices[0]:
        context += chunks[idx]["text"]
        context += "\n\n"

    conversation_context = ""
    if chat_history:
        for message in chat_history[-3:]:
            conversation_context += (f"User: {message['question']}\n")
            conversation_context += (f"Assistant: {message['answer']}\n")

    print(conversation_context)

    prompt = f"""
    You are a TravelMate AI, a friendly travel advisor.

    Provide concise, practical travel recommendations.
    
    Answer the user's question using ONLY
    the information provided in the context.

    If the answer cannot be found in the context,
    say:
    'I could not find that information in the travel guide.'

    conversation History: {conversation_context}

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

    sources = []

    for idx in indices[0]:
        sources.append({
            "city": chunks[idx]["city"],
            "source": chunks[idx]["source"]
        })

    print()

    return response.choices[0].message.content, sources


if __name__ == "__main__":

    while True:

        question = input("\nAsk TravelMate: ")

        if question.lower() in ["exit", "quit"]:
            print("Thank you for using TravelMate. Goodbye!")
            break

        answer, sources = ask_travelmate(question)
        print("Answer:")
        print(answer)
        print("-" * 50)  # Separator for readability
        print("sources:")
        for source in sources:
            print(source)