#!/usr/bin/env python3
"""Base class para todos os analyzers com suporte a ConfigurationRegistry"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseAnalyzer(ABC):
    """Classe base para todos os analyzers"""
    
    def __init__(self):
        self.config = self.get_default_config()
    
    @abstractmethod
    def analyze(self, text: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Método principal de análise"""
        pass
    
    @staticmethod
    @abstractmethod
    def get_config_schema() -> Dict[str, Any]:
        """Retorna o schema de configuração do analyzer"""
        pass
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """Retorna configuração padrão baseada no schema"""
        schema = cls.get_config_schema()
        config = {}
        for param, info in schema.items():
            config[param] = info.get('default')
        return config
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Valida configuração contra o schema"""
        schema = self.get_config_schema()
        for param, value in config.items():
            if param not in schema:
                return False
            # TODO: Validar tipos e ranges
        return True

    def interpret_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpreta resultados numéricos em insights qualitativos
        
        Exemplo:
            {'sentiment': -0.5} → {'sentiment': -0.5, 'sentiment_label': 'Negativo moderado'}
        
        Override este método em cada analyzer para interpretações específicas
        """
        return results
    
    def get_insights(self, results: Dict[str, Any]) -> List[str]:
        """
        Gera insights textuais baseados nos resultados
        
        Returns:
            Lista de insights em linguagem natural
        """
        return []
    
    def format_output(self, results: Dict[str, Any], format_type: str = 'markdown') -> str:
        """
        Formata resultados para diferentes tipos de saída
        
        Args:
            results: Resultados da análise
            format_type: 'markdown', 'json', 'html', 'text'
        
        Returns:
            String formatada no tipo solicitado
        """
        interpreted = self.interpret_results(results)
        
        if format_type == 'markdown':
            return self._format_markdown(interpreted)
        elif format_type == 'json':
            import json
            return json.dumps(interpreted, indent=2, ensure_ascii=False)
        elif format_type == 'text':
            return self._format_text(interpreted)
        else:
            return str(interpreted)
    
    def _format_markdown(self, results: Dict[str, Any]) -> str:
        """Formata resultados como Markdown"""
        # Implementação base - override em analyzers específicos
        lines = [f"## {self.__class__.__name__} Results"]
        
        for key, value in results.items():
            if not key.startswith('_'):
                lines.append(f"- **{key}**: {value}")
        return '\n'.join(lines)
    
    def _format_text(self, results: Dict[str, Any]) -> str:
        """Formata resultados como texto simples"""
        lines = []
        for key, value in results.items():
            if not key.startswith('_'):
                lines.append(f"{key}: {value}")
        return '\n'.join(lines)
