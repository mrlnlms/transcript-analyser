# 5. Como funciona internamente
Quando você executa python run_analysis.py --project nome:
```python
# 1. CARREGA CONFIGURAÇÃO
config = load_config("projects/nome/config_analise.json")


# 2. LISTA ARQUIVOS
files = list_files("projects/nome/arquivos/*.txt")

# 3. PARA CADA ARQUIVO:
for file in files:
    # 3.1 Lê conteúdo
    text = read_file(file)
    
    # 3.2 Cria analisador
    analyzer = TranscriptAnalyzer(config)
    
    # 3.3 Executa análises
    result = analyzer.analyze(text)
    # Internamente faz:
    # - Análise de sentimento (TextBlob/NLTK)
    # - Modelagem de tópicos (LDA)
    # - Padrões linguísticos (regex + contadores)
    # - Métricas globais (cálculos estatísticos)
    
    # 3.4 Gera visualizações
    viz_manager = VisualizationManager()
    viz_manager.create_visualization("bar_chart", result)
    
    # 3.5 Salva resultados
    save_results("projects/nome/resultados/arquivo/", result)

````

Fluxo detalhado:
```mermaidgraph TD
    A[run_analysis.py] --> B[config_loader.py]
    B --> C[analyzer_core.py]
    C --> D[Análise Sentimento]
    C --> E[Análise Tópicos]
    C --> F[Padrões Linguísticos]
    D --> G[visualization_manager.py]
    E --> G
    F --> G
    G --> H[Salva HTML/PNG/MD]
````
