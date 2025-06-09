from typing import Dict, Any, List, Optional, Tuple
#!/usr/bin/env python3
"""
🎯 TRANSCRIPT ANALYZER - CLI PRINCIPAL
🔧 python run_analysis.py --project grupo_docentes

Interface de linha de comando para análise automatizada de entrevistas.
"""

import argparse
import sys
import os
from pathlib import Path
from markdown_generator import MarkdownReportGenerator
from datetime import datetime

# Importar módulos do sistema
try:
    from config_loader import ConfigLoader, ResourceManager, ProjectConfig
    from engine.analyzer_core import TranscriptAnalyzer
    from engine.analysis_orchestrator import AnalysisOrchestrator
    from visuals.dashboard_generator import DashboardGenerator
except ImportError as e:
    print(f"❌ Erro ao importar módulos básicos: {e}")
    print("💡 Execute primeiro: python setup.py para configurar o ambiente")
    sys.exit(1)

# Tentar importar sistema escalável de visualizações
try:
    from visuals.visualization_manager import ScalableVisualizationManager
    SCALABLE_VISUALS = True
    print("✅ Sistema escalável de visualizações carregado")
except ImportError:
    SCALABLE_VISUALS = False
    print("⚠️ Sistema escalável não disponível, usando sistema tradicional")


class AnalysisRunner:
    """🚀 Orquestrador principal das análises"""
    
    def __init__(self):
        self.config_loader = ConfigLoader()
        self.resource_manager = ResourceManager(self.config_loader)
        
    def run_single_analysis(self, project_name: str, file_path: Optional[str] = None):
        """📊 Executa análise individual"""
        
        print(f"🎯 INICIANDO ANÁLISE: {project_name}")
        print("=" * 50)
        
        try:
            # 1. Carregar configuração
            config = self.config_loader.load_project_config(project_name)
            print(f"✅ Configuração carregada: {config.project_name}")
            
            # 2. Inicializar analisador
            analyzer = AnalysisOrchestrator()
            
            # 3. Detectar arquivos para análise
            project_dir = self.config_loader.projects_dir / project_name
            if file_path:
                files_to_analyze = [Path(file_path)]
            else:
                files_to_analyze = list((project_dir / "arquivos").glob("*.txt"))
            
            if not files_to_analyze:
                print("❌ Nenhum arquivo .txt encontrado em arquivos/")
                return False
            
            print(f"📁 Arquivos detectados: {len(files_to_analyze)}")
            
            # 4. Processar cada arquivo
            results = []
            for file_path in files_to_analyze:
                print(f"\n🔍 Analisando: {file_path.name}")
                
                try:
                    result = analyzer.analyze_transcript(file_path, config.__dict__)

                    # DEBUG - Verificar dados disponíveis
                    print("\n🔍 DEBUG - Dados completos disponíveis:")
                    print(f"  ✓ temporal_analysis: {len(result.get('temporal_analysis', []))} pontos")
                    print(f"  ✓ word_frequencies: {len(result.get('word_frequencies', {}))} palavras")
                    print(f"  ✓ linguistic_patterns: {'✓' if result.get('linguistic_patterns') else '✗'}")
                    print(f"  ✓ topic_hierarchy: {len(result.get('topic_hierarchy', {}).get('nodes', []))} nós")
                    print(f"  ✓ phases: {len(result.get('phases', {}))} fases")
                    print(f"  ✓ contradictions: {len(result.get('contradictions', []))} contradições")
                    print("="*60)

                    result['filename'] = file_path.name
                    results.append(result)
                    print(f"✅ {file_path.name} processado")
                    
                except Exception as e:
                    print(f"❌ Erro em {file_path.name}: {e}")
                    continue
            
            if not results:
                print("❌ Nenhuma análise foi concluída com sucesso")
                return False
            
            # 5. Gerar visualizações
            if config.output['generate_visuals']:
                print(f"\n📊 Gerando visualizações...")
                
                for result in results:
                    output_dir = project_dir / "output"
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    print(f"\n🎨 Orquestrando visualizações para {result['filename']}...")
                    
                    # ChartOrchestrator - substitui TODO o código hardcoded!
                    from visuals.chart_orchestrator import ChartOrchestrator
                    chart_orchestrator = ChartOrchestrator()
                    orchestration_result = chart_orchestrator.analyze(result, str(output_dir))
                    
                    print(f"📊 {orchestration_result['charts_created']}/{orchestration_result['charts_available']} gráficos criados com sucesso!")
                    
                    # Mostrar gráficos criados
                    for chart_info in orchestration_result['created_charts']:
                        print(f"  ✅ {chart_info['chart']}")
                    
                    # Mostrar erros se houver
                    for error_info in orchestration_result['errors']:
                        print(f"  ❌ {error_info['chart']}: {error_info['error']}")
                
                print("✅ Visualizações orquestradas geradas")
            
            # 6. Gerar relatórios se habilitado
            if config.output['generate_markdown']:
                print(f"\n📝 Gerando relatórios...")
                try:
                    for result in results:
                        self._generate_markdown_report(result, project_dir / "output")
                except Exception as e:
                    print(f"⚠️ Relatório markdown com problema (gráficos OK): {e}")
            
            # 7. Resumo final
            self._print_analysis_summary(results, project_name)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro crítico na análise: {e}")
            return False
    
    def _generate_visualizations_traditional(self, result, output_dir, config):
        """📊 Gera visualizações usando sistema tradicional"""
        try:
            dashboard = DashboardGenerator(config)
            dashboard.generate_complete_dashboard(result, output_dir)
            print("✅ Visualizações tradicionais geradas")
        except Exception as e:
            print(f"❌ Erro ao gerar visualizações tradicionais: {e}")
    
    def run_comparative_analysis(self, project_names: List[str]):
        """🔄 Executa análise comparativa entre projetos"""
        
        print(f"🔄 ANÁLISE COMPARATIVA")
        print(f"📊 Projetos: {', '.join(project_names)}")
        print("=" * 50)
        
        try:
            all_results = []
            
            # Coletar resultados de todos os projetos
            for project_name in project_names:
                config = self.config_loader.load_project_config(project_name)
                analyzer = AnalysisOrchestrator()
                
                project_dir = self.config_loader.projects_dir / project_name
                files = list((project_dir / "arquivos").glob("*.txt"))
                
                project_results = []
                for file_path in files:
                    result = analyzer.analyze_transcript(file_path, config.__dict__)
                    result['project'] = project_name
                    result['filename'] = file_path.name
                    project_results.append(result)
                
                all_results.extend(project_results)
                print(f"✅ {project_name}: {len(project_results)} arquivos processados")
            
            # Análise comparativa
            from engine.comparative_analyzer import ComparativeAnalyzer
            
            comp_analyzer = ComparativeAnalyzer()
            comparison_results = comp_analyzer.compare_projects(all_results)
            
            # Gerar visualizações comparativas
            dashboard = DashboardGenerator(None)  # Usar config padrão para comparação
            
            # Criar apenas a pasta comparisons se não existir
            comparisons_dir = Path("projects/comparisons")
            comparisons_dir.mkdir(parents=True, exist_ok=True)

            # Gerar nome único para a imagem
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"comparative_{timestamp}_test.png"
            output_path = comparisons_dir / output_filename
            
            dashboard.generate_comparative_dashboard(
                comparison_results,
                output_dir=str(comparisons_dir),
                output_path=str(output_path)
            )
            
            print(f"\n✅ Análise comparativa concluída")
            print(f"📂 Resultados salvos em: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na análise comparativa: {e}")
            return False
    
    def _generate_markdown_report(self, result: Dict[str, Any], output_dir: Path) -> None:
        """Gera relatório Markdown usando o gerador modularizado"""
        try:
            generator = MarkdownReportGenerator()
            generator.generate_report(result, output_dir)
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório Markdown: {e}")
    def _print_analysis_summary(self, results: List[dict], project_name: str):
        """📋 Imprime resumo da análise"""
        
        print(f"\n🎯 RESUMO DA ANÁLISE: {project_name}")
        print("=" * 50)
        
        print(f"📁 Arquivos processados: {len(results)}")
        
        # Métricas médias
        avg_sentiment = sum(r['global_metrics']['global_sentiment'] for r in results) / len(results)
        avg_coherence = sum(r['global_metrics']['thematic_coherence'] for r in results) / len(results)
        avg_openness = sum(r['global_metrics']['emotional_openness'] for r in results) / len(results)
        
        print(f"😊 Sentimento médio: {avg_sentiment:+.2f}")
        print(f"🎯 Coerência média: {avg_coherence:.2f}")
        print(f"💭 Abertura média: {avg_openness:.2f}")
        
        # Arquivos com problemas
        problematic = [r for r in results if isinstance(r.get('global_metrics'), dict) and r['global_metrics'].get('thematic_coherence', 0) < 0.3]
        if problematic:
            print(f"\n⚠️ Arquivos com baixa coerência: {len(problematic)}")
            for r in problematic:
                print(f"   - {r['filename']}")
        
        print(f"\n✅ Análise concluída com sucesso!")


def test_visualization_system():
    """🧪 Testa o sistema de visualizações"""
    
    print("🧪 TESTANDO SISTEMA DE VISUALIZAÇÕES")
    print("=" * 50)
    
    if not SCALABLE_VISUALS:
        print("❌ Sistema escalável não disponível para teste")
        return
    
    try:
        from visuals.visualization_manager import ScalableVisualizationManager
        
        # Criar gerenciador
        viz_manager = ScalableVisualizationManager()
        
        print(f"🎨 Backends disponíveis: {viz_manager.get_available_backends()}")
        
        # Dados de teste
        test_data = {
            'categories': ['A', 'B', 'C', 'D'],
            'values': [10, 25, 15, 30]
        }
        
        test_config = {
            'title': 'Teste de Gráfico de Barras',
            'output_path': 'test_bar_chart.png',
            'xlabel': 'Categorias',
            'ylabel': 'Valores'
        }
        
        # Testar cada backend
        for backend in viz_manager.get_available_backends():
            print(f"\n🔧 Testando backend: {backend}")
            
            test_config['output_path'] = f'test_bar_chart_{backend}.png'
            if backend == 'plotly':
                test_config['output_path'] = f'test_bar_chart_{backend}.html'
            
            result = viz_manager.create_visualization('bar_chart', test_data, test_config, backend)
            
            if result:
                print(f"✅ Sucesso: {result}")
            else:
                print(f"❌ Falha no backend {backend}")
        
        print("\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")


def main():
    """🎯 Função principal do CLI"""
    
    parser = argparse.ArgumentParser(
        description="🎯 Transcript Analyzer - Análise automatizada de entrevistas qualitativas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python run_analysis.py --project grupo_docentes
  python run_analysis.py --project professores_2024 --file entrevista1.txt
  python run_analysis.py --compare projeto1 projeto2 projeto3
  python run_analysis.py --test-visuals
        """
    )
    
    parser.add_argument(
        '--project', '-p',
        help="Nome do projeto para análise"
    )
    
    parser.add_argument(
        '--file', '-f',
        help="Arquivo específico para analisar (opcional)"
    )
    
    parser.add_argument(
        '--compare', '-c',
        nargs='+',
        help="Executar análise comparativa entre projetos"
    )
    
    parser.add_argument(
        '--create-project',
        help="Criar novo projeto com estrutura padrão"
    )
    
    parser.add_argument(
        '--list-projects', '-l',
        action='store_true',
        help="Listar projetos disponíveis"
    )
    
    parser.add_argument(
        '--setup',
        action='store_true',
        help="Configurar ambiente inicial"
    )
    
    parser.add_argument(
        '--test-visuals',
        action='store_true',
        help="Testar sistema de visualizações"
    )
    
    args = parser.parse_args()
    
    # Configurar ambiente se solicitado
    if args.setup:
        from config_loader import setup_environment
        setup_environment()
        return
    
    # Testar visualizações
    if args.test_visuals:
        test_visualization_system()
        return
    
    runner = AnalysisRunner()
    
    # Criar projeto
    if args.create_project:
        runner.config_loader.create_default_project(args.create_project)
        print(f"✅ Projeto '{args.create_project}' criado")
        print(f"📁 Adicione arquivos .txt em: projects/{args.create_project}/arquivos/")
        return
    
    # Listar projetos
    if args.list_projects:
        projects_dir = runner.config_loader.projects_dir
        projects = [d.name for d in projects_dir.iterdir() if d.is_dir()]
        
        if projects:
            print("📁 Projetos disponíveis:")
            for project in projects:
                config_file = projects_dir / project / "config_analise.json"
                status = "✅" if config_file.exists() else "❌"
                print(f"   {status} {project}")
        else:
            print("❌ Nenhum projeto encontrado")
            print("💡 Use: --create-project nome_projeto")
        return
    
    # Análise comparativa
    if args.compare:
        success = runner.run_comparative_analysis(args.compare)
        sys.exit(0 if success else 1)
    
    # Análise individual
    if args.project:
        success = runner.run_single_analysis(args.project, args.file)
        sys.exit(0 if success else 1)
    
    # Se chegou aqui, nenhum comando foi especificado
    parser.print_help()


if __name__ == "__main__":
    main()