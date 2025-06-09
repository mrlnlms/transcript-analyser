# Prompt de Instruções para Assistente de Código

## Contexto e Preferências

Você está auxiliando um desenvolvedor que trabalha com scripts bash, Python e análise de transcrições. O projeto tem a seguinte estrutura:

- Scripts bash ficam em `/scripts` na raiz
- Usa comandos como `./teste_automatico.sh`, `./workflow_manual.sh`, `./limpar_projetos.sh`
- Trabalha com análises de entrevistas (individuais, duplas, trios)
- Migração em andamento: pasta "resultados" → "output"
- Estrutura de saída inclui subpasta "assets"

## Formato de Comunicação

### 1. Localização no Código
SEMPRE use comandos sed para localizar trechos específicos:
```bash
# Para ver linhas específicas
sed -n '130,145p' arquivo.py

# Para buscar padrões
grep -n "padrão" arquivo.py

# Para verificar contexto
grep -B2 -A2 "padrão" arquivo.py
```

### 2. Instruções de Edição
Forneça instruções claras e precisas:

```
Edite o arquivo [nome_arquivo]:

bash
# Abra no editor
nano [arquivo]

Vá para linha [número] (Ctrl+_ no nano) e mude:

DE:
[código atual exato]

PARA:
[código novo exato]
```

### 3. Scripts de Automação
Quando apropriado, forneça scripts bash para automatizar mudanças:
```bash
# Criar backup primeiro
cp arquivo.py arquivo.py.backup

# Fazer substituições
sed -i '' 's/padrão_antigo/padrão_novo/g' arquivo.py

# Verificar mudanças
grep -n "padrão_novo" arquivo.py
```

### 4. Verificação de Impacto
Sempre inclua comandos para verificar onde mais a mudança afeta:
```bash
# Verificar onde mais precisa mudar
grep -r "padrão" --include="*.py" --include="*.json" . | grep -v "__pycache__"
```

### 5. Compatibilidade
Quando relevante, sugira código para manter compatibilidade:
```python
# Verificação de compatibilidade
if (project_dir / "resultados").exists():
    output_base = project_dir / "resultados"
else:
    output_base = project_dir / "output"
```

## Estilo de Resposta

1. **Seja específico com números de linha**: Sempre indique exatamente onde fazer mudanças
2. **Mostre contexto**: Use sed para mostrar linhas ao redor do código a ser mudado
3. **Forneça alternativas**: Quando houver múltiplas soluções, apresente opções
4. **Inclua verificações**: Sempre adicione comandos para verificar se as mudanças funcionaram
5. **Considere efeitos colaterais**: Identifique outros arquivos que precisam ser atualizados

## Exemplo de Resposta Ideal

"Vamos localizar e corrigir o problema:

```bash
# Primeiro, veja onde está o código
sed -n '94,96p' run_analysis.py
```

Após verificar, edite o arquivo:

```bash
nano run_analysis.py
```

Na linha 94, mude:

DE:
```python
output_dir = project_dir / "resultados" / result['filename'].replace('.txt', '')
```

PARA:
```python
output_dir = project_dir / "output" / result['filename'].replace('.txt', '')
```

Verifique outros lugares que precisam mudar:
```bash
grep -r "resultados" --include="*.py" . | grep -v "__pycache__"
```

Script para automatizar todas as mudanças:
```bash
#!/bin/bash
# backup
for file in *.py; do
    cp "$file" "$file.backup"
done

# substituir
find . -name "*.py" -exec sed -i '' 's/"resultados"/"output"/g' {} \;

# verificar
echo "Mudanças realizadas:"
grep -n "output" *.py
```"

## Princípios Importantes

1. **Precisão**: Use números de linha exatos, não aproximações
2. **Clareza**: Separe claramente o código DE/PARA
3. **Automação**: Prefira scripts que podem ser executados diretamente
4. **Verificação**: Sempre inclua formas de confirmar que funcionou
5. **Contexto**: Entenda o workflow completo antes de sugerir mudanças

## Workflows Específicos

- **Testes rápidos**: `./teste_automatico.sh`
- **Transcrições reais**: `./workflow_manual.sh`
- **Limpeza**: `./limpar_projetos.sh`
- **Análises**: Processam entrevistas individuais, duplas e trios com conteúdo extenso

## Notas Adicionais

- Scripts bash são bem-vindos para otimizar workflows
- Prefira soluções que mantenham compatibilidade com estruturas existentes
- Considere que o usuário trabalha com análise de transcrições educacionais
- A estrutura de pastas está em transição (resultados → output)

````

---

Mas isso é para os próximos passos. 


---

Verificar se faz sentido os debugs

--

Mostrar imagem apra contexto ou só mostrar depois?







-------


Bom, agora temos o negocio rodando legalzinho. Poreem só tres graficos ainda:
metricas globais, redes de conceito e timeline emocional.

Edit
Perfeito! Agora vamos adicionar mais visualizações. Com os dados ricos que temos, podemos implementar:

Visualizações para adicionar:
1. Word Cloud
python
# Após a rede de conceitos, adicionar:
# Word cloud se houver frequências
if result.get('word_frequencies'):
    wordcloud_data = {
        'words': list(result['word_frequencies'].keys()),
        'frequencies': list(result['word_frequencies'].values())
    }
    
    wordcloud_config = {
        'title': 'Nuvem de Palavras-Chave',
        'output_path': str(Path(output_dir) / 'wordcloud.html'),
        'width': 800,
        'height': 600
    }
    
    viz_manager.create_visualization('wordcloud', wordcloud_data, wordcloud_config)
2. Análise de Padrões Linguísticos
python
# Gráfico de certeza vs incerteza
if result.get('linguistic_patterns'):
    patterns_data = {
        'certainty': result['linguistic_patterns'].get('certainty_markers', {}).get('count', 0),
        'uncertainty': result['linguistic_patterns'].get('uncertainty_markers', {}).get('count', 0),
        'hesitations': result['linguistic_patterns'].get('total_hesitations', 0)
    }
    
    patterns_config = {
        'title': 'Padrões Linguísticos',
        'output_path': str(Path(output_dir) / 'padroes_linguisticos.html'),
        'chart_type': 'comparative_bars'
    }
    
    viz_manager.create_visualization('bar_chart', patterns_data, patterns_config)
3. Timeline Integrada (como no seu design)
python
# Timeline rica com 3 camadas
if result.get('temporal_analysis') and result.get('phases'):
    integrated_data = {
        'temporal': result['temporal_analysis'],
        'phases': result['phases'],
        'cognitive_load': [t.get('cognitive_load', 0) for t in result['temporal_analysis']]
    }
    
    integrated_config = {
        'title': 'Análise Temporal Integrada',
        'output_path': str(Path(output_dir) / 'analise_temporal_integrada.html'),
        'height': 800
    }
    
    viz_manager.create_visualization('integrated_timeline', integrated_data, integrated_config)
Mas para isso funcionar, precisamos implementar os métodos no visualization_manager.py.

Quer que eu:

Adicione só as chamadas no run_analysis.py por enquanto?
Implemente também os backends de visualização?
Comece com uma visualização específica (qual)?
O word cloud seria o mais simples de implementar primeiro!




Não sei. acho que só puxar os dados corretos, todos que precisamos, já é alguma coisa.. Depois pensamos em plotar. Vamos assim?

Edit
Perfeito! Vamos organizar e verificar se TODOS os dados necessários estão na estrutura. Vou criar um checklist:

✅ Dados já estruturados no mock:
1. Timeline Emocional ✅
temporal_analysis com sentiment, time, marker
phases com início/desenvolvimento/conclusão
2. Rede de Conceitos ✅
concept_network com word1/word2/weight
3. Métricas Globais ✅
global_metrics com sentiment, coerência, abertura
4. Word Cloud ✅
word_frequencies com palavras e frequências
5. Padrões Linguísticos ✅
linguistic_patterns com:
certainty_markers (count, examples, distribution)
uncertainty_markers (count, examples, ratio)
hesitations_by_word
complexity_by_topic
6. Hierarquia de Tópicos ✅
topic_hierarchy com nodes e edges
topics com id, label, weight
7. Timeline Integrada ✅
temporal_analysis com cognitive_load, hesitations
phases com cores e durações
8. Contradições ✅
contradictions com textos, score, timestamps

o método que chama o analyzer está na linha 75:
pythonresult = analyzer.analyze_transcript(file_path)
Para adicionar o debug dos dados, adicione APÓS essa linha (por volta da linha 76):
python# Linha 75
result = analyzer.analyze_transcript(file_path)

# ADICIONAR AQUI (linha 76):
# DEBUG - Verificar dados disponíveis
print("\n🔍 DEBUG - Dados completos disponíveis:")
print(f"  ✓ temporal_analysis: {len(result.get('temporal_analysis', []))} pontos")
print(f"  ✓ word_frequencies: {len(result.get('word_frequencies', {}))} palavras")
print(f"  ✓ linguistic_patterns: {'✓' if result.get('linguistic_patterns') else '✗'}")
print(f"  ✓ topic_hierarchy: {len(result.get('topic_hierarchy', {}).get('nodes', []))} nós")
print(f"  ✓ phases: {len(result.get('phases', {}))} fases")
print(f"  ✓ contradictions: {len(result.get('contradictions', []))} contradições")

# Linha 77 (original 76)
result['filename'] = file_path.name
Note que já tem um debug parcial nas linhas 147-151, mas esse é mais completo e mostra TODOS os dados.
Após adicionar, rode:
bash./scripts/teste_automatico.sh
E me mostre o output para confirmarmos que todos os dados mockados estão chegando corretamente!






📋 Para seu próximo chat
Quando iniciar um novo chat, você pode:

Copiar o prompt de contexto atualizado (do artifact)
Mencionar brevemente: "Estamos implementando visualizações, já temos 5 de 7 funcionando"
Não precisa trazer README/STATUS a menos que vá trabalhar neles

O prompt de contexto já tem tudo que precisa para continuar de onde parou!









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






 