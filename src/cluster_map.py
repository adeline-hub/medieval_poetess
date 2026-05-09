import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# 1. Setup Paths
BASE_DIR = Path(__file__).resolve().parent.parent
TEXTS_DIR = BASE_DIR / "assets" / "texts"

fichiers = {
    'Marie de France': 'Marie_de_France_Lai_du_Chevrefeuille.txt',
    'Anna Komnene': 'Anne_Comnene_Alexiade.txt',
    'Wallada': 'Wallada bint al-Mustakfi.txt',
    'Hildegard von Bingen': 'Hildegarde_O_clarissima_Mater.txt'
}

# 2. Ingest Data
all_data = []
for autrice, nom_fichier in fichiers.items():
    chemin = TEXTS_DIR / nom_fichier
    if chemin.exists():
        with open(chemin, 'r', encoding='utf-8') as f:
            # Filter significant lines
            lines = [line.strip() for line in f if len(line.strip()) > 30]
            for line in lines:
                all_data.append({'autrice': autrice, 'text': line})

df = pd.DataFrame(all_data)

# Convert text to numbers (TF-IDF)
tfidf = TfidfVectorizer(max_features=500, stop_words='english')
matrix = tfidf.fit_transform(df['text'])

# K-Means Clustering (4 Academic Clusters)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster_label'] = kmeans.fit_predict(matrix).astype(str)

# PCA Reduction (to 2D for the chart)
pca = PCA(n_components=2)
pca_results = pca.fit_transform(matrix.toarray())
df['pca1'] = pca_results[:, 0]
df['pca2'] = pca_results[:, 1]

# 4. Visualization (DANKI STUDIO Style)
fig = px.scatter(
    df, 
    x='pca1', 
    y='pca2', 
    color='cluster_label',
    # Adjusting keys to match your df columns
    hover_data={'autrice': True, 'text': True, 'pca1': False, 'pca2': False},
    title="Thematic Vector Space: Cross-Temporal Connections",
    color_discrete_sequence=["#33FFA2", "#00E5FF", "#FF00E5", "#FFFFFF"] # DANKI Palette
)

fig.update_layout(
    plot_bgcolor='#121212',
    paper_bgcolor='#121212',
    font_color='#33FFA2',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    showlegend=True
)

fig.update_traces(
    marker=dict(size=10, opacity=0.8, line=dict(width=1, color='#121212')),
    selector=dict(mode='markers')
)

# 5. Export
output_path = BASE_DIR / "cluster_map.html"
fig.write_html(str(output_path))

print(f"✅ Constellation Map generated at: {output_path}")