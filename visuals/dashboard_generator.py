"""📊 Gerador de dashboards e visualizações"""

import matplotlib
matplotlib.use('Agg')  # Para ambientes sem display
import matplotlib.pyplot as plt
import os
from pathlib import Path
from typing import Dict, Any


class DashboardGenerator:
    """Gerador de visualizações e dashboards"""
    
    def __init__(self, config):
        self.config = config
        print("📊 DashboardGenerator inicializado")
    
    def generate_complete_dashboard(self, result: Dict[str, Any], output_dir: str) -> bool:
        """Gera dashboard completo para um resultado"""
        
        print(f"📈 Gerando dashboard em: {output_dir}")
        
        try:
            # Criar diretório se não existe
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Gerar gráfico simples de exemplo
            self._create_sample_plot(result, output_dir)
            
            print(f"✅ Dashboard gerado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao gerar dashboard: {e}")
            return False
    
    def generate_comparative_dashboard(self, comparison_results: Dict, output_dir: str) -> bool:
        """Gera dashboard comparativo"""
        
        print(f"📊 Gerando dashboard comparativo em: {output_dir}")
        
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Gerar visualizações comparativas
            self._create_comparison_plots(comparison_results, output_dir)
            
            print(f"✅ Dashboard comparativo gerado")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao gerar dashboard comparativo: {e}")
            return False
    
    def _create_sample_plot(self, result: Dict, output_dir: str):
        """Cria gráfico de exemplo"""
        
        try:
            # Gráfico simples de métricas
            metrics = result['global_metrics']
            
            fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            
            labels = ['Sentimento Global', 'Coerência Temática', 'Abertura Emocional']
            values = [metrics['global_sentiment'], metrics['thematic_coherence'], metrics['emotional_openness']]
            colors = ['lightblue', 'lightgreen', 'lightcoral']
            
            bars = ax.bar(labels, values, color=colors, alpha=0.7)
            ax.set_title(f'Métricas Globais - {result["filename"]}', fontsize=14, fontweight='bold')
            ax.set_ylabel('Valores')
            ax.grid(axis='y', alpha=0.3)
            
            # Adicionar valores nas barras
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{value:.2f}', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig(Path(output_dir) / 'metricas_globais.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📊 Gráfico salvo: metricas_globais.png")
            
        except Exception as e:
            print(f"⚠️ Erro ao gerar gráfico: {e}")
    
    def _create_comparison_plots(self, comparison: Dict, output_dir: str):
        """Cria gráficos comparativos"""
        
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Gráfico 1: Métricas médias
            metrics = ['Sentimento Médio', 'Coerência Média']
            values = [comparison['avg_sentiment'], comparison['avg_coherence']]
            
            ax1.bar(metrics, values, color=['skyblue', 'lightgreen'], alpha=0.7)
            ax1.set_title('Métricas Médias dos Projetos', fontweight='bold')
            ax1.set_ylabel('Valores')
            ax1.grid(axis='y', alpha=0.3)
            
            # Gráfico 2: Resumo
            ax2.text(0.1, 0.7, f"Projetos Comparados: {comparison['projects_compared']}", 
                    fontsize=12, transform=ax2.transAxes)
            ax2.text(0.1, 0.5, f"Total de Arquivos: {comparison['total_files']}", 
                    fontsize=12, transform=ax2.transAxes)
            ax2.text(0.1, 0.3, f"Sentimento Médio: {comparison['avg_sentiment']:.2f}", 
                    fontsize=12, transform=ax2.transAxes)
            ax2.text(0.1, 0.1, f"Coerência Média: {comparison['avg_coherence']:.2f}", 
                    fontsize=12, transform=ax2.transAxes)
            ax2.set_title('Resumo da Comparação', fontweight='bold')
            ax2.axis('off')
            
            plt.tight_layout()
            plt.savefig(Path(output_dir) / 'comparacao_projetos.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📊 Gráfico comparativo salvo: comparacao_projetos.png")
            
        except Exception as e:
            print(f"⚠️ Erro ao gerar gráfico comparativo: {e}")
