#!/usr/bin/env python3
"""
Configuration Registry - Sistema Central de Configurações
V2.1 - Gerenciamento unificado de todas as configurações
"""

import json
import logging
import importlib
import inspect
from pathlib import Path
from typing import Dict, Any, List, Optional


class ConfigurationRegistry:
    """Registro central de todas as configurações disponíveis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analyzers_config = {}
        self.charts_config = {}
        self.profiles = self._load_profiles()
        print("🎯 Configuration Registry inicializado!")
        self._scan_all_configurations()
        
    def test(self):
        print("✅ Configuration Registry funcionando!")
    
    def get_available_profiles(self) -> List[str]:
        """Retorna lista de perfis disponíveis"""
        return list(self.profiles.keys())
    
    def get_version(self) -> str:
        """Retorna versão do Configuration Registry"""
        return "2.1.0-alpha"
    
    def _scan_all_configurations(self):
        """Varre todos os componentes e extrai suas configurações"""
        print("🔍 Escaneando configurações disponíveis...")
        
        # Escanear analisadores
        self._scan_analyzers()
        
        # Por enquanto, charts manual
        self._scan_charts()
        
        print(f"✅ Encontrados: {len(self.analyzers_config)} analisadores")
    
    def _scan_analyzers(self):
        """Escaneia configurações dos analisadores"""
        # Por enquanto, vamos adicionar manualmente o word_frequency
        # TODO: Implementar auto-descoberta real quando todos tiverem get_config_schema()
        
        self.analyzers_config['word_frequency'] = {
            'name': 'Word Frequency',
            'schema': {
                'min_frequency': {
                    'type': 'int',
                    'range': [1, 10],
                    'default': 2,
                    'short_text': 1,
                    'long_text': 5,
                    'description': 'Frequência mínima para considerar palavra relevante'
                },
                'max_words': {
                    'type': 'int',
                    'range': [10, 200],
                    'default': 50,
                    'short_text': 30,
                    'long_text': 100,
                    'description': 'Número máximo de palavras no resultado'
                }
            }
        }
    
    def _scan_charts(self):
        """Escaneia configurações das visualizações"""
        self.charts_config = {}
    
    def _load_profiles(self) -> Dict:
        """Carrega perfis pré-configurados"""
        return {
            'academic': {
                'name': 'Acadêmico',
                'description': 'Otimizado para textos acadêmicos longos'
            },
            'interview': {
                'name': 'Entrevista',
                'description': 'Otimizado para transcrições de entrevistas'
            },
            'medical': {
                'name': 'Médico/Saúde',
                'description': 'Otimizado para consultas e relatórios médicos'
            }
        }
    
    def get_consolidated_view(self) -> Dict[str, Any]:
        """Retorna visão consolidada de todas as configurações"""
        return {
            'analyzers': self.analyzers_config,
            'charts': self.charts_config,
            'profiles': self.profiles,
            'total_parameters': self._count_parameters()
        }
    
    def _count_parameters(self) -> int:
        """Conta total de parâmetros configuráveis"""
        count = 0
        for analyzer in self.analyzers_config.values():
            count += len(analyzer.get('schema', {}))
        return count


if __name__ == "__main__":
    registry = ConfigurationRegistry()
    registry.test()
    print(f"📋 Perfis: {registry.get_available_profiles()}")
    print(f"🔖 Versão: {registry.get_version()}")
    print(f"📊 Analyzers: {len(registry.analyzers_config)}")
    
    # Mostrar configurações
    view = registry.get_consolidated_view()
    print(f"⚙️  Total de parâmetros: {view['total_parameters']}")
