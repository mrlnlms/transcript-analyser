# Tutorial de Instalação e Uso - Transcript Analyzer

## 🚀 Instalação Inicial (Primeira vez)

### 1. Clone ou baixe o projeto
```bash
git clone [url-do-repositorio]
cd transcript-analyser
```

### 2. Crie o ambiente virtual Python
```bash
# No macOS/Linux:
python3 -m venv transcript_env

# No Windows:
python -m venv transcript_env
```

### 3. Ative o ambiente virtual
```bash
# No macOS/Linux:
source transcript_env/bin/activate

# No Windows:
transcript_env\Scripts\activate
```

**✅ Você saberá que funcionou quando ver `(transcript_env)` no início do terminal**

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Teste se está funcionando
```bash
python run_analysis.py --help
```

## 📝 Usando o Sistema

### 1. Criar um novo projeto
```bash
python run_analysis.py --create-project meu_estudo
```
Isso cria a estrutura:
```
projects/
└── meu_estudo/
    ├── arquivos/        ← COLOQUE SUAS TRANSCRIÇÕES .TXT AQUI
    ├── resultados/      ← RESULTADOS VÃO APARECER AQUI
    └── config_analise.json
```

### 2. Adicionar suas transcrições
```bash
# Copie seus arquivos .txt para a pasta arquivos
cp /caminho/da/entrevista.txt projects/meu_estudo/arquivos/

# OU crie um teste rápido:
echo "Texto da minha entrevista aqui" > projects/meu_estudo/arquivos/teste.txt
```

### 3. Rodar a análise
```bash
python run_analysis.py --project meu_estudo
```

### 4. Ver os resultados
```bash
# Listar o que foi gerado
ls projects/meu_estudo/output/

# Abrir o dashboard HTML no navegador (macOS)
open projects/meu_estudo/output/dashboard_analise.html

# Ou navegue manualmente para:
# Desktop/transcript-analyser/projects/meu_estudo/output/
```

## 📊 O que esperar como resultado?

Após rodar a análise, você encontrará em `projects/meu_estudo/output/`:

### Arquivos Gerados:
1. **dashboard_analise.html** - Relatório visual completo (abra no navegador!)
2. **emotional_timeline.html** - Timeline interativa de emoções
3. **topic_hierarchy.png** - Hierarquia de tópicos
4. **word_patterns.png** - Padrões linguísticos
5. **relatorio_completo.md** - Relatório em texto
6. **metricas_globais.json** - Dados brutos da análise

### Métricas que você verá:
- 😊 **Sentimento Global** (positivo/negativo/neutro)
- 📊 **Tópicos Principais** (descobertos automaticamente)
- 💭 **Padrões de Hesitação** (uhm, eh, tipo...)
- 🎯 **Coerência Temática** (0-1)
- ⏱️ **Timeline Emocional** (como sentimento varia)
- 🔤 **Frequência de Palavras**

## 🔄 Voltando ao Projeto (Dias depois)

### Sempre que voltar:
```bash
# 1. Entre na pasta
cd ~/Desktop/transcript-analyser

# 2. Ative o ambiente
source transcript_env/bin/activate

# 3. Use normalmente
python run_analysis.py --list-projects
```

## 🛠️ Sobre o setup_auto.py

O `setup_auto.py` faz TUDO automaticamente, mas você já fez manualmente. Ele seria útil:
- Na primeira instalação
- Se algo der errado
- Para outros usuários

```bash
# Se quiser usar no futuro:
python3 setup_auto.py
# Ele detecta seu SO e configura tudo
```

## 💡 Comandos Úteis

```bash
# Listar todos os projetos
python run_analysis.py --list-projects

# Testar visualizações
python run_analysis.py --test-visuals

# Comparar projetos
python run_analysis.py --compare projeto1 projeto2

# Analisar arquivo específico
python run_analysis.py --project meu_estudo --file entrevista1.txt
```

## ❗ Troubleshooting

### "command not found: python"
```bash
# Use python3 ao invés de python
python3 run_analysis.py --help
```

### "No such file or directory: transcript_env"
```bash
# Crie o ambiente primeiro
python3 -m venv transcript_env
```

### Ambiente não ativa
```bash
# Verifique se está na pasta certa
pwd  # Deve mostrar: /Users/[seu-user]/Desktop/transcript-analyser
```

## 📁 Estrutura de Pastas Explicada

```
transcript-analyser/
├── 🐍 transcript_env/       # Ambiente virtual (criado por você)
├── 📂 projects/             # SEUS PROJETOS FICAM AQUI
│   └── meu_estudo/
│       ├── arquivos/        # ← ENTRADA: Coloque .txt aqui
│       ├── resultados/      # ← SAÍDA: Resultados aparecem aqui
│       └── config.json      # Configurações do projeto
├── 🔧 engine/               # Motor de análise (não mexer)
├── 🎨 visuals/              # Sistema de visualização (não mexer)
├── 📚 resources/            # Dicionários e léxicos
└── 🚀 run_analysis.py       # Script principal
```

---

**Salve este tutorial!** É tudo que você precisa para usar o sistema 😄