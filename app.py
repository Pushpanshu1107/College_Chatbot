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


# --- 2. LOAD DATA (UPDATED) ---
@st.cache_data
def load_data():
    raw_df = pd.read_csv('intents.csv')
    
    # This magic part splits the "patterns" by '/' and creates a new row for each one
    # So "Hi / Hello" becomes two rows: one for "Hi", one for "Hello"
    raw_df['patterns'] = raw_df['patterns'].str.split(' / ')
    exploded_df = raw_df.explode('patterns')
    
    # Clean up whitespace
    exploded_df['patterns'] = exploded_df['patterns'].str.strip()
    
    return exploded_df

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

# --- 5. SMART CHAT LOGIC (THE BRAIN) ---
# Added a unique key to prevent the DuplicateElementId error
if prompt := st.chat_input("Ask about admissions, faculty, or campus...", key="gecv_chat_input"):
    
    # 1. Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Check for empty or very short inputs
        if len(prompt.strip()) < 2:
            full_response = "I'm listening! Please type a question about GEC Vaishali (e.g., 'Admission process')."
        else:
            # Fuzzy Matching Logic
            patterns = df['patterns'].tolist()
            best_match, score = process.extractOne(prompt, patterns)

            # --- Confidence Thresholds ---
            if score > 85:
                # High Confidence: Give direct answer
                full_response = df[df['patterns'] == best_match]['responses'].values[0]
            
            elif 65 < score <= 85:
                # Medium Confidence: Acknowledge the guess
                actual_resp = df[df['patterns'] == best_match]['responses'].values[0]
                full_response = f"I think you're asking about **{best_match}**. \n\n{actual_resp}"
            
            else:
                # Low Confidence: Don't guess, offer help
                full_response = (
                    "I'm sorry, I couldn't find a high-match for that in my current database. "
                    "Try asking about **Admissions**, **Fee Structure**, **Hostels**, or **Library timings**."
                )

        # 3. Typewriter Effect (Simulates real AI behavior)
        typed_output = ""
        for word in full_response.split():
            typed_output += word + " "
            message_placeholder.markdown(typed_output + "▌")
            time.sleep(0.05) # Adjust speed here
        
        message_placeholder.markdown(full_response)
        
        # Save to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
