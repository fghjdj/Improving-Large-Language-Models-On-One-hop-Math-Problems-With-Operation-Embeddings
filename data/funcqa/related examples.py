import json
import re
import difflib

# Define file paths
curbest_path = ''
funcqa_oh_path = ''
output_same_path = ''
output_diff_path = ''

cut_count = 50  # Adjust as needed

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[\W_]+', '', text)
    return text

def extract_question(text):
    """
    Extract the question part from a curbest entry, assuming the format is
    "Q: question text\nA: answer text"
    """
    if text.startswith("Q:"):
        parts = text.split("\nA:")
        return parts[0][2:].strip()
    return text.strip()

with open(funcqa_oh_path, 'r', encoding='utf-8') as f:
    funcqa_oh_data = json.load(f)

with open(curbest_path, 'r', encoding='utf-8') as f:
    curbest_data = json.load(f)

funcqa_questions = [
    normalize_text(entry.get("question", "").strip())
    for entry in funcqa_oh_data[:60]
]

# Set similarity threshold
threshold = 0.4

same_list = []
diff_list = []

for entry in curbest_data:
    text = entry.get("text", "")
    question = extract_question(text)
    norm_question = normalize_text(question)
    
    max_similarity = max(
        difflib.SequenceMatcher(None, norm_question, q).ratio()
        for q in funcqa_questions
    )
    
    if max_similarity >= threshold:
        same_list.append(entry)
    else:
        diff_list.append(entry)

if cut_count > 0:
    cut_count = min(cut_count, len(diff_list))
    extra_entries = diff_list[:cut_count]
    same_list.extend(extra_entries)
    diff_list = diff_list[cut_count:]

with open(output_same_path, 'w', encoding='utf-8') as f:
    json.dump(same_list, f, ensure_ascii=False, indent=4)

with open(output_diff_path, 'w', encoding='utf-8') as f:
    json.dump(diff_list, f, ensure_ascii=False, indent=4)
