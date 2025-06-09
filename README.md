# 🎙️ Transcript Analyzer V2.0

Sistema escalável e modular para análise automatizada de entrevistas qualitativas, desenvolvido para pesquisadores, analistas e profissionais que trabalham com dados textuais.

## ⚠️ Nota Importante

**Versão atual usa dados simulados para demonstração**. A implementação completa da análise real (sentimentos via NLTK, LDA para tópicos, etc.) está em desenvolvimento. Os gráficos e estrutura estão funcionais para testes e desenvolvimento.

- 🔍 **Análise Multidimensional**: Sentimentos, tópicos, padrões linguísticos e redes semânticas
- 📊 **Visualizações Interativas**: HTML com Plotly, gráficos estáticos com Matplotlib
- ⚙️ **Configuração Externa**: JSON editável sem tocar no código
- 🚀 **CLI Profissional**: Interface completa de linha de comando
- 🎯 **Análise Comparativa**: Compare múltiplos projetos simultaneamente

## 🚀 Instalação Rápida

### Requisitos
- Python 3.8+
- macOS, Linux ou Windows

### Setup Automático
```bash
# Clone o repositório
git clone https://github.com/mrlnlms/transcript-analyser.git
cd transcript-analyser

# Execute o setup automático
python3 setup_auto.py
```

### Setup Manual
```bash
# 1. Crie ambiente virtual
python3 -m venv transcript_env

# 2. Ative o ambiente
source transcript_env/bin/activate  # Mac/Linux
# ou
transcript_env\Scripts\activate     # Windows

# 3. Instale dependências
pip install -r requirements.txt
```

## 📖 Uso Básico

### 1. Criar um Projeto
```bash
python run_analysis.py --create-project meu_estudo
```

### 2. Adicionar Transcrições
Copie seus arquivos `.txt` para:
```
projects/meu_estudo/arquivos/
```

### 3. Executar Análise
```bash
python run_analysis.py --project meu_estudo
```

### 4. Ver Resultados
Os resultados estarão em:
```
projects/meu_estudo/output/
```
Abra os arquivos `.html` no navegador para visualizações interativas!

## 📚 Documentação Completa

- 📋 [Guia de Instalação](docs/INSTALLATION.md)
- 🎯 [Tutorial de Uso](docs/TUTORIAL.md)
- 🔧 [Configuração Avançada](docs/CONFIGURATION.md)
- 📊 [Exemplos de Análise](docs/EXAMPLES.md)
- 🛠️ [Scripts Auxiliares](scripts/README.md)

## 🏗️ Estrutura do Projeto

```
transcript-analyser/
├── 📂 engine/              # Motor de análise
│   ├── analyzer_core.py    # Analisador principal
│   └── comparative_analyzer.py # Análise comparativa
├── 📂 visuals/             # Sistema de visualizações
│   ├── visualization_manager.py # Gerenciador de backends
│   └── plotly_backend.py   # Visualizações interativas
├── 📂 projects/            # Seus projetos de análise
│   └── meu_projeto/
│       ├── arquivos/       # Suas transcrições .txt
│       ├── output/         # Resultados gerados
│       └── config.json     # Configurações
├── 📂 resources/           # Léxicos e dicionários
├── 📂 docs/               # Documentação
├── 📂 scripts/            # Scripts auxiliares
│   ├── teste_automatico.sh
│   ├── workflow_manual.sh
│   └── limpar_projetos.sh
├── 🚀 run_analysis.py     # Script principal
└── ⚙️ config_loader.py    # Sistema de configuração
```

## 🎮 Comandos Disponíveis

```bash
# Listar projetos
python run_analysis.py --list-projects

# Criar projeto
python run_analysis.py --create-project nome

# Analisar projeto
python run_analysis.py --project nome

# Comparar projetos
python run_analysis.py --compare proj1 proj2 proj3

# Testar visualizações
python run_analysis.py --test-visuals
```

## 📊 Tipos de Análise

### Análise Individual
- Timeline emocional
- Modelagem de tópicos (LDA)
- Padrões linguísticos
- Métricas de sentimento

### Análise Comparativa
- Comparação entre projetos
- Evolução temática
- Diferenças de sentimento
- Padrões cross-projeto

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Changelog

### v2.0.2 (Janeiro 2025)
- ✅ Reorganização da estrutura de output (resultados → output)
- ✅ Adição de suporte para pasta assets
- ✅ Scripts movidos para pasta dedicada
- ✅ Melhorias na documentação

### v2.0.1 (Janeiro 2025)
- ✅ Correção de bug na extensão de arquivos HTML
- ✅ Melhorias na documentação
- ✅ Adição de scripts auxiliares
- ✅ Organização da estrutura de arquivos

### v2.0.0
- 🎉 Lançamento inicial da versão modular
- 📊 Sistema de visualização com múltiplos backends
- ⚙️ Configuração externa via JSON
- 🚀 CLI profissional

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Marlon** - *Desenvolvimento principal* - [@mrlnlms](https://github.com/mrlnlms)

## 🙏 Agradecimentos

- Comunidade de pesquisa qualitativa
- Contribuidores e testers
- Ferramentas open source utilizadas