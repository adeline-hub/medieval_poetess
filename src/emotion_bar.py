import os
import pandas as pd
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import plotly.express as px

# --- 1. SETTINGS & PATHS ---
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
BASE_DIR = Path(__file__).resolve().parent.parent
TEXTS_DIR = BASE_DIR / "assets" / "texts"

# --- 2. INITIALIZE MODELS ---
print("Loading Translation & Emotion Models...")

# Translation: Manual load to bypass pipeline registry errors
trans_name = "Helsinki-NLP/opus-mt-fr-en"
trans_tokenizer = AutoTokenizer.from_pretrained(trans_name)
trans_model = AutoModelForSeq2SeqLM.from_pretrained(trans_name)

# Emotion: distilroberta-base
emotion_model = pipeline(
    "text-classification", 
    model="j-hartmann/emotion-english-distilroberta-base", 
    top_k=1
)

def translate_line(line):
    if not line.strip():
        return ""
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
        print(f"⚠️ File not found: {filename}")
        continue
    
    print(f"→ Analyzing: {author}...")
    with open(path, 'r', encoding='utf-8') as f:
        # Take 10 significant lines per poetess for a better chart sample
        lines = [l.strip() for l in f if len(l.strip()) > 25][:10]
        
        for i, line in enumerate(lines):
            try:
                en_line = translate_line(line)
                raw = emotion_model(en_line)
                result = raw[0][0] if isinstance(raw[0], list) else raw[0]
                
                emotion_data.append({
                    'Author': author,
                    'Original Text': line[:60] + "...",
                    'Emotion': result['label'].upper(), # This creates your column
                    'Confidence': result['score']
                })
            except Exception as e:
                print(f"Error on line {i}: {e}")

# Create DataFrame
df = pd.DataFrame(emotion_data)

# --- 4. GENERATE DANKI BAR CHART ---
print("Generating Brand Visualization...")

# Count frequencies
emotion_counts = df['Emotion'].value_counts().reset_index()
emotion_counts.columns = ['Emotion', 'Count']

fig = px.bar(
    emotion_counts,
    x='Emotion',
    y='Count',
    text='Count',
    title="EMOTIONAL FREQUENCY: GLOBAL CORPUS",
    color_discrete_sequence=['#33FFA2'] # DANKI Neon Green
)

fig.update_layout(
    font_family="Roboto, sans-serif",
    plot_bgcolor='#121212',
    paper_bgcolor='#121212',
    font_color='#FFFFFF',
    title_font=dict(size=20, color='#33FFA2'),
    xaxis=dict(gridcolor='#2A2A2A', title="EMOTION TYPE"),
    yaxis=dict(gridcolor='#2A2A2A', title="NUMBER OF LINES"),
    width=800,
    height=500
)

fig.update_traces(marker_line_color='#FF33FF', marker_line_width=1.5)

# Save Chart
fig.write_html(BASE_DIR / "emotion_chart.html")

# --- 5. EXPORT TABLE HTML ---
sample_html = df.sample(min(len(df), 5)).to_html(classes='danki-table', index=False)
full_html = f"""
<style>
    .danki-table {{ width: 100%; border-collapse: collapse; background: #121212; color: #eee; font-family: sans-serif; }}
    .danki-table th {{ color: #33FFA2; border-bottom: 2px solid #33FFA2; padding: 10px; text-align: left; text-transform: uppercase; }}
    .danki-table td {{ padding: 10px; border-bottom: 1px solid #2A2A2A; }}
</style>
{sample_html}
"""

with open(BASE_DIR / "emotion_sample.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("\n✅ Success! Files generated:")
print(f"- {BASE_DIR}/emotion_sample.html (Table)")
print(f"- {BASE_DIR}/emotion_chart.html (Visual)")