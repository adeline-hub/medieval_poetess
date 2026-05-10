import pandas as pd
import plotly.graph_objects as go
import os

# --- 1. DATA LOADING ---
current_dir = os.path.dirname(os.path.abspath(__file__))
CSV_NAME = "medieval_poetesses_complete.csv"
CSV_PATH = os.path.join(current_dir, CSV_NAME)

# Fallback to absolute path if necessary
if not os.path.exists(CSV_PATH):
    CSV_PATH = "C:/Users/nambo/Documents/GitHub/medieval_poetess/data/" + CSV_NAME

df = pd.read_csv(CSV_PATH)

# --- 2. PRE-PROCESSING FOR PLOT ---
# Ensure line numbers are unique per author for the X-axis
df['line_number'] = df.groupby('Author').cumcount() + 1
df['emotion_code'] = pd.Categorical(df['Emotion']).codes
n_codes = df['emotion_code'].nunique()

# Mapping unique symbols to each poetess
symbols = {
    'Marie de France': 'circle',
    'Anna Komnene': 'diamond',
    'Wallada': 'star',
    'Hildegard von Bingen': 'square'
}

# DANKI Brand Color Mapping for the Lines
line_colors = {
    'Marie de France': '#33FFA2',      # Neon Green
    'Anna Komnene': '#FF33FF',        # Neon Violet
    'Wallada': '#00E5FF',             # Neon Cyan
    'Hildegard von Bingen': '#737373'  # Muted Grey
}

# Custom DANKI Colorscale for the markers (Emotion intensity)
danki_colorscale = [
    [0.0, "#1A1A1A"],   # Deep Charcoal
    [0.5, "#FF33FF"],   # Neon Violet
    [1.0, "#33FFA2"]    # Neon Green
]

# --- 3. BUILD THE FIGURE ---
fig = go.Figure()

# a) Add Lines First (The "Pulse" of each poem)
for author, group in df.groupby('Author'):
    fig.add_trace(go.Scatter(
        x=group['line_number'],
        y=group['Confidence_Score'],
        mode='lines',
        line=dict(color=line_colors[author], width=1.5, dash='solid'),
        name=author,
        opacity=0.4, # Keep lines subtle to prioritize markers
        hoverinfo='skip'
    ))

# b) Add Markers (The thematic "Clusters" per verse)
for author, group in df.groupby('Author'):
    fig.add_trace(go.Scatter(
        x=group['line_number'],
        y=group['Confidence_Score'],
        mode='markers',
        marker=dict(
            symbol=symbols[author],
            size=10,
            color=group['emotion_code'],
            colorscale=danki_colorscale,
            cmin=0,
            cmax=n_codes-1,
            line=dict(width=1, color='#FFFFFF')
        ),
        name=author,
        text=group['Emotion'],
        customdata=group[['Original_Text', 'Translated_Text']].values,
        hovertemplate=(
            "<b>EMOTION: %{text}</b><br>"
            "Poet: " + author + "<br>"
            "Confidence: %{y:.2f}<br>"
            "<i>%{customdata[0]}</i><br>"
            "<extra></extra>"
        )
    ))

# --- 4. LAYOUT UPDATES ---
fig.update_layout(
    title=dict(
        text="PLAYING WITH CLUSTERS: COMPARATIVE EMOTIONAL RADIOGRAPHY",
        font=dict(size=22, color='#33FFA2', family="Roboto")
    ),
    xaxis_title="VERSE SEQUENCE (CHRONOLOGY)",
    yaxis_title="EMOTIONAL INTENSITY SCORE",
    legend_title="POETESS IDENTITY",
    template="plotly_dark",
    width=1500,
    height=650,
    plot_bgcolor='#121212',
    paper_bgcolor='#121212',
    font_color='#FFFFFF',
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#2A2A2A', borderwidth=1),
    margin=dict(t=100)
)

# Refine Axes
fig.update_xaxes(gridcolor='#2A2A2A', zeroline=False)
fig.update_yaxes(gridcolor='#2A2A2A', zeroline=False)

# --- 5. EXPORT ---
output_path = os.path.join(current_dir, "comparative_trajectory.html")
fig.write_html(output_path)
fig.show()

print(f"✅ Dashboard generated: {output_path}")