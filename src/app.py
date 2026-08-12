import streamlit as st
from travelmate_rag import ask_travelmate

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.title("Available Cities")
st.sidebar.write("✅ Tokyo")
st.sidebar.write("✅ Paris")
st.sidebar.write("✅ Sydney")

st.title("TravelMate AI")
st.write(" 🌎 Your AI-powered travel assistant")

for message in st.session_state.messages:
    with st.chat_message("user"):
        st.write(message["question"])

    with st.chat_message("assistant"):
        st.write(message["answer"])

        with st.expander("Sources"):
            for source in message["sources"]:
                st.markdown(f"📍 {source['city']} \n\n 📄 {source['source']}")
   
    st.divider()  # Separator for readability

question = st.chat_input("Ask TravelMate...")

if question:
    with st.spinner("🌎 TravelMate is planning your trip..."):
        answer, sources = ask_travelmate(question, st.session_state.messages)
        st.session_state.messages.append({"question": question, "answer": answer, "sources": sources})
    with st.chat_message("assistant"):
        st.write(answer)

        with st.expander("Sources"):
            for source in sources:
                st.markdown(f"📍 {source['city']} \n\n 📄 {source['source']}")
