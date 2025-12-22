import streamlit as st
from groq import Groq
import os

# CONFIG
st.set_page_config(page_title="Groq Role-Based Chat", page_icon="🤖")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# ROLES
roles = {
    "Maths Tutor": "You are a Maths tutor. Explain concepts step by step, use simple language, and include examples. Only answer math-related questions.",
    "Doctor": "You are a Doctor. Provide general medical information in simple language and avoid diagnosis or prescriptions. Only answers health and medical queries.",
    "Travel Guide": "You are a Travel Guide. Suggest destinations, attractions, itineraries, and travel tips clearly and practically. Only gives travel advice and tips.",
    "Chef": "You are a Chef. Share easy-to-follow recipes, cooking tips, and ingredient substitutions. Only gives travel advice and tips. Only answers questions about cooking and recipes.",
    "Tech Support": "You are Tech Support. Help users troubleshoot technical issues step by step using clear and simple instructions. Only answers technical troubleshooting queries."
}

# SESSION STATE
if "selected_role" not in st.session_state:
    st.session_state.selected_role = None

if "history" not in st.session_state:
    st.session_state.history = []

# UI
st.title("🤖 Role-Based Chatbot")

# Role dropdown
selected_role = st.selectbox(
    "Select AI Role",
    list(roles.keys())
)

if selected_role != st.session_state.selected_role:
    st.session_state.selected_role = selected_role
    st.session_state.history = [
        {"role": "system", "content": roles[selected_role]}
    ]

st.success(f"AI is acting as **{selected_role}**")

# chat history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Chat input
user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.history.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Thinking..."):
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.history,
            max_tokens=1000
        )

    response = completion.choices[0].message.content

    st.session_state.history.append(
        {"role": "assistant", "content": response}
    )

    # Show response
    st.chat_message("assistant").write(response)
