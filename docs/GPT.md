# run_analysis.py (só CLI e orquestração)
AnalysisRunner (150 linhas)
  ├── run_single_analysis()
  ├── run_comparative_analysis() 
  └── delega para outros módulos

# engine/analysis_orchestrator.py (novo)
AnalysisOrchestrator
  ├── process_files()
  ├── aggregate_results()
  └── coordinate_workflow()

# visuals/visualization_orchestrator.py (novo)
VisualizationOrchestrator
  ├── generate_all_visualizations()
  ├── _create_metrics_chart()
  ├── _create_timeline()
  ├── _create_network()
  └── ... (cada visualização em método separado)

# reports/report_generator.py (novo)
ReportGenerator
  ├── generate_markdown_reports()
  ├── generate_summary()
  └── create_comparative_report()


---

# Prompt de introdução para novo chat.
---
Alguma informação relevante
---
Crie os artefatos para cada documento que enviei para você, com isso você consegue ter mais contexto também, além de 
---
#Contexto recente:
[... contexto-conversa-anterior]

[minha-resposta]
