"""
Sistema de auto-descoberta de analisadores
"""
import importlib
import inspect
from pathlib import Path
from typing import Dict, Type
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """Classe base para todos os analisadores"""
    
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path) if config_path else {}
    
    def load_config(self, config_path: str) -> dict:
        """Carrega configuração específica do analisador"""
        import json
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config não encontrado: {config_path}")
            return {}
    
    @abstractmethod
    def analyze(self, text: str) -> Dict:
        """Executa a análise principal"""
        pass
    
    def get_calibration_params(self, text_length: int) -> Dict:
        """Retorna parâmetros calibrados baseado no tamanho do texto"""
        if text_length < 1000:  # Texto curto (~15min)
            return {"segments": 5, "smoothing": 0.1, "min_frequency": 2}
        elif text_length > 10000:  # Texto longo (~1h45+)
            return {"segments": 20, "smoothing": 0.3, "min_frequency": 5}
        else:  # Texto médio
            return {"segments": 10, "smoothing": 0.2, "min_frequency": 3}
    
    def get_name(self) -> str:
        """Retorna nome legível do analisador"""
        return self.__class__.__name__.replace('Analyzer', '').replace('_', ' ').title()

def discover_analyzers() -> Dict[str, Type[BaseAnalyzer]]:
    """Encontra automaticamente todos os analisadores disponíveis"""
    analyzers = {}
    analyzer_dir = Path(__file__).parent
    
    for file_path in analyzer_dir.glob("*.py"):
        if file_path.name.startswith("_") or file_path.name == "__init__.py":
            continue
            
        module_name = f"engine.analyzers.{file_path.stem}"
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BaseAnalyzer) and 
                    obj != BaseAnalyzer and
                    name.endswith("Analyzer")):
                    analyzers[name] = obj
        except ImportError as e:
            print(f"⚠️ Erro ao importar {module_name}: {e}")
    
    return analyzers
