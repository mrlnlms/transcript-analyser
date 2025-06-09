#!/usr/bin/env python3
"""Adiciona get_config_schema aos analyzers"""

# Primeiro, vamos ver a estrutura do arquivo
with open('engine/analyzers/word_frequency.py', 'r') as f:
    lines = f.readlines()

# Procurar onde inserir (depois do __init__ ou no início da classe)
for i, line in enumerate(lines):
    if 'class WordFrequencyAnalyzer' in line:
        print(f"Classe encontrada na linha {i+1}")
        # Mostrar próximas 10 linhas para ver a estrutura
        for j in range(i, min(i+10, len(lines))):
            print(f"{j+1}: {lines[j]}", end='')
        break

print("\n" + "="*50)
print("Adicione o seguinte método na classe WordFrequencyAnalyzer:")
print("="*50)

schema_code = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'min_frequency': {
                'type': 'int',
                'range': [1, 10],
                'default': 2,
                'short_text': 1,
                'long_text': 5,
                'description': 'Frequência mínima para considerar palavra relevante'
            },
            'max_words': {
                'type': 'int',
                'range': [10, 200],
                'default': 50,
                'short_text': 30,
                'long_text': 100,
                'description': 'Número máximo de palavras no resultado'
            },
            'use_stopwords': {
                'type': 'bool',
                'default': True,
                'description': 'Remover palavras comuns (stopwords)'
            },
            'stopwords_file': {
                'type': 'str',
                'default': 'resources/stopwords_custom.txt',
                'academic': 'resources/stopwords_academic.txt',
                'medical': 'resources/stopwords_medical.txt',
                'description': 'Arquivo de stopwords a usar'
            }
        }
'''

print(schema_code)
