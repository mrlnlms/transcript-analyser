"""
Template para criar novos gráficos
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseChart
from typing import Dict

class TemplateChart(BaseChart):
    """
    Template para novos gráficos
    
    Para criar um novo gráfico:
    1. Copie este arquivo: cp _template_chart.py meu_chart.py
    2. Renomeie a classe: TemplateChart -> MeuChart
    3. Implemente o método create()
    4. Crie arquivo de config em config/visualization_configs/
    """
    
    def create(self, data: Dict, output_path: str) -> str:
        """
        Implementar criação do gráfico aqui
        
        Args:
            data: Dados da análise para visualizar
            output_path: Caminho onde salvar o gráfico
            
        Returns:
            Caminho do arquivo criado
        """
        # Ajustar para tamanho dos dados
        adjustments = self.adjust_for_data_size(data)
        
        # Escolher backend baseado na configuração
        if self.backend == "plotly":
            return self._create_plotly(data, output_path, adjustments)
        elif self.backend == "matplotlib":
            return self._create_matplotlib(data, output_path, adjustments)
        else:
            return self._create_text(data, output_path, adjustments)
    
    def _create_plotly(self, data: Dict, output_path: str, adjustments: Dict) -> str:
        """Implementar versão Plotly do gráfico"""
        # Sua implementação Plotly aqui
        import plotly.graph_objects as go
        
        fig = go.Figure()
        # Adicionar seus dados ao gráfico
        
        html_path = output_path.replace('.png', '.html')
        fig.write_html(html_path)
        return html_path
    
    def _create_matplotlib(self, data: Dict, output_path: str, adjustments: Dict) -> str:
        """Implementar versão Matplotlib do gráfico"""
        # Sua implementação Matplotlib aqui
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        # Criar seu gráfico
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return output_path
    
    def _create_text(self, data: Dict, output_path: str, adjustments: Dict) -> str:
        """Implementar versão texto do gráfico (fallback)"""
        # Sua implementação texto aqui
        text_output = f"📊 {self.get_name()}\n"
        text_output += "=" * 40 + "\n"
        # Adicionar representação textual dos dados
        
        text_path = output_path.replace('.png', '.txt').replace('.html', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        return text_path
