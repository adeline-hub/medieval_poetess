import pandas as pd
import os
import random

# --- 1. DATA LOADING & CLUSTERING ---
current_dir = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(current_dir, "..", "data", "medieval_poetesses_complete.csv")
df = pd.read_csv(CSV_PATH)

# Re-run the K-Means clustering (matching your previous script)
from sklearn.cluster import KMeans
import numpy as np

X = df[['Confidence_Score']].values
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
df['cluster'] = kmeans.labels_

# Sort clusters so 0=Low, 1=Med, 2=High
idx = np.argsort(kmeans.cluster_centers_.sum(axis=1))
lut = dict(zip(idx, [0, 1, 2]))
df['cluster'] = df['cluster'].map(lut)

# Mapping names for your HTML output
cluster_names = {0: "Chill", 1: "Tempered", 2: "Intense"}

# --- 2. GENERATE RANDOM REMIXED POEMS ---
def generate_remix(df, cluster_type="mixed", num_verses=3):
    """
    Generates a random poem from the corpus.
    cluster_type: 0, 1, 2, or 'mixed'
    """
    if cluster_type == "mixed":
        sample = df.sample(num_verses)
    else:
        sample = df[df['cluster'] == cluster_type].sample(num_verses)
    
    poem_lines = []
    for _, row in sample.iterrows():
        poem_lines.append(f"{row['Original_Text']} — ({row['Author']})")
    
    return "\n".join(poem_lines)

# Generate the 4 types
remixes = {
    "Chill Poem": generate_remix(df, 0),
    "Tempered Poem": generate_remix(df, 1),
    "Intense Poem": generate_remix(df, 2),
    "Mixed intensity Poem": generate_remix(df, "mixed")
}

# --- 3. EXPORT TO DANKI BRANDED HTML ---
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ background-color: #121212; color: #FFFFFF; font-family: 'Roboto', sans-serif; padding: 40px; }}
        .poem-card {{ 
            background: #1A1A1A; 
            border-left: 5px solid #33FFA2; 
            margin-bottom: 30px; 
            padding: 20px; 
            border-radius: 4px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }}
        h2 {{ color: #33FFA2; text-transform: uppercase; letter-spacing: 2px; }}
        h3 {{ color: #FF33FF; font-style: italic; margin-top: 0; }}
        p {{ line-height: 1.6; font-size: 1.1rem; color: #eee; white-space: pre-line; }}
        .meta {{ color: #737373; font-size: 0.8rem; margin-top: 10px; border-top: 1px solid #2A2A2A; padding-top: 10px; }}
    </style>
</head>
<body>
    <h1>DANKI STUDIO: POETIC REMIXES</h1>
"""

for title, content in remixes.items():
    # Assign specific border colors based on type
    color = "#33FFA2" if "Chill" in title else "#FF33FF" if "Intense" in title else "#00E5FF"
    html_content += f"""
    <div class="poem-card" style="border-left-color: {color}">
        <h3>{title}</h3>
        <p>{content}</p>
        <div class="meta">Generated via NLP Clustering from Global Corpus</div>
    </div>
    """

html_content += "</body></html>"

# Save the final file
output_file = os.path.join(current_dir, "poetic_remixes.html")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✨ SUCCESS: Your 4 remixed poems are ready in {output_file}")