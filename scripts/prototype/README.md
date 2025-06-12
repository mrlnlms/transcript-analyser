# Transcript Analyser Prototype Experiments

Curated reconstruction of the first transcript analysis prototype.

This repository preserves the useful technical line of the original prototype in
a cleaner, runnable form. The original work grew through copied scripts,
renamed files, local outputs and exploratory experiments. This version keeps the
main ideas, normalizes the file layout and documents how each stage can be run
again.

## What This Prototype Does

The project has two experiment families:

1. **Transcript comparison**: compares two Portuguese lecture transcripts using
   text cleaning, stemming, TF-IDF, cosine similarity, Jaccard similarity, key
   phrase overlap, LDA topic modeling, semantic topic interpretation and static
   comparison charts.
2. **Single-transcript interview analysis**: analyzes one long transcript as a
   narrative object, with estimated time segments, topics, simple sentiment,
   contradictions, linguistic patterns, concept co-occurrence, interpretive
   templates, narrative synthesis and PNG visualizations.

The code is still a prototype. The metrics are heuristic and should be validated
with human qualitative analysis before being treated as evidence.

## Repository Layout

```text
data/sample/                    Versioned sample transcripts
docs/previews/                  Selected and archived generated examples
docs/source-map.md              Mapping from original files to curated files
scripts/                        Runnable entry points
src/prototype_experiments/      Importable prototype modules
output/                         Generated charts, ignored by Git
```

## Setup

Create an environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab stopwords rslp
```

In the original reconstruction workspace, the historical virtualenv can also be
used:

```bash
../transcript-analyser-prototype/compare-env/bin/python <script>
```

## Main Command

Run the most complete prototype flow: narrative analysis plus v2 visualizations.

```bash
MPLBACKEND=Agg python scripts/analyze_interview_with_visuals.py
```

This prints the textual report in the terminal and writes PNGs to:

```text
output/interview_visualizations_v2/
```

To open the generated images on macOS:

```bash
open output/interview_visualizations_v2
```

The most useful image to inspect first is:

```text
output/interview_visualizations_v2/unified_timeline.png
```

## Other Commands

Compare the two sample transcripts:

```bash
MPLBACKEND=Agg python scripts/compare_transcripts.py
```

Run the first quick single-transcript analyzer:

```bash
python scripts/analyze_quick_interview.py
```

Run the template-based interpretive analyzer:

```bash
python scripts/analyze_template_interview.py
```

Run the narrative dual-report analyzer without PNG generation:

```bash
python scripts/analyze_narrative_interview.py
```

Generate the first interview visualization set:

```bash
MPLBACKEND=Agg python scripts/generate_interview_visualizations.py
```

Generate the improved v2 visualization set:

```bash
MPLBACKEND=Agg python scripts/generate_interview_visualizations_v2.py
```

## Outputs And Previews

Generated files are written under `output/`, which is ignored by Git because the
charts are reproducible.

Selected previews are preserved in `docs/previews/`:

- `topic_analysis_estatistica_psicobio_aula_2024_vs_estatistica_psicobio_teoria_medida_2025.png`
- `interview_visualizations/emotional_timeline.png`
- `interview_visualizations_v2/unified_timeline.png`

The original preview archive is also preserved under
`docs/previews/original/`. It includes full dashboard captures, the standalone
visualization PNGs and `dash.pdf`, which documents the mature visual report that
the prototype was able to produce.

These previews are documentation evidence, not required inputs.

## Reconstruction Notes

The cleaned history is intentionally not a byte-for-byte copy of the original
folder. The reconstruction keeps the technical progression while removing local
caches, generated outputs, duplicated scripts, broken snapshots, exploratory
tests and sensitive/private transcripts.

`docs/source-map.md` records how original prototype files map to the curated
modules and scripts in this repository. It is mainly historical documentation;
the repository should remain runnable even if the original prototype folder is
deleted.
