"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class LinguisticPatternsAnalyzer(BaseAnalyzer):
    """
    Análise de Padrões Linguísticos
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: LinguisticPatternsAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """
    
    def analyze(self, text: str) -> Dict:
        """Detecta padrões linguísticos reais no texto"""
        import re
        import numpy as np
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Calibração
        calibration = self.get_calibration_params(len(text))
        
        # Marcadores de certeza (igual ao original)
        certainty_phrases = [
            'com certeza', 'obviamente', 'claramente', 'sem dúvida', 
            'definitivamente', 'certamente', 'claro que', 'evidente',
            'tenho certeza', 'absolutamente', 'seguramente'
        ]
        
        # Marcadores de incerteza (igual ao original)
        uncertainty_phrases = [
            'talvez', 'acho que', 'não sei', 'pode ser', 'provavelmente',
            'me parece', 'acredito que', 'suponho', 'imagino que',
            'não tenho certeza', 'possivelmente', 'quem sabe'
        ]
        
        # Hesitações (igual ao original)
        hesitation_words = ['né', 'tipo', 'assim', 'então', 'eh', 'ah', 'uhm', 'ahn']
        
        # Contar ocorrências (igual ao original)
        certainty_count = sum(1 for phrase in certainty_phrases if phrase in text_lower)
        uncertainty_count = sum(1 for phrase in uncertainty_phrases if phrase in text_lower)
        
        # Hesitações por palavra (igual ao original)
        hesitations_by_word = {}
        total_hesitations = 0
        
        for word in hesitation_words:
            count = text_lower.count(word)
            if count > 0:
                hesitations_by_word[word] = {
                    'count': count,
                    'percentage': (count / len(words)) * 100 if words else 0
                }
                total_hesitations += count
        
        # Complexidade das frases (igual ao original)
        sentences = re.split(r'[.!?]+', text)
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        return {
            'analysis_type': 'linguistic_patterns',
            'certainty_markers': {
                'count': certainty_count,
                'examples': [p for p in certainty_phrases if p in text_lower][:5],
                'percentage': (certainty_count / len(sentences)) * 100 if sentences else 0
            },
            'uncertainty_markers': {
                'count': uncertainty_count,
                'examples': [p for p in uncertainty_phrases if p in text_lower][:5],
                'percentage': (uncertainty_count / len(sentences)) * 100 if sentences else 0
            },
            'hesitation_phrases': hesitations_by_word,
            'total_hesitations': total_hesitations,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'sentence_length_std': round(np.std(sentence_lengths), 1) if len(sentence_lengths) > 1 else 0,
            'complexity_by_topic': {},  # TODO: implementar quando tivermos tópicos
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
