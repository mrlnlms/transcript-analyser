# Contexto Essencial - Transcript Analyzer V2.1

## Estado Atual
- Versão: V2.1-alpha (reorganização completa em Jun/2025)
- Repo: github.com/mrlnlms/transcript-analyser
- Status: 100% modular, estrutura profissional
- Ambiente: macOS, Python 3.8+, ambiente virtual transcript_env

## Arquitetura V2.1

run_analysis.py (100 linhas) -> Core -> Orquestradores -> Plugins

### Estrutura Core

core/
├── managers/      # CLI, Project, Analysis managers
├── config/        # ConfigurationRegistry, config_loader
├── generators/    # MarkdownReportGenerator
├── engine/        # Orchestrators e core
└── visuals/       # Visualização e charts orchestrator

### Plugins
- Análises: engine/analyzers/*.py (9 funcionando)
- Gráficos: visuals/charts/*.py (8 funcionando)
- Auto-descoberta: 100% automática

## Comandos Rápidos

# Testar sistema
./scripts/tests/teste_automatico.sh

# Criar projeto
python3 run_analysis.py --create-project teste

# Analisar
python3 run_analysis.py --project teste

# Listar
python3 run_analysis.py --list-projects

## Foco Atual: V2.1 - ConfigurationRegistry

### Status
- ConfigurationRegistry base implementado
- 3 perfis definidos (academic, interview, medical)
- Integração com analyzers em progresso
- Interface CLI de configuração planejada

### Arquitetura ConfigurationRegistry

# core/config/configuration_registry.py
class ConfigurationRegistry:
    - get_config_schema() por analyzer
    - get_consolidated_view() visão unificada
    - auto_adjust_for_text() ajuste inteligente
    - perfis especializados por domínio

## Estrutura Limpa

Raiz: apenas run_analysis.py e setup_auto.py
Core: toda lógica principal organizada
Engine: apenas analyzers/
Visuals: apenas charts/
Scripts: organizados em tests/, maintenance/, development/

## Imports Atualizados

from core.managers.cli_manager import CLIManager
from core.managers.project_manager import ProjectManager
from core.managers.analysis_runner import AnalysisRunner
from core.config.configuration_registry import ConfigurationRegistry
from core.engine.analysis_orchestrator import AnalysisOrchestrator

## Documentação
- README.md - Visão geral e uso
- CONTEXT.md - Este arquivo (novo chat)
- DEVELOPMENT.md - Guia técnico
- ROADMAP.md - Planejamento V2.1

---
Próximo: Implementar get_config_schema() em cada analyzer
## 🎯 Status ConfigurationRegistry V2.1-beta
- ✅ BaseAnalyzer com get_config_schema() implementado
- ✅ WordFrequencyAnalyzer com 4 parâmetros configuráveis
- 🔄 Faltam 8 analyzers para implementar schemas
## 🎯 Status ConfigurationRegistry V2.1-beta
- ✅ BaseAnalyzer com get_config_schema() implementado
- ✅ WordFrequencyAnalyzer com 4 parâmetros configuráveis
- 🔄 Faltam 8 analyzers para implementar schemas
