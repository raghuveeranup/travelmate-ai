📍 This Project aims at learning and applying below AI Engineering concepts

✅ Embeddings
✅ Vector Search
✅ FAISS
✅ Chunking
✅ Retrieval
✅ Metadata
✅ Prompt Engineering
✅ Hallucination Prevention
✅ RAG
✅ Streamlit UI

📍 Architecture 

Travel Guides -> Chunking -> Embeddings -> FAISS

User Question -> Conversation-Aware Retrieval -> Context -> GPT -> Answer

📍 Features:
✅ Multi-City travel guides
✅ Conversation RAG
✅ Metadata-aware retrieval
✅ Source attribution

📍 Responsibilitites

app.py
✅ Streamlit UI
✅ Chat Interface
✅ Session State
✅ Chat History

travelmate_rag.py
✅ Conversation History
✅ Prompt contruction
✅ GPT calls

retrieval.py
✅ Embedding creation
✅ FAISS Search
✅ Context Building
✅ Source Collection
✅ Source Deduplication

prompts.py
✅ Prompt Templates

📍 How to Run
pip install -r requirements.py
streamlit run src/app.py