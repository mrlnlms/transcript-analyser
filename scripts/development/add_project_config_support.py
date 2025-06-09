#!/usr/bin/env python3
"""Adiciona suporte a configuração por projeto no BaseAnalyzer"""

# Código para adicionar ao BaseAnalyzer
CONFIG_SUPPORT = '''
    def configure_for_project(self, project_config: Dict[str, Any]):
        """Configura analyzer com settings específicos do projeto"""
        # Mesclar configuração do projeto com a padrão
        self.config = {**self.config, **project_config.get(self.__class__.__name__, {})}
    
    def get_project_overrides(self) -> Dict[str, Any]:
        """Retorna configurações que podem ser sobrescritas por projeto"""
        schema = self.get_config_schema()
        overridable = {}
        
        for param, info in schema.items():
            # Marcar parâmetros que podem ser sobrescritos
            if info.get('project_override', True):
                overridable[param] = info
        
        return overridable
'''

print("""
💡 IDEIA: Configuração hierárquica

1. Configuração base (do schema)
2. Configuração por perfil (academic, medical, etc)
3. Configuração por tamanho de texto
4. Configuração por projeto (override)

Exemplo:
{
  "project_name": "pesquisa_educacao",
  "analyzer_overrides": {
    "GlobalMetricsAnalyzer": {
      "sentiment_threshold": 0.2,
      "custom_insights": true
    },
    "TemporalAnalysisAnalyzer": {
      "segments": 20,
      "volatility_threshold": 0.15
    }
  }
}
""")
