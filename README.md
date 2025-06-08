# 🎯 Transcript Analyzer V2.0

## Sistema Profissional de Análise Automatizada de Entrevistas Qualitativas

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

---

## 🚀 **O que é o Transcript Analyzer V2?**

Sistema escalável e modular para análise automatizada de entrevistas qualitativas, desenvolvido para pesquisadores, analistas e profissionais que trabalham com dados textuais. Combina análise linguística, emocional e temática com visualizações interativas profissionais.

### ✨ **Principais Funcionalidades**

- 🔍 **Análise Multidimensional**: Sentimentos + Tópicos + Padrões Linguísticos + Redes Semânticas
- 📊 **3 Backends de Visualização**: Plotly (interativo) + Matplotlib (estático) + Text (fallback)
- ⚙️ **Configuração Externa**: JSON/TXT editáveis - zero edição de código
- 🚀 **CLI Profissional**: Interface completa de linha de comando
- 🎨 **Dashboard Inteligente**: Interpretações automáticas e métricas avançadas
- 🔄 **Análise Comparativa**: Compare múltiplos projetos simultaneamente

---

## 📊 **Exemplo de Resultados**

### **Métricas Globais Calculadas:**
- **😊 Sentimento Global**: +0.15 (levemente positivo)
- **🎯 Coerência Temática**: 0.72 (boa estrutura narrativa)
- **💭 Abertura Emocional**: 1.23 (expressivo)

### **Visualizações Geradas:**
- Timeline emocional interativa
- Rede de conceitos e coocorrências
- Análise de padrões linguísticos
- Hierarquia de tópicos com LDA
- Dashboard de métricas globais

---

## 🔧 **Instalação Rápida**

### **Opção 1: Setup Automatizado (Recomendado)**
```bash
# 1. Clone/baixe o projeto
git clone [url-do-repositorio]
cd transcript-analyser

# 2. Execute setup automático (detecta seu SO)
python3 setup_auto.py

# 3. Siga as instruções em QUICK_START.md
```

### **Opção 2: Instalação Manual**
```bash
# 1. Ambiente virtual
python3 -m venv transcript_env
source transcript_env/bin/activate  # Mac/Linux
# transcript_env\Scripts\activate   # Windows

# 2. Dependências testadas
pip install -r requirements_working.txt

# 3. Verificar instalação
python3 run_analysis.py --test-visuals
```

---

## 🎮 **Como Usar (Início Rápido)**

### **Após Reiniciar o Computador:**
```bash
# 1. Navegar para o projeto
cd Desktop/transcript-analyser

# 2. Ativar ambiente virtual
source transcript_env/bin/activate

# 3. Usar sistema normalmente
python3 run_analysis.py --list-projects
```

### **Comandos Principais:**
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

---

## 📁 **Estrutura do Projeto**

```
transcript-analyser/
├── 🚀 run_analysis.py              # CLI principal
├── ⚙️ config_loader.py             # Sistema de configuração
├── 🔧 setup_auto.py                # Setup automatizado
├── 📦 requirements_working.txt     # Dependências testadas
│
├── 📁 engine/                      # Módulos de análise
│   ├── analyzer_core.py            # Analisador principal
│   └── comparative_analyzer.py     # Análise comparativa
│
├── 📁 visuals/                     # Sistema de visualizações
│   ├── visualization_manager.py    # 3 backends escaláveis
│   └── dashboard_generator.py      # Gerador tradicional
│
├── 📁 projects/                    # Seus projetos de análise
│   └── nome_projeto/
│       ├── config_analise.json     # ⚙️ Configuração do projeto
│       ├── arquivos/               # 📄 Suas transcrições .txt
│       └── resultados/             # 📈 Outputs gerados
│
├── 📁 resources/                   # 📝 Léxicos editáveis
│   ├── stopwords_custom.txt
│   ├── emocionais_positivos.txt
│   ├── hesitacao_termos.txt
│   └── pesos_formula_linguistica.json
│
└── 📁 transcript_env/              # Ambiente virtual
```

---

## 🔧 **Configuração e Customização**

### **1. Configurações por Projeto (JSON)**
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

### **2. Léxicos Customizáveis (TXT)**
Edite arquivos em `resources/` para seu domínio:

```bash
# Adicionar termos específicos
echo "gamificação" >> resources/stopwords_custom.txt
echo "BNCC" >> resources/emocionais_positivos.txt

# Editar pesos das fórmulas
nano resources/pesos_formula_linguistica.json
```

### **3. Backends de Visualização**
```bash
# Escolher backend específico por projeto
# Em config_analise.json:
"visualizations": {
  "enabled_backends": ["plotly", "matplotlib"],
  "chart_types": {
    "timeline": {"backend": "plotly", "interactive": true}
  }
}
```

---

## 📊 **Tipos de Análise Realizadas**

### **🔍 Análise Linguística**
- Marcadores de hesitação e incerteza
- Modalizadores de certeza
- Complexidade das respostas
- Padrões discursivos

### **😊 Análise Emocional**
- Sentimento global e temporal
- Picos e vales emocionais
- Abertura emocional
- Trajetória narrativa

### **🎯 Análise Temática**
- Modelagem de tópicos com LDA
- Distribuição temática
- Coerência narrativa
- Hierarquia conceitual

### **🕸️ Análise de Redes**
- Coocorrência de conceitos
- Centralidade semântica
- Conexões entre ideias
- Mapeamento conceitual

---

## 📈 **Visualizações Geradas**

| Tipo | Backend | Formato | Descrição |
|------|---------|---------|-----------|
| **Timeline Emocional** | Plotly | HTML | Evolução temporal interativa |
| **Rede de Conceitos** | Plotly | HTML | Grafo semântico interativo |
| **Métricas Globais** | Matplotlib | PNG | Dashboard de indicadores |
| **Padrões Linguísticos** | Matplotlib | PNG | Análise de marcadores |
| **Hierarquia de Tópicos** | Matplotlib | PNG | Distribuição temática |
| **Relatório Completo** | Text | MD | Síntese narrativa |

---

## 🔄 **Fluxo de Trabalho Típico**

### **1. Setup Inicial (Uma vez)**
```bash
# Configurar ambiente
python3 setup_auto.py
source transcript_env/bin/activate
```

### **2. Novo Projeto**
```bash
# Criar projeto
python3 run_analysis.py --create-project educacao_2024

# Adicionar transcrições
cp entrevista1.txt projects/educacao_2024/arquivos/
cp entrevista2.txt projects/educacao_2024/arquivos/
```

### **3. Customizar (Opcional)**
```bash
# Editar léxicos para domínio educacional
nano resources/stopwords_custom.txt

# Ajustar configurações
nano projects/educacao_2024/config_analise.json
```

### **4. Executar Análise**
```bash
# Análise completa
python3 run_analysis.py --project educacao_2024

# Ver resultados
ls projects/educacao_2024/resultados/
```

### **5. Comparar Projetos**
```bash
# Análise comparativa
python3 run_analysis.py --compare educacao_2024 saude_2024
```

---

## 🛠️ **Arquitetura Técnica**

### **🏗️ Design Modular**
- **Engine**: Análise independente por módulos
- **Visuals**: Sistema escalável com múltiplos backends
- **Config**: Configuração externa hierárquica
- **Resources**: Léxicos e recursos dinâmicos

### **🎨 Sistema de Visualizações**
```python
# Fallback inteligente
Plotly (preferido) → Matplotlib → Text (sempre funciona)
```

### **⚙️ Configuração Hierárquica**
```
Global → Template → Projeto → Análise específica
```

### **🔧 CLI Profissional**
Interface completa com help contextual, validação de entrada e feedback detalhado.

---

## 📚 **Evolução do Projeto**

### **V1.0 → V2.0: Principais Melhorias**

#### **🔧 Arquitetura**
- ❌ V1: Código monolítico, configuração hardcoded
- ✅ V2: Modular, configuração externa, CLI profissional

#### **📊 Visualizações**
- ❌ V1: Matplotlib apenas, estático
- ✅ V2: 3 backends, interativo + estático + fallback

#### **⚙️ Configuração**
- ❌ V1: Editar código Python para mudanças
- ✅ V2: JSON/TXT externos, zero edição de código

#### **🚀 Instalação**
- ❌ V1: Setup manual complexo
- ✅ V2: Setup automatizado detecta SO

#### **📈 Análise**
- ❌ V1: Relatório simples em terminal
- ✅ V2: Dashboard + Markdown + Visualizações + Comparações

---

## 🎯 **Próximos Passos e Roadmap**

### **🔜 Funcionalidades Planejadas**
- [ ] **Interface Web**: Dashboard web interativo
- [ ] **API REST**: Integração com outros sistemas
- [ ] **ML Avançado**: Modelos de deep learning
- [ ] **Análise de Áudio**: Processamento direto de gravações
- [ ] **Colaboração**: Multi-usuário e versionamento
- [ ] **Templates**: Modelos por área (educação, saúde, etc.)

### **🏗️ Melhorias Técnicas**
- [ ] **Performance**: Processamento paralelo
- [ ] **Cache**: Sistema de cache inteligente
- [ ] **Plugins**: Arquitetura extensível
- [ ] **Docker**: Containerização completa
- [ ] **Cloud**: Deploy em AWS/Azure/GCP

### **📊 Análises Avançadas**
- [ ] **Análise de Discurso**: Marcadores pragmáticos
- [ ] **Detecção de Emoções**: ML para sentimentos
- [ ] **Análise Temporal**: Padrões longitudinais
- [ ] **Comparação Automática**: Clustering de entrevistas

---

## 🤝 **Contribuição e Comunidade**

### **Como Contribuir**
1. **Fork** o repositório
2. **Clone** localmente: `git clone [url]`
3. **Setup**: `python3 setup_auto.py`
4. **Desenvolva** sua funcionalidade
5. **Teste**: `python3 run_analysis.py --test-visuals`
6. **Pull Request** com descrição detalhada

### **Áreas de Contribuição**
- 🔍 **Novos tipos de análise**
- 📊 **Backends de visualização**
- 🌐 **Tradução e i18n**
- 📚 **Documentação**
- 🧪 **Testes unitários**
- 🎨 **Templates de configuração**

---

## 📝 **Licença e Créditos**

### **Licença**
MIT License - Uso livre para fins acadêmicos e comerciais.

### **Tecnologias Utilizadas**
- **Python 3.8+**: Linguagem principal
- **Plotly**: Visualizações interativas
- **Matplotlib**: Gráficos estáticos profissionais
- **scikit-learn**: Machine learning e LDA
- **NLTK**: Processamento de linguagem natural
- **NetworkX**: Análise de redes
- **Pandas**: Manipulação de dados

### **Inspiração**
Baseado em técnicas consolidadas de análise qualitativa, com foco na automação e escalabilidade para pesquisadores modernos.

---

## 📞 **Suporte e Contato**

### **Documentação**
- 📖 **README_V2.md**: Este documento
- 🚀 **QUICK_START.md**: Início rápido
- 🔧 **INSTALLATION.md**: Guia de instalação
- 📁 **PROJECT_STRUCTURE.md**: Estrutura detalhada

### **Resolução de Problemas**
- 🔍 Consulte `INSTALLATION.md` para problemas de setup
- 🧪 Execute `python3 run_analysis.py --test-visuals` para validar
- 📊 Verifique logs em `projects/[nome]/resultados/`

### **Comunidade**
- **Issues**: Reporte bugs e suggira melhorias
- **Discussions**: Perguntas e casos de uso
- **Wiki**: Documentação colaborativa

---

## 🎉 **Status do Projeto**

### ✅ **Sistema 100% Funcional**
- **🔧 Instalação**: Setup automatizado testado em macOS/Linux/Windows
- **📊 Análise**: Pipeline completo de processamento
- **🎨 Visualizações**: 3 backends funcionando perfeitamente
- **⚙️ Configuração**: Sistema flexível e escalável
- **📚 Documentação**: Guias completos e atualizados

### 🎯 **Pronto para Produção**
Sistema maduro, testado e documentado, pronto para uso em projetos reais de pesquisa e análise qualitativa.

---

**🚀 Transcript Analyzer V2.0 - Análise Qualitativa Profissional e Escalável**

*Desenvolvido com ❤️ para a comunidade de pesquisadores e analistas*