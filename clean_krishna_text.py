import json
import re

# Load the extracted text JSON
with open('Krishna_1_extracted_text.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Helper: Check if a line is mostly alphabetic (Devanagari or English)
def is_meaningful(line):
    text = re.sub(r'\s+', '', line)
    if not text:
        return False
    # Count Devanagari and English letters
    letters = re.findall(r'[\u0900-\u097F\uA8E0-\uA8FFa-zA-Z]', text)
    # Stricter: must be at least 70% letters, and at least 15 letters
    if len(letters) / max(1, len(text)) < 0.7 or len(letters) < 15:
        return False
    # Must have at least 3 words
    if len(re.findall(r'\w+', line)) < 3:
        return False
    return True

# Helper: Remove known page artifacts and junk
page_artifact_patterns = [
    r'^[\d०१२३४५६७८९\s\|\-–—.,:;#@£$%&*()\[\]{}<>/\\=+~`"\']+$',
    r'^[A-Za-z0-9०१२३४५६७८९\s]+$',
    r'^[\d०१२३४५६७८९]+$',
    r'^[\u0964\u0965॥।.,:;\-–—]+$',
    r'^[\(\)\[\]{}]+$',
    r'^.{1,8}$',
    r'[/\\|]',  # Contains slashes or pipes
]
page_artifact_regexes = [re.compile(p) for p in page_artifact_patterns]

def is_artifact(line):
    for regex in page_artifact_regexes:
        if regex.search(line.strip()):
            return True
    return False

# Clean and collect meaningful paragraphs
cleaned_paragraphs = []
for entry in data:
    text = entry.get('text', '')
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if is_artifact(line):
            continue
        if not is_meaningful(line):
            continue
        line = re.sub(r'\s+', ' ', line)
        cleaned_paragraphs.append(line)

with open('krishna_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_paragraphs, f, ensure_ascii=False, indent=2)

print(f"Saved {len(cleaned_paragraphs)} cleaned paragraphs to krishna_cleaned.json") 