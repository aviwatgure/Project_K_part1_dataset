import json
import re

# Load the extracted text JSON
with open('Krishna_1_extracted_text.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Flatten and clean the text (assuming list of strings or dicts with text fields)
def extract_text(data):
    if isinstance(data, list):
        texts = []
        for item in data:
            if isinstance(item, dict):
                # Try to get the first string value in the dict
                for v in item.values():
                    if isinstance(v, str):
                        texts.append(v)
                        break
            elif isinstance(item, str):
                texts.append(item)
        return texts
    elif isinstance(data, dict):
        return [str(v) for v in data.values() if isinstance(v, str)]
    elif isinstance(data, str):
        return [data]
    return []

raw_texts = extract_text(data)

# Clean junk: remove non-printable, excessive whitespace, and OCR artifacts
def clean_text(text):
    text = re.sub(r'[^\x20-\x7E\n]', '', text)  # Remove non-printable
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    text = text.strip()
    return text

cleaned_texts = [clean_text(t) for t in raw_texts if t.strip()]

# Combine all cleaned text into one string for chunking
full_text = ' '.join(cleaned_texts)
words = full_text.split()

# Chunk into 300-500 word segments
def chunk_words(words, min_words=300, max_words=500):
    chunks = []
    i = 0
    while i < len(words):
        chunk_size = min(max_words, len(words) - i)
        if chunk_size < min_words:
            # Add remaining words to last chunk if too small
            if chunks:
                chunks[-1].extend(words[i:])
            else:
                chunks.append(words[i:])
            break
        chunks.append(words[i:i+chunk_size])
        i += chunk_size
    return [' '.join(chunk) for chunk in chunks]

chunks = chunk_words(words)

# Save the cleaned chunks
with open('krishna_chunks.json', 'w', encoding='utf-8') as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print(f"Saved {len(chunks)} chunks to krishna_chunks.json") 