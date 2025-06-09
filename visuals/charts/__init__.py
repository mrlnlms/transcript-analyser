"""
Sistema de auto-descoberta de gráficos
"""
import importlib
import inspect
from pathlib import Path
from typing import Dict, Type
from abc import ABC, abstractmethod

class BaseChart(ABC):
    """Classe base para todos os gráficos"""
    
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path) if config_path else {}
        self.backend = self.config.get("backend", "plotly")  # plotly, matplotlib, text
    
    def load_config(self, config_path: str) -> dict:
        """Carrega configuração específica do gráfico"""
        import json
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config não encontrado: {config_path}")
            return {}
    
    @abstractmethod
    def create(self, data: Dict, output_path: str) -> str:
        """Cria a visualização"""
        pass
    
    def adjust_for_data_size(self, data: Dict) -> Dict:
        """Ajusta parâmetros visuais baseado no volume de dados"""
        if isinstance(data, dict):
            # Estimar tamanho dos dados
            total_items = sum(len(v) if isinstance(v, (list, dict)) else 1 
                            for v in data.values())
        else:
            total_items = len(data) if hasattr(data, '__len__') else 1
        
        if total_items > 100:
            return {"downsample": True, "max_points": 50, "smoothing": 0.3}
        elif total_items > 50:
            return {"downsample": False, "max_points": 100, "smoothing": 0.1}
        else:
            return {"downsample": False, "smoothing": 0.0}
    
    def get_name(self) -> str:
        """Retorna nome legível do gráfico"""
        return self.__class__.__name__.replace('Chart', '').replace('_', ' ').title()

def discover_charts() -> Dict[str, Type[BaseChart]]:
    """Encontra automaticamente todos os gráficos disponíveis"""
    charts = {}
    chart_dir = Path(__file__).parent
    
    for file_path in chart_dir.glob("*.py"):
        if file_path.name.startswith("_") or file_path.name == "__init__.py":
            continue
            
        module_name = f"visuals.charts.{file_path.stem}"
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BaseChart) and 
                    obj != BaseChart and
                    name.endswith("Chart")):
                    charts[name] = obj
        except ImportError as e:
            print(f"⚠️ Erro ao importar {module_name}: {e}")
    
    return charts
