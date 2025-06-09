import traceback
import sys
sys.path.append('.')

# Importar a classe correta
exec(open('run_analysis.py').read())

# Simular dados reais como chegam do AnalysisOrchestrator
mock_result = {
    'filename': 'test.txt',
    'global_metrics': {
        'global_sentiment': 0.0,
        'thematic_coherence': 0.71,
        'emotional_openness': 0.0
    },
    'word_frequencies': {'teste': 5, 'palavra': 3},
    'topics': [
        {'words': ['tech', 'ai'], 'label': 'Technology'},
        {'words': ['learn', 'study'], 'label': 'Education'}
    ],
    'topic_distribution': [0.6, 0.4],
    'concept_network': [
        {'word1': 'teste', 'word2': 'tech', 'weight': 3}
    ],
    'temporal_analysis': [
        {'segment': 1, 'sentiment': 0.1}
    ],
    'linguistic_patterns': {
        'hesitation_phrases': {'hmm': 2, 'err': 1},
        'total_hesitations': 3,
        'uncertainty_markers': {'count': 5},
        'certainty_markers': {'count': 10},
        'avg_sentence_length': 15.5
    },
    'contradictions': [
        {'score': 0.8, 'text1': 'good', 'text2': 'bad'}
    ]
}

# Testar cada seção individualmente
try:
    cli = TranscriptAnalyzerManager()
    print("🧪 Testando geração de markdown...")
    
    # Tentar gerar markdown
    content = cli._create_markdown_content(mock_result)
    print("✅ Markdown gerado com sucesso!")
    print(f"📄 Conteúdo: {len(content)} caracteres")
    
except Exception as e:
    print(f"❌ Erro específico: {e}")
    traceback.print_exc()
    
    # Mostrar linha exata do erro
    import linecache
    tb = traceback.extract_tb(e.__traceback__)
    for frame in tb:
        if 'run_analysis.py' in frame.filename:
            print(f"🎯 Erro na linha {frame.lineno}: {frame.line}")
            print(f"📄 Código: {linecache.getline(frame.filename, frame.lineno).strip()}")
