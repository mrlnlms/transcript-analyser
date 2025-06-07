import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
import networkx as nx
import pandas as pd
from datetime import datetime
from scipy.interpolate import make_interp_spline
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo global aprimorado
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.facecolor'] = '#f8f9fa'
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.1
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

class InterviewVisualizerV2:
    """Versão 2.0 do Visualizador de Entrevistas com melhorias e correções"""
    
    def __init__(self):
        # Paleta de cores profissional expandida
        self.colors = {
            'primary': '#2E86AB',      # Azul principal
            'secondary': '#A23B72',    # Rosa/roxo
            'positive': '#2ECC71',     # Verde positivo
            'negative': '#E74C3C',     # Vermelho negativo
            'neutral': '#95A5A6',      # Cinza neutro
            'warning': '#F39C12',      # Laranja alerta
            'dark': '#2C3E50',         # Azul escuro
            'light': '#ECF0F1',        # Cinza claro
            'accent': '#9B59B6',       # Roxo accent
            'info': '#3498DB'          # Azul info
        }
        
        # Gradientes para sentimentos expandidos
        self.sentiment_colors = {
            'muito_negativo': '#8B0000',
            'negativo': '#E74C3C',
            'levemente_negativo': '#F39C12',
            'neutro': '#95A5A6',
            'levemente_positivo': '#3498DB',
            'positivo': '#2ECC71',
            'muito_positivo': '#27AE60'
        }
        
        # Configurações de design
        self.fig_dpi = 300
        self.fig_pad = 0.1
    
    def validate_topics(self, topics, topic_distribution):
        """Valida e sugere número ótimo de tópicos"""
        # Verificar tópicos com peso muito baixo
        low_weight_topics = sum(1 for weight in topic_distribution if weight < 0.05)
        
        suggestions = []
        if low_weight_topics > 0:
            suggested_n = len(topics) - low_weight_topics
            suggestions.append(f"⚠️ {low_weight_topics} tópico(s) com peso < 5%. "
                             f"Sugestão: usar {suggested_n} tópicos")
        
        # Calcular entropia da distribuição
        entropy = -sum(p * np.log(p) for p in topic_distribution if p > 0)
        max_entropy = np.log(len(topics))
        entropy_ratio = entropy / max_entropy
        
        if entropy_ratio < 0.6:
            suggestions.append(f"📊 Distribuição muito concentrada (entropia: {entropy_ratio:.2f}). "
                             "Alguns tópicos dominam demais")
        
        return suggestions
    
    def create_unified_emotional_timeline(self, narrative_blocks, temporal_analysis, 
                                        save_path='unified_timeline.png'):
        """Cria timeline emocional unificada com design premium"""
        # Criar figura com proporções customizadas
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(4, 1, height_ratios=[3, 1, 1, 0.5], hspace=0.15)
        
        # Eixo principal - Jornada emocional
        ax_main = fig.add_subplot(gs[0])
        ax_hesitation = fig.add_subplot(gs[1], sharex=ax_main)
        ax_phases = fig.add_subplot(gs[2], sharex=ax_main)
        ax_summary = fig.add_subplot(gs[3])
        ax_summary.axis('off')
        
        # Preparar dados
        times = []
        sentiments = []
        labels = []
        colors = []
        hesitations = []
        
        for block in narrative_blocks:
            time_range = block['time_range']
            start, end = map(int, time_range.replace(' min', '').split('-'))
            mid_time = (start + end) / 2
            times.append(mid_time)
            sentiments.append(block['sentiment'])
            labels.append(f"B{block['block_number']}")
            hesitations.append(block['hesitations'])
            
            # Cor baseada no sentimento
            if block['sentiment'] < -0.7:
                colors.append(self.sentiment_colors['muito_negativo'])
            elif block['sentiment'] < -0.4:
                colors.append(self.sentiment_colors['negativo'])
            elif block['sentiment'] < -0.1:
                colors.append(self.sentiment_colors['levemente_negativo'])
            elif block['sentiment'] < 0.1:
                colors.append(self.sentiment_colors['neutro'])
            elif block['sentiment'] < 0.4:
                colors.append(self.sentiment_colors['levemente_positivo'])
            elif block['sentiment'] < 0.7:
                colors.append(self.sentiment_colors['positivo'])
            else:
                colors.append(self.sentiment_colors['muito_positivo'])
        
        # 1. GRÁFICO PRINCIPAL - Jornada Emocional
        ax_main.set_title('🎭 Jornada Emocional Completa da Entrevista', 
                         fontsize=24, fontweight='bold', pad=20)
        
        # Criar interpolação suave
        if len(times) > 3:
            times_smooth = np.linspace(min(times), max(times), 300)
            spl = make_interp_spline(times, sentiments, k=3)
            sentiments_smooth = spl(times_smooth)
            
            # Plotar linha suave com gradiente
            ax_main.plot(times_smooth, sentiments_smooth, color=self.colors['primary'], 
                        linewidth=3, alpha=0.8, label='Tendência emocional')
            
            # Área preenchida com gradiente
            ax_main.fill_between(times_smooth, 0, sentiments_smooth, 
                               where=(sentiments_smooth >= 0), 
                               color=self.colors['positive'], alpha=0.2, 
                               label='Sentimento positivo')
            ax_main.fill_between(times_smooth, 0, sentiments_smooth, 
                               where=(sentiments_smooth < 0), 
                               color=self.colors['negative'], alpha=0.2, 
                               label='Sentimento negativo')
        
        # Plotar pontos com animação visual
        for i, (t, s, l, c) in enumerate(zip(times, sentiments, labels, colors)):
            # Círculo principal
            ax_main.scatter(t, s, color=c, s=300, zorder=5, 
                          edgecolors='white', linewidth=3, alpha=0.9)
            
            # Halo para momentos críticos
            if abs(s) > 0.7:
                ax_main.scatter(t, s, color=c, s=600, alpha=0.3, zorder=4)
            
            # Emoji e label
            emoji = narrative_blocks[i]['sentiment_emoji']
            offset_y = 25 if s >= 0 else -30
            ax_main.annotate(f'{emoji}\n{l}', (t, s), 
                           xytext=(0, offset_y), textcoords='offset points',
                           ha='center', fontsize=11, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor='white', alpha=0.8, edgecolor=c))
        
        # Adicionar zonas de sentimento
        ax_main.axhspan(0.7, 1.2, alpha=0.05, color=self.colors['positive'])
        ax_main.axhspan(-0.7, -1.2, alpha=0.05, color=self.colors['negative'])
        ax_main.axhline(y=0, color='black', linestyle='-', alpha=0.2, linewidth=1)
        
        # Configurar eixo principal
        ax_main.set_ylabel('Sentimento', fontsize=14)
        ax_main.set_ylim(-1.3, 1.3)
        ax_main.grid(True, alpha=0.1)
        ax_main.legend(loc='upper right', fontsize=11, framealpha=0.9)
        
        # 2. GRÁFICO DE HESITAÇÕES
        bars = ax_hesitation.bar(times, hesitations, width=3, 
                               color=self.colors['warning'], alpha=0.7, 
                               edgecolor='white', linewidth=1)
        
        # Destacar picos de hesitação
        mean_hes = np.mean(hesitations)
        std_hes = np.std(hesitations)
        threshold = mean_hes + std_hes
        
        for bar, hes, time in zip(bars, hesitations, times):
            if hes > threshold:
                bar.set_color(self.colors['negative'])
                bar.set_alpha(0.8)
                ax_hesitation.annotate(f'{hes}', (time, hes), 
                                     xytext=(0, 3), textcoords='offset points',
                                     ha='center', fontsize=9, fontweight='bold')
        
        ax_hesitation.axhline(y=mean_hes, color='red', linestyle='--', 
                            alpha=0.5, linewidth=1, label=f'Média: {mean_hes:.0f}')
        ax_hesitation.set_ylabel('Hesitações', fontsize=12)
        ax_hesitation.set_title('💭 Intensidade de Processamento Cognitivo', 
                              fontsize=14, pad=10)
        ax_hesitation.grid(True, axis='y', alpha=0.1)
        ax_hesitation.legend(loc='upper right', fontsize=10)
        
        # 3. FASES DA ENTREVISTA
        # Calcular limites das fases
        total_time = max(times)
        phase_limits = [0, total_time/3, 2*total_time/3, total_time]
        phase_names = ['INÍCIO', 'DESENVOLVIMENTO', 'CONCLUSÃO']
        phase_colors = [self.colors['info'], self.colors['primary'], self.colors['accent']]
        
        for i, (start, end, name, color) in enumerate(zip(phase_limits[:-1], 
                                                         phase_limits[1:], 
                                                         phase_names, 
                                                         phase_colors)):
            # Calcular sentimento médio da fase
            phase_sentiments = [s for t, s in zip(times, sentiments) 
                              if start <= t <= end]
            if phase_sentiments:
                avg_sentiment = np.mean(phase_sentiments)
                sentiment_text = f"{avg_sentiment:+.2f}"
                
                # Desenhar retângulo da fase
                rect = Rectangle((start, -0.5), end-start, 1, 
                               facecolor=color, alpha=0.3, edgecolor=color)
                ax_phases.add_patch(rect)
                
                # Adicionar texto
                ax_phases.text((start+end)/2, 0, f'{name}\n{sentiment_text}', 
                             ha='center', va='center', fontsize=12, 
                             fontweight='bold', color='white',
                             bbox=dict(boxstyle='round,pad=0.5', 
                                     facecolor=color, alpha=0.8))
        
        ax_phases.set_ylim(-0.6, 0.6)
        ax_phases.set_xlabel('Tempo (minutos)', fontsize=14)
        ax_phases.set_title('📊 Divisão Temporal e Sentimento Médio por Fase', 
                          fontsize=14, pad=10)
        ax_phases.grid(True, axis='x', alpha=0.1)
        
        # 4. RESUMO ESTATÍSTICO
        # Calcular métricas globais
        global_sentiment = np.mean(sentiments)
        sentiment_variance = np.std(sentiments)
        total_hesitations = sum(hesitations)
        emotional_range = max(sentiments) - min(sentiments)
        
        # Criar texto de resumo
        summary_text = (
            f"📈 MÉTRICAS GLOBAIS: "
            f"Sentimento Global: {global_sentiment:+.2f} | "
            f"Variância: {sentiment_variance:.2f} | "
            f"Amplitude Emocional: {emotional_range:.2f} | "
            f"Total de Hesitações: {total_hesitations}"
        )
        
        ax_summary.text(0.5, 0.5, summary_text, ha='center', va='center',
                       fontsize=14, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.8', 
                               facecolor=self.colors['light'], 
                               edgecolor=self.colors['primary'], 
                               linewidth=2))
        
        # Ajustes finais
        plt.suptitle('Análise Temporal Integrada', fontsize=26, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.fig_dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
        print(f"✅ Timeline unificada salva em: {save_path}")
    
    def create_enhanced_concept_network(self, concept_network, save_path='concept_network_v2.png'):
        """Cria mapa de rede aprimorado com melhor visualização"""
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Criar grafo
        G = nx.Graph()
        
        # Adicionar edges com peso e sentimento
        all_concepts = set()
        edge_sentiments = {}
        
        for conn in concept_network[:20]:  # Top 20 conexões
            concept1, concept2 = conn['concept1'], conn['concept2']
            all_concepts.add(concept1)
            all_concepts.add(concept2)
            
            G.add_edge(concept1, concept2, 
                      weight=conn['strength'],
                      sentiment=conn['sentiment'])
            edge_sentiments[(concept1, concept2)] = conn['sentiment']
        
        # Layout otimizado
        pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
        
        # Calcular centralidade para tamanhos
        centrality = nx.degree_centrality(G)
        betweenness = nx.betweenness_centrality(G)
        
        # Combinar métricas para tamanho do nó
        node_sizes = []
        for node in G.nodes():
            size = (centrality[node] + betweenness[node]) * 2000 + 500
            node_sizes.append(size)
        
        # Desenhar edges com cores baseadas em sentimento
        for (u, v, data) in G.edges(data=True):
            sentiment = data['sentiment']
            weight = data['weight']
            
            # Cor baseada no sentimento
            if sentiment > 0.2:
                edge_color = self.colors['positive']
            elif sentiment < -0.2:
                edge_color = self.colors['negative']
            else:
                edge_color = self.colors['neutral']
            
            # Desenhar edge
            nx.draw_networkx_edges(G, pos, [(u, v)], 
                                 width=weight/10 + 1, 
                                 alpha=0.6, 
                                 edge_color=edge_color,
                                 style='solid' if abs(sentiment) > 0.2 else 'dashed')
        
        # Desenhar nós com gradiente de cor
        node_colors = []
        for node in G.nodes():
            # Cor baseada na centralidade
            if centrality[node] > 0.3:
                node_colors.append(self.colors['primary'])
            elif centrality[node] > 0.2:
                node_colors.append(self.colors['secondary'])
            else:
                node_colors.append(self.colors['info'])
        
        nx.draw_networkx_nodes(G, pos, 
                             node_size=node_sizes,
                             node_color=node_colors,
                             alpha=0.8,
                             edgecolors='white',
                             linewidths=2)
        
        # Labels com contraste otimizado
        for node, (x, y) in pos.items():
            ax.text(x, y, node, fontsize=11, fontweight='bold',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', 
                           facecolor='white', 
                           alpha=0.8,
                           edgecolor='gray'))
        
        # Título e legenda
        ax.set_title('🧠 Mapa Mental de Conceitos - Análise de Rede', 
                    fontsize=22, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Legenda aprimorada
        legend_elements = [
            mpatches.Patch(color=self.colors['positive'], label='Conexão positiva'),
            mpatches.Patch(color=self.colors['negative'], label='Conexão negativa'),
            mpatches.Patch(color=self.colors['neutral'], label='Conexão neutra'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=self.colors['primary'], 
                      markersize=15, label='Alta centralidade'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=self.colors['info'], 
                      markersize=10, label='Baixa centralidade')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
                 frameon=True, fancybox=True, shadow=True)
        
        # Adicionar estatísticas
        stats_text = (f"Nós: {G.number_of_nodes()} | "
                     f"Conexões: {G.number_of_edges()} | "
                     f"Densidade: {nx.density(G):.2f}")
        ax.text(0.02, 0.02, stats_text, transform=ax.transAxes,
               fontsize=11, bbox=dict(boxstyle='round', 
                                    facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.fig_dpi, bbox_inches='tight', 
                   facecolor='white')
        plt.show()
        print(f"✅ Rede de conceitos v2 salva em: {save_path}")
    
    def create_topic_hierarchy_fixed(self, topics, topic_distribution, 
                               save_path='topic_hierarchy_v2.png'):
        """Hierarquia de tópicos com texto preto e design aprimorado"""
        fig, ax = plt.subplots(figsize=(18, 14))
        
        # Criar grafo direcionado
        G = nx.DiGraph()
        
        # Validar tópicos primeiro
        suggestions = self.validate_topics(topics, topic_distribution)
        
        # Nó central
        G.add_node("TEMAS\nCENTRAIS", 
                size=4000, 
                color=self.colors['dark'],
                node_type='central')
        
        # Adicionar tópicos válidos (peso > 1%)
        valid_topics = [(i, topic, weight) for i, (topic, weight) in 
                    enumerate(zip(topics, topic_distribution)) if weight > 0.01]
        
        topic_nodes = []
        for i, topic, weight in valid_topics:
            # CORREÇÃO PARA NOMES DUPLICADOS
            # Usar display_name se disponível (criado pelo disambiguate_topics)
            topic_main_word = topic.get('display_name', topic['words'][0])
            
            # Nome do nó com formatação
            topic_name = f"Tópico {i+1}\n{topic_main_word}\n({weight:.0%})"
            topic_nodes.append(topic_name)
            
            # Tamanho baseado no peso
            node_size = max(500, 3000 * weight)
            
            # Cor baseada na importância
            if weight > 0.3:
                node_color = self.colors['primary']
            elif weight > 0.15:
                node_color = self.colors['secondary']
            else:
                node_color = self.colors['info']
            
            G.add_node(topic_name, 
                    size=node_size, 
                    color=node_color,
                    node_type='topic')
            G.add_edge("TEMAS\nCENTRAIS", topic_name, weight=weight)
            
            # Adicionar palavras principais
            for j, (word, score) in enumerate(zip(topic['words'][1:5], 
                                                topic['scores'][1:5])):
                word_node = f"{word}\n({score:.1f})"
                word_size = max(200, 800 * score/20)
                
                G.add_node(word_node, 
                        size=word_size, 
                        color=self.colors['accent'],
                        node_type='word')
                G.add_edge(topic_name, word_node, weight=score/20)
        
        # Layout hierárquico otimizado
        pos = nx.spring_layout(G, k=4, iterations=100, seed=42)
        
        # Ajustar posições para criar hierarquia visual
        for node in G.nodes():
            if G.nodes[node]['node_type'] == 'central':
                pos[node] = (0, 0)
            elif G.nodes[node]['node_type'] == 'topic':
                # Distribuir tópicos em círculo
                angle = 2 * np.pi * topic_nodes.index(node) / len(topic_nodes)
                radius = 2
                pos[node] = (radius * np.cos(angle), radius * np.sin(angle))
        
        # Desenhar edges com espessura variável
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        
        for (u, v), w in zip(edges, weights):
            # Garantir que alpha está no range válido [0, 1]
            edge_alpha = min(1.0, max(0.1, 0.3 + 0.5 * w))
            edge_width = max(0.5, min(10, 1 + 5 * w))
            
            nx.draw_networkx_edges(G, pos, [(u, v)], 
                                edge_color='gray', 
                                alpha=edge_alpha,
                                width=edge_width,
                                arrows=True, 
                                arrowsize=15,
                                arrowstyle='-|>',
                                connectionstyle="arc3,rad=0.1")
        
        # Desenhar nós
        for node in G.nodes():
            node_data = G.nodes[node]
            nx.draw_networkx_nodes(G, pos, [node], 
                                node_size=node_data['size'],
                                node_color=node_data['color'],
                                alpha=0.9,
                                edgecolors='white',
                                linewidths=3)
        
        # CORREÇÃO: Labels com texto preto e fundo adaptativo
        for node, (x, y) in pos.items():
            # Determinar cor do texto baseado no tipo de nó
            if G.nodes[node]['node_type'] == 'central':
                text_color = 'white'
                bbox_props = dict(boxstyle='round,pad=0.5', 
                                facecolor=self.colors['dark'], 
                                alpha=0.9,
                                edgecolor='white',
                                linewidth=2)
            else:
                text_color = 'black'  # TEXTO PRETO para melhor visibilidade
                bbox_props = dict(boxstyle='round,pad=0.4', 
                                facecolor='white', 
                                alpha=0.9,
                                edgecolor=G.nodes[node]['color'],
                                linewidth=2)
            
            ax.text(x, y, node, 
                fontsize=11 if G.nodes[node]['node_type'] != 'word' else 9,
                fontweight='bold',
                ha='center', 
                va='center',
                color=text_color,
                bbox=bbox_props)
        
        # Título e informações
        ax.set_title('🌳 Hierarquia de Temas da Entrevista - Análise Estrutural', 
                    fontsize=24, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Adicionar sugestões de validação
        if suggestions:
            suggestion_text = '\n'.join(suggestions)
            ax.text(0.02, 0.98, suggestion_text, 
                transform=ax.transAxes,
                fontsize=11, 
                va='top',
                bbox=dict(boxstyle='round,pad=0.5', 
                        facecolor=self.colors['warning'], 
                        alpha=0.7))
        
        # Legenda
        legend_elements = [
            mpatches.Circle((0, 0), 0.5, 
                        facecolor=self.colors['dark'], 
                        edgecolor='white',
                        linewidth=2,
                        label='Centro temático'),
            mpatches.Circle((0, 0), 0.5, 
                        facecolor=self.colors['primary'], 
                        edgecolor='white',
                        linewidth=2,
                        label='Tópico principal (>30%)'),
            mpatches.Circle((0, 0), 0.5, 
                        facecolor=self.colors['secondary'], 
                        edgecolor='white',
                        linewidth=2,
                        label='Tópico secundário (15-30%)'),
            mpatches.Circle((0, 0), 0.5, 
                        facecolor=self.colors['info'], 
                        edgecolor='white',
                        linewidth=2,
                        label='Tópico menor (<15%)'),
            mpatches.Circle((0, 0), 0.5, 
                        facecolor=self.colors['accent'], 
                        edgecolor='white',
                        linewidth=2,
                        label='Palavras-chave')
        ]
        
        ax.legend(handles=legend_elements, 
                loc='upper right', 
                fontsize=12,
                frameon=True,
                fancybox=True,
                shadow=True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.fig_dpi, bbox_inches='tight', 
                facecolor='white')
        plt.show()
        print(f"✅ Hierarquia v2 salva em: {save_path}")



# ================================================================
# PARTE 2: CORREÇÕES PARA interview_visualizer_v2.py
# ================================================================

# 2.1 SUBSTITUIR create_linguistic_patterns_fixed COMPLETO
    def create_linguistic_patterns_fixed(self, linguistic_patterns, save_path='linguistic_patterns_v2.png'):
        """Versão corrigida dos padrões linguísticos com dados reais por tópico"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.ravel()
        
        # 1. Razão Certeza vs Incerteza (OK - manter como está)
        ax = axes[0]
        labels = ['Certeza', 'Incerteza']
        values = [linguistic_patterns['certainty_count'], 
                linguistic_patterns['uncertainty_count']]
        colors = [self.colors['positive'], self.colors['negative']]
        
        bars = ax.bar(labels, values, color=colors, alpha=0.8, 
                    edgecolor='white', linewidth=2)
        ax.set_title('🎯 Certeza vs Incerteza', fontsize=16, fontweight='bold')
        ax.set_ylabel('Ocorrências', fontsize=12)
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                f'{value}', ha='center', fontweight='bold', fontsize=14)
        
        ratio = linguistic_patterns['uncertainty_count'] / (linguistic_patterns['certainty_count'] + 1)
        ax.text(0.5, max(values) * 0.8, f'Razão: {ratio:.1f}:1',
            transform=ax.transData, ha='center', fontsize=14,
            bbox=dict(boxstyle='round,pad=0.8', 
                    facecolor=self.colors['warning'], 
                    alpha=0.7, edgecolor='white', linewidth=2))
        
        # 2. Padrões por Tópico (OK - manter como está)
        ax = axes[1]
        if linguistic_patterns['topic_patterns']:
            topics = list(linguistic_patterns['topic_patterns'].keys())[:6]
            uncertainties = [linguistic_patterns['topic_patterns'][t]['uncertainty_score'] 
                        for t in topics]
            
            bar_colors = []
            for score in uncertainties:
                if score > 70:
                    bar_colors.append(self.colors['negative'])
                elif score > 50:
                    bar_colors.append(self.colors['warning'])
                else:
                    bar_colors.append(self.colors['positive'])
            
            topics_short = [t[:25] + '...' if len(t) > 25 else t for t in topics]
            
            bars = ax.barh(topics_short, uncertainties, color=bar_colors, 
                        alpha=0.8, edgecolor='white', linewidth=2)
            ax.set_xlabel('Score de Incerteza (%)', fontsize=12)
            ax.set_title('📊 Incerteza por Tópico', fontsize=16, fontweight='bold')
            ax.grid(axis='x', alpha=0.2)
            
            for bar, score in zip(bars, uncertainties):
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{score:.0f}%', va='center', fontweight='bold', fontsize=11)
            
            ax.axvline(x=50, color='red', linestyle='--', alpha=0.5, 
                    label='Limiar 50%')
            ax.legend()
        
        # 3. HESITAÇÕES POR TEMA - NOVA VERSÃO COM DADOS REAIS
        ax = axes[2]
        if linguistic_patterns['topic_patterns']:
            # Extrair dados REAIS de cada tópico
            topics_list = list(linguistic_patterns['topic_patterns'].keys())[:8]
            hesitations_real = []
            hesitations_per_100 = []
            total_words = []
            
            for topic in topics_list:
                patterns = linguistic_patterns['topic_patterns'][topic]
                hesitations_real.append(patterns.get('hesitations', 0))
                hesitations_per_100.append(patterns.get('hesitations_per_100', 0))
                total_words.append(patterns.get('total_words', 0))
            
            # Verificar se há variação real
            if len(set(hesitations_real)) > 1:
                # HÁ VARIAÇÃO - mostrar gráfico de linha
                x_pos = range(len(hesitations_real))
                
                # Plotar hesitações normalizadas (por 100 palavras)
                ax.plot(x_pos, hesitations_per_100, 
                    color=self.colors['primary'], linewidth=3, 
                    marker='o', markersize=10, 
                    markerfacecolor='white', 
                    markeredgecolor=self.colors['primary'], 
                    markeredgewidth=2,
                    label='Hesitações/100 palavras')
                
                # Adicionar valores reais como anotações
                for i, (h_real, h_norm, words) in enumerate(zip(hesitations_real, hesitations_per_100, total_words)):
                    ax.annotate(f'{h_real}\n({h_norm:.1f}%)\n{words}w', 
                            (i, h_norm), 
                            textcoords="offset points", 
                            xytext=(0, 20), 
                            ha='center', 
                            fontsize=9,
                            bbox=dict(boxstyle='round,pad=0.3', 
                                    facecolor='white', 
                                    alpha=0.8))
                
                # Configurações
                ax.set_xticks(x_pos)
                ax.set_xticklabels([f'T{i+1}' for i in range(len(hesitations_real))])
                ax.set_xlabel('Tópicos', fontsize=12)
                ax.set_ylabel('Hesitações por 100 palavras', fontsize=12)
                ax.set_title('💭 Padrão de Hesitações por Tema', fontsize=16, fontweight='bold')
                ax.grid(True, alpha=0.2)
                
                # Média e desvio padrão
                mean_h = np.mean(hesitations_per_100)
                std_h = np.std(hesitations_per_100)
                ax.axhline(y=mean_h, color='red', linestyle='--', 
                        alpha=0.5, linewidth=2,
                        label=f'Média: {mean_h:.1f}%')
                
                if std_h > 0:
                    ax.fill_between(x_pos, 
                                mean_h - std_h, 
                                mean_h + std_h, 
                                alpha=0.1, 
                                color='red')
                ax.legend()
                
            else:
                # SEM VARIAÇÃO - mostrar como barras
                ax.bar(range(len(hesitations_real)), hesitations_real,
                    color=self.colors['neutral'], alpha=0.7)
                ax.set_title('💭 Hesitações por Tema (sem variação significativa)', 
                        fontsize=16, fontweight='bold')
                ax.set_ylabel('Número de Hesitações')
                
                # Adicionar texto explicativo
                ax.text(0.5, 0.95, f'Todas as hesitações = {hesitations_real[0]}',
                    transform=ax.transAxes, ha='center', fontsize=12,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        # 4. COMPLEXIDADE DAS RESPOSTAS - VERSÃO CORRIGIDA
        ax = axes[3]
        if linguistic_patterns['topic_patterns']:
            topics = list(linguistic_patterns['topic_patterns'].keys())[:6]
            
            # Extrair dados REAIS
            response_times_real = []
            sentence_counts_real = []
            elaboration_levels = []
            topic_labels = []
            
            for t in topics:
                patterns = linguistic_patterns['topic_patterns'][t]
                response_times_real.append(patterns['response_time_estimate'])
                sentence_counts_real.append(patterns.get('sentence_count', 0))
                elaboration_levels.append(patterns['elaboration_level'])
                
                # Criar label mais curto
                if len(t) > 20:
                    if '+' in t:  # É um tópico composto
                        parts = t.split('+')
                        label = f"{parts[0][:10]}+{parts[1][:8]}"
                    else:
                        label = t[:18] + '...'
                else:
                    label = t
                topic_labels.append(label)
            
            # Verificar se há variação real nos tempos
            unique_times = len(set(response_times_real))
            
            if unique_times > 1:
                # HÁ VARIAÇÃO - mostrar gráfico duplo
                x_pos = np.arange(len(topics))
                width = 0.35
                
                # Normalizar sentenças para escala similar
                max_time = max(response_times_real) if response_times_real else 1
                sentence_scaled = [(s / max(sentence_counts_real)) * max_time * 0.7 
                                if sentence_counts_real else 0 
                                for s in sentence_counts_real]
                
                # Barras de tempo
                bars1 = ax.bar(x_pos - width/2, response_times_real, width,
                            label='Tempo de resposta (s)',
                            color=self.colors['primary'],
                            alpha=0.8)
                
                # Barras de sentenças
                bars2 = ax.bar(x_pos + width/2, sentence_scaled, width,
                            label=f'Sentenças (normalizado)',
                            color=self.colors['secondary'],
                            alpha=0.8)
                
                # Adicionar valores reais
                for i, (bar1, bar2, time, sent) in enumerate(zip(bars1, bars2, 
                                                                response_times_real, 
                                                                sentence_counts_real)):
                    # Tempo
                    ax.text(bar1.get_x() + bar1.get_width()/2, 
                        bar1.get_height() + 0.5,
                        f'{time:.0f}s', 
                        ha='center', fontsize=9, fontweight='bold')
                    # Sentenças
                    ax.text(bar2.get_x() + bar2.get_width()/2, 
                        bar2.get_height() + 0.5,
                        f'{sent}', 
                        ha='center', fontsize=9)
                    
                    # Elaboração como cor de fundo
                    elab = elaboration_levels[i]
                    if 'muito elaborado' in elab:
                        bg_color = self.colors['negative']
                        bg_alpha = 0.1
                    elif 'elaborado' in elab:
                        bg_color = self.colors['warning']
                        bg_alpha = 0.1
                    else:
                        bg_color = self.colors['positive']
                        bg_alpha = 0.1
                    
                    # Adicionar faixa colorida de fundo
                    ax.axvspan(i - 0.4, i + 0.4, alpha=bg_alpha, color=bg_color)
                
                # Configurações
                ax.set_xticks(x_pos)
                ax.set_xticklabels(topic_labels, rotation=45, ha='right', fontsize=10)
                ax.set_ylabel('Valores', fontsize=12)
                ax.set_title('⏱️ Complexidade das Respostas por Tópico', fontsize=16, fontweight='bold')
                ax.legend(loc='upper left', fontsize=10)
                ax.grid(axis='y', alpha=0.2)
                
                # Linhas de referência
                ax.axhline(y=40, color='red', linestyle='--', alpha=0.3)
                ax.axhline(y=25, color='orange', linestyle='--', alpha=0.3)
                ax.axhline(y=15, color='blue', linestyle='--', alpha=0.3)
                
            else:
                # SEM VARIAÇÃO - mostrar mensagem
                ax.text(0.5, 0.5, 
                    f'Todos os tópicos têm complexidade similar\n'
                    f'Tempo médio: {response_times_real[0]:.0f}s\n'
                    f'Elaboração: {elaboration_levels[0]}',
                    transform=ax.transAxes, ha='center', va='center',
                    fontsize=14,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
                ax.set_title('⏱️ Complexidade das Respostas (uniforme)', 
                        fontsize=16, fontweight='bold')
                ax.axis('off')
        
        # Título geral
        plt.suptitle('🎭 Análise de Padrões Linguísticos - Dados Reais por Tópico', 
                    fontsize=20, fontweight='bold')
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.fig_dpi, bbox_inches='tight')
        plt.show()
        print(f"✅ Padrões linguísticos v2 salvos em: {save_path}")
    
    def create_smart_dashboard(self, global_metrics, analysis_results, 
                             save_path='smart_dashboard.png'):
        """Dashboard inteligente com interpretações automáticas"""
        fig = plt.figure(figsize=(20, 14))
        
        # Grid customizado
        gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.25, 
                            height_ratios=[1.5, 1, 1.5, 0.8])
        
        # 1. Gauges principais (linha superior)
        ax_sentiment = fig.add_subplot(gs[0, 0])
        ax_coherence = fig.add_subplot(gs[0, 1])
        ax_openness = fig.add_subplot(gs[0, 2])
        
        # Criar gauges
        self._create_enhanced_gauge(ax_sentiment, 
                                  global_metrics['global_sentiment'], 
                                  'Sentimento Global', -1, 1,
                                  self.colors['primary'])
        
        self._create_enhanced_gauge(ax_coherence, 
                                  global_metrics['thematic_coherence'], 
                                  'Coerência Temática', 0, 1,
                                  self.colors['secondary'])
        
        self._create_enhanced_gauge(ax_openness, 
                                  global_metrics['emotional_openness'], 
                                  'Abertura Emocional', 0, 2,
                                  self.colors['accent'])
        
        # 2. Métricas comparativas (segunda linha)
        ax_bars = fig.add_subplot(gs[1, :])
        
        # Normalizar métricas para comparação
        metrics_data = {
            'Variância\nEmocional': global_metrics['sentiment_variance'],
            'Profundidade\nElaboração': min(1, global_metrics['elaboration_depth'] / 100),
            'Conflito\nInterno': global_metrics['internal_conflict_index'],
            'Hesitações\nMédias': min(1, analysis_results['linguistic_patterns']['total_hesitations'] / 1000),
            'Diversidade\nTemática': 1 - global_metrics['thematic_coherence']
        }
        
        # Criar gráfico de barras com cores condicionais
        bars = []
        colors = []
        for i, (name, value) in enumerate(metrics_data.items()):
            if value > 0.7:
                color = self.colors['negative']
            elif value > 0.4:
                color = self.colors['warning']
            else:
                color = self.colors['positive']
            colors.append(color)
            
            bar = ax_bars.bar(i, value, color=color, alpha=0.8,
                            edgecolor='white', linewidth=2)
            bars.append(bar)
            
            # Valor no topo
            ax_bars.text(i, value + 0.02, f'{value:.2f}', 
                       ha='center', fontweight='bold', fontsize=12)
        
        ax_bars.set_xticks(range(len(metrics_data)))
        ax_bars.set_xticklabels(metrics_data.keys(), fontsize=11)
        ax_bars.set_ylim(0, 1.2)
        ax_bars.set_ylabel('Valor Normalizado', fontsize=12)
        ax_bars.set_title('📊 Indicadores Comparativos', fontsize=16, fontweight='bold')
        ax_bars.grid(axis='y', alpha=0.2)
        
        # 3. Análise de padrões (terceira linha)
        ax_patterns = fig.add_subplot(gs[2, :])
        ax_patterns.axis('off')
        
        # Identificar padrões notáveis
        patterns = self._identify_patterns(global_metrics, analysis_results)
        
        # Criar visualização de padrões
        y_pos = 0.9
        for i, (pattern_type, pattern_info) in enumerate(patterns.items()):
            icon = pattern_info['icon']
            text = pattern_info['text']
            color = pattern_info['color']
            
            # Box com padrão
            bbox = FancyBboxPatch((0.05 + (i % 2) * 0.5, y_pos - (i // 2) * 0.25), 
                                0.4, 0.15,
                                boxstyle="round,pad=0.02",
                                facecolor=color,
                                alpha=0.2,
                                edgecolor=color,
                                linewidth=2)
            ax_patterns.add_patch(bbox)
            
            # Texto
            ax_patterns.text(0.07 + (i % 2) * 0.5, y_pos - (i // 2) * 0.25 + 0.075, 
                           f'{icon} {pattern_type}:\n{text}',
                           fontsize=12, 
                           va='center',
                           fontweight='bold')
        
        ax_patterns.set_xlim(0, 1)
        ax_patterns.set_ylim(0, 1)
        ax_patterns.set_title('🔍 Padrões Identificados', fontsize=16, fontweight='bold')
        
        # 4. Resumo executivo (linha inferior)
        ax_summary = fig.add_subplot(gs[3, :])
        ax_summary.axis('off')
        
        # Gerar resumo automático
        summary = self._generate_executive_summary(global_metrics, analysis_results)
        
        ax_summary.text(0.5, 0.5, summary, 
                      ha='center', va='center',
                      fontsize=14,
                      bbox=dict(boxstyle='round,pad=1', 
                              facecolor=self.colors['light'], 
                              edgecolor=self.colors['primary'],
                              linewidth=2))
        
        # Título principal
        plt.suptitle('🌐 Dashboard Analítico Inteligente', 
                    fontsize=26, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.fig_dpi, bbox_inches='tight', 
                   facecolor='white')
        plt.show()
        print(f"✅ Dashboard inteligente salvo em: {save_path}")
    
    def _create_enhanced_gauge(self, ax, value, title, min_val, max_val, color):
        """Cria gauge melhorado com gradiente e indicadores"""
        # Normalizar valor
        normalized = (value - min_val) / (max_val - min_val)
        
        # Criar arco com gradiente
        theta = np.linspace(np.pi, 0, 100)
        r_outer = 1
        r_inner = 0.7
        
        # Criar gradiente de cores
        if value < (min_val + max_val) / 2:
            colors = plt.cm.RdYlGn(np.linspace(0, 0.5, 100))
        else:
            colors = plt.cm.RdYlGn(np.linspace(0.5, 1, 100))
        
        # Desenhar arco segmentado
        for i in range(len(theta)-1):
            angles = [theta[i], theta[i+1], theta[i+1], theta[i]]
            radii = [r_inner, r_inner, r_outer, r_outer]
            
            x = [r * np.cos(a) for r, a in zip(radii, angles)]
            y = [r * np.sin(a) for r, a in zip(radii, angles)]
            
            ax.fill(x, y, color=colors[i], edgecolor='none')
        
        # Ponteiro
        angle = np.pi - normalized * np.pi
        pointer_length = 0.85
        pointer_x = pointer_length * np.cos(angle)
        pointer_y = pointer_length * np.sin(angle)
        
        # Sombra do ponteiro
        ax.plot([0, pointer_x], [0, pointer_y], 
               color='gray', linewidth=8, alpha=0.3)
        # Ponteiro principal
        ax.plot([0, pointer_x], [0, pointer_y], 
               color='black', linewidth=5)
        # Centro
        ax.scatter(0, 0, color='black', s=150, zorder=5)
        ax.scatter(0, 0, color='white', s=50, zorder=6)
        
        # Valor com formatação
        if abs(value) < 0.01:
            value_text = "0.00"
        else:
            value_text = f"{value:+.2f}" if min_val < 0 else f"{value:.2f}"
        
        ax.text(0, -0.4, value_text, 
               ha='center', va='center',
               fontsize=24, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', 
                       facecolor='white', 
                       edgecolor=color,
                       linewidth=2))
        
        # Título
        ax.text(0, 1.4, title, ha='center', va='center',
               fontsize=16, fontweight='bold')
        
        # Labels dos extremos
        ax.text(-1.2, -0.1, f'{min_val}', ha='center', fontsize=12)
        ax.text(1.2, -0.1, f'{max_val}', ha='center', fontsize=12)
        
        # Indicador de qualidade
        quality = ""
        if title == "Sentimento Global":
            if value > 0.3:
                quality = "Positivo"
            elif value < -0.3:
                quality = "Negativo"
            else:
                quality = "Neutro"
        elif title == "Coerência Temática":
            if value > 0.7:
                quality = "Alta"
            elif value > 0.4:
                quality = "Média"
            else:
                quality = "Baixa"
        elif title == "Abertura Emocional":
            if value > 1.5:
                quality = "Muito Alta"
            elif value > 0.8:
                quality = "Alta"
            else:
                quality = "Moderada"
        
        ax.text(0, -0.7, quality, ha='center', va='center',
               fontsize=14, style='italic', color=color)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-0.8, 1.5)
        ax.axis('off')
    
    def _identify_patterns(self, metrics, results):
        """Identifica padrões notáveis nos dados"""
        patterns = {}
        
        # Padrão emocional
        if metrics['global_sentiment'] > 0.3 and metrics['sentiment_variance'] < 0.5:
            patterns['Estabilidade Positiva'] = {
                'icon': '😊',
                'text': 'Emoções consistentemente positivas',
                'color': self.colors['positive']
            }
        elif metrics['sentiment_variance'] > 0.7:
            patterns['Montanha-Russa'] = {
                'icon': '🎢',
                'text': 'Alta volatilidade emocional',
                'color': self.colors['warning']
            }
        
        # Padrão de elaboração
        if metrics['elaboration_depth'] > 40:
            patterns['Hipereelaboração'] = {
                'icon': '📚',
                'text': 'Respostas extremamente detalhadas',
                'color': self.colors['info']
            }
        
        # Padrão de conflito
        if metrics['internal_conflict_index'] > 0.8:
            patterns['Conflito Interno'] = {
                'icon': '⚡',
                'text': 'Múltiplas contradições detectadas',
                'color': self.colors['negative']
            }
        
        # Padrão de coerência
        if metrics['thematic_coherence'] > 0.8:
            patterns['Foco Temático'] = {
                'icon': '🎯',
                'text': 'Narrativa altamente focada',
                'color': self.colors['primary']
            }
        
        return patterns
    
    def _generate_executive_summary(self, metrics, results):
        """Gera resumo executivo automático"""
        parts = []
        
        # Sentimento
        sentiment_desc = ""
        if metrics['global_sentiment'] > 0.3:
            sentiment_desc = "predominantemente POSITIVA"
        elif metrics['global_sentiment'] < -0.3:
            sentiment_desc = "predominantemente NEGATIVA"
        else:
            sentiment_desc = "EQUILIBRADA"
        
        parts.append(f"📊 Entrevista {sentiment_desc} ({metrics['global_sentiment']:+.2f})")
        
        # Variabilidade
        if metrics['sentiment_variance'] > 0.7:
            parts.append("com ALTA variabilidade emocional")
        else:
            parts.append("com estabilidade emocional")
        
        # Temas
        n_topics = len([w for w in results['topic_distribution'] if w > 0.05])
        parts.append(f"• {n_topics} temas principais identificados")
        
        # Elaboração
        if metrics['elaboration_depth'] > 30:
            parts.append("• Participante MUITO detalhista")
        elif metrics['elaboration_depth'] > 20:
            parts.append("• Elaboração moderada")
        else:
            parts.append("• Respostas concisas")
        
        # Coerência
        coherence_level = "alta" if metrics['thematic_coherence'] > 0.7 else "moderada"
        parts.append(f"• Coerência narrativa {coherence_level}")
        
        return " | ".join(parts)
    
    def generate_all_visualizations_v2(self, analysis_results, output_dir='./visualizations_v2/'):
        """Gera todas as visualizações versão 2.0"""
        import os
        
        # Criar diretório
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print("\n🎨 GERANDO VISUALIZAÇÕES 2.0...")
        print("=" * 60)
        
        # 1. Timeline Unificada
        print("\n1️⃣ Gerando timeline emocional unificada...")
        self.create_unified_emotional_timeline(
            analysis_results['narrative_blocks'],
            analysis_results['temporal_analysis'],
            save_path=os.path.join(output_dir, 'unified_timeline.png')
        )
        
        # 2. Hierarquia Corrigida
        print("\n2️⃣ Gerando hierarquia de tópicos v2...")
        self.create_topic_hierarchy_fixed(
            analysis_results['topics'],
            analysis_results['topic_distribution'],
            save_path=os.path.join(output_dir, 'topic_hierarchy_v2.png')
        )
        
        # 3. Rede Aprimorada
        print("\n3️⃣ Gerando rede de conceitos v2...")
        self.create_enhanced_concept_network(
            analysis_results['concept_network'],
            save_path=os.path.join(output_dir, 'concept_network_v2.png')
        )
        
        # 4. Padrões Linguísticos Corrigidos
        print("\n4️⃣ Gerando padrões linguísticos v2...")
        self.create_linguistic_patterns_fixed(
            analysis_results['linguistic_patterns'],
            save_path=os.path.join(output_dir, 'linguistic_patterns_v2.png')
        )
        
        # 5. Dashboard Inteligente
        print("\n5️⃣ Gerando dashboard inteligente...")
        self.create_smart_dashboard(
            analysis_results['global_metrics'],
            analysis_results,
            save_path=os.path.join(output_dir, 'smart_dashboard.png')
        )
        
        # 6. Validação de Tópicos
        suggestions = self.validate_topics(
            analysis_results['topics'],
            analysis_results['topic_distribution']
        )
        
        if suggestions:
            print("\n⚠️ SUGESTÕES DE OTIMIZAÇÃO:")
            for suggestion in suggestions:
                print(f"   {suggestion}")
        
        print(f"\n✅ TODAS AS VISUALIZAÇÕES 2.0 SALVAS EM: {output_dir}")
        print("=" * 60)
        
        return True


# Função auxiliar para usar com o analisador original
def enhance_analysis_with_v2_visualizations(analysis_results):
    """Aplica visualizações v2 aos resultados da análise"""
    visualizer = InterviewVisualizerV2()
    visualizer.generate_all_visualizations_v2(analysis_results)
    return analysis_results


if __name__ == "__main__":
    print("🎨 Interview Visualizer 2.0")
    print("✨ Versão com todas as correções e melhorias implementadas")
    print("\nComo usar:")
    print("1. from interview_visualizer_v2 import InterviewVisualizerV2")
    print("2. visualizer = InterviewVisualizerV2()")
    print("3. visualizer.generate_all_visualizations_v2(analysis_results)")
    print("\n📊 Novas funcionalidades:")
    print("   - Timeline unificada com 3 níveis")
    print("   - Correção dos padrões linguísticos")
    print("   - Texto preto na hierarquia")
    print("   - Validação automática de tópicos")
    print("   - Dashboard inteligente com interpretações")
    print("   - Design premium em todas as visualizações")