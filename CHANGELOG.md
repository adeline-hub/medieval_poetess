# Changelog

All notable changes to this project are documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org) and is archived on Zenodo with a unique DOI for each major release.

For more information, visit:  
🔗 Project site: https://adeline-hub.github.io/medieval_poetess/  
🔗 Repository: [https://github.com/adeline-hub/medieval_poetess]  
🔗 Citable DOI versions: https://doi.org/10.5281/zenodo.XXXXXXX

---

## [Unreleased]

*Next development phase — not yet archived.*

### Added
- Support for community-submitted texts (African, Asian, pre-Columbian American medieval women)
- Template for contribution (GitHub Discussions)
- Placeholder pipeline for multilingual embedding (XLM-RoBERTa)

### Changed
- Refactored emotion pipeline for modular reproducibility
- Improved verse-level tokenization for poetic line breaks

---

## v1.0.0 — 2025-04-05

**Initial research release — cited in "Mapping the Pulse of Medieval Women’s Writing"**

### Added
- NLP pipeline for emotion classification:
  - Translation: Helsinki-NLP (fr, la, grc, ar → en)
  - Vectorization: DistilRoBERTa
  - 7-class emotion prediction (joy, sadness, anger, fear, surprise, love, despair)
- PCA + K-Means clustering (4 thematic zones)
- Interactive Plotly dashboards:
  - Emotional trajectories over verse sequence
  - Cluster maps (semantic space)
  - Violin plots of emotional intensity
  - Poetic remix generator
- Four-author corpus:
  - Anna Komnene (Byzantine Empire)
  - Hildegard von Bingen (Holy Roman Empire)
  - Marie de France (Anglo-Norman England)
  - Wallada bint al-Mustakfi (Al-Andalus)

### Resources
- Dataset: `emotions_df.csv` (processed)
- Notebooks: `nlp_pipeline.ipynb`, `clustering_analysis.ipynb`, `visualizations.py`
- Interactive HTML: `assets/` directory (Plotly exports)

### DOI
- Archived at: https://doi.org/10.5281/zenodo.1234567

---

## v2.0.0 — 2025-XX-XX (planned)

**Upgrade: Diachronic and Spatial Analysis**

### Added
- **Timeline Series Module**:  
  Treats verse order as chronological proxy; enables modeling of affective pacing and narrative arc evolution
- **Historical GIS Prototype**:  
  - Geocoded nodes: Constantinople, Bingen, Caen, Córdoba  
  - Preliminary linkage between lexical clusters and geographic location  
  - Tools: GeoPandas, Folium
- `geodata/` directory (GeoJSON, metadata)
- Coming soon section in dashboard

### Changed
- Refactored PCA pipeline to support longitudinal visualization
- Improved UI: responsive layout, better tooltip handling in Plotly

### Fixed
- Minor misalignment in verse indexing (multi-line lais now segmented correctly)
- Translation stability for Old French idioms

### DOI
- To be assigned upon release

---

## v3.0.0 — Future

**Community Expansion & Multilingual Integration**

### Planned
- Integration of community-submitted texts:
  - Li Qingzhao (China)
  - Akka Mahadevi (India)
  - Kristos Samra (Ethiopia)
  - Pre-Columbian oral traditions (documented forms)
- Support for non-Latin scripts (CJK, Ge'ez, Arabic) in NLP pipeline
- XLM-RoBERTa for cross-lingual sentiment analysis
- Updated cluster architecture (k=6)
- Full open submission form (GitHub Discussions + template)

> This version will mark the transition from prototype to participatory archive.
