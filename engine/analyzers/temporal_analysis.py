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
