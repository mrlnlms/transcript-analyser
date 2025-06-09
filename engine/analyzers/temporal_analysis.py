"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class TemporalAnalysisAnalyzer(BaseAnalyzer):
    """
    Análise Temporal e Evolução
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: TemporalAnalysisAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """

    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'segments': {
                'type': 'int',
                'range': [5, 100],
                'default': 10,
                'short_text': 5,
                'long_text': 20,
                'description': 'Número de segmentos temporais para análise'
            },
            'segment_method': {
                'type': 'str',
                'options': ['fixed', 'dynamic', 'paragraph', 'sentence'],
                'default': 'dynamic',
                'description': 'Método de segmentação do texto'
            },
            'min_segment_size': {
                'type': 'int',
                'range': [10, 1000],
                'default': 100,
                'description': 'Tamanho mínimo de cada segmento (chars)'
            },
            'sentiment_method': {
                'type': 'str',
                'options': ['lexicon', 'pattern', 'hybrid'],
                'default': 'hybrid',
                'description': 'Método de análise de sentimento'
            },
            'smoothing': {
                'type': 'bool',
                'default': True,
                'description': 'Aplicar suavização na linha temporal'
            },
            'smoothing_window': {
                'type': 'int',
                'range': [2, 10],
                'default': 3,
                'description': 'Janela de suavização (se ativada)'
            }
        }

    
    def analyze(self, text: str) -> Dict:
        """Analisa evolução temporal do texto em segmentos"""
        import re
        
        # Calibração baseada no tamanho
        calibration = self.get_calibration_params(len(text))
        max_segments = calibration.get('segments', 10)
        
        # Dividir em parágrafos OU por sentenças se for texto corrido
        paragraphs = []
        current_block = ""

        # Primeiro tentar por quebras de linha
        for line in text.split('\n'):
            line = line.strip()
            if line:
                current_block += line + " "
            else:
                if current_block:
                    paragraphs.append(current_block.strip())
                    current_block = ""

        if current_block:
            paragraphs.append(current_block.strip())

        # Se só tem 1 parágrafo (texto corrido), dividir por sentenças
        if len(paragraphs) == 1 and len(paragraphs[0]) > 1000:
            import re
            sentences = re.split(r'[.!?]+', paragraphs[0])
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # Agrupar sentenças em blocos de ~500-1000 caracteres
            paragraphs = []
            current_block = ""
            
            for sentence in sentences:
                if len(current_block + sentence) > 800:  # Limite por bloco
                    if current_block:
                        paragraphs.append(current_block.strip())
                        current_block = sentence + ". "
                    else:
                        current_block += sentence + ". "
                else:
                    current_block += sentence + ". "
            
            if current_block:
                paragraphs.append(current_block.strip())
        
        # Limitar segmentos baseado na calibração
        if len(paragraphs) > max_segments:
            step = len(paragraphs) // max_segments
            temp = []
            for i in range(0, len(paragraphs), step):
                temp.append(' '.join(paragraphs[i:i+step]))
            paragraphs = temp[:max_segments]
        
        # Analisar cada segmento
        temporal_data = []
        for i, paragraph in enumerate(paragraphs):
            if not paragraph:
                continue
                
            words = paragraph.split()
            paragraph_lower = paragraph.lower()
            
            # Análise de sentimento básica
            positive_words = ['bom', 'ótimo', 'excelente', 'feliz', 'satisfeito', 'gosto', 
                            'adoro', 'maravilh', 'incrível', 'positiv', 'melhor', 'sucesso',
                            'consegui', 'aprendi', 'entendi', 'legal', 'bacana', 'top']
            
            negative_words = ['ruim', 'péssimo', 'triste', 'difícil', 'problema', 'erro',
                            'não', 'nunca', 'medo', 'preocup', 'frustr', 'chato', 'cansado',
                            'complicado', 'confuso', 'dúvida']
            
            # Contar sentimentos
            positive_count = sum(1 for word in positive_words if word in paragraph_lower)
            negative_count = sum(1 for word in negative_words if word in paragraph_lower)
            
            # Calcular sentimento normalizado
            total_sentiment_words = positive_count + negative_count
            if total_sentiment_words > 0:
                sentiment = (positive_count - negative_count) / len(words)
            else:
                sentiment = 0.0
            
            # Detectar hesitações
            hesitation_words = ['hmm', 'ahh', 'então', 'né', 'tipo', 'assim']
            hesitations = sum(paragraph_lower.count(word) for word in hesitation_words)
            
            # Calcular carga cognitiva (aproximação)
            cognitive_load = len([w for w in words if len(w) > 7]) / len(words) if words else 0
            
            temporal_data.append({
                'segment': i + 1,
                'timestamp': f"{i * 100 // max_segments}%",
                'sentiment': round(sentiment, 3),
                'cognitive_load': round(cognitive_load, 3),
                'hesitations': hesitations,
                'word_count': len(words)
            })
        
        return {
            'analysis_type': 'temporal_analysis',
            'total_segments': len(temporal_data),
            'temporal_analysis': temporal_data,
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
        """Interpreta análise temporal em insights"""
        interpreted = results.copy()
        
        if 'temporal_analysis' in results:
            segments = results['temporal_analysis']
            
            # Calcular tendência
            if len(segments) > 2:
                first_third = segments[:len(segments)//3]
                last_third = segments[-(len(segments)//3):]
                
                avg_first = sum(s['sentiment'] for s in first_third) / len(first_third)
                avg_last = sum(s['sentiment'] for s in last_third) / len(last_third)
                
                if avg_last > avg_first + 0.1:
                    interpreted['trend'] = 'Crescente'
                    interpreted['trend_description'] = 'Sentimento melhorando ao longo do tempo'
                elif avg_last < avg_first - 0.1:
                    interpreted['trend'] = 'Decrescente'
                    interpreted['trend_description'] = 'Sentimento piorando ao longo do tempo'
                else:
                    interpreted['trend'] = 'Estável'
                    interpreted['trend_description'] = 'Sentimento manteve-se constante'
            
            # Identificar volatilidade
            sentiments = [s['sentiment'] for s in segments]
            if sentiments:
                variance = sum((s - sum(sentiments)/len(sentiments))**2 for s in sentiments) / len(sentiments)
                if variance > 0.1:
                    interpreted['volatility'] = 'Alta'
                    interpreted['volatility_description'] = 'Grandes variações emocionais'
                elif variance > 0.05:
                    interpreted['volatility'] = 'Média'
                    interpreted['volatility_description'] = 'Variações emocionais moderadas'
                else:
                    interpreted['volatility'] = 'Baixa'
                    interpreted['volatility_description'] = 'Emoções estáveis'
        
        return interpreted
    
    def get_insights(self, results):
        """Gera insights da análise temporal"""
        insights = []
        interpreted = self.interpret_results(results)
        
        # Insight sobre tendência
        if 'trend' in interpreted:
            insights.append(f"Tendência emocional: {interpreted['trend_description']}")
        
        # Insight sobre volatilidade
        if 'volatility' in interpreted:
            insights.append(f"Estabilidade emocional: {interpreted['volatility_description']}")
        
        # Insight sobre picos
        if 'temporal_analysis' in results:
            segments = results['temporal_analysis']
            sentiments = [s['sentiment'] for s in segments]
            
            if sentiments:
                max_idx = sentiments.index(max(sentiments))
                min_idx = sentiments.index(min(sentiments))
                
                if max(sentiments) > 0.3:
                    insights.append(f"Pico positivo significativo no segmento {max_idx + 1}")
                if min(sentiments) < -0.3:
                    insights.append(f"Vale emocional preocupante no segmento {min_idx + 1}")
        
        return insights
