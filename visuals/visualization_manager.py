#!/usr/bin/env python3
"""
📊 ARQUITETURA DE VISUALIZAÇÕES ESCALÁVEL
Modular, extensível e com fallbacks inteligentes
"""

import importlib
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import json


class VisualizationBackend(ABC):
    """Interface base para backends de visualização"""
    
    @abstractmethod
    def create_line_plot(self, data: Dict, config: Dict) -> str:
        """Cria gráfico de linha"""
        pass
    
    @abstractmethod
    def create_bar_chart(self, data: Dict, config: Dict) -> str:
        """Cria gráfico de barras"""
        pass
    
    @abstractmethod
    def create_network_graph(self, data: Dict, config: Dict) -> str:
        """Cria gráfico de rede"""
        pass
    
    @abstractmethod
    def create_heatmap(self, data: Dict, config: Dict) -> str:
        """Cria mapa de calor"""
        pass


class MatplotlibBackend(VisualizationBackend):
    """Backend usando Matplotlib + Seaborn"""
    
    def __init__(self):
        try:
            import matplotlib
            matplotlib.use('Agg')  # Sem display
            import matplotlib.pyplot as plt
            import seaborn as sns
            self.plt = plt
            self.sns = sns
            self.available = True
            print("✅ Matplotlib backend carregado")
        except ImportError:
            self.available = False
            print("❌ Matplotlib não disponível")
    
    def create_line_plot(self, data: Dict, config: Dict) -> str:
        if not self.available:
            return ""
        
        fig, ax = self.plt.subplots(figsize=config.get('figsize', (10, 6)))
        
        # Implementar gráfico de linha
        x_data = data.get('x', [])
        y_data = data.get('y', [])
        
        ax.plot(x_data, y_data, **config.get('plot_params', {}))
        ax.set_title(config.get('title', 'Line Plot'))
        ax.set_xlabel(config.get('xlabel', 'X'))
        ax.set_ylabel(config.get('ylabel', 'Y'))
        ax.grid(True, alpha=0.3)
        
        output_path = config.get('output_path', 'line_plot.png')
        self.plt.savefig(output_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return output_path
    
    def create_bar_chart(self, data: Dict, config: Dict) -> str:
        if not self.available:
            return ""
        
        fig, ax = self.plt.subplots(figsize=config.get('figsize', (10, 6)))
        
        categories = data.get('categories', [])
        values = data.get('values', [])
        
        bars = ax.bar(categories, values, **config.get('bar_params', {}))
        ax.set_title(config.get('title', 'Bar Chart'))
        ax.set_xlabel(config.get('xlabel', 'Categories'))
        ax.set_ylabel(config.get('ylabel', 'Values'))
        
        # Adicionar valores nas barras
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2f}', ha='center', va='bottom')
        
        output_path = config.get('output_path', 'bar_chart.png')
        self.plt.savefig(output_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return output_path
    
    def create_network_graph(self, data: Dict, config: Dict) -> str:
        if not self.available:
            return ""
        
        try:
            import networkx as nx
            
            fig, ax = self.plt.subplots(figsize=config.get('figsize', (12, 8)))
            
            # Criar grafo
            G = nx.Graph()
            nodes = data.get('nodes', [])
            edges = data.get('edges', [])
            
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            
            # Layout
            pos = nx.spring_layout(G, k=1, iterations=50)
            
            # Desenhar
            nx.draw_networkx_nodes(G, pos, ax=ax, **config.get('node_params', {}))
            nx.draw_networkx_edges(G, pos, ax=ax, **config.get('edge_params', {}))
            nx.draw_networkx_labels(G, pos, ax=ax, **config.get('label_params', {}))
            
            ax.set_title(config.get('title', 'Network Graph'))
            ax.axis('off')
            
            output_path = config.get('output_path', 'network_graph.png')
            self.plt.savefig(output_path, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return output_path
            
        except ImportError:
            print("⚠️ NetworkX não disponível para gráficos de rede")
            return ""
    
    def create_heatmap(self, data: Dict, config: Dict) -> str:
        if not self.available:
            return ""
        
        fig, ax = self.plt.subplots(figsize=config.get('figsize', (10, 8)))
        
        matrix = data.get('matrix', [])
        labels = data.get('labels', [])
        
        im = ax.imshow(matrix, cmap=config.get('colormap', 'viridis'))
        
        # Configurar labels
        if labels:
            ax.set_xticks(range(len(labels)))
            ax.set_yticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=45)
            ax.set_yticklabels(labels)
        
        # Colorbar
        self.plt.colorbar(im, ax=ax)
        ax.set_title(config.get('title', 'Heatmap'))
        
        output_path = config.get('output_path', 'heatmap.png')
        self.plt.savefig(output_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return output_path


class PlotlyBackend(VisualizationBackend):
    """Backend usando Plotly para gráficos interativos"""
    
    def __init__(self):
        try:
            import plotly.graph_objects as go
            import plotly.express as px
            self.go = go
            self.px = px
            self.available = True
            print("✅ Plotly backend carregado")
        except ImportError:
            self.available = False
            print("❌ Plotly não disponível")
    
    def create_line_plot(self, data: Dict, config: Dict) -> str:
        if not self.available:
            return ""
        
        fig = self.go.Figure()
        
        x_data = data.get('x', [])
        y_data = data.get('y', [])
        
        fig.add_trace(self.go.Scatter(
            x=x_data, y=y_data,
            mode='lines+markers',
            name=config.get('trace_name', 'Data')
        ))
        
        fig.update_layout(
            title=config.get('title', 'Interactive Line Plot'),
            xaxis_title=config.get('xlabel', 'X'),
            yaxis_title=config.get('ylabel', 'Y')
        )
        
        output_path = config.get('output_path', 'line_plot.html')
        fig.write_html(output_path)
        
        return output_path
    
    def create_bar_chart(self, data: Dict, config: Dict) -> str:
        if not self.available:
            return ""
        
        fig = self.go.Figure()
        
        categories = data.get('categories', [])
        values = data.get('values', [])
        
        fig.add_trace(self.go.Bar(
            x=categories, y=values,
            name=config.get('trace_name', 'Data')
        ))
        
        fig.update_layout(
            title=config.get('title', 'Interactive Bar Chart'),
            xaxis_title=config.get('xlabel', 'Categories'),
            yaxis_title=config.get('ylabel', 'Values')
        )
        
        output_path = config.get('output_path', 'bar_chart.html')
        fig.write_html(output_path)
        
        return output_path
    
    def create_network_graph(self, data: Dict, config: Dict) -> str:
        if not self.available:
            return ""
        
        try:
            import networkx as nx
            
            # Criar grafo
            G = nx.Graph()
            nodes = data.get('nodes', [])
            edges = data.get('edges', [])
            
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            
            # Calcular posições
            pos = nx.spring_layout(G)
            
            # Preparar dados para Plotly
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            node_x = [pos[node][0] for node in G.nodes()]
            node_y = [pos[node][1] for node in G.nodes()]
            
            # Criar figura
            fig = self.go.Figure()
            
            # Adicionar edges
            fig.add_trace(self.go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=2, color='gray'),
                hoverinfo='none',
                mode='lines'
            ))
            
            # Adicionar nodes
            fig.add_trace(self.go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                text=list(G.nodes()),
                textposition="middle center",
                hoverinfo='text',
                marker=dict(size=20, color='lightblue')
            ))
            
            fig.update_layout(
                title=config.get('title', 'Interactive Network Graph'),
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            
            output_path = config.get('output_path', 'network_graph.html')
            fig.write_html(output_path)
            
            return output_path
            
        except ImportError:
            print("⚠️ NetworkX não disponível para gráficos de rede")
            return ""
    
    def create_heatmap(self, data: Dict, config: Dict) -> str:
        if not self.available:
            return ""
        
        matrix = data.get('matrix', [])
        labels = data.get('labels', [])
        
        fig = self.go.Figure(data=self.go.Heatmap(
            z=matrix,
            x=labels,
            y=labels,
            colorscale=config.get('colorscale', 'Viridis')
        ))
        
        fig.update_layout(
            title=config.get('title', 'Interactive Heatmap')
        )
        
        output_path = config.get('output_path', 'heatmap.html')
        fig.write_html(output_path)
        
        return output_path


class TextBackend(VisualizationBackend):
    """Backend fallback que gera visualizações em texto"""
    
    def __init__(self):
        self.available = True
        print("✅ Text fallback backend carregado")
    
    def create_line_plot(self, data: Dict, config: Dict) -> str:
        output_path = config.get('output_path', 'line_plot.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"📈 {config.get('title', 'Line Plot')}\n")
            f.write("=" * 40 + "\n\n")
            
            x_data = data.get('x', [])
            y_data = data.get('y', [])
            
            for i, (x, y) in enumerate(zip(x_data, y_data)):
                f.write(f"Ponto {i+1}: X={x}, Y={y}\n")
        
        return output_path
    
    def create_bar_chart(self, data: Dict, config: Dict) -> str:
        output_path = config.get('output_path', 'bar_chart.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"📊 {config.get('title', 'Bar Chart')}\n")
            f.write("=" * 40 + "\n\n")
            
            categories = data.get('categories', [])
            values = data.get('values', [])
            
            max_val = max(values) if values else 1
            
            for cat, val in zip(categories, values):
                bar_length = int((val / max_val) * 30)
                bar = "█" * bar_length
                f.write(f"{cat:15} {bar} {val:.2f}\n")
        
        return output_path
    
    def create_network_graph(self, data: Dict, config: Dict) -> str:
        output_path = config.get('output_path', 'network_graph.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"🕸️ {config.get('title', 'Network Graph')}\n")
            f.write("=" * 40 + "\n\n")
            
            nodes = data.get('nodes', [])
            edges = data.get('edges', [])
            
            f.write("Nós:\n")
            for node in nodes:
                f.write(f"  • {node}\n")
            
            f.write("\nConexões:\n")
            for edge in edges:
                f.write(f"  {edge[0]} ↔ {edge[1]}\n")
        
        return output_path
    
    def create_heatmap(self, data: Dict, config: Dict) -> str:
        output_path = config.get('output_path', 'heatmap.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"🔥 {config.get('title', 'Heatmap')}\n")
            f.write("=" * 40 + "\n\n")
            
            matrix = data.get('matrix', [])
            labels = data.get('labels', [])
            
            if labels:
                f.write("    " + " ".join(f"{label:>6}" for label in labels) + "\n")
            
            for i, row in enumerate(matrix):
                label = labels[i] if labels and i < len(labels) else f"R{i}"
                f.write(f"{label:3} ")
                for val in row:
                    f.write(f"{val:6.2f}")
                f.write("\n")
        
        return output_path


class ScalableVisualizationManager:
    """Gerenciador escalável de visualizações com fallbacks"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.backends = {}
        self.primary_backend = None
        self.fallback_backend = None
        
        self._initialize_backends()
    
    def _initialize_backends(self):
        """Inicializa backends disponíveis"""
        
        # Tentar carregar backends em ordem de preferência
        backend_classes = [
            ('plotly', PlotlyBackend),
            ('matplotlib', MatplotlibBackend),
            ('text', TextBackend)
        ]
        
        for name, backend_class in backend_classes:
            try:
                backend = backend_class()
                if backend.available:
                    self.backends[name] = backend
                    
                    if self.primary_backend is None:
                        self.primary_backend = name
                    
            except Exception as e:
                print(f"⚠️ Erro ao carregar backend {name}: {e}")
        
        # Fallback sempre disponível
        self.fallback_backend = 'text'
        
        print(f"🎨 Backends disponíveis: {list(self.backends.keys())}")
        print(f"🎯 Backend primário: {self.primary_backend}")
    
    def create_visualization(self, viz_type: str, data: Dict, 
                           config: Optional[Dict] = None,
                           backend: Optional[str] = None) -> str:
        """Cria visualização com fallback automático"""
        
        config = config or {}
        target_backend = backend or self.primary_backend
        
        # Tentar backend preferido
        if target_backend in self.backends:
            try:
                method_name = f"create_{viz_type}"
                if hasattr(self.backends[target_backend], method_name):
                    method = getattr(self.backends[target_backend], method_name)
                    result = method(data, config)
                    if result:
                        print(f"✅ Visualização '{viz_type}' criada com {target_backend}")
                        return result
            except Exception as e:
                print(f"⚠️ Erro no backend {target_backend}: {e}")
        
        # Fallback para text
        if self.fallback_backend in self.backends:
            try:
                method_name = f"create_{viz_type}"
                method = getattr(self.backends[self.fallback_backend], method_name)
                result = method(data, config)
                print(f"🔄 Fallback: Visualização '{viz_type}' criada com texto")
                return result
            except Exception as e:
                print(f"❌ Erro no fallback: {e}")
        
        return ""
    
    def get_available_backends(self) -> List[str]:
        """Retorna backends disponíveis"""
        return list(self.backends.keys())
    
    def set_primary_backend(self, backend_name: str):
        """Define backend primário"""
        if backend_name in self.backends:
            self.primary_backend = backend_name
            print(f"🎯 Backend primário alterado para: {backend_name}")
        else:
            print(f"❌ Backend '{backend_name}' não disponível")


# Função de conveniência
def create_visualization_manager(config: Optional[Dict] = None) -> ScalableVisualizationManager:
    """Cria gerenciador de visualizações"""
    return ScalableVisualizationManager(config)