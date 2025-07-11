import os
import nltk
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Ensure nltk punkt and punkt_tab are downloaded
nltk.download('punkt')
nltk.download('punkt_tab')

# 1. Read the cleaned text file
with open('krishna_storyline_cleaned.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 2. Smart chunking: split by paragraphs, then further by sentences if paragraphs are too long
paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
chunks = []
max_sentences_per_chunk = 5

for para in paragraphs:
    sentences = nltk.sent_tokenize(para)
    # Chunk sentences into groups of max_sentences_per_chunk
    for i in range(0, len(sentences), max_sentences_per_chunk):
        chunk = ' '.join(sentences[i:i+max_sentences_per_chunk])
        if chunk:
            chunks.append(chunk)

# 3. Generate embeddings using SentenceTransformers
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks, show_progress_bar=True)

# 4. Store in ChromaDB
client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = client.get_or_create_collection("krishna_storyline")

# Add chunks and embeddings to ChromaDB
for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
    collection.add(
        documents=[chunk],
        embeddings=[embedding.tolist()],
        ids=[f"chunk_{idx}"]
    )

print(f"Stored {len(chunks)} chunks and embeddings in ChromaDB.")

# Installation instructions (if needed):
# pip install sentence-transformers chromadb nltk 