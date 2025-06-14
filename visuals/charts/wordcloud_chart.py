"""
Template para criar novos gráficos
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseChart
from typing import Dict

class WordCloudChart(BaseChart):
    """
    Template para novos gráficos
    
    Para criar um novo gráfico:
    1. Copie este arquivo: cp _template_chart.py meu_chart.py
    2. Renomeie a classe: WordCloudChart -> MeuChart
    3. Implemente o método create()
    4. Crie arquivo de config em config/visualization_configs/
    """
    
    def create(self, data: Dict, output_path: str) -> str:
        """Cria word cloud interativo"""
        
        adjustments = self.adjust_for_data_size(data)
        
        # Extrair dados de frequência
        if 'word_frequencies' in data:
            sorted_words = sorted(data['word_frequencies'].items(), 
                                key=lambda x: x[1], reverse=True)[:10]
            words = [word for word, freq in sorted_words]
            frequencies = [freq for word, freq in sorted_words]
        else:
            words = data.get('words', [])
            frequencies = data.get('frequencies', [])
        
        if self.backend == "plotly":
            return self._create_plotly(words, frequencies, output_path, adjustments)
        else:
            return self._create_text(words, frequencies, output_path, adjustments)

    def _create_plotly(self, words, frequencies, output_path: str, adjustments: Dict) -> str:
        import plotly.graph_objects as go
        import random
        import math
        
        # Layout em espiral para evitar sobreposição
        x_pos = []
        y_pos = []
        
        for i, word in enumerate(words):
            angle = i * 0.8  # Ângulo progressivo
            radius = 1 + (i * 0.5)  # Raio crescente
            x_pos.append(radius * math.cos(angle))
            y_pos.append(radius * math.sin(angle))
        
        sizes = [max(20, freq * 3) for freq in frequencies]  # Tamanhos maiores
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_pos, y=y_pos,
            mode='markers+text',
            marker=dict(size=sizes, color=frequencies, colorscale='Viridis', opacity=0.7),
            text=words,
            textposition="middle center",
            textfont=dict(size=14, color='white')
        ))
        
        fig.update_layout(
            title=self.config.get('title', 'Word Cloud'),
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        html_path = output_path.replace('.png', '.html')
        fig.write_html(html_path)
        return html_path

    def _create_text(self, words, frequencies, output_path: str, adjustments: Dict) -> str:
        text_output = f"☁️ Word Cloud\n"
        text_output += "=" * 40 + "\n\n"
        
        for word, freq in zip(words, frequencies):
            text_output += f"{word}: {freq}\n"
        
        text_path = output_path.replace('.png', '.txt').replace('.html', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        return text_path