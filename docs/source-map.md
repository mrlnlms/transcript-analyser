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

## Version 5

- Original source: `quick-interview.py`
- Curated module: `src/prototype_experiments/interview_quick_analysis.py`
- Curated script: `scripts/analyze_quick_interview.py`

This update starts a new experiment family: instead of comparing two
transcripts, the prototype analyzes one transcript as a narrative object with
estimated time segments, topics, simple sentiment, contradictions, linguistic
patterns and concept co-occurrence.

## Version 6

- Original source: `taca.py`
- Curated module: `src/prototype_experiments/interview_template_analysis.py`
- Curated script: `scripts/analyze_template_interview.py`

This update expands the quick analyzer with temporal phase analysis, richer
concept-network context and interpretive templates. The output combines
automatic insights with fill-in prompts intended for qualitative analysis.

## Version 7

- Original sources: `interview-analyzer.py`, `interview_analyzer_v3.py`
- Curated module: `src/prototype_experiments/narrative_interview_analysis.py`
- Curated script: `scripts/analyze_narrative_interview.py`

This update introduces the larger narrative analyzer. It organizes the output as
a dual report: technical/structural analysis followed by narrative synthesis,
storyline, hypotheses and recommendations.

The first hyphenated snapshot referenced `generate_dual_report` without defining
it correctly. The curated version uses the importable underscore snapshot because
it preserves the same narrative analyzer line in a runnable state.
