# About

`transcript-analyser` é um projeto experimental sobre análise computacional de
transcrições em português.

O ponto de partida foi uma dúvida comum em pesquisa qualitativa e UX research:
depois de transcrever entrevistas, aulas ou conversas longas, como encontrar
padrões sem perder a necessidade de leitura humana?

O projeto explora duas perguntas principais:

1. Duas transcrições falam de coisas parecidas?
2. O que uma única transcrição longa sugere quando observada por temas, tempo,
   padrões linguísticos, sentimento simples e redes de conceitos?

Para isso, combina técnicas simples de NLP e text mining:

- limpeza e normalização de texto;
- stopwords e stemming em português;
- TF-IDF, cosine similarity e Jaccard;
- topic modeling com LDA;
- dicionários semânticos manuais;
- análise temporal estimada;
- contagem de hesitações e marcadores discursivos;
- visualizações estáticas e HTML.

O projeto tem uma parte mais exploratória, em `scripts/prototype/`, e uma parte
mais estruturada como software, na raiz do repositório. A primeira preserva
melhor a perspectiva de pesquisa. A segunda organiza a execução em analyzers,
orquestrador, CLI e outputs padronizados.

Este repositório deve ser lido como um laboratório de análise de transcrições,
não como um produto final de análise qualitativa. Os resultados automáticos
servem para orientar leitura, comparação e formulação de hipóteses. A
interpretação continua dependendo de revisão humana, contexto e critério
metodológico.
