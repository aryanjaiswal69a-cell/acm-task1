from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)   

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

model = genai.GenerativeModel("models/gemini-2.5-flash")

st.header("CHATBot")

personality_input = st.selectbox(
    "select personality",
    ["roasting personality", "Normal Human like personality", "Funny personality","flirty personality","Sarcastic personality","Motivational personality","Encouraging personality","Professional personality","Empathetic personality","Enthusiastic personality"]
)

# Only initialize chat_history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your message:", key="user_input")

if st.button("GO") and user_input:
    if len(st.session_state.chat_history) == 0:
        persona_message = (
            f"You are a chat bot with {personality_input}. "
            "Have the conversation with the given personality. "
            f"User: {user_input}"
        )
        st.session_state.chat_history.append({"role": "user", "parts": [persona_message]})
    else:
        st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

    result = model.generate_content(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "model", "parts": [result.text]})
    st.write(result.text)

st.header("Chat History")
# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.write("You:", chat["parts"])
    elif chat["role"] == "model":
        st.write("Bot:", chat["parts"])