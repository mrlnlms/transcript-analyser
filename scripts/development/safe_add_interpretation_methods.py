#!/usr/bin/env python3
"""Adiciona métodos de interpretação de forma segura"""

import re

# Métodos para adicionar (sem caracteres especiais problemáticos)
METHODS_TO_ADD = '''
    def interpret_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Interpreta metricas globais em insights qualitativos"""
        interpreted = results.copy()
        
        # Interpretar sentimento
        sentiment = results.get('global_sentiment', 0)
        if sentiment > 0.3:
            interpreted['sentiment_label'] = 'Muito positivo'
            interpreted['sentiment_emoji'] = ':)'
        elif sentiment > 0.1:
            interpreted['sentiment_label'] = 'Positivo'
            interpreted['sentiment_emoji'] = ':)'
        elif sentiment > -0.1:
            interpreted['sentiment_label'] = 'Neutro'
            interpreted['sentiment_emoji'] = ':|'
        elif sentiment > -0.3:
            interpreted['sentiment_label'] = 'Negativo'
            interpreted['sentiment_emoji'] = ':('
        else:
            interpreted['sentiment_label'] = 'Muito negativo'
            interpreted['sentiment_emoji'] = ':('
        
        # Interpretar coerencia
        coherence = results.get('thematic_coherence', 0)
        if coherence > 0.7:
            interpreted['coherence_label'] = 'Excelente estrutura narrativa'
        elif coherence > 0.5:
            interpreted['coherence_label'] = 'Boa estrutura narrativa'
        elif coherence > 0.3:
            interpreted['coherence_label'] = 'Estrutura razoavel'
        else:
            interpreted['coherence_label'] = 'Estrutura fragmentada'
        
        # Interpretar abertura emocional
        openness = results.get('emotional_openness', 0)
        if openness > 1.0:
            interpreted['openness_label'] = 'Muito expressivo'
        elif openness > 0.5:
            interpreted['openness_label'] = 'Moderadamente expressivo'
        else:
            interpreted['openness_label'] = 'Reservado'
        
        return interpreted
    
    def get_insights(self, results: Dict[str, Any]) -> List[str]:
        """Gera insights baseados nas metricas globais"""
        insights = []
        interpreted = self.interpret_results(results)
        
        # Insight sobre sentimento
        sentiment = results.get('global_sentiment', 0)
        sentiment_label = interpreted.get('sentiment_label', '')
        insights.append(f"O discurso apresenta tom {sentiment_label.lower()} ({sentiment:.3f})")
        
        # Insight sobre coerencia
        coherence = results.get('thematic_coherence', 0)
        if coherence > 0.7:
            insights.append("Alta coerencia tematica indica foco claro")
        elif coherence < 0.3:
            insights.append("Baixa coerencia sugere multiplos temas")
        
        # Insight sobre hesitacoes
        hesitations = results.get('total_hesitations', 0)
        if hesitations > 20:
            insights.append(f"Alto numero de hesitacoes ({hesitations})")
        elif hesitations < 5:
            insights.append("Poucas hesitacoes sugerem conviccao")
        
        return insights
'''

# Ler arquivo original
with open('engine/analyzers/global_metrics.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar import List se necessário
if 'List' not in content:
    content = content.replace('from typing import Dict', 'from typing import Dict, Any, List')

# Encontrar o final da classe (última linha com conteúdo antes do fim)
lines = content.split('\n')

# Procurar o último return da função analyze
insert_pos = -1
for i in range(len(lines)-1, 0, -1):
    if 'return {' in lines[i] and 'def analyze' in '\n'.join(lines[i-20:i]):
        # Encontrar o fechamento deste return
        brace_count = 0
        for j in range(i, len(lines)):
            brace_count += lines[j].count('{') - lines[j].count('}')
            if brace_count == 0 and '}' in lines[j]:
                insert_pos = j + 1
                break
        break

if insert_pos > 0:
    # Inserir os novos métodos
    lines.insert(insert_pos, METHODS_TO_ADD)
    
    # Salvar
    with open('engine/analyzers/global_metrics.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("✅ Métodos adicionados com segurança!")
else:
    print("❌ Não encontrei onde inserir")

