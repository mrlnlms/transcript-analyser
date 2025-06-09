"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict, List

class GlobalMetricsAnalyzer(BaseAnalyzer):
    """
    Análise de Métricas Globais
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: GlobalMetricsAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """
    
    def analyze(self, text: str, temporal_data: List = None) -> Dict:
        """Calcula métricas globais do texto"""
        from typing import List
        
        # Se não receber temporal_data, criar análise temporal básica
        if temporal_data is None:
            from .temporal_analysis import TemporalAnalysisAnalyzer
            temporal_analyzer = TemporalAnalysisAnalyzer()
            temporal_result = temporal_analyzer.analyze(text)
            temporal_data = temporal_result['temporal_analysis']
        
        # Sentimento global (média dos segmentos)
        sentiments = [d['sentiment'] for d in temporal_data] if temporal_data else [0]
        global_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
        # Variância do sentimento (abertura emocional)
        if len(sentiments) > 1:
            mean = sum(sentiments) / len(sentiments)
            variance = sum((s - mean) ** 2 for s in sentiments) / len(sentiments)
            sentiment_variance = variance
        else:
            sentiment_variance = 0.1
        
        # Hesitações totais
        total_hesitations = text.lower().count('né') + text.lower().count('tipo') + \
                        text.lower().count('assim') + text.lower().count('então')
        
        # Coerência temática (baseada em repetição de palavras-chave)
        words = text.lower().split()
        unique_words = len(set(words))
        total_words = len(words)
        coherence = 1 - (unique_words / total_words) if total_words > 0 else 0.5
        
        # Calibração
        calibration = self.get_calibration_params(len(text))
        
        return {
        'analysis_type': 'global_metrics',
        'global_sentiment': round(global_sentiment, 3),
        'emotional_openness': round(sentiment_variance, 3),  # ← MUDAR AQUI
        'thematic_coherence': round(coherence, 3),
        'total_hesitations': total_hesitations,
        'segments_analyzed': len(temporal_data),
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

    def interpret_results(self, results):
        """Interpreta resultados em formato qualitativo"""
        interpreted = results.copy()
        
        # Sentimento
        sentiment = results.get('global_sentiment', 0)
        if sentiment > 0.1:
            interpreted['sentiment_label'] = 'Positivo'
        elif sentiment < -0.1:
            interpreted['sentiment_label'] = 'Negativo'
        else:
            interpreted['sentiment_label'] = 'Neutro'
        
        # Coerencia
        coherence = results.get('thematic_coherence', 0)
        if coherence > 0.7:
            interpreted['coherence_label'] = 'Alta'
        elif coherence > 0.4:
            interpreted['coherence_label'] = 'Media'
        else:
            interpreted['coherence_label'] = 'Baixa'
        
        return interpreted
    
    def get_insights(self, results):
        """Gera insights dos resultados"""
        insights = []
        
        sentiment = results.get('global_sentiment', 0)
        if sentiment > 0.1:
            insights.append("Discurso predominantemente positivo")
        elif sentiment < -0.1:
            insights.append("Discurso predominantemente negativo")
        else:
            insights.append("Discurso neutro e equilibrado")
        
        coherence = results.get('thematic_coherence', 0)
        if coherence > 0.7:
            insights.append("Narrativa bem estruturada e coerente")
        elif coherence < 0.3:
            insights.append("Narrativa fragmentada ou com multiplos temas")
        
        return insights

