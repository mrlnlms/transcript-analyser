# 📋 CHANGELOG - Transcript Analyzer

## [2.1.0-alpha] - Junho 2025 - Sistema de Configuração Avançada 🔧

### Added
- ConfigurationRegistry implementado - sistema central de configurações
- 3 perfis especializados: Acadêmico, Entrevista, Médico
- Auto-ajuste de configurações baseado em tamanho do texto
- Schema de configuração para cada analisador
- Organização completa da estrutura de arquivos

### Changed
- Scripts reorganizados em subpastas: tests/, maintenance/, development/
- Documentação reestruturada: CONTEXT.md, DEVELOPMENT.md, ROADMAP.md
- Limpeza completa do diretório raiz

### In Progress
- Integração do ConfigurationRegistry com analyzers reais
- Interface CLI para configuração interativa
- Sistema de validação de configurações

## [2.0.0] - Junho 2025 - Refatoração Épica 🎉

### Added
- Sistema modular completo com 5 novos módulos
- 9 analisadores plugáveis com auto-descoberta
- 8 visualizações plugáveis com orquestração
- Scripts de automação para criar novos plugins
- Gerador de relatórios markdown modularizado

### Changed
- run_analysis.py: 700+ → 100 linhas
- Arquitetura monolítica → 100% modular
- Configuração hardcoded → JSONs externos
- Sistema acoplado → Totalmente plugável

### Fixed
- Gerador de markdown modularizado
- Estrutura de output simplificada
- Todos os HTMLs no mesmo nível
- Correção de caminhos e organização de arquivos

## [1.0.0] - Janeiro 2025 - Versão Inicial

### Added
- Sistema funcional de análise
- 3 visualizações básicas
- CLI profissional
- Suporte a múltiplos projetos

### Known Issues
- Sistema monolítico difícil de manter
- Configurações hardcoded
- Análises com dados parcialmente mockados

---

**Convenções**: Este projeto segue [Semantic Versioning](https://semver.org/) e [Keep a Changelog](https://keepachangelog.com/)

## [2.1.0-beta] - Junho 2025 - ConfigurationRegistry Implementado 🔧

### Added
- BaseAnalyzer com suporte a get_config_schema()
- WordFrequencyAnalyzer com schema de configuração completo
- 4 parâmetros configuráveis: min_frequency, max_words, use_stopwords, stopwords_file
- Suporte para configurações por tamanho de texto (short_text, long_text)
- Suporte para configurações por perfil (academic, medical)

### Changed
- ConfigurationRegistry agora com estrutura real de schemas
- Preparado para auto-descoberta de configurações

### Next
- Implementar get_config_schema() nos outros 8 analyzers
- Auto-descoberta real no ConfigurationRegistry
- Interface CLI para configuração interativa
