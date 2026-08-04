with open("data/tokyo.txt", "r", encoding="utf-8") as file:
    content = file.read()

    chunks = content.split("\n\n")  # Split by double newlines for paragraphs
    print(f"Total chunks created: {len(chunks)}")
    print()

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:")
    print(chunk)
    print("-" * 50)  # Separator for readability