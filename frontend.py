import backend
import streamlit as st

backend_int = backend.BackendInterface()

st.title("GPbeT")
st.text("Chatbot for sports and sports betting analytics with natural language processing. Supports NHL and NBA currently. Enter a bet line with a player name.")
st.text("Example 1: 'Will Seth Jones get more than 25.25 minutes on ice in his next game?'")
st.text("Example 2: 'Will Kevin Durant get a combined total of 35 points + rebounds + assists in his next game?'")

user_text = st.chat_input("Enter your prompt containing a valid current player name...")
if user_text:
    with st.spinner(f"Answering question... '{user_text}"):
        res = backend_int.get_result(user_text, verbose=True)
        st.write(res)
