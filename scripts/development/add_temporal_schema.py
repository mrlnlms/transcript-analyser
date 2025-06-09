#!/usr/bin/env python3
"""Adiciona schema ao TemporalAnalysisAnalyzer de forma segura"""

import re

# Schema para TemporalAnalysisAnalyzer
SCHEMA_CODE = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'segments': {
                'type': 'int',
                'range': [5, 100],
                'default': 10,
                'short_text': 5,
                'long_text': 20,
                'description': 'Número de segmentos temporais para análise'
            },
            'segment_method': {
                'type': 'str',
                'options': ['fixed', 'dynamic', 'paragraph', 'sentence'],
                'default': 'dynamic',
                'description': 'Método de segmentação do texto'
            },
            'min_segment_size': {
                'type': 'int',
                'range': [10, 1000],
                'default': 100,
                'description': 'Tamanho mínimo de cada segmento (chars)'
            },
            'sentiment_method': {
                'type': 'str',
                'options': ['lexicon', 'pattern', 'hybrid'],
                'default': 'hybrid',
                'description': 'Método de análise de sentimento'
            },
            'smoothing': {
                'type': 'bool',
                'default': True,
                'description': 'Aplicar suavização na linha temporal'
            },
            'smoothing_window': {
                'type': 'int',
                'range': [2, 10],
                'default': 3,
                'description': 'Janela de suavização (se ativada)'
            }
        }
'''

# Ler arquivo
with open('engine/analyzers/temporal_analysis.py', 'r') as f:
    content = f.read()

# Verificar se já tem schema
if 'get_config_schema' in content:
    print("⚠️  TemporalAnalysisAnalyzer já tem get_config_schema!")
    exit(1)

# Procurar onde inserir (após a docstring da classe)
lines = content.split('\n')
insert_index = None

# Procurar o fim da docstring da classe
for i, line in enumerate(lines):
    if '"""' in line and i > 10:  # Segunda ou terceira ocorrência de """
        # Verificar se é o fim da docstring da classe
        if 'class TemporalAnalysisAnalyzer' in '\n'.join(lines[max(0, i-20):i]):
            insert_index = i + 1
            break

if insert_index:
    # Inserir o schema
    lines.insert(insert_index, SCHEMA_CODE)
    
    # Salvar backup
    with open('engine/analyzers/temporal_analysis.py.backup', 'w') as f:
        f.write(content)
    
    # Salvar arquivo modificado
    with open('engine/analyzers/temporal_analysis.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Schema adicionado ao TemporalAnalysisAnalyzer!")
    print("📄 Backup salvo em: temporal_analysis.py.backup")
else:
    print("❌ Não consegui encontrar onde inserir o schema")
    print("💡 Faça manualmente após a docstring da classe")
