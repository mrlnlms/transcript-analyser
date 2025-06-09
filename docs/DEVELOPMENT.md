# 🛠️ Guia de Desenvolvimento - Transcript Analyzer

## 📋 Contexto Essencial para Novos Chats

### Informações Críticas do Projeto
- **Versão Atual**: V2.0 (100% modular)
- **Linguagem**: Python 3.8+
- **Arquitetura**: Sistema plugável com orquestradores
- **Estado**: Funcional, em evolução para V2.1

### Arquitetura Core
```
Entry Point (100 linhas) → Módulos → Orquestradores → Plugins
```

### Módulos Principais
1. **cli_manager.py** - Gerencia comandos CLI
2. **project_manager.py** - Gerencia projetos
3. **analysis_runner.py** - Coordena análises
4. **markdown_generator.py** - Gera relatórios
5. **analysis_orchestrator.py** - Orquestra 9 análises
6. **chart_orchestrator.py** - Orquestra 8 gráficos

## 🎯 Padrões e Convenções

### Sistema Plugável
```python
# Para adicionar nova análise:
# 1. Criar arquivo em engine/analyzers/
class MyAnalyzer(BaseAnalyzer):
    def analyze(self, text: str) -> Dict:
        # implementação
        
# 2. Criar config em config/analysis_configs/
{
    "name": "my_analyzer",
    "enabled": true,
    "parameters": {}
}
```

### Convenções de Código
- **Docstrings**: Sempre em português
- **Logs**: Usar emojis para visual (🎯, ✅, ❌)
- **Configs**: JSON externo sempre que possível
- **Nomes**: snake_case para arquivos, CamelCase para classes

## 🚀 Workflow de Desenvolvimento

### Para Adicionar Nova Feature
1. **Discussão**: Criar issue/artifact com proposta
2. **Branch**: feature/nome-da-feature
3. **Implementação**: Seguir arquitetura plugável
4. **Testes**: Usar scripts em `scripts/`
5. **Documentação**: Atualizar artifacts relevantes

### Scripts Úteis
```bash
# Teste rápido com arquivo real
./scripts/teste_real_simples.sh

# Teste completo automático
./scripts/teste_automatico.sh

# Criar nova análise
./scripts/automation/nova_analise.sh "nome" "descrição"

# Criar novo gráfico
./scripts/automation/novo_grafico.sh "nome" "descrição"
```

## 📊 Estado Atual e Próximos Passos

### V2.0 Completa ✅
- Sistema 100% modular
- 9 análises funcionando
- 8 visualizações funcionando
- Orquestração automática

### V2.1 Em Planejamento 🎯
- **ConfigurationRegistry**: Sistema central de configurações
- **Configuration Manager**: Ajustes por contexto/domínio
- **Análise Comparativa**: Implementação modular
- **Perfis Especializados**: Acadêmico, Médico, etc.

## 💡 Conceitos Importantes

### Orquestração
- **AnalysisOrchestrator**: Descobre e coordena análises
- **ChartOrchestrator**: Mapeia dados → visualizações
- **Auto-descoberta**: Zero configuração manual

### Configuração em Camadas
```
Global → Projeto → Análise → Texto
```

### Fallback de Visualização
```
Plotly (interativo) → Matplotlib (estático) → Text (sempre funciona)
```

## 🔧 Implementação do ConfigurationRegistry (V2.1)

```python
# Conceito central para V2.1
class ConfigurationRegistry:
    """Registro central de todas as configurações"""
    
    def __init__(self):
        self.analyzers = self._scan_analyzers()
        self.profiles = self._load_profiles()
        
    def get_config_for_text(self, text_stats: Dict) -> Dict:
        """Retorna config otimizada para o texto"""
        # Auto-detecção baseada em:
        # - Tamanho (curto/médio/longo)
        # - Domínio detectado
        # - Complexidade linguística
```

### Cada Analisador Expõe seu Schema
```python
class BaseAnalyzer:
    @staticmethod
    @abstractmethod
    def get_config_schema() -> Dict:
        """Retorna schema de configuração"""
        pass
```

## 🎨 Interface de Configuração (Conceito V2.1)

### CLI Avançado
```bash
# Configurar análise interativamente
python3 run_analysis.py --configure

# Usar perfil específico
python3 run_analysis.py --project meu_estudo --profile academic

# Exportar configuração
python3 run_analysis.py --export-config meu_estudo > config.json
```

### Web Dashboard (Futuro)
- FastAPI backend
- Vue.js frontend
- Configuração visual drag-and-drop

## 📝 Checklist para Novo Desenvolvedor

- [ ] Ler README.md (visão geral)
- [ ] Ler ARCHITECTURE.md (como funciona)
- [ ] Rodar teste_automatico.sh (ver sistema funcionando)
- [ ] Explorar um analyzer em engine/analyzers/
- [ ] Entender orquestradores (analysis e chart)
- [ ] Criar analyzer de teste com nova_analise.sh
- [ ] Ler ROADMAP.md (futuro do projeto)

## 🤝 Como Contribuir

1. **Issues**: Reportar bugs, sugerir features
2. **Pull Requests**: Seguir padrão de commits
3. **Documentação**: Manter artifacts atualizados
4. **Testes**: Sempre testar com dados reais

## 🎯 Dicas para Manter Contexto

### Em Novo Chat
1. Mencionar versão atual (V2.0)
2. Destacar arquitetura modular
3. Explicar sistema plugável
4. Referenciar ConfigurationRegistry para V2.1

### Artifacts Essenciais
- README.md - Visão geral
- ARCHITECTURE.md - Detalhes técnicos
- ROADMAP.md - Próximos passos
- Este arquivo - Contexto de desenvolvimento

---

**Lembre-se**: O poder do sistema está na modularidade e orquestração. Sempre pense: "Como fazer isso de forma plugável?"