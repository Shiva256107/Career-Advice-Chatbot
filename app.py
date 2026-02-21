import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Google Generative AI
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY in your .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

# Initialize the model with system prompt
system_prompt = """
You are a professional career advisor AI. Your role is to provide helpful, accurate, and encouraging advice on career-related questions.
Always be supportive, empathetic, and provide actionable steps when possible.
Focus on career development, job search, skill building, work-life balance, and professional growth.
If the question is not career-related, politely redirect to career topics.
"""
model = genai.GenerativeModel('gemini-3-flash-preview', system_instruction=system_prompt)

# Streamlit app
st.title("Career Advisor Chatbot")
st.write("Get personalized career advice powered by AI!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your career..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    try:
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Add AI response to history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")