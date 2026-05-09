import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import re

# 1. Setup paths and data loading
BASE_DIR = Path(__file__).resolve().parent.parent 
TEXTS_DIR = BASE_DIR / "assets" / "texts"

fichiers = {
    'Marie de France': 'Marie_de_France_Lai_du_Chevrefeuille.txt',
    'Anna Komnene': 'Anne_Comnene_Alexiade.txt', 
    'Wallada': 'Wallada bint al-Mustakfi.txt',
    'Hildegard von Bingen': 'Hildegarde_O_clarissima_Mater.txt'
}

# 2. Process texts into a DataFrame
all_data = []
for autrice, nom_fichier in fichiers.items():
    chemin_complet = TEXTS_DIR / nom_fichier
    if chemin_complet.exists():
        with open(chemin_complet, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
            for ligne in lignes:
                clean = ligne.strip()
                if len(clean) > 20: # Only keep substantial lines
                    all_data.append({'autrice': autrice, 'texte_complet': clean})

df = pd.DataFrame(all_data)

# 3. Streamlit UI with DANKI BRAND CSS
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .extract-card {
        background-color: #1A1A1A;
        border: 1px solid #2A2A2A;
        padding: 20px;
        border-radius: 8px;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .author-name {
        color: #33FFA2;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .quote-text {
        color: #FFFFFF;
        font-style: italic;
        font-family: 'Georgia', serif;
        font-size: 1.1rem;
        line-height: 1.4;
    }
    </style>
""", unsafe_allow_html=True)

st.title("MEDIEVAL POETESS: RANDOM QUOTE")

# 4. Logic: Sample 1 random row per author
if not df.empty:
    # Group by author and pick one random line
    random_extracts = df.groupby('autrice').sample(n=1)
    
    # Display in 4 columns
    cols = st.columns(4)
    
    # Map each author to a specific column to keep the layout stable
    for i, (idx, row) in enumerate(random_extracts.iterrows()):
        with cols[i]:
            st.markdown(f"""
                <div class="extract-card">
                    <div class="author-name">{row['autrice']}</div>
                    <div class="quote-text">“{row['texte_complet']}”</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("No text found. Check your .txt files in assets/texts/")