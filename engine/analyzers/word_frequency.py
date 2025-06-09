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
