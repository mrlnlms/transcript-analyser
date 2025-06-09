#!/usr/bin/env python3
"""Adiciona schema ao ContradictionDetectionAnalyzer"""

SCHEMA_CODE = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'contradiction_patterns': {
                'type': 'list',
                'default': [
                    (r'não.*mas.*sim', 'negação seguida de afirmação'),
                    (r'nunca.*sempre', 'contradição temporal'),
                    (r'impossível.*possível', 'contradição de possibilidade'),
                    (r'certeza.*dúvida', 'contradição de certeza'),
                    (r'bom.*ruim', 'contradição de qualidade'),
                    (r'fácil.*difícil', 'contradição de dificuldade')
                ],
                'interview': [
                    (r'sim.*não', 'mudança de opinião'),
                    (r'concordo.*discordo', 'contradição de concordância'),
                    (r'gosto.*não gosto', 'contradição de preferência'),
                    (r'sempre.*nunca', 'contradição temporal')
                ],
                'academic': [
                    (r'comprova.*refuta', 'contradição de evidência'),
                    (r'corrobora.*contradiz', 'contradição de suporte'),
                    (r'válido.*inválido', 'contradição de validade')
                ],
                'description': 'Padrões regex para detectar contradições'
            },
            'sentence_proximity': {
                'type': 'int',
                'range': [1, 10],
                'default': 3,
                'description': 'Distância máxima entre sentenças para considerar contradição'
            },
            'min_contradiction_score': {
                'type': 'float',
                'range': [0.0, 1.0],
                'default': 0.5,
                'description': 'Score mínimo para considerar uma contradição'
            },
            'use_semantic_analysis': {
                'type': 'bool',
                'default': False,
                'description': 'Usar análise semântica além de padrões'
            },
            'negation_words': {
                'type': 'list',
                'default': ['não', 'nunca', 'jamais', 'nenhum', 'nada', 'nem'],
                'description': 'Palavras que indicam negação'
            },
            'temporal_words': {
                'type': 'list',
                'default': ['sempre', 'nunca', 'antes', 'depois', 'agora', 'antigamente'],
                'description': 'Palavras temporais para detectar contradições temporais'
            },
            'max_contradictions': {
                'type': 'int',
                'range': [5, 50],
                'default': 20,
                'short_text': 10,
                'long_text': 30,
                'description': 'Número máximo de contradições a reportar'
            },
            'score_calculation_method': {
                'type': 'str',
                'options': ['pattern_based', 'distance_based', 'hybrid'],
                'default': 'hybrid',
                'description': 'Método para calcular score de contradição'
            }
        }
'''

# Ler arquivo
with open('engine/analyzers/contradiction_detection.py', 'r') as f:
    content = f.read()

if 'get_config_schema' in content:
    print("⚠️  ContradictionDetectionAnalyzer já tem get_config_schema!")
    exit(1)

# Procurar onde inserir
lines = content.split('\n')
insert_index = None

for i, line in enumerate(lines):
    if '"""' in line and i > 10:
        if 'class ContradictionDetectionAnalyzer' in '\n'.join(lines[max(0, i-20):i]):
            insert_index = i + 1
            break

if insert_index:
    lines.insert(insert_index, SCHEMA_CODE)
    
    # Backup
    with open('engine/analyzers/contradiction_detection.py.backup', 'w') as f:
        f.write(content)
    
    # Salvar
    with open('engine/analyzers/contradiction_detection.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Schema adicionado ao ContradictionDetectionAnalyzer!")
    print("📄 Backup: contradiction_detection.py.backup")
else:
    print("❌ Não encontrei onde inserir")
