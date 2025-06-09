# 🚀 Guia de Instalação - Transcript Analyzer

Sistema profissional para análise automatizada de entrevistas qualitativas.

## ⚡ Instalação Rápida (Recomendada)

### 1️⃣ **Setup Automatizado**
```bash
# Clone o repositório
git clone [url-do-repositorio]
cd transcript-analyser

# Execute setup automático (detecta seu SO)
python3 setup_auto.py

# Siga as instruções em QUICK_START.md
```

## 🔧 Instalação Manual

### **Para macOS** 🍎
```bash
# 1. Ambiente virtual
python3 -m venv transcript_env
source transcript_env/bin/activate

# 2. Dependências (ordem importante!)
pip install --upgrade pip
pip install --only-binary=all numpy scipy scikit-learn
pip install matplotlib seaborn plotly networkx wordcloud pandas nltk textblob tqdm pyyaml pathlib2

# 3. Testar
python3 run_analysis.py --test-visuals
```

### **Para Windows** 🪟
```bash
# 1. Ambiente virtual
python -m venv transcript_env
transcript_env\Scripts\activate

# 2. Dependências
pip install -r requirements.txt

# 3. Testar
python run_analysis.py --test-visuals
```

### **Para Linux** 🐧
```bash
# 1. Ambiente virtual
python3 -m venv transcript_env
source transcript_env/bin/activate

# 2. Dependências
pip install -r requirements.txt

# 3. Testar
python3 run_analysis.py --test-visuals
```

## ✅ Verificação da Instalação

### **Teste Básico:**
```bash
python3 -c "import pandas, numpy, matplotlib, seaborn, plotly, networkx, wordcloud, nltk, textblob, sklearn; print('✅ TUDO OK!')"
```

### **Teste Completo:**
```bash
# Listar projetos
python3 run_analysis.py --list-projects

# Testar visualizações
python3 run_analysis.py --test-visuals

# Análise de exemplo
python3 run_analysis.py --project exemplo_docentes
```

## 🎯 O que está incluído

### ✅ **Funcionalidades Garantidas:**
- **3 Backends de Visualização**: Plotly (interativo) + Matplotlib (estático) + Text (fallback)
- **Análise Completa**: Sentimentos, tópicos, redes semânticas, timelines
- **Configuração Flexível**: JSON externos para todos os parâmetros
- **Léxicos Editáveis**: Stopwords, marcadores emocionais, etc.
- **CLI Profissional**: Interface de linha de comando completa

### ⚠️ **Dependências Opcionais (podem falhar):**
- **gensim**: Topic modeling avançado
- **spacy**: NLP avançado  
- **torch/transformers**: Deep learning

> **Nota**: O sistema funciona perfeitamente sem as dependências opcionais!

## 🐛 Resolução de Problemas

### **Erro: "No module named matplotlib"**
```bash
# Instalar dependências básicas
pip install matplotlib pandas numpy seaborn plotly
```

### **Erro de compilação (Mac)**
```bash
# Usar versões pré-compiladas
pip install --only-binary=all numpy scipy scikit-learn
```

### **Erro: "command not found: python"**
```bash
# Usar python3 no Mac/Linux
python3 run_analysis.py --list-projects
```

### **Ambiente virtual não ativa**
```bash
# Mac/Linux
source transcript_env/bin/activate

# Windows
transcript_env\Scripts\activate
```

## 📊 Backends de Visualização

| Backend | Tipo | Formato | Quando Usar |
|---------|------|---------|-------------|
| **Plotly** | Interativo | HTML | Exploração, apresentações |
| **Matplotlib** | Estático | PNG/PDF | Publicações, relatórios |
| **Text** | Fallback | TXT | Quando gráficos falham |

## 🎮 Primeiros Passos

```bash
# 1. Ativar ambiente
source transcript_env/bin/activate

# 2. Criar projeto
python3 run_analysis.py --create-project meu_teste

# 3. Adicionar arquivo .txt
# Copie um arquivo de transcrição para:
# projects/meu_teste/arquivos/entrevista.txt

# 4. Executar análise
python3 run_analysis.py --project meu_teste

# 5. Ver resultados
# Resultados em: projects/meu_teste/output/
```

## 🔄 Atualizações Futuras

```bash
# Puxar updates do repo
git pull origin main

# Atualizar dependências se necessário
pip install -r requirements.txt --upgrade
```

---

## 💡 Dicas de Performance

- **Use ambiente virtual sempre** para evitar conflitos
- **Plotly** é melhor para análise interativa
- **Matplotlib** é melhor para relatórios finais
- **Text backend** funciona sempre como fallback
- **Configurações JSON** permitem customizar tudo sem tocar código

---

🎯 **Instalação testada e funcionando em macOS 14+ com Python 3.8+**


----


🎯 RESUMO - Como deixar o processo automático:
🔄 Para você (próximas vezes):

✅ Só ativar ambiente: source transcript_env/bin/activate
✅ Usar requirements.txt: Dependências testadas
✅ Zero configuração: Tudo já funciona

👥 Para outros (fork/clone):

🚀 setup_auto.py: Detecta SO e instala automaticamente
📚 INSTALLATION.md: Guia completo step-by-step
⚡ requirements.txt: Só dependências que funcionam

📋 Arquivos para criar no repo:

setup_auto.py → Setup automatizado
requirements.txt → Dependências testadas
INSTALLATION.md → Guia completo
QUICK_START.md → Início rápido

✅ Status Final:

🎉 Sistema 100% funcional
📊 3 backends de visualização
🔧 Setup automatizado criado
📚 Documentação completa

Agora qualquer pessoa pode usar o sistema só executando python3 setup_auto.py! 🚀
Quer que eu ajude a implementar alguma funcionalidade específica agora que está tudo funcionando?