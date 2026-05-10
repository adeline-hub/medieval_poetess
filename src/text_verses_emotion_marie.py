import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# --- 1. LOAD DATA ---
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "medieval_poetesses_complete.csv"

if not CSV_PATH.exists():
    print(f"Error: {CSV_PATH} not found.")
else:
    df = pd.read_csv(CSV_PATH)

    # Pre-processing: Create line numbers per author and encode emotions
    df['line_number'] = df.groupby('Author').cumcount() + 1
    df['emotion_code'] = pd.Categorical(df['Emotion']).codes
    authors = df['Author'].unique()

    # --- 2. GENERATE INDIVIDUAL CHARTS ---
    for author in authors:
        df_plot = df[df['Author'] == author].copy()
        
        fig = go.Figure()

        # Trace 1: The Connecting Line (Pulse)
        fig.add_trace(go.Scatter(
            x=df_plot['line_number'],
            y=df_plot['Confidence_Score'],
            mode='lines',
            line=dict(color='#737373', width=1, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Trace 2: The Emotional Nodes
        fig.add_trace(go.Scatter(
            x=df_plot['line_number'],
            y=df_plot['Confidence_Score'],
            mode='markers',
            marker=dict(
                size=12,
                color=df_plot['emotion_code'],
                colorscale=[[0, '#33FFA2'], [1, '#FF33FF']], # Neon Green to Neon Violet
                line=dict(width=1.5, color='#121212'),
                showscale=True,
                colorbar=dict(
                    title="EMOTION",
                    tickvals=list(range(len(df['Emotion'].unique()))),
                    ticktext=list(df['Emotion'].unique()),
                    tickfont=dict(color='#737373', size=10)
                )
            ),
            customdata=df_plot[['Original_Text', 'Emotion']],
            hovertemplate="""
            <b>VERSE %{x}</b><br>
            <span style='color:#33FFA2'>Intensity: %{y:.2f}</span><br>
            <span style='color:#FF33FF'>Emotion: %{customdata[1]}</span><br>
            <i>%{customdata[0]}</i><extra></extra>
            """
        ))

        # --- 3. DANKI BRAND LAYOUT ---
        fig.update_layout(
            title=dict(
                text=f"TRAJECTORY ANALYSIS: {author.upper()}",
                font=dict(size=18, color='#33FFA2', family="Roboto")
            ),
            xaxis_title="VERSE SEQUENCE",
            yaxis_title="CONFIDENCE SCORE",
            plot_bgcolor='#121212',
            paper_bgcolor='#121212',
            font_color='#FFFFFF',
            width=900,
            height=500,
            xaxis=dict(gridcolor='#2A2A2A', zeroline=False),
            yaxis=dict(gridcolor='#2A2A2A', zeroline=False, range=[0, 1.1])
        )

        # --- 4. EXPORT ---
        filename = f"trajectory_{author.replace(' ', '_').lower()}.html"
        fig.write_html(BASE_DIR / filename)
        print(f"✅ Generated: {filename}")

    # Optional: Display the last one generated
    fig.show()