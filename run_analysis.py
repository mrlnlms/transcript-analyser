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
from datetime import datetime
from typing import Optional, List

# Importar módulos do sistema
try:
    from config_loader import ConfigLoader, ResourceManager, ProjectConfig
    from engine.analyzer_core import TranscriptAnalyzer
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
            analyzer = TranscriptAnalyzer(config, self.resource_manager)
            
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
                    result = analyzer.analyze_transcript(file_path)

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
                    output_dir = project_dir / "output" / result['filename'].replace('.txt', '')
                    output_dir.mkdir(parents=True, exist_ok=True)
                    # Criar subpasta para assets
                    assets_dir = output_dir / "assets"
                    assets_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Usar método inteligente de visualização
                    self._generate_visualizations_smart(result, str(output_dir), config)
            
            # 6. Gerar relatórios se habilitado
            if config.output['generate_markdown']:
                print(f"\n📝 Gerando relatórios...")
                self._generate_markdown_reports(results, project_dir / "output")
            
            # 7. Resumo final
            self._print_analysis_summary(results, project_name)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro crítico na análise: {e}")
            return False
    
    def _generate_visualizations_smart(self, result, output_dir, config):
        """🎨 Gera visualizações usando sistema escalável ou fallback"""
        
        if SCALABLE_VISUALS:
            try:
                # Usar sistema novo e escalável
                viz_manager = ScalableVisualizationManager(config.output)
                
                print(f"🎨 Backends disponíveis: {viz_manager.get_available_backends()}")
                
                # Gráfico de métricas
                metrics_data = {
                    'categories': ['Sentimento', 'Coerência', 'Abertura'],
                    'values': [
                        result['global_metrics']['global_sentiment'],
                        result['global_metrics']['thematic_coherence'], 
                        result['global_metrics']['emotional_openness']
                    ]
                }
                extension = 'html' if hasattr(viz_manager, 'primary_backend') and viz_manager.primary_backend == 'plotly' else 'png'

                metrics_config = {
                    'title': f'Métricas Globais - {result["filename"]}',
                    'output_path': str(Path(output_dir) / f'metricas_globais.{extension}'),
                    'figsize': (12, 8),
                    'bar_params': {'alpha': 0.8, 'color': ['skyblue', 'lightgreen', 'coral']}
                }
                
                viz_manager.create_visualization('bar_chart', metrics_data, metrics_config)
                
                # DEBUG temporário
                print(f"\n🔍 DEBUG - Dados disponíveis para {result['filename']}:")
                print(f"  - temporal_analysis: {len(result.get('temporal_analysis', []))} items")
                print(f"  - concept_network: {len(result.get('concept_network', []))} items")
                if result.get('concept_network'):
                    print(f"  - Primeiro item network: {result['concept_network'][0]}")
                
                # Timeline emocional se houver dados temporais
                if result.get('temporal_analysis'):
                    timeline_data = {
                        'x': [i for i in range(len(result['temporal_analysis']))],
                        'y': [seg['sentiment'] for seg in result['temporal_analysis']]
                    }
                    
                    timeline_config = {
                        'title': 'Timeline Emocional',
                        'xlabel': 'Segmentos',
                        'ylabel': 'Sentimento',
                        'output_path': str(Path(output_dir) / 'timeline_emocional.html'),
                        'trace_name': 'Evolução Emocional'
                    }
                    
                    viz_manager.create_visualization('line_plot', timeline_data, timeline_config, backend='plotly')
                
                # Rede de conceitos se disponível
                if result.get('concept_network'):
                    network_data = {
                        'nodes': [conn['word1'] for conn in result['concept_network'][:10]] + 
                                [conn['word2'] for conn in result['concept_network'][:10]],
                        'edges': [(conn['word1'], conn['word2']) for conn in result['concept_network'][:10]]
                    }
                    
                    network_config = {
                        'title': 'Rede de Conceitos',
                        'output_path': str(Path(output_dir) / 'rede_conceitos.html'),
                        'node_params': {'node_size': 300, 'node_color': 'lightblue'},
                        'edge_params': {'width': 2, 'alpha': 0.7}
                    }
                    
                    viz_manager.create_visualization('network_graph', network_data, network_config, backend='plotly')
                # 4. Word Cloud (usando bar chart por enquanto)
                if result.get('word_frequencies'):
                    # Pegar top 10 palavras mais frequentes
                    sorted_words = sorted(result['word_frequencies'].items(), 
                                        key=lambda x: x[1], 
                                        reverse=True)[:10]
                    
                    wordcloud_data = {
                        'words': [word for word, freq in sorted_words],      # Mudou de 'categories' para 'words'
                        'frequencies': [freq for word, freq in sorted_words]  # Mudou de 'values' para 'frequencies'
                    }
                    
                    wordcloud_config = {
                        'title': f'Word Cloud - {result["filename"]}',
                        'output_path': str(Path(output_dir) / 'wordcloud.html'),
                        'xlabel': 'Palavras',
                        'ylabel': 'Frequência',
                        'figsize': (12, 6),
                        'bar_params': {'alpha': 0.9, 'color': 'purple'}
                    }
                    # DEBUG wordcloud
                    print(f"DEBUG Wordcloud - Top 5 palavras: {list(result['word_frequencies'].items())[:5]}")
                    #viz_manager.create_visualization('wordcloud', wordcloud_data, wordcloud_config)

                    # DEBUG para wordcloud
                    print(f"DEBUG - Tipo de visualização: wordcloud")
                    print(f"DEBUG - Backends disponíveis: {viz_manager.get_available_backends()}")
                    print(f"DEBUG - Backend primário: {viz_manager.primary_backend}")

                    # DEBUG - Verificar se o método existe
                    print(f"DEBUG - PlotlyBackend tem create_wordcloud? {hasattr(viz_manager.backends.get('plotly'), 'create_wordcloud')}")
                    print(f"DEBUG - Métodos disponíveis no PlotlyBackend: {[m for m in dir(viz_manager.backends.get('plotly')) if m.startswith('create_')]}")

                    # Forçar uso direto do método wordcloud
                    if hasattr(viz_manager.backends.get('plotly'), 'create_wordcloud'):
                        output = viz_manager.backends['plotly'].create_wordcloud(wordcloud_data, wordcloud_config)
                        print(f"✅ Word Cloud criado diretamente: {output}")
                    else:
                        viz_manager.create_visualization('wordcloud', wordcloud_data, wordcloud_config)
                
                # 4.1 Top 10 Palavras em Barras (complementar ao wordcloud)
                if result.get('word_frequencies'):
                    # Mesmos dados, mas para gráfico de barras
                    sorted_words = sorted(result['word_frequencies'].items(), 
                                        key=lambda x: x[1], 
                                        reverse=True)[:10]
                    
                    bar_words_data = {
                        'categories': [word for word, freq in sorted_words],
                        'values': [freq for word, freq in sorted_words]
                    }
                    
                    bar_words_config = {
                        'title': f'Top 10 Palavras (Frequência) - {result["filename"]}',
                        'output_path': str(Path(output_dir) / 'top_palavras_freq.html'),
                        'xlabel': 'Palavras',
                        'ylabel': 'Frequência',
                        'figsize': (12, 6),
                        'bar_params': {'alpha': 0.9, 'color': 'indigo'}
                    }
                    
                    viz_manager.create_visualization('bar_chart', bar_words_data, bar_words_config)

                # 5. Padrões Linguísticos
                if result.get('linguistic_patterns'):
                    patterns = result['linguistic_patterns']
                    patterns_data = {
                        'categories': ['Certeza', 'Incerteza', 'Hesitações'],
                        'values': [
                            patterns.get('certainty_markers', {}).get('count', 0),
                            patterns.get('uncertainty_markers', {}).get('count', 0),
                            patterns.get('total_hesitations', 0)
                        ]
                    }
                    
                    patterns_config = {
                        'title': f'Padrões Linguísticos - {result["filename"]}',
                        'output_path': str(Path(output_dir) / 'padroes_linguisticos.html'),
                        'figsize': (10, 6),
                        'bar_params': {'alpha': 0.8, 'color': ['green', 'orange', 'red']}
                    }
                    
                    viz_manager.create_visualization('bar_chart', patterns_data, patterns_config)

                # 6. Hierarquia de Tópicos
                if result.get('topic_hierarchy') and result['topic_hierarchy'].get('nodes'):
                    # Agora sabemos que nodes tem 'id' e 'label'
                    hierarchy_data = {
                        'nodes': [node['label'] for node in result['topic_hierarchy']['nodes'][:15]],
                        'edges': [(edge['source'], edge['target']) for edge in result['topic_hierarchy'].get('edges', [])]
                    }
                    
                    hierarchy_config = {
                        'title': f'Hierarquia de Tópicos - {result["filename"]}',
                        'output_path': str(Path(output_dir) / 'hierarquia_topicos.html'),
                        'node_params': {'node_size': 500, 'node_color': 'lightcoral'},
                        'edge_params': {'width': 1, 'alpha': 0.5}
                    }
                    
                    viz_manager.create_visualization('network_graph', hierarchy_data, hierarchy_config)
                
                # 7. Análise de Contradições
                if result.get('contradictions') and len(result['contradictions']) > 0:
                    contradictions_data = {
                        'categories': [f"Contradição {i+1}" for i in range(len(result['contradictions']))],
                        'values': [c['score'] for c in result['contradictions']]
                    }
                    
                    contradictions_config = {
                        'title': f'Análise de Contradições - {result["filename"]}',
                        'output_path': str(Path(output_dir) / 'contradicoes.html'),
                        'xlabel': 'Contradições Detectadas',
                        'ylabel': 'Score de Contradição',
                        'figsize': (10, 6),
                        'bar_params': {'alpha': 0.7, 'color': 'salmon'}
                    }
                    
                    viz_manager.create_visualization('bar_chart', contradictions_data, contradictions_config)

                

                print("✅ Visualizações escaláveis geradas")
                
            except Exception as e:
                print(f"⚠️ Erro no sistema escalável: {e}")
                print("🔄 Usando sistema tradicional como fallback...")
                self._generate_visualizations_traditional(result, output_dir, config)
        else:
            # Usar sistema tradicional
            self._generate_visualizations_traditional(result, output_dir, config)
    
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
                analyzer = TranscriptAnalyzer(config, self.resource_manager)
                
                project_dir = self.config_loader.projects_dir / project_name
                files = list((project_dir / "arquivos").glob("*.txt"))
                
                project_results = []
                for file_path in files:
                    result = analyzer.analyze_transcript(file_path)
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
    
    def _generate_markdown_reports(self, results: List[dict], output_dir: Path):
        """📝 Gera relatórios em Markdown"""
        
        for result in results:
            # Criar caminho correto dentro da pasta do arquivo
            file_folder = result['filename'].replace('.txt', '')
            # output_dir já é projects/nome/output/
            # Então: projects/nome/output/arquivo/arquivo.md
            report_path = output_dir / file_folder / f"{file_folder}.md"
            
            # Garantir que a pasta existe (caso ainda não tenha sido criada)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(self._create_markdown_content(result))
                
                print(f"📄 Relatório gerado: {file_folder}.md")
            except Exception as e:
                print(f"❌ Erro ao gerar relatório {file_folder}.md: {e}")
    
    def _create_markdown_content(self, result: dict) -> str:
        """📋 Cria conteúdo do relatório em Markdown"""
        
        content = f"""# Análise de Entrevista: {result['filename']}

**Data da Análise:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

## 📊 Métricas Globais

- **Sentimento Global:** {result['global_metrics']['global_sentiment']:.2f}
- **Coerência Temática:** {result['global_metrics']['thematic_coherence']:.2f}
- **Abertura Emocional:** {result['global_metrics']['emotional_openness']:.2f}

## 🎭 Análise Linguística
"""
        # Extrair dados com segurança
        linguistic = result.get('linguistic_patterns', {})
        
        # Para compatibilidade com estrutura antiga E nova
        if 'uncertainty_markers' in linguistic:
            # Estrutura nova
            uncertainty = linguistic.get('uncertainty_markers', {}).get('count', 0)
            certainty = linguistic.get('certainty_markers', {}).get('count', 0)
        else:
            # Estrutura antiga
            uncertainty = linguistic.get('uncertainty_count', 0)
            certainty = linguistic.get('certainty_count', 0)
        
        content += f"- **Total de Hesitações:** {linguistic.get('total_hesitations', 0)}\n"
        content += f"- **Marcadores de Incerteza:** {uncertainty}\n"
        content += f"- **Marcadores de Certeza:** {certainty}\n"
        
        if certainty > 0:
            ratio = uncertainty / certainty
            content += f"- **Razão Incerteza/Certeza:** {ratio:.2f}\n"
        else:
            content += f"- **Razão Incerteza/Certeza:** N/A\n"
            
        content += f"- **Complexidade Média:** {linguistic.get('avg_sentence_length', 0):.1f} palavras/frase\n"
        content += """
## 📈 Tópicos Principais

"""
        
        # Adicionar tópicos
        for i, topic in enumerate(result['topics'][:5]):
            distribution = result['topic_distribution'][i]
            content += f"### Tópico {i+1} ({distribution:.1%})\n"
            content += f"**Palavras-chave:** {', '.join(topic['words'][:8])}\n\n"
        # Adicionar contradições se existirem
        if result.get('contradictions'):
            content += "## ⚠️ Contradições Detectadas\n\n"
            for i, contradiction in enumerate(result['contradictions'][:3]):
                content += f"### Contradição {i+1}\n"
                # Tenta diferentes campos possíveis
                if 'topic_words' in contradiction:
                    content += f"- **Tópico:** {', '.join(contradiction['topic_words'][:5])}\n"
                elif 'text1' in contradiction:
                    # Se não tem topic_words, mostra os textos
                    content += f"- **Texto 1:** \"{contradiction.get('text1', '')[:50]}...\"\n"
                    content += f"- **Texto 2:** \"{contradiction.get('text2', '')[:50]}...\"\n"

                # Intensidade ou score
                if 'intensity' in contradiction:
                    content += f"- **Intensidade:** {contradiction['intensity']:.2f}\n\n"
                elif 'score' in contradiction:
                    content += f"- **Score:** {contradiction['score']:.2f}\n\n"
                else:
                    content += "\n"  # Garante espaçamento mesmo sem score
        
        return content
    
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
        problematic = [r for r in results if r['global_metrics']['thematic_coherence'] < 0.3]
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