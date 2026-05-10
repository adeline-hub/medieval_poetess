import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans

# --- 1. SMART PATH LOGIC (Moving from src to data) ---
# Get the location of the current script (which is in /src/)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Move UP one level to the project root, then DOWN into the data folder
CSV_PATH = os.path.abspath(os.path.join(current_dir, "..", "data", "medieval_poetesses_complete.csv"))

if not os.path.exists(CSV_PATH):
    print(f"❌ ERROR: Still cannot find the CSV.")
    print(f"Tried looking at: {CSV_PATH}")
    print("Check if your folder is named 'data' or 'Data' (case sensitivity matters!)")
else:
    df = pd.read_csv(CSV_PATH)
    print(f"✅ SUCCESS! Data loaded from: {CSV_PATH}")
    
    # ... (Rest of the script remains exactly the same)

df = pd.read_csv(CSV_PATH)
df['line_number'] = df.groupby('Author').cumcount() + 1

# --- 2. GENERATE CLUSTERS (K-MEANS) ---
# We cluster solely on the Confidence_Score to find 3 levels of intensity
X = df[['Confidence_Score']].values
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
df['intensity_cluster'] = kmeans.labels_

# Sort clusters so 0 is low, 2 is high for consistent coloring
idx = np.argsort(kmeans.cluster_centers_.sum(axis=1))
lut = dict(zip(idx, [0, 1, 2]))
df['intensity_cluster'] = df['intensity_cluster'].map(lut)

# --- 3. DANKI VISUAL SETTINGS ---
symbols = {'Marie de France': 'circle', 'Anna Komnene': 'diamond', 
           'Wallada': 'star', 'Hildegard von Bingen': 'square'}

# Colors for the 3 Intensity Hulls (Muted Grey, Neon Violet, Neon Green)
cluster_colors = {
    0: 'rgba(115, 115, 115, 0.2)', # Low: Muted Grey
    1: 'rgba(255, 51, 255, 0.2)',  # Med: Neon Violet
    2: 'rgba(51, 255, 162, 0.2)'   # High: Neon Green
}
line_colors = {0: '#737373', 1: '#FF33FF', 2: '#33FFA2'}

# --- 4. BUILD FIGURE ---
fig = go.Figure()

# a) Draw the Convex Hulls first (Background Layers)
for cluster_id in range(3):
    cluster_data = df[df['intensity_cluster'] == cluster_id]
    points = cluster_data[['line_number', 'Confidence_Score']].values
    
    if len(points) >= 3:
        hull = ConvexHull(points)
        # Close the loop by appending the first point at the end
        hull_points = np.append(points[hull.vertices], [points[hull.vertices][0]], axis=0)

        fig.add_trace(go.Scatter(
            x=hull_points[:, 0], y=hull_points[:, 1],
            fill='toself',
            fillcolor=cluster_colors[cluster_id],
            line=dict(color=line_colors[cluster_id], width=1),
            name=f"Intensity Tier {cluster_id}",
            showlegend=False,
            hoverinfo='skip'
        ))

# b) Draw the Individual Verses (Foreground)
for poet, group in df.groupby('Author'):
    fig.add_trace(go.Scatter(
        x=group['line_number'],
        y=group['Confidence_Score'],
        mode='markers',
        marker=dict(
            symbol=symbols[poet],
            size=11,
            color=group['intensity_cluster'],
            colorscale=[[0, '#737373'], [0.5, '#FF33FF'], [1, '#33FFA2']],
            line=dict(width=1, color='#121212')
        ),
        name=poet,
        text=group['Emotion'],
        customdata=group[['Original_Text']].values,
        hovertemplate="<b>%{text}</b><br>Poet: "+poet+"<br>Score: %{y:.2f}<extra></extra>"
    ))

# --- 5. DANKI STUDIO LAYOUT ---
fig.update_layout(
    title=dict(
        text="EMOTIONAL RADIOGRAPHY: INTENSITY CLUSTERS",
        font=dict(size=22, color='#33FFA2')
    ),
    xaxis_title="VERSE SEQUENCE",
    yaxis_title="INTENSITY",
    template="plotly_dark",
    width=1400, height=600,
    plot_bgcolor='#121212',
    paper_bgcolor='#121212',
    font_color='#FFFFFF'
)

fig.update_xaxes(gridcolor='#2A2A2A', zeroline=False)
fig.update_yaxes(gridcolor='#2A2A2A', zeroline=False)

fig.show()
fig.write_html(os.path.join(current_dir, "intensity_hulls.html"))