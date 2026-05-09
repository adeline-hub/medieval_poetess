import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from pathlib import Path
import re


# 1. Gestion des chemins (Dynamique)
BASE_DIR = Path(__file__).resolve().parent.parent # Remonte au dossier racine 'medieval_poetess'
TEXTS_DIR = BASE_DIR / "assets" / "texts"

fichiers = {
    'Marie de France': 'Marie_de_France_Lai_du_Chevrefeuille.txt',
    'Anna Komnene': 'Anne_Comnene_Alexiade.txt', # Pense à renommer tes fichiers réels ici
    'Wallada': 'Wallada bint al-Mustakfi.txt',
    'Hildegard von Bingen': 'Hildegarde_O_clarissima_Mater.txt'
}
# Racines de mots pour maximiser les détections
themes = {
    'amour': r'amour|aim|mari|baiser|passion|désir|amie|enlacer',
    'pouvoir': r'père|césar|lignée|éclat|supériorité|autocrate|campagne|autorité|ordre|roi|reine|chevalier',
    'nature': r'chèvrefeuille|noisetier|forêt|soleil|branche|fleur|lune|palmier|terre|aurore'
}
# Racines de mots pour maximiser les détections
themes = {
    'amour': r'amour|aim|mari|baiser|passion|désir|amie|enlacer',
    'pouvoir': r'père|césar|lignée|éclat|supériorité|autocrate|campagne|autorité|ordre|roi|reine|chevalier',
    'nature': r'chèvrefeuille|noisetier|forêt|soleil|branche|fleur|lune|palmier|terre|aurore'
}

all_data = []

# --- CORRECTION ICI : On boucle sur les fichiers, pas sur les thèmes ---
for autrice, nom_fichier in fichiers.items():
    chemin_complet = TEXTS_DIR / nom_fichier
    
    if chemin_complet.exists():
        with open(chemin_complet, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
            
            for i, ligne in enumerate(lignes):
                clean = ligne.strip().lower()
                # On ne traite que les lignes avec du contenu
                if len(clean) > 5:
                    # Comptage via Regex
                    s_amour = len(re.findall(themes['amour'], clean))
                    s_pouvoir = len(re.findall(themes['pouvoir'], clean))
                    s_nature = len(re.findall(themes['nature'], clean))
                    
                    # JITTER : Étale les points pour éviter les superpositions à (0,0)
                    all_data.append({
                        'autrice': autrice,
                        'texte_complet': clean,
                        'occ_amour': s_amour + np.random.uniform(-0.3, 0.3),
                        'occ_pouvoir': s_pouvoir + np.random.uniform(-0.3, 0.3),
                        'occ_nature': (s_nature * 8) + 5  # Taille des points
                    })
    else:
        print(f"Fichier introuvable : {nom_fichier}")

# Vérification du DataFrame
if not all_data:
    print("Aucune donnée trouvée. Vérifie l'emplacement de tes fichiers .txt")
else:
    df = pd.DataFrame(all_data)

    # 2. Clustering K-Means
    # On ajuste n_clusters selon le nombre d'autrices trouvées
    n_clusters = min(4, len(df['autrice'].unique()))
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    df['cluster'] = kmeans.fit_predict(df[['occ_amour', 'occ_pouvoir']]).astype(str)

    # Mapping avec nomenclature académique
    cluster_academic_names = {
        '0': 'Segments Narratifs Neutres',
        '1': 'Topos de la Lyrique Amoureuse',
        '2': 'Lexique de l\'Autorité et du Pouvoir',
        '3': 'Allégories Naturelles et Cosmologiques'
    }

    df['Analyse Thématique'] = df['cluster'].map(cluster_academic_names)

    # Mise à jour de la figure
    fig = px.scatter(
        df, x='occ_amour', y='occ_pouvoir', 
        color='Analyse Thématique',
        size='occ_nature',
        hover_name='autrice',
        title="<b>Classification Lexicométrique des Écrits Féminins Médiévaux</b>",
        color_discrete_sequence=['#33FFA2', '#FF33FF', '#737373', '#FFFFFF'], # Couleurs conservées
        template="plotly_dark"
    )

    # Ajustement de la légende pour le style académique
    fig.update_layout(
        legend_title_text='Classification Critique',
        font_family="Arial", # Plus sobre pour l'académique
        xaxis_title="Indice de Densité Émotionnelle",
        yaxis_title="Indice de Lexique Politique/Curial"
    )

    fig.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color='white')))
    fig.show()