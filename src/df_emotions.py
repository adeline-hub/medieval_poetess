import os
import pandas as pd
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# --- 1. SETTINGS & PATHS ---
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
BASE_DIR = Path(__file__).resolve().parent.parent
TEXTS_DIR = BASE_DIR / "assets" / "texts"

# --- 2. INITIALIZE MODELS (Manual Method) ---
print("Loading Translation & Emotion Models...")

# Translation: Loading manually to bypass "Unknown task translation" error
trans_name = "Helsinki-NLP/opus-mt-fr-en"
trans_tokenizer = AutoTokenizer.from_pretrained(trans_name)
trans_model = AutoModelForSeq2SeqLM.from_pretrained(trans_name)

# Emotion: 'text-classification' is recognized by your system, so pipeline works here
emotion_model = pipeline(
    "text-classification", 
    model="j-hartmann/emotion-english-distilroberta-base", 
    top_k=1
)

def translate_line(line):
    if not line.strip():
        return ""
    # Manual tokenization and generation
    inputs = trans_tokenizer(line, return_tensors="pt", padding=True, truncation=True)
    outputs = trans_model.generate(**inputs)
    return trans_tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- 3. DATA PROCESSING ---
fichiers = {
    'Marie de France': 'Marie_de_France_Lai_du_Chevrefeuille.txt',
    'Anna Komnene': 'Anne_Comnene_Alexiade.txt',
    'Wallada': 'Wallada bint al-Mustakfi.txt',
    'Hildegard von Bingen': 'Hildegarde_O_clarissima_Mater.txt'
}

emotion_data = []

for author, filename in fichiers.items():
    path = TEXTS_DIR / filename
    if not path.exists():
        continue
    
    print(f"Processing: {author}...")
    with open(path, 'r', encoding='utf-8') as f:
        # Take 5 significant lines per poetess
        lines = [l.strip() for l in f if len(l.strip()) > 25][:5]
        
        for i, line in enumerate(lines):
            try:
                en_line = translate_line(line)
                
                # Analyze emotion
                raw = emotion_model(en_line)
                first = raw[0]
                result = first[0] if isinstance(first, list) else first
                
                emotion_data.append({
                    'Author': author,
                    'Original Text': line[:60] + "...",
                    'Emotion': result['label'].upper(),
                    'Confidence': f"{result['score']:.2%}"
                })
            except Exception as e:
                print(f"Error on line {i}: {e}")

# --- 4. EXPORT TO HTML ---
df = pd.DataFrame(emotion_data)
# Save a 5-row sample for the GitHub Page
sample_html = df.sample(min(len(df), 5)).to_html(classes='danki-table', index=False)

full_html = f"""
<style>
    .danki-table {{ width: 100%; border-collapse: collapse; background: #121212; color: #eee; font-family: sans-serif; font-size: 0.9rem; }}
    .danki-table th {{ color: #33FFA2; border-bottom: 2px solid #33FFA2; padding: 10px; text-align: left; }}
    .danki-table td {{ padding: 10px; border-bottom: 1px solid #2A2A2A; }}
</style>
{sample_html}
"""

with open(BASE_DIR / "emotion_sample.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("\n✅ Success! emotion_sample.html generated.")