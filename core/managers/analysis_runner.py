#!/usr/bin/env python3
"""
Analysis Runner - Coordenação de análises
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Imports dos orquestradores
from core.engine.analysis_orchestrator import AnalysisOrchestrator
from core.visuals.chart_orchestrator import ChartOrchestrator
from core.generators.markdown_generator import MarkdownReportGenerator


class AnalysisRunner:
    """Coordena a execução de análises"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analysis_orchestrator = AnalysisOrchestrator()
        self.chart_orchestrator = ChartOrchestrator()
        self.markdown_generator = MarkdownReportGenerator()
        
    def analyze_project(self, project_path: Path) -> bool:
        """Executa análise completa de um projeto"""
        try:
            print(f"\n🎯 INICIANDO ANÁLISE: {project_path.name}")
            print("=" * 50)
            
            # Encontrar arquivos
            arquivos_dir = project_path / "arquivos"
            txt_files = list(arquivos_dir.glob("*.txt"))
            
            if not txt_files:
                print("❌ Nenhum arquivo .txt encontrado!")
                return False
                
            print(f"📁 Arquivos detectados: {len(txt_files)}")
            
            results = []
            
            # Analisar cada arquivo
            for file_path in txt_files:
                print(f"\n🔍 Analisando: {file_path.name}")
                
                # Análise via orchestrator
                result = self.analysis_orchestrator.analyze_transcript(file_path)
                
                if result:
                    results.append(result)
                    print(f"✅ {file_path.name} processado")
                else:
                    print(f"❌ Erro ao processar {file_path.name}")
            
            if not results:
                print("\n❌ Nenhum arquivo foi processado com sucesso!")
                return False
            
            # Gerar visualizações e relatórios
            output_dir = project_path / "output"
            output_dir.mkdir(exist_ok=True)
            
            print("\n📊 Gerando visualizações...")
            for result in results:
                # Gráficos via orchestrator
                self.chart_orchestrator.analyze(result, str(output_dir))
                
                # Relatório markdown
                self.markdown_generator.generate_report(result, output_dir)
            
            # Resumo final
            self._print_summary(results)
            
            print(f"\n✅ Análise concluída com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro na análise: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _print_summary(self, results: List[Dict]):
        """Imprime resumo da análise"""
        print(f"\n🎯 RESUMO DA ANÁLISE")
        print("=" * 50)
        print(f"📁 Arquivos processados: {len(results)}")
        
        # Calcular médias
        sentiments = []
        coherences = []
        
        for result in results:
            if 'global_metrics' in result:
                metrics = result['global_metrics']
                sentiments.append(metrics.get('global_sentiment', 0))
                coherences.append(metrics.get('thematic_coherence', 0))
        
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            print(f"😊 Sentimento médio: {avg_sentiment:.2f}")
            
        if coherences:
            avg_coherence = sum(coherences) / len(coherences)
            print(f"🎯 Coerência média: {avg_coherence:.2f}")


# Teste básico
if __name__ == "__main__":
    print("✅ Analysis Runner criado!")
    # Não podemos testar completamente sem os imports
