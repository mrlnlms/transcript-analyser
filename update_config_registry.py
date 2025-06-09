#!/usr/bin/env python3
"""Script para atualizar o ConfigurationRegistry com auto-descoberta real"""

import ast

# Ler o arquivo atual
with open('core/config/configuration_registry.py', 'r') as f:
    content = f.read()

# Adicionar método de scan real
new_scan_method = '''
    def _scan_analyzers(self):
        """Escaneia configurações dos analisadores"""
        import importlib
        import inspect
        from pathlib import Path
        
        analyzers_path = Path("engine/analyzers")
        if not analyzers_path.exists():
            print("⚠️  Pasta engine/analyzers não encontrada")
            return
            
        print("📊 Escaneando analyzers...")
        
        for py_file in analyzers_path.glob("*.py"):
            if py_file.stem.startswith('_'):
                continue
                
            try:
                # Importar módulo
                module_name = f"engine.analyzers.{py_file.stem}"
                module = importlib.import_module(module_name)
                
                # Procurar classes Analyzer
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name.endswith('Analyzer') and hasattr(obj, 'get_config_schema'):
                        # Adicionar ao registry
                        schema = obj.get_config_schema()
                        self.analyzers_config[py_file.stem] = {
                            'name': name.replace('Analyzer', '').replace('_', ' ').title(),
                            'class': name,
                            'schema': schema
                        }
                        print(f"   ✅ {name}: {len(schema)} parâmetros")
                        
            except Exception as e:
                print(f"   ❌ Erro ao escanear {py_file.stem}: {e}")
'''

# Substituir o método placeholder
# TODO: Implementar substituição

print("✅ Script criado! Execute manualmente as mudanças no ConfigurationRegistry")
