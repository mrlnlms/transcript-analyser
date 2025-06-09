#!/usr/bin/env python3
"""Testa todos os schemas implementados"""

import sys
import os
sys.path.append('.')

# Importar cada analyzer individualmente
from engine.analyzers.word_frequency import WordFrequencyAnalyzer
from engine.analyzers.temporal_analysis import TemporalAnalysisAnalyzer
from engine.analyzers.global_metrics import GlobalMetricsAnalyzer
from engine.analyzers.linguistic_patterns import LinguisticPatternsAnalyzer
from engine.analyzers.concept_network import ConceptNetworkAnalyzer
from engine.analyzers.topic_modeling import TopicModelingAnalyzer
from engine.analyzers.contradiction_detection import ContradictionDetectionAnalyzer
from engine.analyzers.sentiment_analysis import SentimentAnalysisAnalyzer
from engine.analyzers.test_velocity import TestVelocityAnalyzer

analyzers = [
    WordFrequencyAnalyzer,
    TemporalAnalysisAnalyzer,
    GlobalMetricsAnalyzer,
    LinguisticPatternsAnalyzer,
    ConceptNetworkAnalyzer,
    TopicModelingAnalyzer,
    ContradictionDetectionAnalyzer,
    SentimentAnalysisAnalyzer,
    TestVelocityAnalyzer
]

print("🧪 TESTANDO TODOS OS SCHEMAS\n")
print("=" * 60)

total_params = 0
all_valid = True

for analyzer_class in analyzers:
    analyzer_name = analyzer_class.__name__
    print(f"\n📊 {analyzer_name}:")
    
    try:
        # Testar get_config_schema
        schema = analyzer_class.get_config_schema()
        param_count = len(schema)
        total_params += param_count
        
        print(f"  ✅ Schema OK - {param_count} parâmetros")
        
        # Testar get_default_config
        config = analyzer_class.get_default_config()
        print(f"  ✅ Default config OK - {len(config)} valores")
        
        # Verificar se todos os parâmetros têm default
        for param in schema:
            if param not in config:
                print(f"  ⚠️  Parâmetro '{param}' sem valor default!")
                all_valid = False
                
        # Mostrar alguns parâmetros
        params_list = list(schema.keys())[:3]
        print(f"  📋 Parâmetros: {params_list}...")
        
    except Exception as e:
        print(f"  ❌ ERRO: {e}")
        all_valid = False

print("\n" + "=" * 60)
print(f"\n📈 RESUMO FINAL:")
print(f"  - Total de analyzers: {len(analyzers)}")
print(f"  - Total de parâmetros: {total_params}")
print(f"  - Status: {'✅ TUDO OK!' if all_valid else '❌ Alguns problemas encontrados'}")
