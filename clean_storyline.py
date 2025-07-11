import re

with open('krishna_storyline.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove all numbers (Latin and Devanagari)
text = re.sub(r'[0-9०१२३४५६७८९]', '', text)
# Remove special symbols and punctuation except sentence-ending marks
text = re.sub(r'[\[\]{}()<>|\\/@#$%^&*_+=~`"\'\-–—•:;!?]', ' ', text)
# Remove repeated punctuation and extra whitespace
text = re.sub(r'[.,।॥]{2,}', '.', text)
text = re.sub(r'\s+', ' ', text)

# Optionally, remove very short fragments (less than 15 Devanagari/English letters in a row)
def is_meaningful(line):
    letters = re.findall(r'[\u0900-\u097F\uA8E0-\uA8FFa-zA-Z]', line)
    return len(letters) > 15

# Split into sentences for filtering
sentences = re.split(r'[.।॥]', text)
cleaned_sentences = [s.strip() for s in sentences if is_meaningful(s)]

# Join back into a single string
cleaned_story = ' '.join(cleaned_sentences)

with open('krishna_storyline_cleaned.txt', 'w', encoding='utf-8') as f:
    f.write(cleaned_story)

print(f"Saved cleaned storyline to krishna_storyline_cleaned.txt. Length: {len(cleaned_story)} characters.") 