#!/usr/bin/env python3
"""Adiciona schema ao LinguisticPatternsAnalyzer"""

SCHEMA_CODE = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'certainty_phrases': {
                'type': 'list',
                'default': [
                    'com certeza', 'obviamente', 'claramente', 'sem dúvida', 
                    'definitivamente', 'certamente', 'claro que', 'evidente',
                    'tenho certeza', 'absolutamente', 'seguramente'
                ],
                'academic': [
                    'indubitavelmente', 'inquestionavelmente', 'comprovadamente',
                    'demonstra-se que', 'evidencia-se', 'constata-se'
                ],
                'description': 'Frases que indicam certeza'
            },
            'uncertainty_phrases': {
                'type': 'list',
                'default': [
                    'talvez', 'acho que', 'não sei', 'pode ser', 'provavelmente',
                    'me parece', 'acredito que', 'suponho', 'imagino que',
                    'não tenho certeza', 'possivelmente', 'quem sabe'
                ],
                'academic': [
                    'possivelmente', 'hipoteticamente', 'presumivelmente',
                    'sugere-se que', 'indica-se que', 'aparentemente'
                ],
                'description': 'Frases que indicam incerteza'
            },
            'hesitation_markers': {
                'type': 'list',
                'default': ['né', 'tipo', 'assim', 'então', 'eh', 'ah', 'uhm', 'ahn'],
                'interview': ['né', 'tipo', 'assim', 'então', 'sabe', 'entende', 'viu'],
                'academic': ['isto é', 'ou seja', 'quer dizer', 'por assim dizer'],
                'description': 'Marcadores de hesitação'
            },
            'min_pattern_frequency': {
                'type': 'int',
                'range': [1, 10],
                'default': 1,
                'short_text': 1,
                'long_text': 3,
                'description': 'Frequência mínima para considerar padrão relevante'
            },
            'analyze_complexity': {
                'type': 'bool',
                'default': True,
                'description': 'Analisar complexidade sintática'
            },
            'complexity_metrics': {
                'type': 'list',
                'options': ['sentence_length', 'word_length', 'punctuation_density'],
                'default': ['sentence_length', 'word_length'],
                'description': 'Métricas de complexidade a calcular'
            }
        }
'''

# Ler arquivo
with open('engine/analyzers/linguistic_patterns.py', 'r') as f:
    content = f.read()

if 'get_config_schema' in content:
    print("⚠️  LinguisticPatternsAnalyzer já tem get_config_schema!")
    exit(1)

# Procurar onde inserir
lines = content.split('\n')
insert_index = None

for i, line in enumerate(lines):
    if '"""' in line and i > 10:
        if 'class LinguisticPatternsAnalyzer' in '\n'.join(lines[max(0, i-20):i]):
            insert_index = i + 1
            break

if insert_index:
    lines.insert(insert_index, SCHEMA_CODE)
    
    # Backup
    with open('engine/analyzers/linguistic_patterns.py.backup', 'w') as f:
        f.write(content)
    
    # Salvar
    with open('engine/analyzers/linguistic_patterns.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Schema adicionado ao LinguisticPatternsAnalyzer!")
    print("📄 Backup: linguistic_patterns.py.backup")
else:
    print("❌ Não encontrei onde inserir")
