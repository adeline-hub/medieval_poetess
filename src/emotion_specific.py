import pandas as pd
import plotly.express as px
import os

# --- 1. DIRECTORY & DATA LOADING ---
current_dir = os.path.dirname(os.path.abspath(__file__))
CSV_NAME = "medieval_poetesses_complete.csv"
CSV_PATH = os.path.join(current_dir, CSV_NAME)

if not os.path.exists(CSV_PATH):
    # Fallback to the specific path from your screenshot if not in current folder
    CSV_PATH = "C:/Users/nambo/Documents/GitHub/medieval_poetess/data/" + CSV_NAME

if not os.path.exists(CSV_PATH):
    print(f"❌ ERROR: Could not find {CSV_NAME}")
else:
    df = pd.read_csv(CSV_PATH)
    
    # --- 2. DANKI BRAND PALETTE ---
    # We use a mix of our neons and muted tones for the various emotions
    danki_emotions_palette = [
        "#33FFA2", # Neon Green
        "#FF33FF", # Neon Violet
        "#00E5FF", # Cyan
        "#737373", # Muted Grey
        "#FFFFFF", # White
        "#444444", # Dark Grey
        "#1A1A1A"  # Deep Charcoal
    ]

    # --- 3. CREATE THE EMOTION VIOLIN PLOT ---
    # Note: Using 'Emotion' and 'Confidence_Score' from your saved CSV
    fig = px.violin(
        df,
        x='Emotion',
        y='Confidence_Score',
        box=True,
        points='all',  # Displays individual verses as dots next to the violin
        color='Emotion',
        color_discrete_sequence=danki_emotions_palette,
        title="DISTRIBUTION OF INTENSITY BY EMOTION TYPE"
    )

    # --- 4. APPLY DANKI BRAND STYLING ---
    fig.update_layout(
        title={
            'text': "EMOTIONAL INTENSITY PROFILE",
            'font': {'size': 20, 'color': '#33FFA2', 'family': 'Roboto'}
        },
        xaxis_title="DETECTED EMOTIONS",
        yaxis_title="CONFIDENCE SCORE (INTENSITY)",
        template="plotly_dark",
        width=1000,
        height=600,
        showlegend=False,
        plot_bgcolor='#121212',  # bg-charcoal
        paper_bgcolor='#121212', # bg-charcoal
        font=dict(color='#FFFFFF')
    )

    # Style axes and grid
    fig.update_xaxes(
        gridcolor='#2A2A2A', 
        zeroline=False, 
        tickfont=dict(color='#33FFA2', size=10)
    )
    fig.update_yaxes(
        gridcolor='#2A2A2A', 
        zeroline=False,
        tickformat='.0%' # Displays 0.8 as 80%
    )

    # --- 5. EXPORT & DISPLAY ---
    output_name = "emotion_intensity_distribution.html"
    fig.write_html(os.path.join(current_dir, output_name))
    print(f"✨ SUCCESS: {output_name} generated in DANKI style.")
    fig.show()