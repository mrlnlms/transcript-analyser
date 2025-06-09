#!/usr/bin/env python3
"""Implementa métodos de interpretação no GlobalMetricsAnalyzer"""

INTERPRETATION_CODE = '''
    def interpret_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Interpreta métricas globais em insights qualitativos"""
        interpreted = results.copy()
        
        # Interpretar sentimento
        sentiment = results.get('global_sentiment', 0)
        if sentiment > 0.3:
            interpreted['sentiment_label'] = 'Muito positivo'
            interpreted['sentiment_emoji'] = '😊'
        elif sentiment > 0.1:
            interpreted['sentiment_label'] = 'Positivo'
            interpreted['sentiment_emoji'] = '🙂'
        elif sentiment > -0.1:
            interpreted['sentiment_label'] = 'Neutro'
            interpreted['sentiment_emoji'] = '😐'
        elif sentiment > -0.3:
            interpreted['sentiment_label'] = 'Negativo'
            interpreted['sentiment_emoji'] = '😟'
        else:
            interpreted['sentiment_label'] = 'Muito negativo'
            interpreted['sentiment_emoji'] = '😢'
        
        # Interpretar coerência
        coherence = results.get('thematic_coherence', 0)
        if coherence > 0.7:
            interpreted['coherence_label'] = 'Excelente estrutura narrativa'
            interpreted['coherence_quality'] = 'alta'
        elif coherence > 0.5:
            interpreted['coherence_label'] = 'Boa estrutura narrativa'
            interpreted['coherence_quality'] = 'média-alta'
        elif coherence > 0.3:
            interpreted['coherence_label'] = 'Estrutura razoável'
            interpreted['coherence_quality'] = 'média'
        else:
            interpreted['coherence_label'] = 'Estrutura fragmentada'
            interpreted['coherence_quality'] = 'baixa'
        
        # Interpretar abertura emocional
        openness = results.get('emotional_openness', 0)
        if openness > 1.0:
            interpreted['openness_label'] = 'Muito expressivo'
            interpreted['openness_level'] = 'alta'
        elif openness > 0.5:
            interpreted['openness_label'] = 'Moderadamente expressivo'
            interpreted['openness_level'] = 'média'
        else:
            interpreted['openness_label'] = 'Reservado'
            interpreted['openness_level'] = 'baixa'
        
        return interpreted
    
    def get_insights(self, results: Dict[str, Any]) -> List[str]:
        """Gera insights baseados nas métricas globais"""
        insights = []
        interpreted = self.interpret_results(results)
        
        # Insight sobre sentimento
        sentiment = results.get('global_sentiment', 0)
        sentiment_label = interpreted.get('sentiment_label', '')
        insights.append(f"O discurso apresenta tom {sentiment_label.lower()} ({sentiment:.3f})")
        
        # Insight sobre coerência
        coherence = results.get('thematic_coherence', 0)
        if coherence > 0.7:
            insights.append("Alta coerência temática indica foco claro e organização mental estruturada")
        elif coherence < 0.3:
            insights.append("Baixa coerência sugere múltiplos temas ou pensamento disperso")
        
        # Insight sobre hesitações
        hesitations = results.get('total_hesitations', 0)
        if hesitations > 20:
            insights.append(f"Alto número de hesitações ({hesitations}) pode indicar incerteza ou reflexão cuidadosa")
        elif hesitations < 5:
            insights.append("Poucas hesitações sugerem convicção ou preparação prévia")
        
        # Insight combinado
        if sentiment < -0.2 and coherence > 0.6:
            insights.append("Apesar do tom negativo, a narrativa é bem estruturada - possível análise crítica consciente")
        elif sentiment > 0.2 and coherence < 0.4:
            insights.append("Tom positivo com baixa coerência pode indicar entusiasmo não estruturado")
        
        return insights
    
    def _format_markdown(self, results: Dict[str, Any]) -> str:
        """Formata métricas globais como Markdown"""
        lines = ["## �� Métricas Globais\n"]
        
        # Sentimento
        sentiment = results.get('global_sentiment', 0)
        emoji = results.get('sentiment_emoji', '')
        label = results.get('sentiment_label', '')
        lines.append(f"### Sentimento: {emoji} {label}")
        lines.append(f"- Valor: {sentiment:.3f}")
        lines.append(f"- Interpretação: {self._get_sentiment_description(sentiment)}")
        lines.append("")
        
        # Coerência
        coherence = results.get('thematic_coherence', 0)
        coherence_label = results.get('coherence_label', '')
        lines.append(f"### Coerência Temática: {coherence:.2f}")
        lines.append(f"- Qualidade: {coherence_label}")
        lines.append("")
        
        # Abertura
        openness = results.get('emotional_openness', 0)
        openness_label = results.get('openness_label', '')
        lines.append(f"### Abertura Emocional: {openness:.2f}")
        lines.append(f"- Nível: {openness_label}")
        lines.append("")
        
        # Insights
        insights = self.get_insights(results)
        if insights:
            lines.append("### 💡 Insights")
            for insight in insights:
                lines.append(f"- {insight}")
        
        return '\n'.join(lines)
    
    def _get_sentiment_description(self, sentiment: float) -> str:
        """Descrição detalhada do sentimento"""
        if sentiment > 0.3:
            return "Discurso predominantemente otimista e positivo"
        elif sentiment > 0.1:
            return "Tom geral positivo com equilíbrio emocional"
        elif sentiment > -0.1:
            return "Discurso equilibrado sem tendência emocional clara"
        elif sentiment > -0.3:
            return "Presença de elementos negativos ou críticos"
        else:
            return "Forte presença de negatividade ou crítica"
'''

# Adicionar ao GlobalMetricsAnalyzer
with open('engine/analyzers/global_metrics.py', 'r') as f:
    content = f.read()

# Adicionar import List se necessário
if 'from typing import Dict, List' not in content:
    content = content.replace('from typing import Dict', 'from typing import Dict, Any, List')

# Encontrar onde inserir (no final da classe, antes do último })
lines = content.split('\n')
insert_index = len(lines) - 1

# Voltar até encontrar uma linha com conteúdo
while insert_index > 0 and not lines[insert_index].strip():
    insert_index -= 1

# Inserir antes do return ou no final do analyze
for i in range(len(lines)-1, 0, -1):
    if 'return {' in lines[i]:
        # Adicionar após o return
        insert_index = i
        # Encontrar o fim do return
        brace_count = 0
        for j in range(i, len(lines)):
            brace_count += lines[j].count('{') - lines[j].count('}')
            if brace_count == 0:
                insert_index = j + 1
                break
        break

# Inserir o código
lines.insert(insert_index, INTERPRETATION_CODE)

with open('engine/analyzers/global_metrics.py', 'w') as f:
    f.write('\n'.join(lines))

print("✅ Métodos de interpretação implementados no GlobalMetricsAnalyzer!")
