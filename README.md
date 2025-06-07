# Transcript Analyser Prototype Experiments

Curated reconstruction of the first transcript analysis prototype.

This version compares Portuguese lecture transcripts with text cleaning,
stemming, TF-IDF, cosine similarity, Jaccard similarity, key phrase overlap,
LDA topic modeling, smart topic interpretation, a weighted similarity score and
static topic visualizations.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab stopwords rslp
```

## Run

```bash
MPLBACKEND=Agg python scripts/compare_transcripts.py
```

Generated charts are written to `output/visualizations/`.

An example chart from the reconstructed prototype is kept in
`docs/previews/topic_analysis_estatistica_psicobio_aula_2024_vs_estatistica_psicobio_teoria_medida_2025.png`.

Run the first single-transcript interview analyzer:

```bash
python scripts/analyze_quick_interview.py
```
