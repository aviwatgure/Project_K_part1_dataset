# Required packages: streamlit, sentence-transformers, chromadb, google-generativeai, nltk
# pip install streamlit sentence-transformers chromadb google-generativeai nltk

import streamlit as st
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import nltk

# Ensure nltk punkt is available
nltk.download('punkt')

# Google Gemini API setup
GEMINI_API_KEY = "AIzaSyDwu2onUoDs6EX02B30I1zfJxrSV-yBTAE"
genai.configure(api_key=GEMINI_API_KEY)

# Load embedding model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Connect to ChromaDB
@st.cache_resource
def get_chroma_collection():
    client = chromadb.Client(Settings(persist_directory="./chroma_db"))
    return client.get_or_create_collection("krishna_storyline")

collection = get_chroma_collection()

# Streamlit UI
st.title("Krishna QA Chatbot (Retrieval-Augmented)")
st.write("Ask any question about the Krishna storyline!")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Your question:")

if st.button("Ask") and user_input:
    # 1. Embed the user query
    query_embedding = model.encode([user_input])[0]
    # 2. Retrieve top 3 relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=3
    )
    retrieved_chunks = results['documents'][0]
    context = "\n".join(retrieved_chunks)
    # 3. Generate answer using Gemini
    prompt = f"Context:\n{context}\n\nQuestion: {user_input}\n\nAnswer:"
    try:
        response = genai.generate_text(
            model="gemini-pro",
            prompt=prompt,
            max_output_tokens=512
        )
        answer = response.result
    except Exception as e:
        answer = f"Error from Gemini: {e}"
    # 4. Display
    st.session_state.chat_history.append((user_input, answer))

for q, a in st.session_state.chat_history:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}") 