"""
Template para criar novos gráficos
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseChart
from typing import Dict

class PatternsChart(BaseChart):
    """
    Template para novos gráficos
    
    Para criar um novo gráfico:
    1. Copie este arquivo: cp _template_chart.py meu_chart.py
    2. Renomeie a classe: PatternsChart -> MeuChart
    3. Implemente o método create()
    4. Crie arquivo de config em config/visualization_configs/
    """
    
    def create(self, data: Dict, output_path: str) -> str:
        """Padrões linguísticos"""
        
        if 'linguistic_patterns' in data:
            patterns = data['linguistic_patterns']
            categories = ['Certeza', 'Incerteza', 'Hesitações']
            values = [
                patterns.get('certainty_markers', {}).get('count', 0),
                patterns.get('uncertainty_markers', {}).get('count', 0),
                patterns.get('total_hesitations', 0)
            ]
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
        fig.add_trace(go.Bar(x=categories, y=values, marker_color=['green', 'orange', 'red']))
        fig.update_layout(title=self.config.get('title', 'Padrões Linguísticos'))
        
        html_path = output_path.replace('.png', '.html')
        fig.write_html(html_path)
        return html_path

    def _create_text(self, categories, values, output_path: str) -> str:
        text_output = f"🔤 Padrões Linguísticos\n" + "=" * 40 + "\n\n"
        for cat, val in zip(categories, values):
            text_output += f"{cat}: {val}\n"
        
        text_path = output_path.replace('.png', '.txt').replace('.html', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        return text_path
