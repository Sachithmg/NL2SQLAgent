# frontend/streamlit_app.py
import requests
import streamlit as st
import base64

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="atamai NL2SQL Chatbot", page_icon="🤖", layout="centered")

# ---- Add logo (top right) ----
def load_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_base64_image("mnt/data/atomai.png")

st.markdown(
    f"""
    <div style="display: flex; justify-content: flex-end; margin-bottom: -40px;">
        <img src="data:image/png;base64,{logo_base64}" width="150" />
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("atamai NL2SQL Chatbot")

# Initialise chat history in Streamlit session
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # list of {"role": "user"/"assistant", "content": str}

# Render previous messages
for msg in st.session_state["messages"]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Ask a question about your database...")

if user_input:
    # 1) Add user message to UI history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Render user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # 2) Call FastAPI backend
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Thinking...")

        try:
            response = requests.post(API_URL, json={"question": user_input})
            response.raise_for_status()
            answer = response.json().get("answer", "No answer returned.")
        except Exception as e:
            answer = f"Error calling backend API: {e}"

        # Show final answer
        placeholder.write(answer)

    # 3) Save assistant message in history
    st.session_state["messages"].append({"role": "assistant", "content": answer})
