# 🛠️ Guia de Desenvolvimento - Transcript Analyzer V2.1

## 📋 Estado do Desenvolvimento

### V2.1-beta: Sistema de Configuração Avançada
- **Data**: Junho 2025
- **Foco**: ConfigurationRegistry e schemas de configuração
- **Status**: Em desenvolvimento

### Progresso Atual (V2.1-beta COMPLETO! - 09/Jun/2025)
- [x] BaseAnalyzer com método abstrato `get_config_schema()`
- [x] **TODOS os 9 analyzers com schemas implementados!** ✅
  - [x] WordFrequencyAnalyzer (4 params)
  - [x] TemporalAnalysisAnalyzer (6 params)
  - [x] GlobalMetricsAnalyzer (6 params)
  - [x] LinguisticPatternsAnalyzer (6 params)
  - [x] ConceptNetworkAnalyzer (8 params)
  - [x] TopicModelingAnalyzer (8 params)
  - [x] ContradictionDetectionAnalyzer (8 params)
  - [x] SentimentAnalysisAnalyzer (8 params)
  - [x] TestVelocityAnalyzer (6 params)
- [x] **Total: 60 parâmetros configuráveis**
- [x] ConfigurationRegistry com auto-descoberta implementado
- [x] Integração com AnalysisOrchestrator
- [x] MarkdownReportGenerator corrigido e funcional
- [x] Sistema completamente testado
- [ ] Interface CLI de configuração
- [ ] Manual de configurações (CONFIG_MANUAL.md)

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios
```
transcript-analyser/
├── core/               # Núcleo do sistema
│   ├── config/        # ConfigurationRegistry (V2.1)
│   ├── engine/        # Orquestradores
│   ├── generators/    # Geradores de relatório
│   ├── managers/      # Gerenciadores (CLI, Project, Analysis)
│   └── visuals/       # Sistema de visualização
├── engine/            # Plugins de análise
│   └── analyzers/     # 9 analisadores + base + orchestrator
├── visuals/           # Plugins de visualização  
│   └── charts/        # 8 tipos de gráficos
└── scripts/           # Scripts organizados
    ├── development/   # Scripts para desenvolvimento
    ├── maintenance/   # Scripts de manutenção
    └── tests/        # Scripts de teste
```

### Sistema de Configuração (V2.1)

#### ConfigurationRegistry
```python
# core/config/configuration_registry.py
class ConfigurationRegistry:
    """Registro central de todas as configurações"""
    
    def __init__(self):
        self.analyzer_schemas = {}
        self.profiles = {}
        self._discover_schemas()
    
    def get_config_for_analyzer(analyzer_name, text_size, profile):
        """Retorna config ajustada para contexto"""
```

#### Schema de Configuração
```python
# Cada analyzer deve implementar:
@staticmethod
def get_config_schema():
    return {
        'param_name': {
            'type': 'int',              # int, float, bool, str, list
            'default': 10,              # valor padrão
            'range': [1, 100],          # para numéricos
            'options': ['a', 'b', 'c'], # para escolhas
            'short_text': 5,            # ajuste para texto curto
            'long_text': 20,            # ajuste para texto longo
            'academic': 15,             # ajuste para perfil acadêmico
            'description': 'Descrição'   # documentação
        }
    }
```

## 🔧 Workflow de Desenvolvimento

### 1. Antes de Começar
```bash
# Sempre fazer backup
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz core/ engine/ visuals/

# Ativar ambiente virtual
source transcript_env/bin/activate

# Verificar que tudo funciona
python run_analysis.py --test-visuals
```

### 2. Adicionando Schema a um Analyzer

#### Passo 1: Verificar analyzer atual
```bash
# Ver estrutura do analyzer
head -50 engine/analyzers/[nome_analyzer].py

# Verificar se já tem schema
grep "get_config_schema" engine/analyzers/[nome_analyzer].py
```

#### Passo 2: Adicionar método get_config_schema
```python
# Adicionar após a docstring da classe
@staticmethod
def get_config_schema():
    """Retorna o schema de configuração deste analyzer"""
    return {
        # Definir parâmetros configuráveis
    }
```

#### Passo 3: Testar schema
```bash
# Testar importação
python -c "
from engine.analyzers.[nome] import [NomeAnalyzer]
schema = [NomeAnalyzer].get_config_schema()
print('Schema:', schema)
"
```

### 3. Testando Mudanças

#### Teste Individual de Analyzer
```bash
# Testar analyzer específico
python -c "
from engine.analyzers.[nome] import [NomeAnalyzer]
analyzer = [NomeAnalyzer]()
# Testar com dados mock
"
```

#### Teste do Sistema Completo
```bash
# Teste automático com dados mockados
./scripts/tests/teste_automatico.sh

# Teste com arquivo real
./scripts/tests/teste_real_simples.sh
```

### 4. Commits e Documentação

#### Antes do Commit
1. Atualizar artifacts (README, CONTEXT, DEVELOPMENT)
2. Atualizar CHANGELOG.md
3. Verificar que testes passam
4. Fazer backup se mudança grande

#### Padrão de Commit
```bash
# feat: nova funcionalidade
git commit -m "feat: add config schema to [analyzer_name]"

# fix: correção
git commit -m "fix: correct schema validation in [component]"

# docs: documentação
git commit -m "docs: update development guide for V2.1"

# refactor: refatoração
git commit -m "refactor: simplify config discovery logic"
```

## 📊 Analyzers e Seus Parâmetros

### 1. WordFrequencyAnalyzer ✅
- `min_frequency`: Frequência mínima (1-10)
- `max_words`: Máximo de palavras (10-200)
- `use_stopwords`: Usar stopwords (bool)
- `stopwords_file`: Arquivo de stopwords

### 2. TemporalAnalysisAnalyzer ⏳
- `segments`: Número de segmentos
- `segment_method`: Método de segmentação
- `sentiment_lexicon`: Léxico emocional
- `smoothing`: Suavização

### 3. GlobalMetricsAnalyzer ⏳
- `metrics_to_calculate`: Lista de métricas
- `sentiment_threshold`: Limiar de sentimento
- `coherence_method`: Método de coerência

### 4. LinguisticPatternsAnalyzer ⏳
- `patterns_file`: Arquivo de padrões
- `min_pattern_frequency`: Frequência mínima
- `detect_hesitations`: Detectar hesitações
- `detect_certainty`: Detectar certeza

### 5. ConceptNetworkAnalyzer ⏳
- `window_size`: Janela de coocorrência
- `min_cooccurrence`: Coocorrências mínimas
- `max_connections`: Máximo de conexões
- `centrality_metric`: Métrica de centralidade

### 6. TopicModelingAnalyzer ⏳
- `n_topics`: Número de tópicos
- `method`: Algoritmo (lda, nmf, lsa)
- `n_words_per_topic`: Palavras por tópico
- `min_doc_frequency`: Frequência mínima

### 7. ContradictionDetectionAnalyzer ⏳
- `contradiction_threshold`: Limiar de detecção
- `negation_words`: Arquivo de negações
- `min_distance`: Distância mínima
- `semantic_analysis`: Análise semântica

### 8. SentimentAnalysisAnalyzer ⏳
- `lexicon_positive`: Léxico positivo
- `lexicon_negative`: Léxico negativo
- `compound_phrases`: Frases compostas
- `intensity_modifiers`: Modificadores

### 9. TestVelocityAnalyzer ⏳
- `test_mode`: Modo de teste
- `delay_seconds`: Delay simulado
- `mock_data`: Usar dados mock

## 🐛 Debugging

### Problemas Comuns

#### Import Error
```bash
# Verificar estrutura de imports
python -c "import sys; print('\n'.join(sys.path))"

# Verificar __init__.py
ls -la engine/analyzers/__init__.py
```

#### Schema não encontrado
```bash
# Verificar método implementado
grep -n "get_config_schema" engine/analyzers/[nome].py

# Verificar herança de BaseAnalyzer
grep -n "BaseAnalyzer" engine/analyzers/[nome].py
```

#### Configuração inválida
```python
# Testar validação
from core.config.configuration_registry import ConfigurationRegistry
registry = ConfigurationRegistry()
valid, errors = registry.validate_config('analyzer_name', config)
print(errors)
```

## 🚀 Próximas Etapas

### Fase 1: Schemas (atual)
1. Implementar schemas nos 8 analyzers restantes
2. Testar cada schema individualmente
3. Garantir consistência entre schemas

### Fase 2: Auto-descoberta
1. Implementar scanner no ConfigurationRegistry
2. Remover configurações hardcoded
3. Cache de schemas para performance

### Fase 3: Interface
1. CLI interativo para configuração
2. Visualização de todas as opções
3. Salvar/carregar perfis

### Fase 4: Integração
1. AnalysisOrchestrator usar configs
2. Ajustes automáticos funcionando
3. Validação em tempo real

### Fase 5: Documentação
1. CONFIG_MANUAL.md - Manual de uso das configurações
2. Exemplos práticos por perfil
3. Guia de customização
4. FAQ de configurações comuns

## 📝 Checklist de Qualidade

Antes de considerar uma tarefa completa:

- [ ] Código testado individualmente
- [ ] Sistema completo testado
- [ ] Documentação atualizada
- [ ] Artifacts atualizados
- [ ] CHANGELOG atualizado
- [ ] Sem quebrar funcionalidade existente
- [ ] Backup criado se mudança grande
- [ ] Commit com mensagem clara

## 🔗 Links Úteis

- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

**Última atualização**: 09/Jun/2025 - V2.1-beta em desenvolvimento