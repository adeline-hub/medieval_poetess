import os
import pandas as pd
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# --- 1. CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
TEXTS_DIR = BASE_DIR / "assets" / "texts"
OUTPUT_FILE = BASE_DIR / "medieval_poetesses_complete.csv"

# --- 2. MODELS ---
trans_name = "Helsinki-NLP/opus-mt-fr-en"
trans_tokenizer = AutoTokenizer.from_pretrained(trans_name)
trans_model = AutoModelForSeq2SeqLM.from_pretrained(trans_name)

emotion_model = pipeline(
    "text-classification", 
    model="j-hartmann/emotion-english-distilroberta-base", 
    top_k=1
)

def translate_line(line):
    if not line.strip(): return ""
    inputs = trans_tokenizer(line, return_tensors="pt", padding=True, truncation=True)
    outputs = trans_model.generate(**inputs)
    return trans_tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- 3. FULL DF GENERATION ---
fichiers = {
    'Marie de France': 'Marie_de_France_Lai_du_Chevrefeuille.txt',
    'Anna Komnene': 'Anne_Comnene_Alexiade.txt',
    'Wallada': 'Wallada bint al-Mustakfi.txt',
    'Hildegard von Bingen': 'Hildegarde_O_clarissima_Mater.txt'
}

all_processed_data = []

for author, filename in fichiers.items():
    path = TEXTS_DIR / filename
    if not path.exists():
        print(f"Skipping {author}: File not found.")
        continue
    
    print(f"Processing entire text for: {author}...")
    with open(path, 'r', encoding='utf-8') as f:
        # We process all lines longer than 25 chars (no [:10] limit here)
        lines = [l.strip() for l in f if len(l.strip()) > 25]
        
        for line in lines:
            try:
                en_line = translate_line(line)
                raw = emotion_model(en_line)
                result = raw[0][0] if isinstance(raw[0], list) else raw[0]
                
                all_processed_data.append({
                    'Author': author,
                    'Original_Text': line,
                    'Translated_Text': en_line,
                    'Emotion': result['label'].upper(),
                    'Confidence_Score': round(result['score'], 4)
                })
            except Exception as e:
                continue

# --- 4. CSV EXPORT ---
df_complete = pd.DataFrame(all_processed_data)
df_complete.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

print(f"\n✅ FULL CORPUS SAVED: {OUTPUT_FILE}")
print(f"Total lines processed: {len(df_complete)}")