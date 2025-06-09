# Workflow Completo - Transcript Analyzer

## 🚀 Início Rápido

### Ativar ambiente
```bash
cd ~/Desktop/transcript-analyser
source transcript_env/bin/activate
```

### Executar scripts (NOVA LOCALIZAÇÃO!)
```bash
# Scripts agora estão em scripts/
./scripts/teste_automatico.sh    # Teste com dados automáticos
./scripts/workflow_manual.sh      # Workflow com seus arquivos
./scripts/limpar_projetos.sh      # Limpar projetos
```

## 📋 Workflows Disponíveis

### 1. 🤖 Workflow Automatizado (Para Testes)

Use quando quiser testar rapidamente o sistema com dados de exemplo.

```bash
./scripts/teste_automatico.sh
```

**O que faz:**
- Limpa projetos de teste anteriores
- Cria 3 projetos com transcrições automáticas densas
- Executa análises em todos
- Compara os projetos
- Abre todos os resultados

**Projetos criados:**
- `teste_auto_individual` - 1 transcrição longa
- `teste_auto_dupla` - 2 transcrições médias  
- `teste_auto_trio` - 3 transcrições variadas

### 2. 📝 Workflow Manual (Para Suas Transcrições)

Use com suas transcrições reais.

```bash
./scripts/workflow_manual.sh
```

**O que faz:**
1. Pergunta nomes dos projetos
2. Cria estrutura
3. **Pausa** para você copiar arquivos
4. Analisa quando você confirmar
5. Oferece comparação
6. Abre resultados

---
Sobre nomenclatura das pastas
Você pode usar QUALQUER nome! Exemplos válidos:

projeto_individual ✅
entrevistas_professores_2024 ✅
grupo_A ✅
mestrado_coleta_1 ✅
pilot_study ✅

Evite apenas:

Espaços: meu projeto ❌ (use meu_projeto ✅)
Caracteres especiais: projeto#1 ❌
Acentos: análise_são_paulo ❌ (use analise_sao_paulo ✅)

---

**Fluxo interativo:**
```
📝 Digite o nome do projeto 1: estudo_professores
📝 Digite o nome do projeto 2: estudo_alunos
📝 Digite o nome do projeto 3: estudo_gestores

[Pausa para copiar arquivos]

📊 Deseja comparar os projetos? (s/n)
```

### 3. 🧹 Limpeza de Projetos

```bash
./scripts/limpar_projetos.sh
```

**Opções:**
- Listar e escolher projetos específicos
- Deletar todos com `todos`
- Interface interativa

## 📁 Criação Manual de Projetos

### Via comando
```bash
python run_analysis.py --create-project nome_projeto
```

### Estrutura criada
```
projects/
└── nome_projeto/
    ├── arquivos/         # ← Coloque .txt aqui
    ├── resultados/       # ← Resultados aparecem aqui
    └── config_analise.json
```

## 🔍 Análises Disponíveis

### Análise Individual
```bash
# Analisa todas transcrições de um projeto
python run_analysis.py --project nome_projeto

# Analisa arquivo específico
python run_analysis.py --project nome_projeto --file entrevista1.txt
```

### Análise Comparativa
```bash
# Compara múltiplos projetos
python run_analysis.py --compare projeto1 projeto2 projeto3
```

### Resultados gerados
- 📊 `metricas_globais.html` - Dashboard principal
- 📈 `timeline_emocional.html` - Evolução de sentimentos
- 🕸️ `rede_conceitos.html` - Conexões entre ideias
- 📝 `relatorio.md` - Relatório em texto

## 🎯 Comandos Úteis

### Básicos
```bash
# Listar todos os projetos
python run_analysis.py --list-projects

# Testar visualizações
python run_analysis.py --test-visuals

# Ver help
python run_analysis.py --help
```

### Abrir resultados
```bash
# Mac - abrir todos HTMLs
open projects/*/output/*/*.html

# Abrir projeto específico
open projects/nome_projeto/output/*/*.html

# Ver estrutura de resultados
ls -la projects/nome_projeto/output/
```

## 💡 Dicas Pro

### Aliases úteis
Adicione ao seu `.zshrc` ou `.bashrc`:
```bash
# Atalho para ativar ambiente
alias ta='cd ~/Desktop/transcript-analyser && source transcript_env/bin/activate'

# Atalho para scripts
alias ta-test='cd ~/Desktop/transcript-analyser && ./scripts/teste_automatico.sh'
alias ta-work='cd ~/Desktop/transcript-analyser && ./scripts/workflow_manual.sh'
alias ta-clean='cd ~/Desktop/transcript-analyser && ./scripts/limpar_projetos.sh'
```

Uso:
```bash
ta        # Ativa ambiente e entra na pasta
ta-test   # Roda teste automático
ta-work   # Roda workflow manual
ta-clean  # Limpa projetos
```

### Workflow rápido para múltiplas análises
```bash
# Criar vários projetos de uma vez
for i in {1..5}; do 
    python run_analysis.py --create-project "estudo_grupo_$i"
done

# Analisar todos de uma vez
for proj in projects/*/; do
    python run_analysis.py --project "$(basename "$proj")"
done
```

## 📊 Exemplos de Uso Real

### Pesquisa com grupos diferentes
```bash
# 1. Criar projetos por grupo
python run_analysis.py --create-project grupo_controle
python run_analysis.py --create-project grupo_experimental

# 2. Adicionar transcrições
# Copie arquivos .txt para projects/grupo_*/arquivos/

# 3. Analisar cada grupo
python run_analysis.py --project grupo_controle
python run_analysis.py --project grupo_experimental

# 4. Comparar grupos
python run_analysis.py --compare grupo_controle grupo_experimental
```

### Análise longitudinal
```bash
# Projetos por período
python run_analysis.py --create-project fase1_janeiro
python run_analysis.py --create-project fase2_junho
python run_analysis.py --create-project fase3_dezembro

# Após análises individuais, comparar evolução
python run_analysis.py --compare fase1_janeiro fase2_junho fase3_dezembro
```

## 🛠️ Solução de Problemas

### Scripts não executam
```bash
# Dar permissão
chmod +x scripts/*.sh

# Verificar se está na pasta certa
pwd  # Deve mostrar: .../transcript-analyser
```

### Ambiente não ativa
```bash
# Recriar ambiente
python3 -m venv transcript_env
source transcript_env/bin/activate
pip install -r requirements.txt
```

### Falta de memória em análises grandes
```bash
# Analisar arquivos individualmente
python run_analysis.py --project grande --file parte1.txt
python run_analysis.py --project grande --file parte2.txt
```

## 📈 Interpretando Resultados

### Métricas principais
- **Sentimento**: -1 (negativo) a +1 (positivo)
- **Coerência**: 0 a 1 (consistência temática)
- **Abertura**: Expressividade emocional

### Visualizações
- **Timeline**: Evolução temporal dos sentimentos
- **Rede**: Conexões entre conceitos
- **Tópicos**: Temas emergentes via LDA

## 🚀 Próximos Passos

1. **Explorar configurações**
   ```bash
   nano projects/seu_projeto/config_analise.json
   ```

2. **Customizar léxicos**
   ```bash
   nano resources/stopwords_custom.txt
   nano resources/emocionais_positivos.txt
   ```

3. **Integrar com Obsidian** (em desenvolvimento)

---

💡 **Lembre-se**: Sempre ative o ambiente virtual antes de usar o sistema!


