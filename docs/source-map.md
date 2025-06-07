# Source Map

This repository is a curated reconstruction from
`../transcript-analyser-prototype`.

## Version 1

- Original source: `compare-text.py`
- Curated module: `src/prototype_experiments/transcript_comparison.py`
- Original inputs:
  - `Estatistica Psicobio III Aula I 2024.txt`
  - `Estatistica Psicobio III 2025 Teo da Medida.txt`
- Curated inputs:
  - `data/sample/estatistica_psicobio_aula_2024.txt`
  - `data/sample/estatistica_psicobio_teoria_medida_2025.txt`

The implementation keeps the original comparison behavior while normalizing
file names and module entry points.

## Version 2

- Original source: `multi-compare.py`
- Curated module: `src/prototype_experiments/transcript_comparison.py`

This update keeps the same curated module name and evolves the comparison
workflow with LDA topic modeling, topic distribution comparison and weighted
similarity ranking.

## Version 3

- Original source: `smart-analyzer.py`
- Curated module: `src/prototype_experiments/transcript_comparison.py`

This update adds a hand-built semantic dictionary for automatic topic
interpretation. LDA still discovers the topic terms, but the script now maps
those terms to human-readable categories such as teaching methodology,
measurement/statistics, attributes/properties and phenomena/objects.

## Version 4

- Original source: `final-analyzer-visual.py`
- Curated module: `src/prototype_experiments/transcript_comparison.py`

This update adds static visual output for the comparison workflow: topic
distribution bars, topic-word heatmap, word cloud and topic similarity matrix.
In the curated version, generated PNGs are written to `output/visualizations/`
instead of the project root.

One generated example is preserved in `docs/previews/` as documentation evidence.
