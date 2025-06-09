"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class TestVelocityAnalyzer(BaseAnalyzer):
    """
    Análise de Velocidade de Teste
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: TestVelocityAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """

    @staticmethod
    def get_config_schema():
        """Retorna o schema de configuração deste analyzer"""
        return {
            'test_mode': {
                'type': 'bool',
                'default': True,
                'description': 'Ativar modo de teste'
            },
            'mock_delay': {
                'type': 'float',
                'range': [0.0, 5.0],
                'default': 0.5,
                'description': 'Delay simulado em segundos'
            },
            'use_mock_data': {
                'type': 'bool',
                'default': True,
                'description': 'Usar dados mockados ao invés de análise real'
            },
            'complexity_simulation': {
                'type': 'str',
                'options': ['simple', 'medium', 'complex'],
                'default': 'medium',
                'description': 'Nível de complexidade da simulação'
            },
            'error_rate': {
                'type': 'float',
                'range': [0.0, 1.0],
                'default': 0.0,
                'description': 'Taxa de erro simulada (0.0 = sem erros)'
            },
            'verbose_output': {
                'type': 'bool',
                'default': False,
                'description': 'Saída verbosa para debug'
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
