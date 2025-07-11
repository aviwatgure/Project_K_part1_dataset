import json

# Load cleaned paragraphs
with open('krishna_cleaned.json', 'r', encoding='utf-8') as f:
    paragraphs = json.load(f)

# Remove commas and concatenate into one story line
story = ' '.join(p.replace(',', '') for p in paragraphs)

# Save to text file
with open('krishna_storyline.txt', 'w', encoding='utf-8') as f:
    f.write(story)

print(f"Saved storyline to krishna_storyline.txt. Length: {len(story)} characters.") 