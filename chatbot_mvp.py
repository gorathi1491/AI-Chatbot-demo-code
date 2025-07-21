import streamlit as st
import openai
from datetime import datetime

openai.api_key = st.secrets["openai_api_key"]

# --- Persona & FAQ Setup ---
personas = {
    "Support Agent": "You're a friendly support agent. Help users understand our subscription model and troubleshoot issues.",
    "Sales Pro": "You're a high-energy salesperson. Your goal is to upsell users to premium plans.",
    "Helpful Assistant": "You're a calm, helpful assistant answering questions about our content."
}

faqs = {
    "What are the subscription tiers?": "We offer Free, Basic ($9/mo), and Premium ($29/mo) plans.",
    "What kind of content is included?": "We offer exclusive videos, courses, and guides for digital marketing and branding.",
    "How can I contact support?": "You can reach us at support@contentplus.com or via live chat 24/7."
}

# --- UI Setup ---
st.title("📢 Content+ AI Chatbot Demo")
persona = st.selectbox("Choose a Persona", list(personas.keys()))
st.markdown("Chat with our assistant below. Ask about subscriptions, content, or offers!")

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": personas[persona]}]

# --- User Input ---
user_input = st.chat_input("Ask me anything about your subscription...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # --- Dynamic Response from OpenAI ---
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=st.session_state.messages,
        temperature=0.7
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- Show Chat ---
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Admin Panel ---
with st.sidebar:
    st.header("Admin Panel")
    if st.text_input("Password", type="password") == "admin123":
        st.success("Access granted")
        new_faq = st.text_input("Add new FAQ question")
        new_answer = st.text_area("FAQ Answer")
        if st.button("Save FAQ"):
            faqs[new_faq] = new_answer
            st.success("FAQ added.")
    else:
        st.warning("Enter admin password to edit content")