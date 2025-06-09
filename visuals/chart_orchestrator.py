"""
Orquestrador de gráficos - coordena criação automática de todas as visualizações
"""
from engine.analyzers import BaseAnalyzer
from typing import Dict, List
from pathlib import Path

class ChartOrchestrator(BaseAnalyzer):
    """
    Coordena criação automática de todos os gráficos baseado nos dados disponíveis
    """
    
    def __init__(self, config_path: str = None):
        super().__init__(config_path)
        # Importar sistema de charts
        from visuals.charts import discover_charts
        self.available_charts = discover_charts()
        
        # Mapeamento: que dados cada chart precisa
        self.chart_mappings = {
            'TimelineChart': {
                'data_key': 'temporal_analysis',
                'filename': 'timeline_emocional.html',
                'title_template': 'Timeline Emocional'
            },
            'NetworkChart': {
                'data_key': 'concept_network', 
                'filename': 'rede_conceitos.html',
                'title_template': 'Rede de Conceitos'
            },
            'MetricsChart': {
                'data_key': 'global_metrics',
                'filename': 'metricas_globais.html', 
                'title_template': 'Métricas Globais'
            },
            'WordCloudChart': {
                'data_key': 'word_frequencies',
                'filename': 'wordcloud.html',
                'title_template': 'Word Cloud - {filename}'
            },
            'FrequencyChart': {
                'data_key': 'word_frequencies',
                'filename': 'frequencia_palavras.html',
                'title_template': 'Top 10 Palavras - {filename}'
            },
            'PatternsChart': {
                'data_key': 'linguistic_patterns',
                'filename': 'padroes_linguisticos.html',
                'title_template': 'Padrões Linguísticos - {filename}'
            },
            'TopicsChart': {
                'data_key': 'topics',
                'filename': 'hierarquia_topicos.html',
                'title_template': 'Hierarquia de Tópicos - {filename}'
            },
            'ContradictionsChart': {
                'data_key': 'contradictions',
                'filename': 'contradicoes.html',
                'title_template': 'Análise de Contradições - {filename}'
            }
        }
    
    def analyze(self, analysis_result: Dict, output_dir: str) -> Dict:
        """Cria todos os gráficos automaticamente baseado nos dados disponíveis"""
        
        created_charts = []
        errors = []
        
        print(f"🎨 ChartOrchestrator: Descobriu {len(self.available_charts)} charts")
        print(f"📊 Dados disponíveis: {list(analysis_result.keys())}")
        
        for chart_name, chart_class in self.available_charts.items():
            try:
                if chart_name in self.chart_mappings:
                    mapping = self.chart_mappings[chart_name]
                    data_key = mapping['data_key']
                    
                    # Verificar se temos os dados necessários
                    if data_key in analysis_result and analysis_result[data_key]:
                        print(f"🎯 Criando {chart_name} com dados de '{data_key}'")
                        
                        # Criar instância do chart
                        chart_instance = chart_class()
                        
                        # Preparar dados
                        chart_data = {data_key: analysis_result[data_key]}
                        
                        # Caminho de saída
                        output_path = str(Path(output_dir) / mapping['filename'])
                        
                        # Configurar título
                        title = mapping['title_template']
                        if '{filename}' in title:
                            title = title.format(filename=analysis_result.get('filename', 'Análise'))
                        
                        # Configurar chart
                        chart_instance.config.update({
                            'title': title,
                            'output_path': output_path
                        })
                        
                        # Criar gráfico
                        result_path = chart_instance.create(chart_data, output_path)
                        
                        created_charts.append({
                            'chart': chart_name,
                            'data_used': data_key,
                            'output': result_path,
                            'status': 'success'
                        })
                        
                        print(f"✅ {chart_name} criado: {result_path}")
                    else:
                        print(f"⏭️  {chart_name} ignorado (sem dados '{data_key}')")
                else:
                    print(f"⚠️  {chart_name} não mapeado ainda")
                    
            except Exception as e:
                error_msg = f"❌ Erro ao criar {chart_name}: {e}"
                print(error_msg)
                errors.append({
                    'chart': chart_name,
                    'error': str(e),
                    'status': 'error'
                })
        
        return {
            'analysis_type': 'chart_orchestration',
            'charts_created': len(created_charts),
            'charts_available': len(self.available_charts),
            'created_charts': created_charts,
            'errors': errors,
            'success_rate': len(created_charts) / len(self.chart_mappings) if self.chart_mappings else 0
        }

    def get_available_charts(self) -> List[str]:
        """Retorna lista de charts disponíveis"""
        return list(self.available_charts.keys())
    
    def get_chart_requirements(self) -> Dict:
        """Retorna que dados cada chart precisa"""
        return {chart: mapping['data_key'] for chart, mapping in self.chart_mappings.items()}