import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="GEC Vaishali AI Assistant", page_icon="🎓", layout="centered")

# Custom CSS for a modern "Chat" look
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True) 


# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    # Ensure intents.csv is in the same folder
    return pd.read_csv('intents.csv')

df = load_data()

# --- 3. SIDEBAR DESIGN ---
with st.sidebar:
    st.image("https://www.gecvaishali.ac.in/wp-content/uploads/2026/03/logo-1.png", width=200)
    st.title("Government Engineering College Vaishali")
    st.info("Shyampur, Chaksikandar, Bidupur, Vaishali, Bihar - 844115")
    st.markdown("---")
    st.markdown("### Quick Links")
    st.link_button("Official Website", "https://www.gecvaishali.ac.in/")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- 4. CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to GEC Vaishali! I am your virtual assistant. How can I help you today?"}
    ]

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT LOGIC (THE BRAIN) ---
if prompt := st.chat_input("Ask about admissions, faculty, or campus..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response with "Thinking" animation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Searching college database...")
        
        # Fuzzy Matching Logic (Intelligence)
        # It finds the best match even if the user makes a typo
        patterns = df['patterns'].tolist()
        best_match, score = process.extractOne(prompt, patterns)

        time.sleep(0.5) # Artificial delay to feel more like "AI"

        if score > 65: # Confidence threshold
            full_response = df[df['patterns'] == best_match]['responses'].values[0]
        else:
            full_response = "I'm sorry, I don't have that specific information yet. Please visit [GEC Vaishali Website](https://www.gecvaishali.ac.in/) for detailed info."

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})