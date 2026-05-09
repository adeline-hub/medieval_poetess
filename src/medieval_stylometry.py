import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- 1. DATA INGESTION (Using your actual project structure) ---
BASE_DIR = Path(__file__).resolve().parent.parent
TEXTS_DIR = BASE_DIR / "assets" / "texts"

fichiers = {
    'Marie de France': 'Marie_de_France_Lai_du_Chevrefeuille.txt',
    'Anna Komnene': 'Anne_Comnene_Alexiade.txt',
    'Wallada': 'Wallada bint al-Mustakfi.txt',
    'Hildegard von Bingen': 'Hildegarde_O_clarissima_Mater.txt'
}

all_data = []
for autrice, nom_fichier in fichiers.items():
    chemin = TEXTS_DIR / nom_fichier
    if chemin.exists():
        with open(chemin, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if len(line.strip()) > 20]
            for line in lines:
                all_data.append({'autrice': autrice, 'text': line})

df = pd.DataFrame(all_data)

# --- 2. VECTORIZATION & DIMENSIONALITY REDUCTION ---
vectorizer = TfidfVectorizer(max_features=500, stop_words=None) # Keep all for medieval nuance
X = vectorizer.fit_transform(df['text']).toarray()

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)
df['x'], df['y'] = X_reduced[:, 0], X_reduced[:, 1]

# --- 3. ACADEMIC CLUSTERING ---
# Using 4 clusters to match your 4 poetesses/topoi
kmeans = KMeans(n_clusters=4, random_state=42)
df['cluster'] = kmeans.fit_predict(X_reduced).astype(str)

cluster_map = {
    '0': 'I. Narratological Transitions',
    '1': 'II. Lyrical & Erotic Topos',
    '2': 'III. Political & Curial Rhetoric',
    '3': 'IV. Cosmological & Natural Metaphor'
}
df['academic_label'] = df['cluster'].map(cluster_map)

# --- 4. DANKI STUDIO VISUALIZATION ---
fig = go.Figure()

# Neon Palette for DANKI Style
colors = {'Marie de France': '#33FFA2', 'Anna Komnene': '#FF33FF', 
          'Wallada': '#FFFF33', 'Hildegard von Bingen': '#FFFFFF'}

for autrice, group in df.groupby('autrice'):
    fig.add_trace(go.Scatter(
        x=group['x'], y=group['y'],
        mode='markers+lines',
        name=autrice,
        text=group['text'],
        marker=dict(size=8, color=colors[autrice], opacity=0.7, 
                    line=dict(color='white', width=0.5)),
        line=dict(width=0.5, dash='dot'),
        hovertemplate="<b>%{name}</b><br>'%{text}'<extra></extra>"
    ))

fig.update_layout(
    title="<b>MEDIEVAL POETESSES MULTIDIMENSIONAL TOPOGRAPHY</b>",
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
    font=dict(color='#FFFFFF', family="Arial"),
    xaxis=dict(title="Stylometric Variance (PCA 1)", gridcolor='#2A2A2A', showgrid=True),
    yaxis=dict(title="Thematic Density (PCA 2)", gridcolor='#2A2A2A', showgrid=True),
    legend=dict(bgcolor='#1A1A1A', bordercolor='#2A2A2A'),
    width=1000, height=700
)

fig.show()

from pathlib import Path

# 1. Setup the directory path
BASE_DIR = Path(__file__).resolve().parent.parent 
# This assumes your script is in 'src/' and you want to save in the root
# or change this to where your index.html is located.
SAVE_PATH = BASE_DIR / "medieval_stylometry.html"

# 2. Export the interactive HTML
fig.write_html(
    str(SAVE_PATH),
    full_html=True,        
    include_plotlyjs='cdn', 
    config={'displayModeBar': False} 
)

print(f"Interactive map saved at: {SAVE_PATH}")