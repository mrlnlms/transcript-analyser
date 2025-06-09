# 🔍 Transcript Analyzer V2.0

Sistema escalável e modular para análise automatizada de entrevistas qualitativas, desenvolvido para pesquisadores, analistas e profissionais que trabalham com dados textuais. Combina análise linguística, emocional e temática com visualizações interativas profissionais.

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

### Visualizações Disponíveis (8 tipos)

- Timeline emocional interativa com sentimento real
- Rede de conceitos e coocorrências extraída do texto
- Word cloud de termos frequentes (HTML interativo)
- Top 10 palavras por frequência real
- Análise de padrões linguísticos detectados
- Hierarquia de tópicos categorizados
- Análise de contradições (implementada)
- Dashboard de métricas globais calculadas

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

O projeto inclui scripts bash para facilitar o workflow:

### Scripts de Teste

#### `teste_automatico.sh`
Executa teste completo com dados mockados/densos:
```bash
./scripts/teste_automatico.sh      # Executa sem abrir resultados
./scripts/teste_automatico.sh yes  # Executa e abre imagem comparativa
```
- Limpa projetos anteriores (teste_auto_*)
- Cria 3 projetos com 1, 2 e 3 arquivos
- Gera análise individual e comparativa
- Remove comparações antigas (*_test)

#### `teste_real_simples.sh`
Teste rápido com arquivo real:
```bash
./scripts/teste_real_simples.sh
```
- Limpa testes anteriores (teste_real_*)
- Cria projeto único
- Abre Finder para adicionar arquivo .txt
- Executa análise e abre resultados

### Scripts de Produção

#### `workflow_manual.sh`
Workflow completo para análise real:
```bash
./scripts/workflow_manual.sh
```
- Solicita nomes de 3 projetos
- Cria estrutura e aguarda arquivos
- Executa análise individual
- Opção de análise comparativa

### Scripts de Manutenção

#### `limpar_projetos.sh`
Limpeza básica de projetos:
```bash
./scripts/limpar_projetos.sh
```

#### `limpar_completo.sh`
Limpeza inteligente com opções:
```bash
./scripts/limpar_completo.sh
```
- Menu interativo
- Opções: teste apenas, teste+comparações, tudo, seletivo
- Mostra espaço a ser liberado
- Confirmação para operações destrutivas

## 💻 Uso Diário

### Ativação do Ambiente

```bash
# 1. Navegar para o projeto
cd Desktop/transcript-analyser

# 2. Ativar ambiente virtual
source transcript_env/bin/activate

# 3. Usar sistema normalmente
python3 run_analysis.py --list-projects
```

### Comandos Principais

```bash
# Listar projetos disponíveis
python3 run_analysis.py --list-projects

# Criar novo projeto
python3 run_analysis.py --create-project meu_projeto

# Executar análise
python3 run_analysis.py --project meu_projeto

# Análise comparativa
python3 run_analysis.py --compare projeto1 projeto2 projeto3

# Testar visualizações
python3 run_analysis.py --test-visuals
```

## 📁 Estrutura do Projeto

```
transcript-analyser/
├── 🚀 run_analysis.py          # CLI principal
├── ⚙️ config_loader.py         # Sistema de configuração
├── 🔧 setup_auto.py           # Setup automatizado
├── 📦 requirements.txt        # Dependências
│
├── 📁 engine/                 # Módulos de análise
│   ├── analyzer_core.py       # Analisador principal
│   └── comparative_analyzer.py # Análise comparativa
│
├── 📁 visuals/               # Sistema de visualizações
│   ├── visualization_manager.py # 3 backends escaláveis
│   └── dashboard_generator.py   # Gerador tradicional
│
├── 📁 projects/              # Seus projetos de análise
│   └── nome_projeto/
│       ├── config_analise.json  # ⚙️ Configuração do projeto
│       ├── arquivos/           # 📄 Suas transcrições .txt
│       └── output/            # 📈 Outputs gerados
│           └── assets/        # 🖼️ Imagens e recursos
│
├── 📁 resources/             # 📝 Léxicos editáveis
│   ├── stopwords_custom.txt
│   ├── emocionais_positivos.txt
│   ├── hesitacao_termos.txt
│   └── pesos_formula_linguistica.json
│
├── 📁 scripts/               # 🛠️ Scripts auxiliares
│   ├── teste_automatico.sh
│   ├── workflow_manual.sh
│   └── limpar_projetos.sh
│
└── 📁 transcript_env/        # Ambiente virtual Python
```

## ⚙️ Configuração

### Configuração do Projeto

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

### Sistema de Visualizações

```json
# Escolher backend específico por projeto
# Em config_analise.json:
"visualizations": {
    "enabled_backends": ["plotly", "matplotlib"],
    "chart_types": {
        "timeline": {"backend": "plotly", "interactive": true}
    }
}
```

## 📊 Análises Disponíveis

### 1. Análise Linguística
- Marcadores de hesitação e incerteza
- Modalizadores de certeza
- Complexidade das respostas
- Padrões discursivos

### 2. Análise Emocional
- Sentimento global e temporal
- Picos e vales emocionais
- Abertura emocional
- Trajetória narrativa

### 3. Análise Temática
- Modelagem de tópicos com LDA
- Distribuição temática
- Coerência narrativa
- Hierarquia conceitual

### 4. Análise de Redes
- Coocorrência de conceitos
- Centralidade semântica
- Conexões entre ideias
- Mapeamento conceitual

## 🎨 Tipos de Visualização

| Tipo | Backend | Formato | Descrição |
|------|---------|---------|-----------|
| Timeline Emocional | Plotly | HTML | Evolução temporal interativa |
| Rede de Conceitos | Plotly | HTML | Grafo semântico interativo |
| Métricas Globais | Matplotlib | PNG | Dashboard de indicadores |
| Padrões Linguísticos | Matplotlib | PNG | Análise de marcadores |
| Hierarquia de Tópicos | Matplotlib | PNG | Distribuição temática |
| Relatório Completo | Text | MD | Síntese narrativa |

## 📝 Exemplo de Workflow Completo

```bash
# Configurar ambiente
python3 setup_auto.py
source transcript_env/bin/activate

# Criar projeto
python3 run_analysis.py --create-project educacao_2024

# Adicionar transcrições
cp entrevista1.txt projects/educacao_2024/arquivos/
cp entrevista2.txt projects/educacao_2024/arquivos/

# Editar léxicos para domínio educacional
nano resources/stopwords_custom.txt

# Ajustar configurações
nano projects/educacao_2024/config_analise.json

# Análise completa
python3 run_analysis.py --project educacao_2024

# Ver resultados
ls projects/educacao_2024/output/

# Análise comparativa
python3 run_analysis.py --compare educacao_2024 saude_2024
```

## 🏗️ Arquitetura

### Análises Implementadas (100% Real)
- **Contagem de Palavras**: Frequências reais com filtro de stopwords
- **Análise Temporal**: Divisão em segmentos com evolução de sentimento
- **Padrões Linguísticos**: Detecção de hesitações, certeza/incerteza
- **Rede de Conceitos**: Coocorrência de palavras em sentenças
- **Categorização de Tópicos**: Agrupamento por palavras-chave temáticas
- **Métricas Globais**: Sentimento, coerência e abertura emocional  
- **Detecção de Contradições**: Padrões linguísticos e negações detectadas

### Princípios de Design
- **Engine**: Análise independente por módulos
- **Visuals**: Sistema escalável com múltiplos backends
- **Config**: Configuração externa hierárquica
- **Resources**: Léxicos e recursos dinâmicos

### Sistema de Fallback
```
# Fallback inteligente
Plotly (preferido) → Matplotlib → Text (sempre funciona)
```

### Hierarquia de Configuração
```
Global → Template → Projeto → Análise específica
```

### CLI Profissional
Interface completa com help contextual, validação de entrada e feedback detalhado.

## 📈 Evolução do Sistema

### V1 → V2

#### Estrutura
- ❌ V1: Código monolítico, configuração hardcoded
- ✅ V2: Modular, configuração externa, CLI profissional

#### Visualizações
- ❌ V1: Matplotlib apenas, estático
- ✅ V2: 3 backends, interativo + estático + fallback

#### Usabilidade
- ❌ V1: Editar código Python para mudanças
- ✅ V2: JSON/TXT externos, zero edição de código

#### Setup
- ❌ V1: Setup manual complexo
- ✅ V2: Setup automatizado detecta SO

#### Output
- ❌ V1: Relatório simples em terminal
- ✅ V2: Dashboard + Markdown + Visualizações + Comparações

## 🔮 Roadmap

### Curto Prazo
- Interface Web: Dashboard web interativo
- API REST: Integração com outros sistemas
- ML Avançado: Modelos de deep learning
- Análise de Áudio: Processamento direto de gravações

### Médio Prazo
- Colaboração: Multi-usuário e versionamento
- Templates: Modelos por área (educação, saúde, etc.)
- Performance: Processamento paralelo
- Cache: Sistema de cache inteligente

### Longo Prazo
- Plugins: Arquitetura extensível
- Docker: Containerização completa
- Cloud: Deploy em AWS/Azure/GCP
- Análise de Discurso: Marcadores pragmáticos
- Detecção de Emoções: ML para sentimentos
- Análise Temporal: Padrões longitudinais
- Comparação Automática: Clustering de entrevistas

## 🤝 Contribuindo

1. Fork o repositório
2. Clone localmente: `git clone [url]`
3. Setup: `python3 setup_auto.py`
4. Desenvolva sua funcionalidade
5. Teste: `python3 run_analysis.py --test-visuals`
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

## 🎯 Casos de Uso

Baseado em técnicas consolidadas de análise qualitativa, com foco na automação e escalabilidade para pesquisadores modernos.

## 📚 Documentação

- 📖 **README.md**: Este documento
- 🚀 **QUICK_START.md**: Início rápido
- 🔧 **INSTALLATION.md**: Guia de instalação
- 📁 **PROJECT_STRUCTURE.md**: Estrutura detalhada
- 📋 **STATUS.md**: Estado atual do desenvolvimento

## 🆘 Troubleshooting

- 🔍 Consulte `INSTALLATION.md` para problemas de setup
- 🧪 Execute `python3 run_analysis.py --test-visuals` para validar
- 📊 Verifique logs em `projects/[nome]/output/`

## 💬 Suporte

- **Issues**: Reporte bugs e suggira melhorias
- **Discussions**: Perguntas e casos de uso
- **Wiki**: Documentação colaborativa

## ✅ Status

- 🔧 **Instalação**: Setup automatizado testado em macOS/Linux/Windows
- 📊 **Análise**: Pipeline completo de processamento
- 🎨 **Visualizações**: 3 backends funcionando perfeitamente
- ⚙️ **Configuração**: Sistema flexível e escalável
- 📚 **Documentação**: Guias completos e atualizados

Sistema maduro, testado e documentado, pronto para uso em projetos reais de pesquisa e análise qualitativa.

---

🚀 **Transcript Analyzer V2.0** - Análise Qualitativa Profissional e Escalável

Desenvolvido com ❤️ para a comunidade de pesquisadores e analistas