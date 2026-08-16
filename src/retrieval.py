import numpy as np

def retrieve_context(
        client,
        index,
        chunks,
        question,
        k=5
):

    # Create embedding for the question
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    query_vector = np.array([response.data[0].embedding]).astype("float32")
    # Search the index for the most similar chunks
    distances,indices = index.search(query_vector, k=5)

    context = ""
    for idx in indices[0]:
        context += chunks[idx]["text"]
        context += "\n\n"

        sources = []
    unique_sources = []
    seen = set()
    for idx in indices[0]:
        sources.append({
            "city": chunks[idx]["city"],
            "source": chunks[idx]["source"]
        })
        source_key = (chunks[idx]["city"], chunks[idx]["source"])
        if source_key not in seen:
            seen.add(source_key)
            unique_sources.append({
                "city": chunks[idx]["city"],
                "source": chunks[idx]["source"]
            })
    return context, unique_sources