#!/usr/bin/env python3
"""Integra ConfigurationRegistry ao AnalysisOrchestrator"""

import re

# Código para adicionar ao __init__
INIT_CODE = '''        # Sistema de configuração
        from core.config.configuration_registry import ConfigurationRegistry
        self.config_registry = ConfigurationRegistry()
        self.logger.info(f"📊 ConfigurationRegistry: {len(self.config_registry.analyzer_schemas)} analyzers configuráveis")
'''

# Código para adicionar método de configuração
CONFIG_METHOD = '''
    def get_analyzer_config(self, analyzer_name: str, text_length: int = None, profile: str = None) -> Dict:
        """Obtém configuração para um analyzer baseado no contexto"""
        if not self.config_registry:
            return {}
        
        # Determinar tamanho do texto
        text_size = 'medium'
        if text_length:
            word_count = text_length // 5  # Estimativa grosseira
            text_size = self.config_registry.get_text_size_category(word_count)
        
        # Obter configuração
        config = self.config_registry.get_config_for_analyzer(
            analyzer_name, 
            text_size=text_size,
            profile=profile
        )
        
        return config
'''

# Ler arquivo
with open('core/engine/analysis_orchestrator.py', 'r') as f:
    content = f.read()

# Backup
with open('core/engine/analysis_orchestrator.py.backup', 'w') as f:
    f.write(content)

# Adicionar import no topo se não existir
if 'ConfigurationRegistry' not in content:
    # Adicionar no __init__
    lines = content.split('\n')
    
    # Encontrar onde adicionar no __init__
    for i, line in enumerate(lines):
        if 'def __init__(self):' in line:
            # Procurar o fim das inicializações existentes
            for j in range(i+1, len(lines)):
                if 'self.logger' in lines[j] and 'Descobertos' in lines[j]:
                    # Adicionar após essa linha
                    lines.insert(j+1, INIT_CODE)
                    break
            break
    
    # Adicionar método antes do analyze_transcript
    for i, line in enumerate(lines):
        if 'def analyze_transcript' in line:
            # Adicionar método antes
            lines.insert(i-1, CONFIG_METHOD)
            break
    
    # Salvar
    content = '\n'.join(lines)
    with open('core/engine/analysis_orchestrator.py', 'w') as f:
        f.write(content)
    
    print("✅ ConfigurationRegistry integrado ao AnalysisOrchestrator!")
else:
    print("⚠️  ConfigurationRegistry já está integrado")
