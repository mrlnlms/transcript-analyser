#!/usr/bin/env python3
"""Adiciona schema ao ConceptNetworkAnalyzer"""

SCHEMA_CODE = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'max_words_for_network': {
                'type': 'int',
                'range': [10, 100],
                'default': 30,
                'short_text': 20,
                'long_text': 50,
                'description': 'Número máximo de palavras para construir a rede'
            },
            'cooccurrence_window': {
                'type': 'str',
                'options': ['sentence', 'paragraph', 'fixed_window'],
                'default': 'sentence',
                'description': 'Janela para detectar coocorrência'
            },
            'fixed_window_size': {
                'type': 'int',
                'range': [3, 20],
                'default': 10,
                'description': 'Tamanho da janela fixa (se usar fixed_window)'
            },
            'min_cooccurrence_count': {
                'type': 'int',
                'range': [1, 10],
                'default': 1,
                'short_text': 1,
                'long_text': 2,
                'description': 'Número mínimo de coocorrências para criar conexão'
            },
            'max_connections': {
                'type': 'int',
                'range': [10, 200],
                'default': 20,
                'short_text': 15,
                'long_text': 50,
                'description': 'Número máximo de conexões na rede'
            },
            'use_word_frequencies': {
                'type': 'bool',
                'default': True,
                'description': 'Usar análise de frequência para filtrar palavras'
            },
            'centrality_metric': {
                'type': 'str',
                'options': ['degree', 'betweenness', 'closeness', 'eigenvector'],
                'default': 'degree',
                'description': 'Métrica de centralidade para análise da rede'
            },
            'include_weak_ties': {
                'type': 'bool',
                'default': False,
                'description': 'Incluir conexões fracas (coocorrência = 1)'
            }
        }
'''

# Ler arquivo
with open('engine/analyzers/concept_network.py', 'r') as f:
    content = f.read()

if 'get_config_schema' in content:
    print("⚠️  ConceptNetworkAnalyzer já tem get_config_schema!")
    exit(1)

# Procurar onde inserir
lines = content.split('\n')
insert_index = None

for i, line in enumerate(lines):
    if '"""' in line and i > 10:
        if 'class ConceptNetworkAnalyzer' in '\n'.join(lines[max(0, i-20):i]):
            insert_index = i + 1
            break

if insert_index:
    lines.insert(insert_index, SCHEMA_CODE)
    
    # Backup
    with open('engine/analyzers/concept_network.py.backup', 'w') as f:
        f.write(content)
    
    # Salvar
    with open('engine/analyzers/concept_network.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Schema adicionado ao ConceptNetworkAnalyzer!")
    print("📄 Backup: concept_network.py.backup")
else:
    print("❌ Não encontrei onde inserir")
