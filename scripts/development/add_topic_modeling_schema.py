#!/usr/bin/env python3
"""Adiciona schema ao TopicModelingAnalyzer"""

SCHEMA_CODE = '''
    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'n_topics': {
                'type': 'int',
                'range': [2, 50],
                'default': 5,
                'short_text': 3,
                'long_text': 10,
                'academic': 15,
                'description': 'Número de tópicos a extrair'
            },
            'modeling_method': {
                'type': 'str',
                'options': ['keyword_based', 'lda', 'nmf', 'lsa'],
                'default': 'keyword_based',
                'description': 'Método de modelagem de tópicos'
            },
            'topic_keywords': {
                'type': 'dict',
                'default': {
                    'Tecnologia': ['sistema', 'software', 'código', 'programa', 'computador', 'dados', 'tecnologia', 'digital', 'internet', 'aplicativo'],
                    'Educação': ['curso', 'aula', 'professor', 'aluno', 'escola', 'ensino', 'aprendizagem', 'estudo', 'educação', 'conhecimento'],
                    'Trabalho': ['trabalho', 'empresa', 'projeto', 'equipe', 'cliente', 'processo', 'resultado', 'meta', 'objetivo', 'prazo'],
                    'Pessoal': ['vida', 'família', 'casa', 'tempo', 'dia', 'pessoa', 'gente', 'amigo', 'momento', 'experiência'],
                    'Análise': ['problema', 'solução', 'questão', 'situação', 'caso', 'exemplo', 'forma', 'maneira', 'aspecto', 'ponto']
                },
                'medical': {
                    'Sintomas': ['dor', 'febre', 'tosse', 'cansaço', 'tontura', 'náusea', 'mal-estar'],
                    'Tratamento': ['medicamento', 'remédio', 'dose', 'tratamento', 'terapia', 'cirurgia'],
                    'Diagnóstico': ['exame', 'teste', 'resultado', 'diagnóstico', 'avaliação', 'consulta'],
                    'Prevenção': ['prevenção', 'vacina', 'cuidado', 'higiene', 'saúde', 'bem-estar']
                },
                'description': 'Palavras-chave por tópico (para método keyword_based)'
            },
            'min_topic_score': {
                'type': 'int',
                'range': [0, 10],
                'default': 1,
                'description': 'Score mínimo para considerar um tópico relevante'
            },
            'use_word_frequencies': {
                'type': 'bool',
                'default': True,
                'description': 'Usar frequências de palavras na análise'
            },
            'normalize_distribution': {
                'type': 'bool',
                'default': True,
                'description': 'Normalizar distribuição de tópicos para somar 1.0'
            },
            'min_word_length': {
                'type': 'int',
                'range': [2, 10],
                'default': 3,
                'description': 'Comprimento mínimo de palavra para análise'
            },
            'max_words_per_topic': {
                'type': 'int',
                'range': [5, 30],
                'default': 10,
                'description': 'Número máximo de palavras por tópico'
            }
        }
'''

# Ler arquivo
with open('engine/analyzers/topic_modeling.py', 'r') as f:
    content = f.read()

if 'get_config_schema' in content:
    print("⚠️  TopicModelingAnalyzer já tem get_config_schema!")
    exit(1)

# Procurar onde inserir
lines = content.split('\n')
insert_index = None

for i, line in enumerate(lines):
    if '"""' in line and i > 10:
        if 'class TopicModelingAnalyzer' in '\n'.join(lines[max(0, i-20):i]):
            insert_index = i + 1
            break

if insert_index:
    lines.insert(insert_index, SCHEMA_CODE)
    
    # Backup
    with open('engine/analyzers/topic_modeling.py.backup', 'w') as f:
        f.write(content)
    
    # Salvar
    with open('engine/analyzers/topic_modeling.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Schema adicionado ao TopicModelingAnalyzer!")
    print("📄 Backup: topic_modeling.py.backup")
else:
    print("❌ Não encontrei onde inserir")
