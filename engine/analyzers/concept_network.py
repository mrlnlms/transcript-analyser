"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class ConceptNetworkAnalyzer(BaseAnalyzer):
    """
    Análise de Rede de Conceitos
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: ConceptNetworkAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """

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

    
    def analyze(self, text: str, word_frequencies: dict = None) -> Dict:
        """Constrói rede de conceitos baseada em coocorrência"""
        import re
        from collections import defaultdict
        
        # Se não receber word_frequencies, criar análise de frequência
        if word_frequencies is None:
            from .word_frequency import WordFrequencyAnalyzer
            freq_analyzer = WordFrequencyAnalyzer()
            freq_result = freq_analyzer.analyze(text)
            word_frequencies = freq_result['word_frequencies']
        
        # Calibração
        calibration = self.get_calibration_params(len(text))
        
        # Pegar top palavras mais frequentes (igual ao original)
        top_words = list(word_frequencies.keys())[:30]
        
        # Dividir em sentenças (igual ao original)
        sentences = re.split(r'[.!?]+', text.lower())
        
        # Contar coocorrências (igual ao original)
        cooccurrence = defaultdict(int)
        
        for sentence in sentences:
            words_in_sentence = [w for w in sentence.split() if w in top_words]
            
            # Para cada par de palavras na sentença (igual ao original)
            for i, word1 in enumerate(words_in_sentence):
                for word2 in words_in_sentence[i+1:]:
                    if word1 != word2:
                        # Ordenar para evitar duplicatas (a,b) e (b,a)
                        pair = tuple(sorted([word1, word2]))
                        cooccurrence[pair] += 1
        
        # Criar lista de conexões (igual ao original)
        connections = []
        for (word1, word2), weight in sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)[:20]:
            if weight >= 1:  # Apenas conexões significativas
                connections.append({
                    'word1': word1,
                    'word2': word2,
                    'weight': weight
                })
        
        return {
            'analysis_type': 'concept_network',
            'concept_network': connections,
            'total_pairs_analyzed': len(cooccurrence),
            'significant_connections': len(connections),
            'words_analyzed': len(top_words),
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
