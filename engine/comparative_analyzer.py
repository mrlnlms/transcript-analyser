"""🔄 Analisador comparativo entre projetos"""

from typing import Dict, List, Any


class ComparativeAnalyzer:
    """Análise comparativa entre múltiplos projetos"""
    
    def __init__(self):
        print("🔄 ComparativeAnalyzer inicializado")
    
    def compare_projects(self, all_results: List[Dict]) -> Dict[str, Any]:
        """Compara resultados de múltiplos projetos"""
        
        print(f"📊 Comparando {len(all_results)} resultados")
        
        # Análise comparativa simulada
        comparison = {
            "projects_compared": len(set(r.get('project', 'unknown') for r in all_results)),
            "total_files": len(all_results),
            "avg_sentiment": sum(r['global_metrics']['global_sentiment'] for r in all_results) / len(all_results),
            "avg_coherence": sum(r['global_metrics']['thematic_coherence'] for r in all_results) / len(all_results),
            "similarity_matrix": [],
            "common_themes": [],
            "distinctive_features": {}
        }
        
        return comparison
