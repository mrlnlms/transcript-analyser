import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
import networkx as nx
from matplotlib.patches import FancyBboxPatch
from matplotlib.animation import FuncAnimation
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo global
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = '#f8f9fa'
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

class InterviewVisualizer:
    """Classe para criar visualizações da análise de entrevistas"""
    
    def __init__(self):
        # Paleta de cores profissional
        self.colors = {
            'primary': '#2E86AB',      # Azul principal
            'secondary': '#A23B72',    # Rosa/roxo
            'positive': '#2ECC71',     # Verde positivo
            'negative': '#E74C3C',     # Vermelho negativo
            'neutral': '#95A5A6',      # Cinza neutro
            'warning': '#F39C12',      # Laranja alerta
            'dark': '#2C3E50',         # Azul escuro
            'light': '#ECF0F1'         # Cinza claro
        }
        
        # Gradientes para sentimentos
        self.sentiment_colors = {
            'muito_negativo': '#8B0000',
            'negativo': '#E74C3C',
            'levemente_negativo': '#F39C12',
            'neutro': '#95A5A6',
            'levemente_positivo': '#3498DB',
            'positivo': '#2ECC71',
            'muito_positivo': '#27AE60'
        }
    
    def create_emotional_timeline(self, narrative_blocks, save_path='emotional_timeline.png'):
        """Cria linha do tempo emocional estilo gráfico de economia"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), 
                                       gridspec_kw={'height_ratios': [3, 1]})
        
        # Preparar dados
        times = []
        sentiments = []
        labels = []
        colors = []
        
        for block in narrative_blocks:
            # Extrair tempo médio do range
            time_range = block['time_range']
            start, end = map(int, time_range.replace(' min', '').split('-'))
            mid_time = (start + end) / 2
            times.append(mid_time)
            sentiments.append(block['sentiment'])
            labels.append(f"B{block['block_number']}")
            
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
        
        # Gráfico principal - Linha do tempo emocional
        ax1.set_title('📈 Jornada Emocional da Entrevista', fontsize=20, fontweight='bold', pad=20)
        
        # Criar interpolação suave
        from scipy.interpolate import make_interp_spline
        times_smooth = np.linspace(min(times), max(times), 300)
        spl = make_interp_spline(times, sentiments, k=3)
        sentiments_smooth = spl(times_smooth)
        
        # Plotar linha suave
        ax1.plot(times_smooth, sentiments_smooth, color=self.colors['primary'], 
                linewidth=3, alpha=0.8, label='Tendência emocional')
        
        # Adicionar área preenchida
        ax1.fill_between(times_smooth, 0, sentiments_smooth, 
                        where=(sentiments_smooth >= 0), 
                        color=self.colors['positive'], alpha=0.3, label='Sentimento positivo')
        ax1.fill_between(times_smooth, 0, sentiments_smooth, 
                        where=(sentiments_smooth < 0), 
                        color=self.colors['negative'], alpha=0.3, label='Sentimento negativo')
        
        # Plotar pontos
        for i, (t, s, l, c) in enumerate(zip(times, sentiments, labels, colors)):
            ax1.scatter(t, s, color=c, s=200, zorder=5, edgecolors='white', linewidth=2)
            
            # Adicionar emoji e label
            emoji = narrative_blocks[i]['sentiment_emoji']
            ax1.annotate(f'{emoji}\n{l}', (t, s), 
                        xytext=(0, 20 if s >= 0 else -25), 
                        textcoords='offset points',
                        ha='center', fontsize=10, fontweight='bold')
        
        # Linha zero
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
        
        # Configurar eixos
        ax1.set_xlabel('Tempo (minutos)', fontsize=14)
        ax1.set_ylabel('Sentimento', fontsize=14)
        ax1.set_ylim(-1.2, 1.2)
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper right', fontsize=12)
        
        # Adicionar zonas de sentimento
        ax1.axhspan(0.7, 1.2, alpha=0.1, color=self.colors['positive'], label='Zona muito positiva')
        ax1.axhspan(-0.7, -1.2, alpha=0.1, color=self.colors['negative'], label='Zona muito negativa')
        
        # Gráfico secundário - Volume de hesitações
        hesitations = [block['hesitations'] for block in narrative_blocks]
        ax2.bar(times, hesitations, width=3, color=self.colors['warning'], alpha=0.7)
        ax2.set_xlabel('Tempo (minutos)', fontsize=14)
        ax2.set_ylabel('Hesitações', fontsize=12)
        ax2.set_title('💭 Intensidade de Processamento (Hesitações)', fontsize=14, pad=10)
        ax2.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✅ Gráfico salvo em: {save_path}")
    
    def create_topic_hierarchical_tree(self, topics, topic_distribution, save_path='topic_hierarchy.png'):
        """Cria visualização hierárquica dos tópicos usando networkx"""
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Criar grafo
        G = nx.DiGraph()
        
        # Nó central
        G.add_node("TEMAS\nCENTRAIS", size=3000, color=self.colors['dark'])
        
        # Adicionar nós de tópicos
        topic_nodes = []
        for i, (topic, weight) in enumerate(zip(topics, topic_distribution)):
            topic_name = f"Tópico {i+1}\n{topic['words'][0]}\n({weight:.0%})"
            topic_nodes.append(topic_name)
            G.add_node(topic_name, size=2000 * weight, color=self.colors['primary'])
            G.add_edge("TEMAS\nCENTRAIS", topic_name, weight=weight)
            
            # Adicionar palavras do tópico
            for j, (word, score) in enumerate(zip(topic['words'][1:5], topic['scores'][1:5])):
                word_node = f"{word}\n({score:.1f})"
                G.add_node(word_node, size=500 * score/10, color=self.colors['secondary'])
                G.add_edge(topic_name, word_node, weight=score/10)
        
        # Layout hierárquico
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Desenhar edges
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.4, 
                              width=[w*3 for w in weights], 
                              arrows=True, arrowsize=20, arrowstyle='->')
        
        # Desenhar nodes
        node_sizes = [G.nodes[node].get('size', 1000) for node in G.nodes()]
        node_colors = [G.nodes[node].get('color', self.colors['neutral']) for node in G.nodes()]
        
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                              node_color=node_colors, alpha=0.8)
        
        # Adicionar labels
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=10, 
                               font_weight='bold', font_color='white')
        
        ax.set_title('🌳 Hierarquia de Temas da Entrevista', 
                    fontsize=22, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Adicionar legenda
        legend_elements = [
            mpatches.Circle((0, 0), 0.5, facecolor=self.colors['dark'], 
                          label='Centro temático'),
            mpatches.Circle((0, 0), 0.5, facecolor=self.colors['primary'], 
                          label='Tópicos principais'),
            mpatches.Circle((0, 0), 0.5, facecolor=self.colors['secondary'], 
                          label='Palavras-chave')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        print(f"✅ Gráfico salvo em: {save_path}")
    
    def create_concept_network(self, concept_network, save_path='concept_network.png'):
        """Cria mapa de rede de conceitos"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Criar grafo
        G = nx.Graph()
        
        # Adicionar nós e edges
        all_concepts = set()
        for conn in concept_network[:15]:  # Top 15 conexões
            all_concepts.add(conn['concept1'])
            all_concepts.add(conn['concept2'])
            G.add_edge(conn['concept1'], conn['concept2'], 
                      weight=conn['strength'],
                      sentiment=conn['sentiment'])
        
        # Layout circular com ajustes
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Desenhar edges com cores baseadas em sentimento
        for edge in G.edges(data=True):
            sentiment = edge[2]['sentiment']
            weight = edge[2]['weight']
            
            if sentiment > 0.2:
                color = self.colors['positive']
            elif sentiment < -0.2:
                color = self.colors['negative']
            else:
                color = self.colors['neutral']
            
            nx.draw_networkx_edges(G, pos, [(edge[0], edge[1])], 
                                  width=weight/5, alpha=0.6, edge_color=color)
        
        # Calcular centralidade para tamanho dos nós
        centrality = nx.degree_centrality(G)
        node_sizes = [3000 * centrality[node] + 1000 for node in G.nodes()]
        
        # Desenhar nós
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                      node_color=self.colors['primary'], 
                      alpha=0.8, edgecolors='white', linewidths=2)
        
        # Labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        
        ax.set_title('🧠 Mapa Mental de Conceitos', fontsize=22, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Legenda
        legend_elements = [
            mpatches.Patch(color=self.colors['positive'], label='Conexão positiva'),
            mpatches.Patch(color=self.colors['negative'], label='Conexão negativa'),
            mpatches.Patch(color=self.colors['neutral'], label='Conexão neutra')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        print(f"✅ Gráfico salvo em: {save_path}")
    
    def create_wordcloud_analysis(self, text, topics, temporal_segments, save_path='wordclouds.png'):
        """Cria word clouds: geral e temporal com limpeza integrada"""
        
        # FUNÇÃO DE LIMPEZA LOCAL (não depende mais do analyzer)
        def limpar_texto_wordcloud(texto, stop_words_base):
            texto = texto.lower()
            
            # Lista COMPLETA de palavras a remover
            palavras_remover = {
                # Palavras vazias comuns
                'gente', 'então', 'ali', 'aqui', 'hoje', 'agora', 'porque', 'por que',
                'não', 'sim', 'ter', 'fazer', 'vai', 'pode', 'quer', 'ser',
                'estava', 'estou', 'está', 'estão', 'tinha', 'tenho', 'tem', 'têm',
                'faz', 'fez', 'faço', 'fazem', 'fizer', 'feito', 'fazendo',
                'disse', 'diz', 'dizer', 'falou', 'fala', 'falar', 'falando',
                'acho', 'acha', 'acham', 'achei', 'achou', 'achando',
                'sei', 'sabe', 'saber', 'sabia', 'sabem', 'sabendo',
                'todo', 'toda', 'todos', 'todas', 'tudo',
                'outro', 'outra', 'outros', 'outras',
                'coisa', 'coisas', 'algo', 'algum', 'alguma', 'alguns', 'algumas',
                'parte', 'partes', 'lugar', 'lugares', 'momento', 'momentos',
                'dia', 'dias', 'mês', 'meses', 'ano', 'anos', 'hora', 'horas',
                'vez', 'vezes', 'primeira', 'primeiro', 'última', 'último',
                'bom', 'boa', 'bem', 'mal', 'melhor', 'pior',
                'grande', 'pequeno', 'maior', 'menor', 'muito', 'pouco',
                'novo', 'nova', 'velho', 'velha', 'mesmo', 'mesma',
                'pessoa', 'pessoas', 'alguém', 'ninguém',
                'talvez', 'bastante', 'apenas', 'somente', 'sempre', 'nunca',
                'ainda', 'já', 'mais', 'menos', 'tão', 'tanto', 'tantos',
                'cada', 'qualquer', 'nenhum', 'nenhuma', 'vários', 'várias',
                'certo', 'certa', 'errado', 'errada', 'verdade', 'mentira',
                'né', 'tá', 'ok', 'tipo', 'assim', 'jeito', 'forma', 'maneira',
                'vai', 'vou', 'vamos', 'vão', 'foi', 'foram', 'iam', 'ia',
                'fica', 'ficou', 'ficar', 'ficam', 'ficando',
                'aquilo', 'isso', 'isto', 'essa', 'esse', 'esta', 'este',
                'aquela', 'aquele', 'aqueles', 'aquelas', 'estes', 'estas',
                'dela', 'dele', 'deles', 'delas', 'nela', 'nele', 'neles', 'nelas',
                'pra', 'pro', 'pros', 'pras', 'pelo', 'pela', 'pelos', 'pelas',
                'num', 'numa', 'nuns', 'numas', 'dum', 'duma', 'duns', 'dumas',
                'entre', 'sobre', 'depois', 'antes', 'durante', 'através',
                'precisar', 'precisa', 'preciso', 'precisam', 'precisamos',
                'quero', 'quer', 'querem', 'queremos', 'queria', 'queriam',
                'posso', 'pode', 'podem', 'podemos', 'podia', 'podiam',
                'deve', 'devem', 'devemos', 'devia', 'deviam', 'dever',
                'consigo', 'consegue', 'conseguem', 'conseguimos', 'conseguir',
                'começa', 'começar', 'começou', 'começam', 'começando',
                'termina', 'terminar', 'terminou', 'terminam', 'terminando',
                'acaba', 'acabar', 'acabou', 'acabam', 'acabando',
                'vira', 'virar', 'virou', 'viram', 'virando',
                'volta', 'voltar', 'voltou', 'voltam', 'voltando',
                'passa', 'passar', 'passou', 'passam', 'passando',
                'fica', 'ficar', 'ficou', 'ficam', 'ficando',
                'deixa', 'deixar', 'deixou', 'deixam', 'deixando',
                'leva', 'levar', 'levou', 'levam', 'levando',
                'traz', 'trazer', 'trouxe', 'trazem', 'trazendo',
                'pega', 'pegar', 'pegou', 'pegam', 'pegando',
                'usa', 'usar', 'usou', 'usam', 'usando',
                'cria', 'criar', 'criou', 'criam', 'criando',
                'pensa', 'pensar', 'pensou', 'pensam', 'pensando',
                'sente', 'sentir', 'sentiu', 'sentem', 'sentindo',
                'olha', 'olhar', 'olhou', 'olham', 'olhando',
                'ouve', 'ouvir', 'ouviu', 'ouvem', 'ouvindo',
                'entende', 'entender', 'entendeu', 'entendem', 'entendendo',
                'compreende', 'compreender', 'compreendeu', 'compreendem',
                'explica', 'explicar', 'explicou', 'explicam', 'explicando',
                'mostra', 'mostrar', 'mostrou', 'mostram', 'mostrando',
                'ensina', 'ensinar', 'ensinou', 'ensinam', 'ensinando',
                'aprende', 'aprender', 'aprendeu', 'aprendem', 'aprendendo',
                'compra', 'comprar', 'comprou', 'compram', 'comprando',
                'vende', 'vender', 'vendeu', 'vendem', 'vendendo',
                'paga', 'pagar', 'pagou', 'pagam', 'pagando',
                'recebe', 'receber', 'recebeu', 'recebem', 'recebendo',
                'envia', 'enviar', 'enviou', 'enviam', 'enviando',
                'manda', 'mandar', 'mandou', 'mandam', 'mandando',
                'chega', 'chegar', 'chegou', 'chegam', 'chegando',
                'sai', 'sair', 'saiu', 'saem', 'saindo',
                'entra', 'entrar', 'entrou', 'entram', 'entrando',
                'continua', 'continuar', 'continuou', 'continuam', 'continuando',
                'para', 'parar', 'parou', 'param', 'parando'
            }
            
            # Combinar com stopwords do analyzer
            todas_stopwords = stop_words_base.union(palavras_remover)
            
            # Remover pontuação
            import re
            texto = re.sub(r'[^a-záàâãéêíóôõúçñ\s]', ' ', texto)
            
            # Dividir em palavras
            palavras = texto.split()
            
            # Filtrar palavras
            palavras_limpas = []
            for palavra in palavras:
                # Pular palavras muito curtas
                if len(palavra) < 4:
                    continue
                
                # Pular stopwords
                if palavra in todas_stopwords:
                    continue
                
                # Pular números
                if palavra.isdigit():
                    continue
                
                # Pular se tem números
                if any(char.isdigit() for char in palavra):
                    continue
                
                # Pular verbos conjugados comuns
                if palavra.endswith(('ando', 'endo', 'indo', 'ado', 'ido', 'ar', 'er', 'ir')):
                    # Mas manter palavras importantes
                    palavras_importantes = ['cliente', 'importante', 'seguro', 'sistema', 
                                        'proposta', 'emissão', 'renovação', 'relatório',
                                        'empresa', 'companhia', 'produto', 'serviço']
                    if palavra not in palavras_importantes:
                        continue
                
                palavras_limpas.append(palavra)
            
            return ' '.join(palavras_limpas)
        
        # Criar figura
        fig = plt.figure(figsize=(16, 10))
        
        # Importar o analisador só para pegar as stopwords base
        try:
            from interview_analyzer_v3 import NarrativeInterviewAnalyzer
            analyzer = NarrativeInterviewAnalyzer()
            stop_words_base = analyzer.stop_words
        except:
            # Se falhar, usar conjunto vazio
            stop_words_base = set()
        
        # Word cloud geral
        ax1 = plt.subplot(2, 2, 1)
        
        # USAR NOSSA FUNÇÃO LOCAL DE LIMPEZA
        clean_text = limpar_texto_wordcloud(text, stop_words_base)
        
        # Verificar se sobrou texto suficiente
        if len(clean_text.split()) < 10:
            print("⚠️ Aviso: Poucas palavras após limpeza!")
            # Adicionar palavras dos tópicos
            if topics:
                topic_words = []
                for topic in topics:
                    topic_words.extend(topic['words'][:5])
                clean_text = ' '.join(topic_words) + ' ' + clean_text
        
        # Criar WordCloud
        wordcloud_general = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            colormap='viridis',
            max_words=100,
            min_word_length=4,
            collocations=False
        ).generate(clean_text)
        
        ax1.imshow(wordcloud_general, interpolation='bilinear')
        ax1.set_title('☁️ Nuvem de Palavras - Visão Geral', fontsize=16, fontweight='bold')
        ax1.axis('off')
        
        # Word cloud por fase temporal
        phases = ['Início', 'Meio', 'Fim']
        phase_texts = []
        
        n_segments = len(temporal_segments)
        third = n_segments // 3
        
        phase_texts.append(' '.join([s['text'] for s in temporal_segments[:third]]))
        phase_texts.append(' '.join([s['text'] for s in temporal_segments[third:2*third]]))
        phase_texts.append(' '.join([s['text'] for s in temporal_segments[2*third:]]))
        
        for i, (phase, phase_text) in enumerate(zip(phases, phase_texts)):
            ax = plt.subplot(2, 2, i+2)
            
            # Limpar texto da fase
            clean_phase_text = limpar_texto_wordcloud(phase_text, stop_words_base)
            
            # Se muito pouco texto, adicionar palavras dos tópicos
            if len(clean_phase_text.split()) < 5:
                if topics and i < len(topics):
                    topic_words = topics[i]['words'][:5]
                    clean_phase_text = ' '.join(topic_words) + ' ' + clean_phase_text
            
            try:
                wordcloud = WordCloud(
                    width=800, 
                    height=400,
                    background_color='white',
                    colormap='plasma',
                    max_words=50,
                    min_word_length=4,
                    collocations=False
                ).generate(clean_phase_text)
                
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(f'☁️ Fase: {phase}', fontsize=14, fontweight='bold')
            except:
                ax.text(0.5, 0.5, f'Fase: {phase}\n(Vocabulário insuficiente)', 
                    ha='center', va='center', fontsize=12)
            
            ax.axis('off')
        
        # Estatísticas
        total_words = len(text.split())
        clean_words = len(clean_text.split())
        unique_words = len(set(clean_text.split()))
        
        stats_text = f'Total: {total_words} → Filtradas: {clean_words} (únicas: {unique_words})'
        plt.figtext(0.99, 0.01, stats_text, ha='right', va='bottom', 
                fontsize=10, style='italic', color='gray')
        
        plt.suptitle('📊 Análise de Frequência de Palavras', fontsize=20, fontweight='bold')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✅ Gráfico salvo em: {save_path}")
    
    def create_contradiction_analysis(self, contradictions, save_path='contradictions.png'):
        """Visualiza contradições e ambivalências"""
        if not contradictions:
            print("⚠️ Sem contradições para visualizar")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
        
        # Gráfico de barras - Intensidade das contradições
        topics = [', '.join(c['topic_words'][:2]) for c in contradictions[:5]]
        intensities = [c['intensity'] for c in contradictions[:5]]
        
        bars = ax1.barh(topics, intensities, color=self.colors['warning'])
        ax1.set_xlabel('Intensidade da Contradição', fontsize=12)
        ax1.set_title('⚖️ Principais Contradições/Ambivalências', fontsize=16, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # Adicionar valores nas barras
        for bar, intensity in zip(bars, intensities):
            ax1.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{intensity:.2f}', va='center', fontweight='bold')
        
        # Gráfico circular - Distribuição de contradições por categoria
        if len(contradictions) > 1:
            # Categorizar por intensidade
            categories = {
                'Muito Alta (>1.0)': sum(1 for c in contradictions if c['intensity'] > 1.0),
                'Alta (0.7-1.0)': sum(1 for c in contradictions if 0.7 <= c['intensity'] <= 1.0),
                'Moderada (<0.7)': sum(1 for c in contradictions if c['intensity'] < 0.7)
            }
            
            # Remover categorias vazias
            categories = {k: v for k, v in categories.items() if v > 0}
            
            if categories:
                colors_pie = [self.colors['negative'], self.colors['warning'], self.colors['neutral']]
                wedges, texts, autotexts = ax2.pie(categories.values(), 
                                                   labels=categories.keys(),
                                                   autopct='%1.0f%%',
                                                   colors=colors_pie[:len(categories)],
                                                   startangle=90)
                
                ax2.set_title('📊 Distribuição por Intensidade', fontsize=16, fontweight='bold')
                
                # Melhorar aparência
                for text in texts:
                    text.set_fontsize(12)
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(12)
        else:
            ax2.text(0.5, 0.5, 'Dados insuficientes\npara distribuição', 
                    ha='center', va='center', fontsize=14)
            ax2.axis('off')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✅ Gráfico salvo em: {save_path}")
    
    def create_linguistic_patterns(self, linguistic_patterns, save_path='linguistic_patterns.png'):
        """Visualiza padrões linguísticos"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.ravel()
        
        # 1. Razão Certeza vs Incerteza
        ax = axes[0]
        labels = ['Certeza', 'Incerteza']
        values = [linguistic_patterns['certainty_count'], 
                 linguistic_patterns['uncertainty_count']]
        colors = [self.colors['positive'], self.colors['negative']]
        
        bars = ax.bar(labels, values, color=colors, alpha=0.8)
        ax.set_title('🎯 Certeza vs Incerteza', fontsize=14, fontweight='bold')
        ax.set_ylabel('Ocorrências')
        
        # Adicionar valores nas barras
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                   str(value), ha='center', fontweight='bold')
        
        # Adicionar razão
        ratio = linguistic_patterns['uncertainty_count'] / (linguistic_patterns['certainty_count'] + 1)
        ax.text(0.5, max(values) * 0.8, f'Razão: {ratio:.1f}:1',
               transform=ax.transData, ha='center', fontsize=12,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 2. Padrões por Tópico
        ax = axes[1]
        if linguistic_patterns['topic_patterns']:
            topics = list(linguistic_patterns['topic_patterns'].keys())[:5]
            uncertainties = [linguistic_patterns['topic_patterns'][t]['uncertainty_score'] 
                           for t in topics]
            
            # Truncar nomes longos
            topics_short = [t[:20] + '...' if len(t) > 20 else t for t in topics]
            
            bars = ax.barh(topics_short, uncertainties, color=self.colors['warning'])
            ax.set_xlabel('Score de Incerteza (%)')
            ax.set_title('📊 Incerteza por Tópico', fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            for bar, score in zip(bars, uncertainties):
                ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                       f'{score:.0f}%', va='center')
        
        # 3. Evolução das Hesitações
        ax = axes[2]
        hesitations_data = []
        time_labels = []
        
        for topic, patterns in linguistic_patterns['topic_patterns'].items():
            hesitations_data.append(patterns['hesitations'])
            time_labels.append(topic[:15] + '...' if len(topic) > 15 else topic)
        
        if hesitations_data:
            ax.plot(range(len(hesitations_data)), hesitations_data, 
                   marker='o', color=self.colors['primary'], linewidth=2, markersize=8)
            ax.set_xticks(range(len(time_labels)))
            ax.set_xticklabels(time_labels, rotation=45, ha='right')
            ax.set_ylabel('Número de Hesitações')
            ax.set_title('💭 Hesitações por Tema', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        # 4. Complexidade das Respostas
        ax = axes[3]
        if linguistic_patterns['topic_patterns']:
            topics = list(linguistic_patterns['topic_patterns'].keys())[:6]
            response_times = [linguistic_patterns['topic_patterns'][t]['response_time_estimate'] 
                            for t in topics]
            elaboration_levels = [linguistic_patterns['topic_patterns'][t]['elaboration_level'] 
                                for t in topics]
            
            # Cores por nível de elaboração
            colors_elab = []
            for level in elaboration_levels:
                if 'muito elaborado' in level:
                    colors_elab.append(self.colors['negative'])
                elif 'elaborado' in level:
                    colors_elab.append(self.colors['warning'])
                else:
                    colors_elab.append(self.colors['positive'])
            
            topics_short = [t[:15] + '...' if len(t) > 15 else t for t in topics]
            
            bars = ax.bar(range(len(topics_short)), response_times, color=colors_elab, alpha=0.8)
            ax.set_xticks(range(len(topics_short)))
            ax.set_xticklabels(topics_short, rotation=45, ha='right')
            ax.set_ylabel('Tempo de Resposta (segundos)')
            ax.set_title('⏱️ Complexidade das Respostas', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            # Adicionar linha de referência
            ax.axhline(y=30, color='red', linestyle='--', alpha=0.5, 
                      label='Limiar "muito elaborado"')
            ax.legend()
        
        plt.suptitle('🎭 Análise de Padrões Linguísticos', fontsize=18, fontweight='bold')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✅ Gráfico salvo em: {save_path}")
    
    def create_global_metrics_dashboard(self, global_metrics, save_path='metrics_dashboard.png'):
        """Cria dashboard com métricas globais"""
        fig = plt.figure(figsize=(16, 10))
        
        # Criar grid customizado
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Gauge de Sentimento Global
        ax1 = fig.add_subplot(gs[0, 0])
        self._create_gauge(ax1, global_metrics['global_sentiment'], 
                          'Sentimento Global', -1, 1)
        
        # 2. Gauge de Coerência Temática
        ax2 = fig.add_subplot(gs[0, 1])
        self._create_gauge(ax2, global_metrics['thematic_coherence'], 
                          'Coerência Temática', 0, 1)
        
        # 3. Gauge de Abertura Emocional
        ax3 = fig.add_subplot(gs[0, 2])
        self._create_gauge(ax3, global_metrics['emotional_openness'], 
                          'Abertura Emocional', 0, 2)
        
        # 4. Barras de Métricas
        ax4 = fig.add_subplot(gs[1, :])
        metrics_names = ['Variância\nEmocional', 'Profundidade\nElaboração', 
                        'Conflito\nInterno']
        metrics_values = [global_metrics['sentiment_variance'],
                         global_metrics['elaboration_depth'] / 100,  # Normalizar
                         global_metrics['internal_conflict_index']]
        
        bars = ax4.bar(metrics_names, metrics_values, 
                       color=[self.colors['primary'], self.colors['secondary'], 
                             self.colors['warning']], alpha=0.8)
        
        ax4.set_title('📊 Indicadores Complementares', fontsize=16, fontweight='bold')
        ax4.set_ylim(0, max(metrics_values) * 1.2)
        ax4.grid(axis='y', alpha=0.3)
        
        # Adicionar valores
        for bar, value in zip(bars, metrics_values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 5. Resumo Interpretativo
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')
        
        # Criar texto interpretativo
        interpretations = []
        
        # Sentimento
        if global_metrics['global_sentiment'] > 0.3:
            interpretations.append("✅ Entrevista predominantemente POSITIVA")
        elif global_metrics['global_sentiment'] < -0.3:
            interpretations.append("⚠️ Entrevista predominantemente NEGATIVA")
        else:
            interpretations.append("⚖️ Entrevista EQUILIBRADA/AMBIVALENTE")
        
        # Coerência
        if global_metrics['thematic_coherence'] > 0.7:
            interpretations.append("🎯 Narrativa FOCADA e coerente")
        else:
            interpretations.append("🔀 Narrativa DISPERSA entre temas")
        
        # Elaboração
        if global_metrics['elaboration_depth'] > 30:
            interpretations.append("📖 Participante MUITO DETALHISTA")
        elif global_metrics['elaboration_depth'] > 20:
            interpretations.append("📖 Participante ELABORADO nas respostas")
        else:
            interpretations.append("📖 Participante CONCISO nas respostas")
        
        # Conflito
        if global_metrics['internal_conflict_index'] > 0.8:
            interpretations.append("⚡ ALTO conflito interno detectado")
        elif global_metrics['internal_conflict_index'] > 0.5:
            interpretations.append("⚡ Conflito interno MODERADO")
        else:
            interpretations.append("⚡ BAIXO conflito interno")
        
        # Plotar interpretações
        y_pos = 0.8
        for interp in interpretations:
            ax5.text(0.5, y_pos, interp, transform=ax5.transAxes,
                    fontsize=16, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.5', 
                             facecolor='lightblue', alpha=0.3))
            y_pos -= 0.2
        
        plt.suptitle('🌐 Dashboard de Métricas Globais', fontsize=22, fontweight='bold')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✅ Gráfico salvo em: {save_path}")
    
    def _create_gauge(self, ax, value, title, min_val, max_val):
        """Cria um gauge (velocímetro) para métricas"""
        # Normalizar valor
        normalized = (value - min_val) / (max_val - min_val)
        
        # Criar arco
        theta = np.linspace(np.pi, 0, 100)
        r = 1
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Cores do arco
        colors = plt.cm.RdYlGn(np.linspace(0, 1, 100))
        
        # Plotar arco colorido
        for i in range(len(x)-1):
            ax.plot([x[i], x[i+1]], [y[i], y[i+1]], 
                   color=colors[i], linewidth=15)
        
        # Ponteiro
        angle = np.pi - normalized * np.pi
        pointer_x = 0.8 * np.cos(angle)
        pointer_y = 0.8 * np.sin(angle)
        ax.plot([0, pointer_x], [0, pointer_y], 'k-', linewidth=3)
        ax.scatter(0, 0, color='black', s=100, zorder=5)
        
        # Valor
        ax.text(0, -0.3, f'{value:.2f}', ha='center', va='center',
               fontsize=20, fontweight='bold')
        
        # Título
        ax.text(0, 1.3, title, ha='center', va='center',
               fontsize=14, fontweight='bold')
        
        # Limites
        ax.text(-1.1, -0.1, f'{min_val}', ha='center', fontsize=10)
        ax.text(1.1, -0.1, f'{max_val}', ha='center', fontsize=10)
        ax.text(0, 1.1, f'{(min_val+max_val)/2:.1f}', ha='center', fontsize=10)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-0.5, 1.5)
        ax.axis('off')
    
    def create_topic_distribution_pie(self, topics, topic_distribution, save_path='topic_distribution.png'):
        """Cria gráfico de pizza sofisticado para distribuição de tópicos"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
        
        # Preparar dados
        topic_names = []
        for i, topic in enumerate(topics):
            main_words = ', '.join(topic['words'][:2])
            topic_names.append(f"Tópico {i+1}\n{main_words}")
        
        # Gráfico de pizza
        colors = plt.cm.Set3(np.linspace(0, 1, len(topics)))
        wedges, texts, autotexts = ax1.pie(topic_distribution, 
                                           labels=topic_names,
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           startangle=90,
                                           explode=[0.05] * len(topics))
        
        # Melhorar aparência
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)
        
        ax1.set_title('📊 Distribuição de Tópicos', fontsize=16, fontweight='bold')
        
        # Gráfico de barras horizontais
        sorted_indices = np.argsort(topic_distribution)[::-1]
        sorted_topics = [topic_names[i].replace('\n', ' - ') for i in sorted_indices]
        sorted_weights = [topic_distribution[i] for i in sorted_indices]
        
        bars = ax2.barh(sorted_topics, sorted_weights, color=colors[sorted_indices])
        ax2.set_xlabel('Peso do Tópico (%)')
        ax2.set_title('🏆 Ranking de Tópicos', fontsize=16, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        # Adicionar valores
        for bar, weight in zip(bars, sorted_weights):
            ax2.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                    f'{weight:.1%}', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✅ Gráfico salvo em: {save_path}")
    
    def generate_all_visualizations(self, analysis_results, output_dir='./visualizations/'):
        """Gera todas as visualizações de uma vez"""
        import os
        
        # Criar diretório se não existir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print("\n🎨 GERANDO TODAS AS VISUALIZAÇÕES...")
        print("=" * 60)
        
        # 1. Timeline Emocional
        print("\n1️⃣ Gerando linha do tempo emocional...")
        self.create_emotional_timeline(
            analysis_results['narrative_blocks'],
            save_path=os.path.join(output_dir, 'emotional_timeline.png')
        )
        
        # 2. Hierarquia de Tópicos
        print("\n2️⃣ Gerando hierarquia de tópicos...")
        self.create_topic_hierarchical_tree(
            analysis_results['topics'],
            analysis_results['topic_distribution'],
            save_path=os.path.join(output_dir, 'topic_hierarchy.png')
        )
        
        # 3. Rede de Conceitos
        print("\n3️⃣ Gerando rede de conceitos...")
        self.create_concept_network(
            analysis_results['concept_network'],
            save_path=os.path.join(output_dir, 'concept_network.png')
        )
        
        # 4. Word Clouds
        print("\n4️⃣ Gerando word clouds...")
        # Reconstruir texto completo
        full_text = ' '.join([seg['text'] for seg in analysis_results['segments']])
        self.create_wordcloud_analysis(
            full_text,
            analysis_results['topics'],
            analysis_results['segments'],
            save_path=os.path.join(output_dir, 'wordclouds.png')
        )
        
        # 5. Análise de Contradições
        if analysis_results['contradictions']:
            print("\n5️⃣ Gerando análise de contradições...")
            self.create_contradiction_analysis(
                analysis_results['contradictions'],
                save_path=os.path.join(output_dir, 'contradictions.png')
            )
        
        # 6. Padrões Linguísticos
        print("\n6️⃣ Gerando padrões linguísticos...")
        self.create_linguistic_patterns(
            analysis_results['linguistic_patterns'],
            save_path=os.path.join(output_dir, 'linguistic_patterns.png')
        )
        
        # 7. Dashboard de Métricas
        print("\n7️⃣ Gerando dashboard de métricas...")
        self.create_global_metrics_dashboard(
            analysis_results['global_metrics'],
            save_path=os.path.join(output_dir, 'metrics_dashboard.png')
        )
        
        # 8. Distribuição de Tópicos
        print("\n8️⃣ Gerando distribuição de tópicos...")
        self.create_topic_distribution_pie(
            analysis_results['topics'],
            analysis_results['topic_distribution'],
            save_path=os.path.join(output_dir, 'topic_distribution.png')
        )
        
        print(f"\n✅ TODAS AS VISUALIZAÇÕES FORAM SALVAS EM: {output_dir}")
        print("=" * 60)


# Exemplo de uso integrado com o código original
def enhance_analysis_with_visualizations(analysis_results):
    """Função para adicionar visualizações à análise existente"""
    visualizer = InterviewVisualizer()
    
    # Gerar todas as visualizações
    visualizer.generate_all_visualizations(analysis_results)
    
    return analysis_results


# Se executar diretamente este arquivo
if __name__ == "__main__":
    print("🎨 Sistema de Visualização de Entrevistas")
    print("Este módulo deve ser importado e usado com o analisador principal")
    print("\nExemplo de uso:")
    print("from interview_visualizer import InterviewVisualizer, enhance_analysis_with_visualizations")
    print("\n# Após rodar a análise:")
    print("results = analyze_interview_narrative('entrevista.txt')")
    print("enhance_analysis_with_visualizations(results)")