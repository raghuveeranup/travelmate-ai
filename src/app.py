import streamlit as st
from travelmate_rag import ask_travelmate

st.title("TravelMate AI")
st.write(" 🌎 Your AI-powered travel assistant")

question = st.text_input("Ask TravelMate:")

if question:
    with st.spinner("TravelMate is thinking..."):
        answer, sources = ask_travelmate(question)
    st.subheader("Answer:")
    st.write(answer)

    st.subheader("Sources:")
    for source in sources:
        st.markdown(f"📍 {source['city']} \n\n 📄 {source['source']}")
