"""
🎭 AnalysisOrchestrator - Coordenação Automática de Análises

Sistema revolucionário que descobre e executa automaticamente todas as análises disponíveis,
eliminando código hardcoded e permitindo arquitetura 100% plugável.

Princípio: "Descobre → Mapeia → Executa → Coordena"
"""

import os
import importlib
import inspect
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import json

class AnalysisOrchestrator:
    """
    🎯 Orquestrador que descobre e coordena automaticamente todas as análises
    
    REVOLUÇÃO:
    - Auto-descoberta total de analisadores
    - Mapeamento inteligente de dependências
    - Execução coordenada com cache
    - Mensagens informativas em tempo real
    - Zero código hardcoded para análises
    """
    
    def __init__(self, config_path: str = "config/analysis_configs"):
        self.config_path = Path(config_path)
        self.analyzers = {}
        self.dependencies = {}
        self.results_cache = {}
        
        # Auto-descoberta revolucionária
        self._discover_analyzers()
        self._map_dependencies()
        
    def _discover_analyzers(self):
        """🔍 Auto-descoberta de todos os analisadores disponíveis"""
        analyzers_dir = Path("engine/analyzers")
        
        if not analyzers_dir.exists():
            print("⚠️  Diretório engine/analyzers não encontrado")
            return
            
        # Percorrer todos os arquivos Python
        for py_file in analyzers_dir.glob("*.py"):
            if py_file.name.startswith("_") or py_file.name == "__init__.py":
                continue
                
            try:
                # Importar módulo dinamicamente
                module_name = f"engine.analyzers.{py_file.stem}"
                module = importlib.import_module(module_name)
                
                # Encontrar classes que terminam com 'Analyzer'
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name.endswith('Analyzer') and not name.startswith('_') and name != 'BaseAnalyzer':
                        analyzer_key = self._get_analyzer_key(name)
                        self.analyzers[analyzer_key] = {
                            'class': obj,
                            'name': name,
                            'module': module_name,
                            'config': self._load_config(analyzer_key)
                        }
                        
            except Exception as e:
                print(f"⚠️  Erro ao carregar analisador de {py_file}: {e}")
                
        print(f"🎯 AnalysisOrchestrator: Descobertos {len(self.analyzers)} analisadores:")
        for key in self.analyzers.keys():
            print(f"   ✅ {key}")
    
    def _get_analyzer_key(self, class_name: str) -> str:
        """🔑 Converter nome da classe para chave de análise"""
        # WordFrequencyAnalyzer -> word_frequency
        # TemporalAnalysisAnalyzer -> temporal_analysis
        # GlobalMetricsAnalyzer -> global_metrics
        
        key = class_name.replace('Analyzer', '')
        # Converter CamelCase para snake_case
        import re
        key = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
        key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        return key
    
    def _load_config(self, analyzer_key: str) -> Dict:
        """📋 Carregar configuração específica do analisador"""
        config_file = self.config_path / f"{analyzer_key}_config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Erro ao carregar config de {analyzer_key}: {e}")
                
        return {}
    
    def _map_dependencies(self):
        """🗺️ Mapear dependências entre analisadores"""
        # Análise de dependências baseada na assinatura dos métodos
        for key, analyzer_info in self.analyzers.items():
            deps = []
            
            # Verificar se o analisador usa resultados de outros
            analyzer_class = analyzer_info['class']
            
            # Verificar método analyze para dependencies
            if hasattr(analyzer_class, 'analyze'):
                try:
                    # Instanciar temporariamente para verificar dependências
                    temp_instance = analyzer_class()
                    if hasattr(temp_instance, 'get_dependencies'):
                        deps = temp_instance.get_dependencies()
                except:
                    pass
            
            self.dependencies[key] = deps
            
        print(f"🗺️  Dependências mapeadas:")
        for key, deps in self.dependencies.items():
            if deps:
                print(f"   📊 {key} → depende de: {deps}")
    
    def analyze(self, text: str, config: Dict = None) -> Dict[str, Any]:
        """
        🎯 MÉTODO PRINCIPAL - Coordena execução de todas as análises
        
        REVOLUÇÃO: Uma linha substitui centenas de linhas hardcoded!
        """
        
        print(f"\n🎭 AnalysisOrchestrator: Iniciando coordenação de {len(self.analyzers)} análises...")
        
        # Limpar cache para nova análise
        self.results_cache = {}
        
        # Configuração global + específica
        final_config = config or {}
        
        # Executar análises respeitando dependências
        execution_order = self._resolve_execution_order()
        
        results = {}
        successful_analyses = 0
        
        for analyzer_key in execution_order:
            try:
                print(f"   🔄 Executando: {analyzer_key}")
                
                result = self._execute_analyzer(analyzer_key, text, final_config)
                
                if result:
                    if result:
                        results[analyzer_key] = result
                        self.results_cache[analyzer_key] = result
                        # Também adicionar dados ao nível raiz para compatibilidade com gráficos
                        for key, value in result.items():
                            if key not in ['analysis_type', 'calibration_used']:
                                results[key] = value
                    successful_analyses += 1
                    print(f"   ✅ {analyzer_key}: Concluído")
                else:
                    print(f"   ⚠️  {analyzer_key}: Sem resultados")
                   
            except Exception as e:
                print(f"   ❌ {analyzer_key}: Erro - {e}")
                continue
        
        print(f"\n🎯 AnalysisOrchestrator: {successful_analyses}/{len(self.analyzers)} análises concluídas!")
        
        return results
    
    def _resolve_execution_order(self) -> List[str]:
        """📊 Resolver ordem de execução baseada em dependências"""
        
        # Ordenação topológica simples
        visited = set()
        temp_visited = set()
        order = []
        
        def visit(analyzer_key):
            if analyzer_key in temp_visited:
                # Dependência circular - ignorar
                return
            if analyzer_key in visited:
                return
                
            temp_visited.add(analyzer_key)
            
            # Visitar dependências primeiro
            for dep in self.dependencies.get(analyzer_key, []):
                if dep in self.analyzers:
                    visit(dep)
            
            temp_visited.remove(analyzer_key)
            visited.add(analyzer_key)
            order.append(analyzer_key)
        
        # Visitar todos os analisadores
        for analyzer_key in self.analyzers.keys():
            if analyzer_key not in visited:
                visit(analyzer_key)
        
        print(f"📊 Ordem de execução resolvida: {order}")
        return order
    
    def _execute_analyzer(self, analyzer_key: str, text: str, config: Dict) -> Optional[Dict]:
        """🚀 Executar um analisador específico"""
        
        analyzer_info = self.analyzers[analyzer_key]
        analyzer_class = analyzer_info['class']
        analyzer_config = analyzer_info['config']
        
        # Mesclar configurações: global + específica do analisador
        final_config = {**config, **analyzer_config}
        
        try:
            # Instanciar analisador
            analyzer = analyzer_class()
            
            # Preparar dados de entrada
            input_data = {'text': text, 'config': final_config}
            
            # Adicionar resultados de dependências
            for dep_key in self.dependencies.get(analyzer_key, []):
                if dep_key in self.results_cache:
                    input_data[dep_key] = self.results_cache[dep_key]
            
            # Executar análise
            if hasattr(analyzer, 'analyze'):
                result = analyzer.analyze(text)
                return result
            else:
                print(f"⚠️  {analyzer_key}: Método 'analyze' não encontrado")
                return None
                
        except Exception as e:
            print(f"❌ Erro na execução de {analyzer_key}: {e}")
            return None
    
    def get_available_analyzers(self) -> List[str]:
        """📋 Listar analisadores disponíveis"""
        return list(self.analyzers.keys())
    
    def get_analyzer_info(self, analyzer_key: str) -> Optional[Dict]:
        """📊 Informações detalhadas de um analisador"""
        return self.analyzers.get(analyzer_key)
    
    def get_dependencies_info(self) -> Dict[str, List[str]]:
        """🗺️ Informações de dependências"""
        return self.dependencies
    
    def enable_analyzer(self, analyzer_key: str) -> bool:
        """✅ Habilitar analisador específico"""
        if analyzer_key in self.analyzers:
            self.analyzers[analyzer_key]['enabled'] = True
            return True
        return False
    
    def disable_analyzer(self, analyzer_key: str) -> bool:
        """❌ Desabilitar analisador específico"""
        if analyzer_key in self.analyzers:
            self.analyzers[analyzer_key]['enabled'] = False
            return True
        return False
    
    def get_orchestration_stats(self) -> Dict:
        """📈 Estatísticas da orquestração"""
        return {
            'total_analyzers': len(self.analyzers),
            'analyzers_with_dependencies': sum(1 for deps in self.dependencies.values() if deps),
            'total_dependencies': sum(len(deps) for deps in self.dependencies.values()),
            'available_analyzers': self.get_available_analyzers(),
            'dependency_map': self.dependencies
        }


    def create_analysis_orchestrator(config_path: str = "config/analysis_configs") -> AnalysisOrchestrator:
        """🎭 Factory function para criar o orquestrador"""
        return AnalysisOrchestrator(config_path)


        # Exemplo de uso
        if __name__ == "__main__":
            print("🎭 AnalysisOrchestrator - Teste de Auto-descoberta")
            
            orchestrator = create_analysis_orchestrator()
            
            print(f"\n📊 Estatísticas:")
            stats = orchestrator.get_orchestration_stats()
            for key, value in stats.items():
                print(f"   {key}: {value}")
            
            # Teste com texto simples
            test_text = "Este é um teste do sistema de análise orquestrada."
            
            print(f"\n🧪 Teste de execução:")
            results = orchestrator.analyze(test_text)
        
        print(f"\n✅ Resultados obtidos: {list(results.keys())}")