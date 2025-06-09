"""🔍 Engine de análise principal"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


class TranscriptAnalyzer:
    """Analisador principal de transcrições"""
    
    def __init__(self, config, resource_manager):
        self.config = config
        self.resources = resource_manager
        print(f"✅ TranscriptAnalyzer inicializado para projeto: {config.project_name}")
    
    def analyze_transcript(self, file_path: Path) -> Dict[str, Any]:
        """Análise completa de uma transcrição"""
        
        print(f"🔍 Iniciando análise de: {file_path.name}")
        
        try:
            # Ler arquivo
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if not text.strip():
                raise ValueError("Arquivo vazio ou inválido")
            
            # TEMPORÁRIO: Usar dados mockados
            #from tests.mock_data import load_mock_result
            #result = load_mock_result(file_path.name)
            
            # TODO: Implementar análise real
            # ANÁLISE REAL (básica por enquanto)
            result = {
                'filename': file_path.name,
                'status': 'success',
                'global_metrics': {
                    'global_sentiment': 0.0,  # TODO: implementar
                    'thematic_coherence': 0.5,
                    'emotional_openness': 1.0,
                    'sentiment_variance': 0.2,
                    'total_hesitations': 0
                },
                'word_frequencies': self._count_word_frequencies(text),
                'temporal_analysis': [],  # TODO: implementar
                'phases': {},  # TODO: implementar
                'linguistic_patterns': {},  # TODO: implementar
                'topics': [],  # TODO: implementar
                'topic_distribution': [],
                'topic_hierarchy': {'nodes': [], 'edges': []},
                'contradictions': [],
                'concept_network': []
            }

            print(f"✅ Análise concluída: {file_path.name}")
            return result
            
        except Exception as e:
            print(f"❌ Erro na análise de {file_path.name}: {e}")
            raise

    def _count_word_frequencies(self, text: str) -> Dict[str, int]:
        """Conta frequência real das palavras"""
        from collections import Counter
        import re
        
        # Limpar e tokenizar
        text_lower = text.lower()
        # Remove pontuação e separa palavras
        words = re.findall(r'\b[a-záàâãéèêíïóôõöúçñ]+\b', text_lower)
        
        # Filtrar stopwords se disponível
        stopwords = set()
        if hasattr(self, 'resource_manager'):
            stopwords = set(self.resource_manager.get_stopwords())
        
        # Contar palavras significativas
        filtered_words = [w for w in words if len(w) > 3 and w not in stopwords]
        word_counts = Counter(filtered_words)
        
        # Retornar top 50 palavras
        return dict(word_counts.most_common(50))