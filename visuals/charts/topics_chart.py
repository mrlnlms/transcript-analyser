"""
Template para criar novos gráficos
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseChart
from typing import Dict

class TopicsChart(BaseChart):
    """
    Template para novos gráficos
    
    Para criar um novo gráfico:
    1. Copie este arquivo: cp _template_chart.py meu_chart.py
    2. Renomeie a classe: TopicsChart -> MeuChart
    3. Implemente o método create()
    4. Crie arquivo de config em config/visualization_configs/
    """
    
    def create(self, data: Dict, output_path: str) -> str:
        """Hierarquia de tópicos"""
        
        if 'topics' in data:
            topics = data['topics']
            categories = [t['label'] for t in topics]
            values = [t['weight'] for t in topics]
        else:
            categories = data.get('categories', [])
            values = data.get('values', [])
        
        if self.backend == "plotly":
            return self._create_plotly(categories, values, output_path)
        else:
            return self._create_text(categories, values, output_path)

    def _create_plotly(self, categories, values, output_path: str) -> str:
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=categories, y=values, marker_color='lightblue'))
        fig.update_layout(title=self.config.get('title', 'Tópicos'))
        
        html_path = output_path.replace('.png', '.html')
        fig.write_html(html_path)
        return html_path

    def _create_text(self, categories, values, output_path: str) -> str:
        text_output = f"📚 Tópicos\n" + "=" * 40 + "\n\n"
        for cat, val in zip(categories, values):
            text_output += f"{cat}: {val:.3f}\n"
        
        text_path = output_path.replace('.png', '.txt').replace('.html', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        return text_path
