# Transcript Analyser

Experimentos em análise computacional de transcrições em português.

Este projeto nasceu de uma pergunta prática de pesquisa: como usar técnicas de
data science e NLP para apoiar a leitura de transcrições longas, sem tratar os
resultados automáticos como interpretação final?

A ideia central não é substituir análise qualitativa humana. O objetivo é criar
formas de explorar corpus textuais, comparar transcrições, localizar padrões,
gerar visualizações e levantar hipóteses que depois precisam ser revisadas por
uma pessoa pesquisadora ou analista.

## O Que Tem Aqui

O repositório reúne duas linhas de trabalho.

### 1. Protótipo exploratório

Local: `scripts/prototype/`

Essa é a parte mais próxima da pergunta original de pesquisa. Ela inclui:

- comparação entre duas transcrições por similaridade textual;
- limpeza, stopwords em português e stemming;
- TF-IDF, cosine similarity e Jaccard similarity;
- topic modeling com LDA;
- interpretação semântica por dicionários manuais;
- análise de uma transcrição única por blocos temporais;
- sentimento simples por listas de palavras;
- hesitações, marcadores de certeza/incerteza e rede de conceitos;
- relatórios narrativos com hipóteses abertas;
- visualizações PNG para inspeção qualitativa.

O protótipo é heurístico. Ele ajuda a organizar a leitura, mas não produz
evidência definitiva sozinho.

### 2. Versão modular

Local: raiz do projeto (`run_analysis.py`, `core/`, `engine/`, `visuals/`)

Essa linha tenta transformar parte da exploração em uma estrutura mais
organizada de software:

- CLI para criar, listar e analisar projetos;
- analyzers plugáveis;
- orquestrador de análises;
- gráficos HTML;
- relatórios Markdown;
- configuração por arquivos;
- projetos de exemplo em `projects/`.

Essa versão é mais robusta como arquitetura, mas o relatório ainda é mais
técnico do que interpretativo. A camada de leitura qualitativa do protótipo é
mais rica.

## Como Rodar

### Setup

```bash
git clone https://github.com/mrlnlms/transcript-analyser.git
cd transcript-analyser

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt -r scripts/prototype/requirements.txt
python -m nltk.downloader punkt punkt_tab stopwords rslp
```

### Validar ambiente

```bash
MPLBACKEND=Agg .venv/bin/python run_analysis.py --test-visuals
```

## Rodar o Protótipo

Comparar duas transcrições sample:

```bash
MPLBACKEND=Agg .venv/bin/python scripts/prototype/scripts/compare_transcripts.py
```

Comparar arquivos específicos:

```bash
MPLBACKEND=Agg .venv/bin/python scripts/prototype/scripts/compare_transcripts.py arquivo1.txt arquivo2.txt
```

Rodar a análise narrativa com visualizações:

```bash
MPLBACKEND=Agg .venv/bin/python scripts/prototype/scripts/analyze_interview_with_visuals.py
```

Os PNGs gerados ficam em:

```text
scripts/prototype/output/interview_visualizations_v2/
```

## Rodar a Versão Modular

Listar projetos disponíveis:

```bash
.venv/bin/python run_analysis.py --list-projects
```

Analisar um projeto de exemplo:

```bash
MPLBACKEND=Agg .venv/bin/python run_analysis.py --project teste_auto_individual
```

Os resultados ficam em:

```text
projects/teste_auto_individual/output/
```

O output inclui um relatório Markdown e gráficos HTML:

```text
report_entrevista_completa.md
timeline_emocional.html
hierarquia_topicos.html
rede_conceitos.html
metricas_globais.html
padroes_linguisticos.html
wordcloud.html
contradicoes.html
frequencia_palavras.html
```

## Estrutura

```text
transcript-analyser/
├── run_analysis.py              # CLI da versão modular
├── core/                        # managers, engine core, geração de relatório
├── engine/analyzers/            # analyzers plugáveis
├── visuals/charts/              # gráficos HTML
├── resources/                   # léxicos e listas auxiliares
├── projects/                    # projetos de exemplo e outputs locais
├── scripts/prototype/           # linha exploratória original
└── docs/                        # notas técnicas e documentação histórica
```

## Limitações Importantes

- Similaridade textual não prova equivalência de significado.
- LDA sugere agrupamentos de palavras, não temas qualitativos prontos.
- Rótulos semânticos do protótipo vêm de dicionários manuais.
- Sentimento por listas de palavras é frágil e depende muito do contexto.
- Segmentação temporal por palavras por minuto é estimada.
- Hesitações podem indicar oralidade, estilo de fala, transcrição ruim ou carga
  cognitiva. Não devem ser interpretadas isoladamente.
- Visualizações ajudam a localizar padrões, mas podem dar aparência de precisão
  maior do que o método sustenta.

## Para Que Serve

Este projeto é útil para:

- estudar técnicas de NLP aplicadas a transcrições em português;
- explorar entrevistas, aulas ou corpus textuais longos;
- comparar documentos por proximidade lexical e temática;
- gerar hipóteses iniciais para análise qualitativa;
- experimentar formas de visualização de material textual;
- pensar a ponte entre UX research, análise qualitativa e data science.

Ele não é uma ferramenta validada para tomada de decisão automática, diagnóstico
ou conclusão interpretativa sem revisão humana.

## Licença

MIT.
