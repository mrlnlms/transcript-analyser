"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class WordFrequencyAnalyzer(BaseAnalyzer):
    """
    Análise de Frequência de Palavras
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: WordFrequencyAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """
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
    def analyze(self, text: str) -> Dict:
        """Analisa frequência de palavras no texto"""
        from collections import Counter
        import re
        
        # Calibração baseada no tamanho
        calibration = self.get_calibration_params(len(text))
        min_frequency = calibration.get('min_frequency', 3)
        
        # Processar texto (copiado do analyzer_core.py)
        text_lower = text.lower()
        words = re.findall(r'\b[a-záàâãéèêíïóôõöúçñ]{3,}\b', text_lower)
        
        # Filtrar stopwords básicas
        stopwords = {'que', 'para', 'com', 'uma', 'por', 'mas', 'das', 'dos', 'como', 'isso', 'então', 'muito', 'mais', 'também'}
        filtered_words = [w for w in words if w not in stopwords]
        
        # Contar palavras (igual ao original)
        word_counts = Counter(filtered_words)
        
        # Retornar top 50 
        top_words = dict(word_counts.most_common(50))
        
        return {
            'analysis_type': 'word_frequency',
            'total_words': len(words),
            'unique_words': len(word_counts),
            'word_frequencies': top_words,  # Nome igual ao original
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
    