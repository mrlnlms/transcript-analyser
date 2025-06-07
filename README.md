# Transcript Analyser Prototype Experiments

Curated reconstruction of the first transcript analysis prototype.

This version compares Portuguese lecture transcripts with text cleaning,
stemming, TF-IDF, cosine similarity, Jaccard similarity, key phrase overlap,
LDA topic modeling, smart topic interpretation and a weighted similarity score.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab stopwords rslp
```

## Run

```bash
python scripts/compare_transcripts.py
```
