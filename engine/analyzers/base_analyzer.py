#!/usr/bin/env python3
"""Base class para todos os analyzers com suporte a ConfigurationRegistry"""

from abc import ABC, abstractmethod
from typing import Dict, Any


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
