"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class ContradictionDetectionAnalyzer(BaseAnalyzer):
    """
    Detecção de Contradições
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: ContradictionDetectionAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """
    
    def analyze(self, text: str, temporal_data: list = None) -> Dict:
        """Detecta possíveis contradições no texto"""
        import re
        
        # Se não receber temporal_data, criar análise temporal
        if temporal_data is None:
            from .temporal_analysis import TemporalAnalysisAnalyzer
            temporal_analyzer = TemporalAnalysisAnalyzer()
            temporal_result = temporal_analyzer.analyze(text)
            temporal_data = temporal_result['temporal_analysis']
        
        # Calibração
        calibration = self.get_calibration_params(len(text))
        
        contradictions = []
        
        # Dividir em sentenças (igual ao original)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Padrões de contradição (igual ao original)
        contradiction_patterns = [
            (r'não.*mas.*sim', 'negação seguida de afirmação'),
            (r'nunca.*sempre', 'contradição temporal'),
            (r'impossível.*possível', 'contradição de possibilidade'),
            (r'certeza.*dúvida', 'contradição de certeza'),
            (r'bom.*ruim', 'contradição de qualidade'),
            (r'fácil.*difícil', 'contradição de dificuldade')
        ]
        
        # Verificar padrões de contradição
        for i, sent1 in enumerate(sentences):
            for j, sent2 in enumerate(sentences[i+1:], i+1):
                if abs(i - j) <= 3:  # Sentenças próximas
                    combined = f"{sent1.lower()} {sent2.lower()}"
                    
                    for pattern, desc in contradiction_patterns:
                        if re.search(pattern, combined):
                            score = 0.8 + (len(combined.split()) * 0.01)  # Score variado
                            contradictions.append({
                                'score': round(score, 2),
                                'text1': sent1.strip(),
                                'text2': sent2.strip(),
                                'type': desc,
                                'topics': self._extract_keywords(combined),
                                'timestamp1': i * 2.5,  # Estimativa temporal
                                'timestamp2': j * 2.5
                            })
                            break
                
                # Verificar negações do mesmo conceito
                words1 = set(re.findall(r'\b\w{4,}\b', sent1.lower()))
                words2 = set(re.findall(r'\b\w{4,}\b', sent2.lower()))
                common_words = words1.intersection(words2)
                
                if common_words and len(common_words) >= 2:
                    # Verificar se há negação em uma e afirmação na outra
                    has_negation1 = any(neg in sent1.lower() for neg in ['não', 'nunca', 'jamais'])
                    has_negation2 = any(neg in sent2.lower() for neg in ['não', 'nunca', 'jamais'])
                    
                    if has_negation1 != has_negation2:  # Uma tem negação, outra não
                        score = 0.6 + (len(common_words) * 0.1)
                        contradictions.append({
                            'score': round(score, 2),
                            'text1': sent1.strip(),
                            'text2': sent2.strip(),
                            'type': 'negação conceitual',
                            'topics': list(common_words)[:5],
                            'timestamp1': i * 2.5,
                            'timestamp2': j * 2.5
                        })
        
        # Detectar mudanças de sentimento extremas (igual ao original)
        if temporal_data and len(temporal_data) > 1:
            for i in range(len(temporal_data) - 1):
                current = temporal_data[i]
                next_seg = temporal_data[i + 1]
                
                sentiment_diff = abs(current.get('sentiment', 0) - next_seg.get('sentiment', 0))
                if sentiment_diff > 0.5:  # Mudança emocional significativa
                    score = 0.4 + sentiment_diff
                    contradictions.append({
                        'score': round(score, 2),
                        'text1': f"Segmento {current['segment']}",
                        'text2': f"Segmento {next_seg['segment']}",
                        'type': 'mudança emocional extrema',
                        'topics': ['mudança emocional', 'sentimento'],
                        'timestamp1': current.get('timestamp', f"{i}%"),
                        'timestamp2': next_seg.get('timestamp', f"{i+1}%")
                    })
        
        # Ordenar por score e retornar top contradições
        contradictions.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'analysis_type': 'contradiction_detection',
            'contradictions': contradictions[:5],  # Máximo 5 contradições
            'total_contradictions_found': len(contradictions),
            'sentences_analyzed': len(sentences),
            'calibration_used': calibration
        }

    def _extract_keywords(self, text: str) -> list:
        """Extrai palavras-chave de um texto"""
        import re
        words = re.findall(r'\b\w{4,}\b', text.lower())
        return list(set(words))[:5]
    
    def get_calibration_params(self, text_length: int) -> Dict:
        """Sobrescrever se precisar de calibração específica"""
        base_params = super().get_calibration_params(text_length)
        
        # Adicionar parâmetros específicos da sua análise
        specific_params = {
            "my_parameter": "valor_baseado_no_tamanho"
        }
        
        return {**base_params, **specific_params}
