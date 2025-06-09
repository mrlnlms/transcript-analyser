"""
Timeline emocional interativo
"""
from . import BaseChart
from typing import Dict

class TimelineChart(BaseChart):
    """
    Gráfico de timeline emocional
    """
    
    def create(self, data: Dict, output_path: str) -> str:
        """Cria timeline emocional interativo"""
        
        # Ajustar para volume de dados
        adjustments = self.adjust_for_data_size(data)
        
        # Extrair dados temporais
        if 'temporal_analysis' in data:
            temporal_data = data['temporal_analysis']
            x_data = [seg.get('timestamp', f"{i}%") for i, seg in enumerate(temporal_data)]
            y_data = [seg['sentiment'] for seg in temporal_data]
        else:
            x_data = data.get('x', [])
            y_data = data.get('y', [])
        
        if self.backend == "plotly":
            return self._create_plotly(x_data, y_data, output_path, adjustments)
        elif self.backend == "matplotlib":
            return self._create_matplotlib(x_data, y_data, output_path, adjustments)
        else:
            return self._create_text(x_data, y_data, output_path, adjustments)
    
    def _create_plotly(self, x_data, y_data, output_path: str, adjustments: Dict) -> str:
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_data, y=y_data,
            mode='lines+markers',
            name='Evolução Emocional',
            line=dict(width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=self.config.get('title', 'Timeline Emocional'),
            xaxis_title='Segmentos Temporais',
            yaxis_title='Sentimento'
        )
        
        html_path = output_path.replace('.png', '.html')
        fig.write_html(html_path)
        return html_path
    
    def _create_matplotlib(self, x_data, y_data, output_path: str, adjustments: Dict) -> str:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_data, y_data, marker='o', linewidth=2)
        plt.title(self.config.get('title', 'Timeline Emocional'))
        plt.xlabel('Segmentos')
        plt.ylabel('Sentimento')
        plt.grid(True, alpha=0.3)
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return output_path
    
    def _create_text(self, x_data, y_data, output_path: str, adjustments: Dict) -> str:
        text_output = f"📈 Timeline Emocional\n"
        text_output += "=" * 40 + "\n\n"
        
        for x, y in zip(x_data, y_data):
            text_output += f"Segmento {x}: {y:.3f}\n"
        
        text_path = output_path.replace('.png', '.txt').replace('.html', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        return text_path