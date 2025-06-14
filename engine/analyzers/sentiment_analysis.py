"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class SentimentAnalysisAnalyzer(BaseAnalyzer):
    """
    Análise de Sentimento
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: SentimentAnalysisAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """

    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'positive_lexicon': {
                'type': 'str',
                'default': 'resources/emocionais_positivos.txt',
                'academic': 'resources/sentiment_academic_positive.txt',
                'medical': 'resources/sentiment_medical_positive.txt',
                'description': 'Arquivo com palavras/frases positivas'
            },
            'negative_lexicon': {
                'type': 'str',
                'default': 'resources/emocionais_negativos.txt',
                'academic': 'resources/sentiment_academic_negative.txt',
                'medical': 'resources/sentiment_medical_negative.txt',
                'description': 'Arquivo com palavras/frases negativas'
            },
            'neutral_threshold': {
                'type': 'float',
                'range': [-0.5, 0.5],
                'default': 0.1,
                'description': 'Limiar para considerar sentimento neutro'
            },
            'compound_phrases': {
                'type': 'bool',
                'default': True,
                'description': 'Detectar frases compostas (ex: "não é ruim" = positivo)'
            },
            'intensity_modifiers': {
                'type': 'dict',
                'default': {
                    'muito': 1.5,
                    'bastante': 1.3,
                    'pouco': 0.7,
                    'levemente': 0.5,
                    'extremamente': 2.0
                },
                'description': 'Modificadores de intensidade e seus pesos'
            },
            'negation_words': {
                'type': 'list',
                'default': ['não', 'nunca', 'nem', 'jamais', 'nada'],
                'description': 'Palavras que invertem sentimento'
            },
            'sentiment_method': {
                'type': 'str',
                'options': ['lexicon', 'rule_based', 'hybrid'],
                'default': 'hybrid',
                'description': 'Método de análise de sentimento'
            },
            'context_window': {
                'type': 'int',
                'range': [1, 5],
                'default': 2,
                'description': 'Janela de contexto para análise (palavras antes/depois)'
            }
        }

    
    def analyze(self, text: str) -> Dict:
        """
        Implementar análise principal aqui
        
        Args:
            text: Texto da transcrição para analisar
            
        Returns:
            Dict com resultados da análise
        """
        # Exemplo de implementação:
        text_length = len(text)
        calibration = self.get_calibration_params(text_length)
        
        # Sua lógica de análise aqui
        results = {
            "analysis_type": self.get_name(),
            "text_length": text_length,
            "calibration_used": calibration,
            "results": {
                # Seus resultados aqui
            }
        }
        
        return results
    
    def get_calibration_params(self, text_length: int) -> Dict:
        """Sobrescrever se precisar de calibração específica"""
        base_params = super().get_calibration_params(text_length)
        
        # Adicionar parâmetros específicos da sua análise
        specific_params = {
            "my_parameter": "valor_baseado_no_tamanho"
        }
        
        return {**base_params, **specific_params}
