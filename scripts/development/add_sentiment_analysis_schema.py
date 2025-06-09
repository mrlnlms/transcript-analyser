#!/usr/bin/env python3
"""Adiciona schema ao SentimentAnalysisAnalyzer"""

SCHEMA_CODE = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'positive_lexicon': {
                'type': 'str',
                'default': 'resources/emocionais_positivos.txt',
                'academic': 'resources/sentiment_academic_positive.txt',
                'medical': 'resources/sentiment_medical_positive.txt',
                'description': 'Arquivo com palavras/frases positivas'
            },
            'negative_lexicon': {
                'type': 'str',
                'default': 'resources/emocionais_negativos.txt',
                'academic': 'resources/sentiment_academic_negative.txt',
                'medical': 'resources/sentiment_medical_negative.txt',
                'description': 'Arquivo com palavras/frases negativas'
            },
            'neutral_threshold': {
                'type': 'float',
                'range': [-0.5, 0.5],
                'default': 0.1,
                'description': 'Limiar para considerar sentimento neutro'
            },
            'compound_phrases': {
                'type': 'bool',
                'default': True,
                'description': 'Detectar frases compostas (ex: "não é ruim" = positivo)'
            },
            'intensity_modifiers': {
                'type': 'dict',
                'default': {
                    'muito': 1.5,
                    'bastante': 1.3,
                    'pouco': 0.7,
                    'levemente': 0.5,
                    'extremamente': 2.0
                },
                'description': 'Modificadores de intensidade e seus pesos'
            },
            'negation_words': {
                'type': 'list',
                'default': ['não', 'nunca', 'nem', 'jamais', 'nada'],
                'description': 'Palavras que invertem sentimento'
            },
            'sentiment_method': {
                'type': 'str',
                'options': ['lexicon', 'rule_based', 'hybrid'],
                'default': 'hybrid',
                'description': 'Método de análise de sentimento'
            },
            'context_window': {
                'type': 'int',
                'range': [1, 5],
                'default': 2,
                'description': 'Janela de contexto para análise (palavras antes/depois)'
            }
        }
'''

with open('engine/analyzers/sentiment_analysis.py', 'r') as f:
    content = f.read()

if 'get_config_schema' in content:
    print("⚠️  Já tem get_config_schema!")
    exit(1)

lines = content.split('\n')
insert_index = None

for i, line in enumerate(lines):
    if '"""' in line and i > 10:
        if 'class SentimentAnalysisAnalyzer' in '\n'.join(lines[max(0, i-20):i]):
            insert_index = i + 1
            break

if insert_index:
    lines.insert(insert_index, SCHEMA_CODE)
    with open('engine/analyzers/sentiment_analysis.py.backup', 'w') as f:
        f.write(content)
    with open('engine/analyzers/sentiment_analysis.py', 'w') as f:
        f.write('\n'.join(lines))
    print("✅ Schema adicionado ao SentimentAnalysisAnalyzer!")
