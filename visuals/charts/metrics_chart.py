"""
Template para criar novos gráficos
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseChart
from typing import Dict

class MetricsChart(BaseChart):
    """
    Template para novos gráficos
    
    Para criar um novo gráfico:
    1. Copie este arquivo: cp _template_chart.py meu_chart.py
    2. Renomeie a classe: MetricsChart -> MeuChart
    3. Implemente o método create()
    4. Crie arquivo de config em config/visualization_configs/
    """
    
    def create(self, data: Dict, output_path: str) -> str:
        """Cria dashboard de métricas globais"""
        
        adjustments = self.adjust_for_data_size(data)
        
        # Extrair métricas
        if 'global_metrics' in data:
            metrics = data['global_metrics']
            categories = ['Sentimento Global', 'Abertura Emocional', 'Coerência Temática']
            values = [
                metrics.get('global_sentiment', 0),
                metrics.get('emotional_openness', 0), 
                metrics.get('thematic_coherence', 0)
            ]
        else:
            categories = data.get('categories', [])
            values = data.get('values', [])
        
        if self.backend == "plotly":
            return self._create_plotly(categories, values, output_path, adjustments)
        else:
            return self._create_text(categories, values, output_path, adjustments)

    def _create_plotly(self, categories, values, output_path: str, adjustments: Dict) -> str:
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['skyblue', 'lightgreen', 'coral']
        ))
        
        fig.update_layout(
            title=self.config.get('title', 'Métricas Globais'),
            xaxis_title='Métricas',
            yaxis_title='Valores'
        )
        
        html_path = output_path.replace('.png', '.html')
        fig.write_html(html_path)
        return html_path

    def _create_text(self, categories, values, output_path: str, adjustments: Dict) -> str:
        text_output = f"📊 Métricas Globais\n"
        text_output += "=" * 40 + "\n\n"
        
        for cat, val in zip(categories, values):
            text_output += f"{cat}: {val:.3f}\n"
        
        text_path = output_path.replace('.png', '.txt').replace('.html', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        return text_path
