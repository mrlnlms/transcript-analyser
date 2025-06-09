#!/usr/bin/env python3
"""Adiciona schema ao TestVelocityAnalyzer"""

SCHEMA_CODE = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'test_mode': {
                'type': 'bool',
                'default': True,
                'description': 'Ativar modo de teste'
            },
            'mock_delay': {
                'type': 'float',
                'range': [0.0, 5.0],
                'default': 0.5,
                'description': 'Delay simulado em segundos'
            },
            'use_mock_data': {
                'type': 'bool',
                'default': True,
                'description': 'Usar dados mockados ao invés de análise real'
            },
            'complexity_simulation': {
                'type': 'str',
                'options': ['simple', 'medium', 'complex'],
                'default': 'medium',
                'description': 'Nível de complexidade da simulação'
            },
            'error_rate': {
                'type': 'float',
                'range': [0.0, 1.0],
                'default': 0.0,
                'description': 'Taxa de erro simulada (0.0 = sem erros)'
            },
            'verbose_output': {
                'type': 'bool',
                'default': False,
                'description': 'Saída verbosa para debug'
            }
        }
'''

with open('engine/analyzers/test_velocity.py', 'r') as f:
    content = f.read()

if 'get_config_schema' in content:
    print("⚠️  Já tem get_config_schema!")
    exit(1)

lines = content.split('\n')
insert_index = None

for i, line in enumerate(lines):
    if '"""' in line and i > 10:
        if 'class TestVelocityAnalyzer' in '\n'.join(lines[max(0, i-20):i]):
            insert_index = i + 1
            break

if insert_index:
    lines.insert(insert_index, SCHEMA_CODE)
    with open('engine/analyzers/test_velocity.py.backup', 'w') as f:
        f.write(content)
    with open('engine/analyzers/test_velocity.py', 'w') as f:
        f.write('\n'.join(lines))
    print("✅ Schema adicionado ao TestVelocityAnalyzer!")
