# Prototype Experiments

Esta pasta reúne a linha exploratória inicial do projeto de análise de
transcrições.

Aqui o foco é menos arquitetura de software e mais entendimento analítico:
comparar transcrições, observar temas, gerar hipóteses e experimentar formas de
visualizar uma fala longa como objeto de pesquisa.

## O Que O Protótipo Faz

Há duas famílias de experimentos.

1. **Comparação entre transcrições**: compara duas transcrições em português
   usando limpeza de texto, stemming, TF-IDF, cosine similarity, Jaccard,
   sobreposição de termos, topic modeling com LDA, interpretação semântica por
   dicionário manual e gráficos estáticos.
2. **Análise de uma transcrição única**: analisa uma transcrição longa como
   narrativa temporal, com segmentos estimados, tópicos, sentimento simples,
   possíveis contradições, padrões linguísticos, coocorrência de conceitos,
   templates interpretativos, síntese narrativa e visualizações PNG.

As métricas são heurísticas. Elas devem ser usadas como apoio exploratório, não
como evidência final sem leitura qualitativa humana.

## Estrutura

```text
data/sample/                    Transcrições sample versionadas
docs/previews/                  Exemplos e artefatos visuais preservados
docs/source-map.md              Mapa entre snapshots originais e arquivos atuais
scripts/                        Entry points executáveis
src/prototype_experiments/      Módulos importáveis do protótipo
output/                         Gráficos gerados localmente, ignorados pelo Git
```

## Setup

A partir da raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r scripts/prototype/requirements.txt
python -m nltk.downloader punkt punkt_tab stopwords rslp
```

## Comando Principal

Rodar o fluxo mais completo: relatório narrativo no terminal mais visualizações
v2 em PNG.

```bash
MPLBACKEND=Agg .venv/bin/python scripts/prototype/scripts/analyze_interview_with_visuals.py
```

As imagens geradas ficam em:

```text
scripts/prototype/output/interview_visualizations_v2/
```

O arquivo mais útil para olhar primeiro é:

```text
scripts/prototype/output/interview_visualizations_v2/unified_timeline.png
```

## Outros Comandos

Comparar as duas transcrições sample:

```bash
MPLBACKEND=Agg .venv/bin/python scripts/prototype/scripts/compare_transcripts.py
```

Rodar a primeira análise rápida de transcrição única:

```bash
.venv/bin/python scripts/prototype/scripts/analyze_quick_interview.py
```

Rodar o analisador com templates interpretativos:

```bash
.venv/bin/python scripts/prototype/scripts/analyze_template_interview.py
```

Rodar o relatório narrativo sem gerar PNGs:

```bash
.venv/bin/python scripts/prototype/scripts/analyze_narrative_interview.py
```

Gerar o primeiro conjunto de visualizações:

```bash
MPLBACKEND=Agg .venv/bin/python scripts/prototype/scripts/generate_interview_visualizations.py
```

Gerar o conjunto v2 de visualizações:

```bash
MPLBACKEND=Agg .venv/bin/python scripts/prototype/scripts/generate_interview_visualizations_v2.py
```

## Outputs E Previews

Arquivos gerados localmente ficam em `output/`, que é ignorado pelo Git.

Alguns exemplos estão preservados em `docs/previews/` como evidência visual do
que o protótipo produz:

- `topic_analysis_estatistica_psicobio_aula_2024_vs_estatistica_psicobio_teoria_medida_2025.png`
- `interview_visualizations/emotional_timeline.png`
- `interview_visualizations_v2/unified_timeline.png`

O arquivo original de previews também foi preservado em:

```text
docs/previews/original/
```

Ele inclui capturas de dashboard, PNGs avulsos e `dash.pdf`.

## Nota Histórica

`docs/source-map.md` registra como os arquivos atuais se relacionam com os
snapshots e nomes originais do processo. Esse mapa existe para preservar a
história técnica sem obrigar o usuário a navegar pela pasta antiga cheia de
cópias, caches, outputs locais e arquivos quebrados.
