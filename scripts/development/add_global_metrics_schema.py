#!/usr/bin/env python3
"""Adiciona schema ao GlobalMetricsAnalyzer"""

SCHEMA_CODE = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'metrics_to_calculate': {
                'type': 'list',
                'options': ['sentiment', 'coherence', 'emotional_openness', 'hesitations'],
                'default': ['sentiment', 'coherence', 'emotional_openness', 'hesitations'],
                'description': 'Métricas globais a calcular'
            },
            'use_temporal_data': {
                'type': 'bool',
                'default': True,
                'description': 'Usar dados da análise temporal para cálculos'
            },
            'coherence_method': {
                'type': 'str',
                'options': ['word_repetition', 'topic_consistency', 'semantic_similarity'],
                'default': 'word_repetition',
                'description': 'Método para calcular coerência temática'
            },
            'hesitation_markers': {
                'type': 'list',
                'default': ['né', 'tipo', 'assim', 'então'],
                'interview': ['né', 'tipo', 'assim', 'então', 'sabe', 'entendeu'],
                'academic': ['portanto', 'ou seja', 'isto é'],
                'description': 'Marcadores de hesitação a detectar'
            },
            'sentiment_aggregation': {
                'type': 'str',
                'options': ['mean', 'median', 'weighted_mean'],
                'default': 'mean',
                'description': 'Como agregar sentimentos dos segmentos'
            },
            'min_variance_threshold': {
                'type': 'float',
                'range': [0.0, 1.0],
                'default': 0.1,
                'description': 'Variância mínima para abertura emocional'
            }
        }
'''

# Ler arquivo
with open('engine/analyzers/global_metrics.py', 'r') as f:
    content = f.read()

# Verificar se já tem schema
if 'get_config_schema' in content:
    print("⚠️  GlobalMetricsAnalyzer já tem get_config_schema!")
    exit(1)

# Procurar onde inserir
lines = content.split('\n')
insert_index = None

for i, line in enumerate(lines):
    if '"""' in line and i > 10:
        if 'class GlobalMetricsAnalyzer' in '\n'.join(lines[max(0, i-20):i]):
            insert_index = i + 1
            break

if insert_index:
    lines.insert(insert_index, SCHEMA_CODE)
    
    # Backup
    with open('engine/analyzers/global_metrics.py.backup', 'w') as f:
        f.write(content)
    
    # Salvar
    with open('engine/analyzers/global_metrics.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Schema adicionado ao GlobalMetricsAnalyzer!")
    print("📄 Backup: global_metrics.py.backup")
else:
    print("❌ Não encontrei onde inserir")
