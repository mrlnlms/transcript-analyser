# 🚀 Transcript Analyzer V2.1 - Roadmap

## 📋 Visão Geral

A V2.0 focou em **modularização e orquestração**. A V2.1 focará em **configuração avançada e personalização**.

## 🎯 Objetivos Principais V2.1

### 1. Sistema de Configuração em Camadas
```
Global → Projeto → Análise → Texto
```

### 2. Interface de Configuração Unificada
- Dashboard web/CLI para configurar TODAS as análises
- Perfis pré-configurados (acadêmico, empresarial, médico, etc.)
- Ajuste automático baseado em características do texto

### 3. Análise Comparativa Avançada
- Implementar no novo sistema modular
- Comparações visuais lado a lado
- Métricas de similaridade/diferença

## 🔧 Arquitetura de Configuração Proposta

### ConfigurationManager
```python
class ConfigurationManager:
    def __init__(self):
        self.global_config = {}
        self.profiles = {}
        self.text_analyzers = {}
    
    def get_config_for_text(self, text_stats):
        """Retorna configuração otimizada baseada no texto"""
        # Texto curto vs longo
        # Domínio detectado
        # Complexidade linguística
        pass
```

### Estrutura de Configuração por Análise
```json
{
  "word_frequency": {
    "min_frequency": {
      "default": 2,
      "short_text": 1,
      "long_text": 5,
      "description": "Frequência mínima para considerar palavra relevante"
    },
    "stopwords": {
      "default": ["resources/stopwords_custom.txt"],
      "academic": ["resources/stopwords_academic.txt"],
      "medical": ["resources/stopwords_medical.txt"]
    },
    "max_words": {
      "default": 50,
      "range": [10, 200],
      "auto_adjust": true
    }
  },
  "temporal_analysis": {
    "segments": {
      "default": 10,
      "short_text": 5,
      "long_text": 20,
      "method": ["fixed", "dynamic", "sentence_based"]
    },
    "sentiment_lexicon": {
      "default": "general",
      "options": ["general", "academic", "business", "medical"]
    }
  }
}
```

## 📊 Casos de Uso

### 1. Texto Acadêmico Longo (Tese)
- word_frequency: min=10, stopwords acadêmicas
- temporal_analysis: 50 segmentos, análise por capítulos
- topic_modeling: 15 tópicos, hierarquia profunda

### 2. Entrevista Curta (10 min)
- word_frequency: min=1, todas as palavras importam
- temporal_analysis: 5 segmentos, análise minuto a minuto
- linguistic_patterns: foco em hesitações e mudanças

### 3. Relatório Médico
- Léxico especializado médico
- Detecção de termos técnicos
- Análise de consistência diagnóstica

## 🛠️ Implementação Proposta

### Fase 1: Configuration Registry (1 semana) 🎯
- [ ] Criar configuration_registry.py
- [ ] Implementar scanner de configurações
- [ ] Cada analyzer expor get_config_schema()
- [ ] Sistema de validação de configurações
- [ ] Cache de schemas para performance

### Arquitetura do ConfigurationRegistry
```python
class ConfigurationRegistry:
    """Registro central de todas as configurações disponíveis"""
    
    def __init__(self):
        self.analyzers = {}
        self.charts = {}
        self._scan_all_components()
    
    def _scan_all_components(self):
        """Varre analyzers e charts extraindo schemas"""
        # Auto-descoberta já existe, aproveitar!
        pass
    
    def get_consolidated_view(self) -> Dict:
        """Retorna visão unificada de TODAS as configs"""
        return {
            'analyzers': self.analyzers,
            'charts': self.charts,
            'profiles': self.profiles,
            'text_size_adjustments': self.get_size_rules()
        }
```

### Fase 2: UI de Configuração (2 semanas)
- [ ] CLI interativo para configuração
- [ ] Export/import de perfis
- [ ] Presets por domínio
- [ ] Documentação inline

### Fase 3: Análise Comparativa (1 semana)
- [ ] Implementar comparative_analysis.py
- [ ] Visualizações lado a lado
- [ ] Métricas de diferença
- [ ] Export comparativo

### Fase 4: Perfis Especializados (2 semanas)
- [ ] Perfil Acadêmico
- [ ] Perfil Empresarial
- [ ] Perfil Médico/Saúde
- [ ] Perfil Jornalístico

## 🎨 Interface de Configuração (Conceito)

```
🔧 CONFIGURAÇÃO DE ANÁLISE
========================

📊 Perfil Base: [Personalizado ▼]
📄 Tipo de Texto: [Entrevista ▼]
📏 Tamanho: 15.234 palavras (médio)

ANÁLISES DISPONÍVEIS:
--------------------
✅ Frequência de Palavras
   ├─ Frequência mínima: [2] (1-10)
   ├─ Máximo de palavras: [50] (10-200)
   └─ Stopwords: [✓] Padrão [✓] Domínio [ ] Custom

✅ Análise Temporal
   ├─ Segmentos: [AUTO] 15 detectados
   ├─ Método: [Dinâmico ▼]
   └─ Suavização: [✓] Ativada

✅ Modelagem de Tópicos
   ├─ Número de tópicos: [5] (2-20)
   ├─ Método: [LDA ▼]
   └─ Hierarquia: [✓] Gerar

[Salvar Perfil] [Aplicar] [Resetar]
```

## 📈 Benefícios Esperados

1. **Flexibilidade Total**: Cada análise ajustada ao contexto
2. **Resultados Mais Precisos**: Configurações otimizadas por tipo de texto
3. **Facilidade de Uso**: Perfis pré-configurados para começar rápido
4. **Extensibilidade**: Novos analisadores herdam sistema de config
5. **Reprodutibilidade**: Configs exportáveis/importáveis

## 🔍 Considerações Técnicas

### Auto-Ajuste Inteligente
```python
def auto_adjust_config(text_stats, base_config):
    # Tamanho do texto
    if text_stats['words'] < 500:
        config['temporal_analysis']['segments'] = 5
    elif text_stats['words'] > 10000:
        config['temporal_analysis']['segments'] = 50
    
    # Complexidade
    if text_stats['avg_sentence_length'] > 25:
        config['readability']['target'] = 'academic'
    
    return config
```

### Validação de Configurações
- Ranges permitidos por parâmetro
- Dependências entre configs
- Avisos de configurações incompatíveis

## 🚀 Próximos Passos

1. **Discussão**: Refinar conceitos e prioridades
2. **Prototipagem**: Configuration Manager básico
3. **Testes**: Com diferentes tipos de texto
4. **Iteração**: Baseado em feedback

## 💭 Questões para Discussão

1. Quais domínios/perfis são prioritários?
2. Interface web ou continuar com CLI?
3. Quanto de "mágica" vs controle manual?
4. Integração com Obsidian nesta fase?