import pandas as pd
import plotly.express as px
from pathlib import Path

# --- 1. LOAD DATA ---
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "medieval_poetesses_complete.csv"

if not CSV_PATH.exists():
    print("CSV not found. Please run the data generation script first.")
else:
    df = pd.read_csv(CSV_PATH)

    # --- 2. DANKI BRAND PALETTE ---
    # One unique neon for each of the 4 poetesses
    danki_palette = ["#33FFA2", "#FF33FF", "#00E5FF", "#737373"] 

    # --- 3. CREATE VIOLIN PLOT ---
    fig_violin = px.violin(
        df,
        x="Author",
        y="Confidence_Score",
        color="Author",
        box=True,         # Show the quartiles inside the violin
        points="all",     # Show every single verse as a dot
        hover_data=["Original_Text", "Emotion"],
        color_discrete_sequence=danki_palette
    )

    # --- 4. APPLY BRANDED STYLING ---
    fig_violin.update_layout(
        title={
            'text': "EMOTIONAL DENSITY DISTRIBUTION BY POETESS",
            'font': {'size': 20, 'color': '#33FFA2', 'family': 'Roboto'}
        },
        yaxis_title="INTENSITY SCORE",
        xaxis_title="POETESS IDENTITY",
        template="plotly_dark",
        width=1000,
        height=600,
        showlegend=False,
        plot_bgcolor='#121212',
        paper_bgcolor='#121212',
        font=dict(color='#FFFFFF'),
        # Dynamic annotations for the 4 voices
        annotations=[
            dict(x='Marie de France', y=1.1, text="High Variety", showarrow=False, font=dict(color='#33FFA2')),
            dict(x='Anna Komnene', y=1.1, text="Controlled Rhetoric", showarrow=False, font=dict(color='#FF33FF')),
            dict(x='Wallada', y=1.1, text="Fierce Independence", showarrow=False, font=dict(color='#00E5FF')),
            dict(x='Hildegard von Bingen', y=1.1, text="Mystical Intensity", showarrow=False, font=dict(color='#737373'))
        ]
    )

    # Clean up grid lines to match DANKI border-color
    fig_violin.update_xaxes(gridcolor='#2A2A2A', zeroline=False)
    fig_violin.update_yaxes(gridcolor='#2A2A2A', zeroline=False)

    # --- 5. EXPORT & SHOW ---
    fig_violin.write_html(BASE_DIR / "emotional_distribution.html")
    fig_violin.show()
    print("✅ Success: emotional_distribution.html generated in DANKI style.")