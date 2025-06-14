"""
Rede de conceitos interativa
"""
from . import BaseChart
from typing import Dict

class NetworkChart(BaseChart):
    """
    Gráfico de rede de conceitos
    """
    
    def create(self, data: Dict, output_path: str) -> str:
        """Cria rede de conceitos"""
        
        adjustments = self.adjust_for_data_size(data)
        
        # Extrair dados da rede
        if 'concept_network' in data:
            concept_data = data['concept_network']
            if isinstance(concept_data, list):
                connections = concept_data[:10]
            else:
                connections = list(concept_data.items())[:10] if isinstance(concept_data, dict) else []
            
            # Corrigir: criar nodes e edges corretamente
            if connections and len(connections) > 0 and isinstance(connections[0], dict):
                nodes = list(set([c["word1"] for c in connections] + [c["word2"] for c in connections]))
                edges = [(c['word1'], c['word2']) for c in connections]
            else:
                nodes = []
                edges = []
        else:
            nodes = data.get('nodes', [])
            edges = data.get('edges', [])
        
        if self.backend == "plotly":
            return self._create_plotly(nodes, edges, output_path, adjustments)
        else:
            return self._create_text(nodes, edges, output_path, adjustments)
    
    def _create_plotly(self, nodes, edges, output_path: str, adjustments: Dict) -> str:
        import plotly.graph_objects as go
        import random
        import math
        
        # Verificar se temos dados válidos
        if not nodes or not edges:
            # Criar gráfico vazio com mensagem
            fig = go.Figure()
            fig.add_annotation(
                text="Dados de rede não disponíveis",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            fig.update_layout(title=self.config.get('title', 'Rede de Conceitos'))
            html_path = output_path.replace('.png', '.html')
            fig.write_html(html_path)
            return html_path
        
        # Layout simples sem NetworkX
        positions = {}
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes) if len(nodes) > 0 else 0
            positions[node] = (2 * math.cos(angle), 2 * math.sin(angle))
        
        # Criar edges
        edge_x, edge_y = [], []
        for edge in edges:
            x0, y0 = positions.get(edge[0], (0, 0))
            x1, y1 = positions.get(edge[1], (0, 0))
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Criar nodes
        node_x = [positions[node][0] for node in nodes]
        node_y = [positions[node][1] for node in nodes]
        
        fig = go.Figure()
        
        # Adicionar edges
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                               line=dict(width=2, color='gray'),
                               showlegend=False))
        
        # Adicionar nodes
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text',
                               marker=dict(size=20, color='lightblue'),
                               text=nodes, textposition="middle center",
                               showlegend=False))
        
        fig.update_layout(
            title=self.config.get('title', 'Rede de Conceitos'),
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        html_path = output_path.replace('.png', '.html')
        fig.write_html(html_path)
        return html_path
    
    def _create_text(self, nodes, edges, output_path: str, adjustments: Dict) -> str:
        text_output = f"🕸️ Rede de Conceitos\n"
        text_output += "=" * 40 + "\n\n"
        text_output += f"Nós: {len(nodes)}\n"
        text_output += f"Conexões: {len(edges)}\n\n"
        
        for edge in edges[:10]:
            text_output += f"{edge[0]} ↔ {edge[1]}\n"
        
        text_path = output_path.replace('.png', '.html').replace('.html', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        return text_path