from openai import OpenAI
from dotenv import load_dotenv
from prompts import TRAVEL_ADVISOR_PROMPT
from retrieval import retrieve_context
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

    conversation_context = ""

    if chat_history:
        for message in chat_history[-3:]:
            conversation_context += (f"User: {message['question']}\n")
            conversation_context += (f"Assistant: {message['answer']}\n")

    context, unique_sources = retrieve_context(client, index, chunks, question, k=5)

    prompt = TRAVEL_ADVISOR_PROMPT.format(
        conversation_context=conversation_context,
        context=context,
        question=question
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }])

    return response.choices[0].message.content, unique_sources


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