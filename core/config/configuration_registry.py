"""Sistema central de configuração do Transcript Analyzer com auto-descoberta"""
import sys
sys.path.append(".")
import os
import importlib.util
from typing import Dict, List, Any, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ConfigurationRegistry:
    """Registro central de todas as configurações disponíveis no sistema"""
    
    def __init__(self):
        self.analyzer_schemas = {}
        self.chart_schemas = {}
        self.profiles = {
            'academic': {
                'description': 'Perfil para análise de textos acadêmicos',
                'adjustments': {
                    'n_topics': 10,
                    'min_frequency': 5,
                    'stopwords_file': 'academic',
                    'hesitation_markers': 'academic',
                    'certainty_phrases': 'academic'
                }
            },
            'interview': {
                'description': 'Perfil para análise de entrevistas',
                'adjustments': {
                    'detect_hesitations': True,
                    'segments': 15,
                    'window_size': 3,
                    'hesitation_markers': 'interview'
                }
            },
            'medical': {
                'description': 'Perfil para análise de textos médicos',
                'adjustments': {
                    'stopwords_file': 'medical',
                    'lexicon_positive': 'medical',
                    'lexicon_negative': 'medical',
                    'topic_keywords': 'medical'
                }
            }
        }
        self._discover_schemas()
    
    def _discover_schemas(self):
        """Auto-descobre schemas de analyzers e charts"""
        # Descobrir analyzers
        self._discover_analyzer_schemas()
        # Descobrir charts (futuro)
        self._discover_chart_schemas()
        
        logger.info(f"📊 ConfigurationRegistry: Descobertos {len(self.analyzer_schemas)} analyzers")
        logger.info(f"📈 Total de parâmetros: {self._count_total_parameters()}")
    
    def _discover_analyzer_schemas(self):
        """Descobre automaticamente schemas dos analyzers"""
        analyzers_dir = Path('engine/analyzers')
        
        if not analyzers_dir.exists():
            logger.warning(f"⚠️  Diretório de analyzers não encontrado: {analyzers_dir}")
            return
        
        for filepath in sorted(analyzers_dir.glob('*.py')):
            if filepath.name.startswith('_') or filepath.name in ['base_analyzer.py', 'analysis_orchestrator.py']:
                continue
                
            try:
                # Importar módulo dinamicamente
                module_name = filepath.stem
                spec = importlib.util.spec_from_file_location(
                    f"engine.analyzers.{module_name}", 
                    filepath
                )
                
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Encontrar classe analyzer
                    for attr_name in dir(module):
                        if (attr_name.endswith('Analyzer') and 
                            attr_name != 'BaseAnalyzer' and
                            not attr_name.startswith('_')):
                            
                            analyzer_class = getattr(module, attr_name)
                            
                            # Verificar se tem get_config_schema
                            if hasattr(analyzer_class, 'get_config_schema'):
                                try:
                                    schema = analyzer_class.get_config_schema()
                                    self.analyzer_schemas[module_name] = {
                                        'class_name': attr_name,
                                        'schema': schema,
                                        'param_count': len(schema)
                                    }
                                    logger.debug(f"✅ {module_name}: {len(schema)} parâmetros")
                                except Exception as e:
                                    logger.error(f"❌ Erro ao obter schema de {attr_name}: {e}")
                            break
                            
            except Exception as e:
                logger.warning(f"⚠️  Erro ao carregar {filepath.name}: {e}")
    
    def _discover_chart_schemas(self):
        """Descobre automaticamente schemas dos charts (futuro)"""
        # TODO: Implementar quando charts tiverem schemas
        pass
    
    def _count_total_parameters(self) -> int:
        """Conta o total de parâmetros configuráveis"""
        total = 0
        for analyzer_info in self.analyzer_schemas.values():
            total += analyzer_info['param_count']
        return total
    
    def get_analyzer_names(self) -> List[str]:
        """Retorna lista de nomes dos analyzers disponíveis"""
        return sorted(self.analyzer_schemas.keys())
    
    def get_analyzer_schema(self, analyzer_name: str) -> Dict:
        """Retorna schema de um analyzer específico"""
        if analyzer_name in self.analyzer_schemas:
            return self.analyzer_schemas[analyzer_name]['schema']
        return {}
    
    def get_all_analyzer_schemas(self) -> Dict:
        """Retorna todos os schemas de analyzers"""
        return {
            name: info['schema'] 
            for name, info in self.analyzer_schemas.items()
        }
    
    def get_consolidated_view(self) -> Dict:
        """Retorna visão consolidada de todas as configurações"""
        return {
            'analyzers': self.get_all_analyzer_schemas(),
            'charts': self.chart_schemas,
            'profiles': self.profiles,
            'text_size_rules': {
                'short': {'max_words': 500, 'label': 'Texto curto'},
                'medium': {'max_words': 5000, 'label': 'Texto médio'},
                'long': {'max_words': float('inf'), 'label': 'Texto longo'}
            },
            'summary': {
                'total_analyzers': len(self.analyzer_schemas),
                'total_parameters': self._count_total_parameters(),
                'available_profiles': list(self.profiles.keys())
            }
        }
    
    def get_config_for_analyzer(self, analyzer_name: str, 
                               text_size: str = 'medium',
                               profile: str = None) -> Dict:
        """Retorna configuração ajustada para um analyzer"""
        schema = self.get_analyzer_schema(analyzer_name)
        if not schema:
            return {}
            
        config = {}
        
        # Aplicar valores padrão
        for param, param_schema in schema.items():
            # Valor base
            config[param] = param_schema.get('default')
            
            # Ajuste por tamanho de texto
            if text_size in param_schema:
                config[param] = param_schema[text_size]
            
            # Ajuste por perfil
            if profile and profile in self.profiles:
                # Primeiro verificar ajustes gerais do perfil
                adjustments = self.profiles[profile]['adjustments']
                if param in adjustments:
                    config[param] = adjustments[param]
                
                # Depois verificar valores específicos no schema
                if profile in param_schema:
                    config[param] = param_schema[profile]
        
        return config
    
    def validate_config(self, analyzer_name: str, config: Dict) -> Tuple[bool, List[str]]:
        """Valida configuração contra schema"""
        schema = self.get_analyzer_schema(analyzer_name)
        if not schema:
            return False, [f"Analyzer '{analyzer_name}' não encontrado"]
            
        errors = []
        
        for param, value in config.items():
            if param not in schema:
                errors.append(f"Parâmetro desconhecido: {param}")
                continue
                
            param_schema = schema[param]
            param_type = param_schema.get('type')
            
            # Validar tipo
            type_valid = True
            if param_type == 'int' and not isinstance(value, int):
                errors.append(f"{param} deve ser int, recebido {type(value).__name__}")
                type_valid = False
            elif param_type == 'float' and not isinstance(value, (int, float)):
                errors.append(f"{param} deve ser float, recebido {type(value).__name__}")
                type_valid = False
            elif param_type == 'bool' and not isinstance(value, bool):
                errors.append(f"{param} deve ser bool, recebido {type(value).__name__}")
                type_valid = False
            elif param_type == 'str' and not isinstance(value, str):
                errors.append(f"{param} deve ser str, recebido {type(value).__name__}")
                type_valid = False
            elif param_type == 'list' and not isinstance(value, list):
                errors.append(f"{param} deve ser list, recebido {type(value).__name__}")
                type_valid = False
            elif param_type == 'dict' and not isinstance(value, dict):
                errors.append(f"{param} deve ser dict, recebido {type(value).__name__}")
                type_valid = False
            
            # Validar range (apenas se o tipo está correto)
            if type_valid and 'range' in param_schema and isinstance(value, (int, float)):
                min_val, max_val = param_schema['range']
                if value < min_val or value > max_val:
                    errors.append(f"{param} deve estar entre {min_val} e {max_val}, recebido {value}")
            
            # Validar opções
            if type_valid and 'options' in param_schema:
                if param_type == 'list':
                    for item in value:
                        if item not in param_schema['options']:
                            errors.append(f"{param}: '{item}' não é uma opção válida")
                elif value not in param_schema['options']:
                    errors.append(f"{param}: '{value}' não é uma opção válida. Opções: {param_schema['options']}")
        
        return len(errors) == 0, errors
    
    def print_analyzer_config(self, analyzer_name: str):
        """Imprime configuração de um analyzer de forma legível"""
        if analyzer_name not in self.analyzer_schemas:
            print(f"❌ Analyzer '{analyzer_name}' não encontrado")
            return
            
        schema = self.get_analyzer_schema(analyzer_name)
        info = self.analyzer_schemas[analyzer_name]
        
        print(f"\n📊 Configurações para {analyzer_name}")
        print(f"   Classe: {info['class_name']}")
        print(f"   Total de parâmetros: {info['param_count']}")
        print("=" * 60)
        
        for param, param_schema in schema.items():
            print(f"\n▶ {param}")
            print(f"  Tipo: {param_schema.get('type', 'não especificado')}")
            print(f"  Padrão: {param_schema.get('default', 'não especificado')}")
            
            if 'description' in param_schema:
                print(f"  Descrição: {param_schema['description']}")
            
            if 'range' in param_schema:
                print(f"  Range: {param_schema['range']}")
            
            if 'options' in param_schema:
                print(f"  Opções: {param_schema['options']}")
            
            # Valores especiais
            special_values = []
            for key in ['short_text', 'long_text', 'academic', 'medical', 'interview']:
                if key in param_schema:
                    special_values.append(f"{key}={param_schema[key]}")
            
            if special_values:
                print(f"  Valores especiais: {', '.join(special_values)}")
    
    def get_text_size_category(self, word_count: int) -> str:
        """Determina a categoria de tamanho do texto"""
        rules = self.get_consolidated_view()['text_size_rules']
        
        if word_count <= rules['short']['max_words']:
            return 'short_text'
        elif word_count <= rules['medium']['max_words']:
            return 'medium'
        else:
            return 'long_text'


# Testes se executado diretamente
if __name__ == '__main__':
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    print("🔍 Testando ConfigurationRegistry com auto-descoberta...\n")
    
    registry = ConfigurationRegistry()
    
    # Mostrar resumo
    view = registry.get_consolidated_view()
    summary = view['summary']
    
    print(f"\n📊 RESUMO DA AUTO-DESCOBERTA:")
    print(f"  - Analyzers descobertos: {summary['total_analyzers']}")
    print(f"  - Total de parâmetros: {summary['total_parameters']}")
    print(f"  - Perfis disponíveis: {summary['available_profiles']}")
    
    # Listar analyzers
    print(f"\n📋 Analyzers disponíveis:")
    for name in registry.get_analyzer_names():
        info = registry.analyzer_schemas[name]
        print(f"  - {name}: {info['param_count']} parâmetros")
    
    # Exemplo de configuração contextual
    print(f"\n🧪 Exemplo de configuração (word_frequency, texto curto, perfil acadêmico):")
    config = registry.get_config_for_analyzer('word_frequency', 
                                             text_size='short_text',
                                             profile='academic')
    for k, v in config.items():
        print(f"  {k}: {v}")
