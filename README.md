-------------------------------------------------------------------------------
medieval_poetess
-------------------------------------------------------------------------------

Medieval Poetesses: Emotional Intensity in Historical Verse

A .danki studio project

https://adeline-hub.github.io/medieval_poetess/

-------------------------------------------------------------------------------

This project explores the linguistic and emotional dimensions of texts by four 
medieval women:

- Anna Komnene (Byzantine Empire)
- Hildegard von Bingen (Holy Roman Empire)
- Marie de France (Anglo-Norman England)
- Wallada bint al-Mustakfi (Al-Andalus)

Using natural language processing (NLP), machine learning, and interactive 
visualization, the analysis focuses on:

- Emotional trajectories across verse sequences
- Thematic clustering via K-Means
- Stylistic patterns via PCA and TF-IDF
- Narrative rhythm as a time series

The goal is not comparative identity, but structural resonance: to map affect, 
rhythm, and theme across linguistic and cultural boundaries.

-------------------------------------------------------------------------------

Methods

1. Linguistic Feature Extraction (NLP)
   - Texts processed via Helsinki-NLP (translation)
   - Emotion classification using DistilRoBERTa
   - Vectorization and semantic analysis

2. Comparative Stylometry (PCA)
   - Dimensionality reduction of linguistic features
   - Visualization of tonal journeys (connected scatterplots)

3. Unsupervised Clustering (K-Means)
   - Four thematic clusters identified:
     1. Nature / Love
     2. Power / History
     3. Spirituality
     4. Loss / Memory
   - Convex hulls define emotional climates

4. Interactive Visualization (Plotly)
   - Emotional trajectories over time
   - Violin plots of intensity distribution
   - Comparative dashboards and poetic remixes

Coming soon:
- Timeline series modeling: affect as a sequential signal
- Historical GIS layer: geographic mapping of keyword clusters
  (Constantinople, Bingen, Caen, Córdoba)

-------------------------------------------------------------------------------

Tools

- Python
- pandas
- scikit-learn
- transformers (Hugging Face)
- Plotly
- Streamlit
- GeoPandas (upcoming)

-------------------------------------------------------------------------------

Sources

- Anna Komnene: Alexiad (Wikisource, BnF Gallica)
- Hildegard von Bingen: O Clarissima Mater (critical editions)
- Marie de France: Lais, Chevrefeuille (BnF, Anglo-Norman texts)
- Wallada bint al-Mustakfi: Arabic poetry fragments (Wikipedia)
- NLP models: Helsinki-NLP, DistilRoBERTa (Hugging Face)

-------------------------------------------------------------------------------

Call for Contributions

This project is open to expansion. If you know of a text by a medieval woman 
from Africa, Asia, or the pre-Columbian Americas (5th–15th c.), please share:

- The text (original or translation)
- Author (if known), origin, century
- Source (manuscript, edition, oral tradition)

Contact: nambona@pm.me

Even one line may shift the cluster.

-------------------------------------------------------------------------------

