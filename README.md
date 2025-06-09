# 🔍 Transcript Analyzer V2.1

Sistema escalável e modular para análise automatizada de entrevistas qualitativas, desenvolvido para pesquisadores, analistas e profissionais que trabalham com dados textuais. Combina análise linguística, emocional e temática com visualizações interativas profissionais.

## 🆕 Novidades V2.1 - Sistema de Configuração Avançada

A versão 2.1 está implementando um sistema revolucionário de configuração:

- **Auto-descoberta**: Sistema descobre automaticamente TODAS as configurações disponíveis
- **Perfis Especializados**: Acadêmico, Médico, Entrevista (ajustes automáticos)
- **Ajuste por Tamanho**: Configurações otimizadas para textos curtos/médios/longos
- **40+ Parâmetros**: Controle fino sobre cada aspecto da análise

### Status da Implementação V2.1-beta COMPLETO! 🎉
- ✅ BaseAnalyzer com suporte a schemas de configuração
- ✅ **TODOS os 9 analyzers com schemas implementados!**
- ✅ **60 parâmetros configuráveis no total**
- ✅ **ConfigurationRegistry com auto-descoberta funcionando**
- ✅ **Integração completa com AnalysisOrchestrator**
- ✅ **Sistema 100% testado e funcional**
- ✅ **Geração de relatórios Markdown funcionando perfeitamente**
- ✅ **Projeto organizado e estruturado**
- ⏳ Interface CLI de configuração (próxima fase)
- ⏳ Manual de uso das configurações (próxima fase)

## ✨ Características Principais

- 🔍 **Análise Multidimensional**: Sentimentos + Tópicos + Padrões Linguísticos + Redes Semânticas
- 📊 **3 Backends de Visualização**: Plotly (interativo) + Matplotlib (estático) + Text (fallback)
- ⚙️ **Configuração Externa**: JSON/TXT editáveis - zero edição de código
- 🚀 **CLI Profissional**: Interface completa de linha de comando
- 🎨 **Dashboard Inteligente**: Interpretações automáticas e métricas avançadas
- 🔄 **Análise Comparativa**: Compare múltiplos projetos simultaneamente

## 📊 Métricas de Análise

- 😊 **Sentimento Global**: +0.15 (levemente positivo)
- 🎯 **Coerência Temática**: 0.72 (boa estrutura narrativa)
- 💭 **Abertura Emocional**: 1.23 (expressivo)

## 🚀 Quick Start

```bash
# 1. Clone/baixe o projeto
git clone https://github.com/mrlnlms/transcript-analyser
cd transcript-analyser

# 2. Execute setup automático (detecta seu SO)
python3 setup_auto.py

# 3. Siga as instruções em QUICK_START.md
```

### Setup Manual Alternativo

```bash
# 1. Ambiente virtual
python3 -m venv transcript_env
source transcript_env/bin/activate  # Mac/Linux
# transcript_env\Scripts\activate   # Windows

# 2. Dependências
pip install -r requirements.txt

# 3. Verificar instalação
python3 run_analysis.py --test-visuals
```

## 🛠️ Scripts Auxiliares

O projeto inclui scripts bash organizados em subpastas:

### Scripts de Teste (`scripts/tests/`)

#### `teste_automatico.sh`
Executa teste completo com dados mockados/densos:
```bash
./scripts/tests/teste_automatico.sh      # Executa sem abrir resultados
./scripts/tests/teste_automatico.sh yes  # Executa e abre imagem comparativa
```

#### `teste_real_simples.sh`
Teste rápido com arquivo real:
```bash
./scripts/tests/teste_real_simples.sh
```

### Scripts de Manutenção (`scripts/maintenance/`)

#### `workflow_manual.sh`
Workflow completo para análise real:
```bash
./scripts/maintenance/workflow_manual.sh
```

#### `limpar_projetos.sh`
Limpeza básica de projetos:
```bash
./scripts/maintenance/limpar_projetos.sh
```

### Scripts de Desenvolvimento (`scripts/development/`)
Scripts para auxiliar no desenvolvimento de novas funcionalidades.

## 💻 Uso Diário

### Comandos Essenciais

```bash
# Criar novo projeto
python3 run_analysis.py --create-project meu_estudo

# Analisar projeto
python3 run_analysis.py --project meu_estudo

# Listar projetos
python3 run_analysis.py --list-projects

# Comparação
python3 run_analysis.py --compare projeto1 projeto2

# Testar sistema
python3 run_analysis.py --test-visuals
```

### Workflow Típico

1. **Criar projeto**
   ```bash
   python3 run_analysis.py --create-project entrevistas_2025
   ```

2. **Adicionar arquivos**
   ```bash
   # Copie seus .txt para:
   projects/entrevistas_2025/arquivos/
   ```

3. **Executar análise**
   ```bash
   python3 run_analysis.py --project entrevistas_2025
   ```

4. **Ver resultados**
   ```bash
   # Abrir pasta de output
   open projects/entrevistas_2025/output/
   
   # Resultados incluem:
   # - 8 visualizações HTML interativas
   # - report_[arquivo].md com interpretações
   # - Dados brutos em JSON
   ```

## 📁 Estrutura do Projeto V2.1

```
transcript-analyser/
├── 🚀 run_analysis.py          # Entry point único na raiz (~100 linhas)
├── 🔧 setup_auto.py           # Setup automatizado
│
├── 📂 core/                   # Núcleo do sistema V2.1
│   ├── managers/              # Gerenciadores principais
│   │   ├── cli_manager.py     # Interface CLI
│   │   ├── project_manager.py # Gestão de projetos
│   │   └── analysis_runner.py # Coordenação de análises
│   ├── config/               # Sistema de Configuração V2.1
│   │   ├── configuration_registry.py # Registry central (novo!)
│   │   └── config_loader.py  # Carregador de configs
│   ├── generators/           # Geradores
│   │   └── markdown_generator.py # Relatórios markdown
│   ├── engine/              # Motor de análise
│   │   ├── analysis_orchestrator.py # Orquestrador principal
│   │   ├── analyzer_core.py  # Core do sistema
│   │   └── comparative_analyzer.py # Análise comparativa
│   └── visuals/             # Sistema de visualização
│       ├── chart_orchestrator.py # Orquestrador de gráficos
│       ├── visualization_manager.py # 3 backends
│       └── dashboard_generator.py # Dashboard HTML
│
├── 📊 engine/                # Analisadores plugáveis
│   └── analyzers/           # 9 análises + base_analyzer.py
│       ├── base_analyzer.py # Classe base com suporte a schemas
│       ├── word_frequency.py # ✅ Schema implementado
│       ├── temporal_analysis.py # ⏳ Schema em implementação
│       └── ... (7 outros analyzers)
│
├── 🎨 visuals/              # Visualizações plugáveis
│   └── charts/              # 8 gráficos disponíveis
│
├── ⚙️ config/               # Configurações JSON
├── 📚 resources/            # Léxicos e dicionários
├── 🛠️ scripts/              # Scripts organizados
│   ├── tests/               # Scripts de teste
│   ├── maintenance/         # Scripts de manutenção
│   └── development/         # Scripts de desenvolvimento
│
├── 📁 projects/             # Projetos dos usuários
├── 🧪 tests/                # Testes e mocks
│   └── mock_data/          # Dados mockados
└── 📋 docs/                 # Documentação completa
    ├── CONTEXT.md           # Contexto para novos chats
    ├── DEVELOPMENT.md       # Guia de desenvolvimento
    └── ROADMAP.md          # Planejamento V2.1+
```

## ⚙️ Configuração

### V2.1: Sistema de Configuração Avançada (em desenvolvimento)

Cada analyzer terá parâmetros configuráveis através de schemas:

```python
# Exemplo: WordFrequencyAnalyzer
{
    'min_frequency': {
        'type': 'int',
        'range': [1, 10],
        'default': 2,
        'short_text': 1,      # Para textos < 500 palavras
        'long_text': 5,       # Para textos > 5000 palavras
        'academic': 5,        # Perfil acadêmico
        'description': 'Frequência mínima para considerar palavra relevante'
    },
    'max_words': {
        'type': 'int',
        'range': [10, 200],
        'default': 50,
        'description': 'Número máximo de palavras no resultado'
    }
}
```

### Configuração do Projeto (V2.0 - ainda funcional)

Cada projeto tem um arquivo `config_analise.json` editável:

```json
{
    "project_name": "meu_estudo",
    "topic_modeling": {
        "n_topics": 5,
        "auto_adjust": true
    },
    "emotion": {
        "block_size": 10,
        "smoothing": true
    },
    "output": {
        "generate_visuals": true,
        "dashboard_style": "premium"
    }
}
```

### Personalização de Léxicos

Edite arquivos em `resources/` para seu domínio:

```bash
# Adicionar termos específicos
echo "gamificação" >> resources/stopwords_custom.txt
echo "BNCC" >> resources/emocionais_positivos.txt

# Editar pesos das fórmulas
nano resources/pesos_formula_linguistica.json
```

## 📊 Análises Disponíveis

### Análises Implementadas (V2.0 - 100% funcionais)
1. **Frequência de Palavras** - Top palavras e distribuição
2. **Análise Temporal** - Evolução emocional e narrativa
3. **Métricas Globais** - Sentimento, coerência, abertura
4. **Padrões Linguísticos** - Hesitações, certeza/incerteza
5. **Rede de Conceitos** - Conexões semânticas
6. **Modelagem de Tópicos** - Temas principais
7. **Detecção de Contradições** - Inconsistências narrativas
8. **Análise de Sentimento** - Polaridade emocional
9. **Test Velocity** - Análise de desenvolvimento

## 🎨 Tipos de Visualização

| Tipo | Backend | Formato | Descrição |
|------|---------|---------|-----------|
| Timeline Emocional | Plotly | HTML | Evolução temporal interativa |
| Rede de Conceitos | Plotly | HTML | Grafo semântico interativo |
| Métricas Globais | Matplotlib | PNG | Dashboard de indicadores |
| Word Cloud | HTML | HTML | Nuvem de palavras interativa |
| Padrões Linguísticos | Matplotlib | PNG | Análise de marcadores |
| Top Palavras | Matplotlib | PNG | Ranking de frequências |
| Hierarquia de Tópicos | Matplotlib | PNG | Distribuição temática |
| Contradições | Matplotlib | PNG | Análise de inconsistências |

## 🏗️ Arquitetura V2.0/V2.1

### Princípios de Design
- **Modular**: Cada componente tem responsabilidade única
- **Plugável**: Adicione funcionalidades sem tocar no core
- **Configurável**: Tudo ajustável via JSON/schemas
- **Orquestrado**: Sistema auto-gerenciado

### Sistema de Orquestração
```python
# Análises: 9/9 funcionando automaticamente
analysis_result = analysis_orchestrator.analyze_transcript(file_path)

# Visualizações: 8/8 criadas automaticamente
chart_result = chart_orchestrator.analyze(analysis_result, output_dir)
```

### Sistema de Fallback
```
Plotly (interativo) → Matplotlib (estático) → Text (sempre funciona)
```

## 📈 Evolução do Sistema

### V1 → V2.0 → V2.1

#### V2.0 (Completa)
- ✅ Modularização total (700+ → 100 linhas)
- ✅ 9 análises plugáveis
- ✅ 8 visualizações plugáveis
- ✅ Orquestração automática
- ✅ 3 backends de visualização

#### V2.1 (Em desenvolvimento)
- 🔄 Sistema de configuração avançada
- 🔄 Schemas para todos os analyzers
- 📋 Auto-descoberta de configurações
- 📋 Interface CLI para configuração
- 📋 Perfis especializados

## 🔮 Roadmap

### Curto Prazo (V2.1)
- Sistema de configuração completo
- Interface CLI para configuração
- Perfis por domínio
- Validação automática

### Médio Prazo
- Interface Web
- API REST
- Cache inteligente
- Docker

### Longo Prazo
- Plugins externos
- Cloud deployment
- ML avançado
- Análise de áudio

## 🤝 Contribuindo

1. Fork o repositório
2. Clone localmente: `git clone [url]`
3. Setup: `python3 setup_auto.py`
4. Crie sua branch: `git checkout -b feature/nome`
5. Desenvolva e teste
6. Pull Request com descrição detalhada

### Áreas para Contribuição
- 🔍 Novos tipos de análise
- 📊 Backends de visualização
- 🌐 Tradução e i18n
- 📚 Documentação
- 🧪 Testes unitários
- 🎨 Templates de configuração

## 📜 Licença

MIT License - Uso livre para fins acadêmicos e comerciais.

## 🛠️ Stack Tecnológica

- **Python 3.8+**: Linguagem principal
- **Plotly**: Visualizações interativas
- **Matplotlib**: Gráficos estáticos profissionais
- **scikit-learn**: Machine learning e LDA
- **NLTK**: Processamento de linguagem natural
- **NetworkX**: Análise de redes
- **Pandas**: Manipulação de dados

## 📚 Documentação

- 📖 **README.md**: Este documento
- 🚀 **QUICK_START.md**: Início rápido
- 🔧 **INSTALLATION.md**: Guia de instalação
- 📋 **CONTEXT.md**: Contexto para desenvolvimento
- 🛠️ **DEVELOPMENT.md**: Guia técnico
- 🗺️ **ROADMAP.md**: Planejamento futuro

## 🆘 Troubleshooting

- 🔍 Consulte `INSTALLATION.md` para problemas de setup
- 🧪 Execute `python3 run_analysis.py --test-visuals` para validar
- 📊 Verifique logs em `projects/[nome]/output/`

## 💬 Suporte

- **Issues**: Reporte bugs e sugira melhorias
- **Discussions**: Perguntas e casos de uso
- **Wiki**: Documentação colaborativa

## ✅ Status

- 🟢 **V2.0**: Sistema completo e funcional
- 🟡 **V2.1**: Em desenvolvimento ativo
- 🔧 **Instalação**: Setup automatizado testado
- 📊 **Análise**: 9 análises funcionando
- 🎨 **Visualizações**: 8 gráficos automáticos
- ⚙️ **Configuração**: Sistema básico + avançado em desenvolvimento

---

🚀 **Transcript Analyzer V2.1** - Análise Qualitativa Profissional e Escalável

Desenvolvido com ❤️ para a comunidade de pesquisadores e analistas