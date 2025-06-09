"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class TopicModelingAnalyzer(BaseAnalyzer):
    """
    Análise de Tópicos e Categorização
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: TopicModelingAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """

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

    
    def analyze(self, text: str, word_frequencies: dict = None) -> Dict:
        """Extrai tópicos simples baseados em agrupamento de palavras"""
        
        # Se não receber word_frequencies, criar análise de frequência
        if word_frequencies is None:
            from .word_frequency import WordFrequencyAnalyzer
            freq_analyzer = WordFrequencyAnalyzer()
            freq_result = freq_analyzer.analyze(text)
            word_frequencies = freq_result['word_frequencies']
        
        # Calibração
        calibration = self.get_calibration_params(len(text))
        
        # Agrupar palavras por categorias temáticas simples (igual ao original)
        topic_keywords = {
            'Tecnologia': ['sistema', 'software', 'código', 'programa', 'computador', 'dados', 'tecnologia', 'digital', 'internet', 'aplicativo'],
            'Educação': ['curso', 'aula', 'professor', 'aluno', 'escola', 'ensino', 'aprendizagem', 'estudo', 'educação', 'conhecimento'],
            'Trabalho': ['trabalho', 'empresa', 'projeto', 'equipe', 'cliente', 'processo', 'resultado', 'meta', 'objetivo', 'prazo'],
            'Pessoal': ['vida', 'família', 'casa', 'tempo', 'dia', 'pessoa', 'gente', 'amigo', 'momento', 'experiência'],
            'Análise': ['problema', 'solução', 'questão', 'situação', 'caso', 'exemplo', 'forma', 'maneira', 'aspecto', 'ponto']
        }
        
        # Contar palavras por tópico (igual ao original)
        topic_scores = {}
        text_lower = text.lower()
        
        for topic, keywords in topic_keywords.items():
            score = sum(text_lower.count(keyword) for keyword in keywords)
            if score > 0:
                topic_scores[topic] = score
        
        # Se nenhum tópico específico, usar genérico
        if not topic_scores:
            topic_scores['Geral'] = len(text.split())
        
        # Normalizar para distribuição
        total = sum(topic_scores.values())
        topic_distribution = [score/total for score in topic_scores.values()]
        
        # Criar estrutura de tópicos (igual ao original)
        topics = []
        for i, (topic_name, score) in enumerate(topic_scores.items()):
            # Pegar palavras relevantes do word_freq que se relacionam
            relevant_words = []
            for word in word_frequencies.keys():
                if any(keyword in word for keyword in topic_keywords.get(topic_name, [])):
                    relevant_words.append(word)
            
            # Se não encontrou palavras relevantes, pegar as top do word_freq
            if not relevant_words:
                relevant_words = list(word_frequencies.keys())[i*8:(i+1)*8]
            
            topics.append({
                'id': f'topic_{i}',
                'words': relevant_words[:8],
                'weight': topic_distribution[i] if i < len(topic_distribution) else 0.1,
                'label': topic_name
            })
        
        # Criar hierarquia simples (igual ao original)
        topic_hierarchy = {
            'central_theme': 'TEMAS PRINCIPAIS',
            'nodes': [{'id': 'central', 'label': 'TEMAS PRINCIPAIS', 'level': 0, 'size': 50}],
            'edges': []
        }
        
        for topic in topics:
            topic_hierarchy['nodes'].append({
                'id': topic['id'],
                'label': topic['label'],
                'level': 1,
                'size': int(topic['weight'] * 100)
            })
            topic_hierarchy['edges'].append({
                'source': 'central',
                'target': topic['id'],
                'weight': topic['weight']
            })
        
        return {
            'analysis_type': 'topic_modeling',
            'topics': topics,
            'topic_distribution': topic_distribution,
            'topic_hierarchy': topic_hierarchy,
            'calibration_used': calibration
        }
    
    def get_calibration_params(self, text_length: int) -> Dict:
        """Sobrescrever se precisar de calibração específica"""
        base_params = super().get_calibration_params(text_length)
        
        # Adicionar parâmetros específicos da sua análise
        specific_params = {
            "my_parameter": "valor_baseado_no_tamanho"
        }
        
        return {**base_params, **specific_params}
