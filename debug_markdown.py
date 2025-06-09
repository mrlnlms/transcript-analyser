import traceback
import sys
sys.path.append('.')

try:
    from run_analysis import TranscriptAnalyzerCLI
    
    # Simular dados como chegam na função
    mock_results = [
        {
            'global_metrics': {
                'thematic_coherence': 0.71,
                'global_sentiment': 0.0,
                'emotional_openness': 0.0
            },
            'filename': 'test.txt'
        }
    ]
    
    cli = TranscriptAnalyzerCLI()
    
    print("Tentando gerar markdown...")
    markdown = cli._create_markdown_content(mock_results[0])
    print("✅ Markdown gerado com sucesso!")
    
except Exception as e:
    print(f"❌ Erro encontrado: {e}")
    traceback.print_exc()
