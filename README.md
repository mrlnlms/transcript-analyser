# Transcript Analyser Prototype Experiments

Curated reconstruction of the first transcript analysis prototype.

This initial version compares two Portuguese lecture transcripts with text
cleaning, stemming, TF-IDF, cosine similarity, Jaccard similarity and key phrase
overlap.

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

