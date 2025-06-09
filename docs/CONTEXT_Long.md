# 🎯 Prompt de Contexto - Transcript Analyzer

## Contexto do Projeto

Estou desenvolvendo o **Transcript Analyzer V2.1**, um sistema de análise automatizada de transcrições qualitativas em Python. O repositório está em: https://github.com/mrlnlms/transcript-analyser

### Estado Atual
- **SISTEMA V2.1-beta COMPLETO!!! 🎉🎉🎉**
- **Base V2.0**: 9 análises + 8 gráficos funcionando perfeitamente
- **ConfigurationRegistry**: Sistema completo e funcionando
- **Relatórios Markdown**: Geração corrigida e testada
- **60 parâmetros configuráveis** em todos os analyzers
- **Projeto organizado**: Scripts movidos para pastas apropriadas

### Arquivos Principais (V2.1 Estruturada)
- `run_analysis.py` - Entry point único na raiz (~100 linhas)
- `core/managers/` - CLI, Project e Analysis managers
- `core/config/` - ConfigurationRegistry e config_loader
- `core/generators/` - MarkdownReportGenerator
- `core/engine/` - Orchestrators e core do sistema
- `core/visuals/` - Sistema de visualização completo
- `engine/analyzers/` - 9 analisadores plugáveis
- `visuals/charts/` - 8 gráficos plugáveis

## 🛠️ Estilo de Trabalho e Instruções

### Princípios de Desenvolvimento
1. **SEMPRE fazer backup antes de mudanças grandes**
2. **Testar cada mudança incrementalmente**
3. **Verificar código existente antes de propor mudanças**
4. **Atualizar documentação (artifacts) antes de commits**

### Contexto de Desenvolvimento
- Projeto em Python com workflows organizados por scripts Bash
- Scripts localizados em `./scripts/`, executados da raiz
- Diferentes scripts: análise, testes, limpeza
- Output vai para `./output/` com subpastas como `assets/`

### Scripts Principais
```bash
# Testes rápidos com dados mockados
./scripts/tests/teste_automatico.sh

# Workflow para transcrições reais
./scripts/maintenance/workflow_manual.sh  # Cria projeto, espera arquivos, analisa

# Limpeza de projetos
./scripts/maintenance/limpar_projetos.sh
```

### Padrões para Instruções

1. **Formato das instruções**
   - Use bloco `bash` para comandos de terminal
   - Use bloco `python` para código Python
   - Para alterações, indique linha e DE/PARA
   - Use `sed` para localizar/modificar automaticamente

2. **Exemplo de comando para localizar código**
   ```bash
   # Veja as linhas ao redor da 136
   sed -n '130,145p' run_analysis.py
   ```

3. **Estilo desejado**
   - Instruções diretas e passo a passo
   - Scripts de automação Bash quando a tarefa for complexa/repetitiva
   - Evite explicações longas: foco em ação rápida
   - Workflow replicável

4. **Quando automatizar com bash**
   - Se precisar adicionar mais de 20 linhas de código
   - Se precisar modificar múltiplos arquivos
   - Se a tarefa for repetitiva
   - Sempre perguntar antes: "Quer que eu crie um script para isso?"

5. **Para localizar trechos específicos no código**
   - Procure por trechos únicos usando: `**Procure por**:`
   - Indique onde adicionar usando: `**Adicione LOGO APÓS**:` ou `**Adicione ANTES**:`

### Ambiente
- macOS (Marlons-MacBook-Pro)
- Python via Homebrew (`/opt/homebrew/bin/python3`)
- Ambiente virtual em `transcript_env/`
- Usuário: mosx
- VSCode como editor principal

## 📁 Estrutura do Projeto V2.1

```
transcript-analyser/
├── run_analysis.py              # CLI principal (~100 linhas)
├── core/                        # Núcleo do sistema
│   ├── managers/               # Gerenciadores
│   ├── config/                 # ConfigurationRegistry (V2.1)
│   ├── generators/             # Geradores de relatório
│   ├── engine/                 # Orquestradores
│   └── visuals/                # Sistema de visualização
├── engine/
│   └── analyzers/              # 9 analisadores + base_analyzer
├── visuals/
│   └── charts/                 # 8 visualizações
├── scripts/                    # Scripts organizados
│   ├── tests/                  # Scripts de teste
│   ├── maintenance/            # Scripts de manutenção
│   └── development/            # Scripts de desenvolvimento
├── config/                     # Configurações JSON
├── resources/                  # Léxicos editáveis
├── projects/                   # Projetos de usuário
└── tests/
    └── mock_data/             # Dados mockados

```

## 📊 V2.1 - Sistema de Configuração

### Objetivo
Criar um sistema onde TODAS as configurações de TODOS os analyzers sejam:
- Descobertas automaticamente
- Configuráveis por perfil (academic, medical, interview)
- Ajustáveis por tamanho de texto (short, medium, long)
- Validadas automaticamente

### Status Atual (09/Jun/2025) - V2.1-beta COMPLETO! 🎉
- ✅ BaseAnalyzer criado com método abstrato `get_config_schema()`
- ✅ **TODOS os 9 analyzers com schemas implementados!**
- ✅ **60 parâmetros configuráveis no total**
- ✅ **ConfigurationRegistry com auto-descoberta implementado e funcionando**
- ✅ **Integração ConfigurationRegistry + AnalysisOrchestrator COMPLETA**
- ✅ **Sistema 100% testado e funcional**
- ⏳ Interface CLI de configuração (próxima fase)
- ⏳ CONFIG_MANUAL.md - Manual de configurações (próxima fase)

### Analyzers Existentes
1. `word_frequency.py` - ✅ Schema implementado
2. `temporal_analysis.py` - ✅ Schema implementado
3. `global_metrics.py` - ✅ Schema implementado
4. `linguistic_patterns.py` - ✅ Schema implementado
5. `concept_network.py` - ✅ Schema implementado
6. `topic_modeling.py` - ✅ Schema implementado
7. `contradiction_detection.py` - ✅ Schema implementado
8. `sentiment_analysis.py` - ✅ Schema implementado
9. `test_velocity.py` - ✅ Schema implementado

## 🎯 Próximos Passos V2.1

1. ~~**Implementar schemas nos analyzers restantes**~~ ✅ Implementado
2. ~~**Testar cada schema individualmente**~~ ✅ Implementado
3. **Implementar auto-descoberta no ConfigurationRegistry** ✅ Implementado
4. **Criar interface CLI para configuração** <- ESTAMOS AQUI
5. **Integrar com AnalysisOrchestrator** 

## ⚠️ Pontos de Atenção

- **SEMPRE FAZER BACKUP** antes de mudanças estruturais
- **Testar incrementalmente** - um analyzer por vez
- **Verificar imports** após mudanças na estrutura
- **Sistema V2.0 funcionando** - não quebrar funcionalidade existente
- **analysis_orchestrator.py** está em `engine/analyzers/` (não é um analyzer!)

## 🔧 Comandos Úteis para Debug

```bash
# Localizar trecho de código
grep -n "pattern" arquivo.py

# Ver contexto de uma linha
sed -n '130,145p' arquivo.py

# Encontrar onde função é chamada
grep -r "nome_funcao" . --include="*.py"

# Testar visualizações
python run_analysis.py --test-visuals

# Verificar schemas implementados
grep -l "get_config_schema" engine/analyzers/*.py

# Commit e push (macOS)
git add .
git commit -m "feat: descrição da mudança"
git push
```

---

**IMPORTANTE**: 
1. Sempre verificar código existente antes de propor mudanças
2. Fazer backup antes de mudanças estruturais
3. Atualizar artifacts (README, CONTEXT, etc) antes de commits
4. Testar cada mudança incrementalmente