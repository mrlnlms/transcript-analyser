#!/usr/bin/env python3
"""Mostra como simplificar o MarkdownGenerator"""

print("""
🔄 ANTES (MarkdownGenerator com lógica hardcoded):
----------------------------------------
def _generate_global_metrics(self, data):
    sentiment = data.get('global_sentiment', 0)
    
    # Lógica de interpretação hardcoded
    if sentiment > 0.1:
        sentiment_desc = "😊 Positivo"
    elif sentiment < -0.1:
        sentiment_desc = "😟 Negativo"
    else:
        sentiment_desc = "😐 Neutro"
    
    lines = [
        f"**Sentimento**: {sentiment} {sentiment_desc}",
        # ... mais lógica hardcoded
    ]

🔄 DEPOIS (MarkdownGenerator simplificado):
----------------------------------------
def _generate_global_metrics(self, data):
    # Pegar analyzer correspondente
    analyzer = self.get_analyzer('global_metrics')
    
    # Deixar o analyzer interpretar
    interpreted = analyzer.interpret_results(data)
    insights = analyzer.get_insights(data)
    
    # Apenas formatar o que foi retornado
    lines = ["## Métricas Globais"]
    
    # Adicionar interpretações
    lines.append(f"**Sentimento**: {interpreted.get('sentiment_label')}")
    lines.append(f"**Coerência**: {interpreted.get('coherence_label')}")
    
    # Adicionar insights
    lines.append("\\n### Insights:")
    for insight in insights:
        lines.append(f"- {insight}")
    
    return lines

✨ VANTAGENS:
- MarkdownGenerator fica simples (só formatação)
- Lógica de negócio fica no analyzer (onde deve estar)
- Fácil adicionar novos analyzers
- Cada analyzer controla sua apresentação
""")
