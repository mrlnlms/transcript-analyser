import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter, defaultdict
import numpy as np
from difflib import SequenceMatcher
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

class NarrativeInterviewAnalyzer:
    def __init__(self):
        self.stemmer = RSLPStemmer()
        self.stop_words = set(stopwords.words('portuguese'))
        self.stop_words.update(['né', 'eh', 'tá', 'ó', 'ah', 'oh', 'um', 'uma', 'tipo', 'assim'])
        
        # Palavras que indicam certeza vs incerteza
        self.certainty_words = ['sempre', 'nunca', 'certeza', 'claro', 'óbvio', 'definitivamente', 
                               'com certeza', 'sem dúvida', 'evidentemente']
        self.uncertainty_words = ['acho', 'talvez', 'sei', 'pode', 'parece', 'quem sabe',
                                'provavelmente', 'possivelmente', 'será', 'de repente']
        
        # Marcadores de hesitação expandidos
        self.hesitation_markers = ['eh', 'né', 'tipo', 'assim', 'ué', 'ah', 'oh', 'hm', 
                                  'uhm', 'então', 'quer dizer', 'sei lá']
        
        # Palavras emocionais expandidas
        self.positive_words = ['amo', 'gosto', 'bom', 'feliz', 'alegre', 'esperança', 'sonho', 
                              'motivação', 'prazer', 'satisfação', 'realização', 'conquista', 
                              'ótimo', 'excelente', 'maravilhoso']
        self.negative_words = ['triste', 'ruim', 'difícil', 'problema', 'medo', 'ansiedade', 
                              'pressão', 'stress', 'frustração', 'raiva', 'decepção', 'solidão',
                              'péssimo', 'horrível', 'terrível']
    
    def clean_text(self, text):
        """Limpa texto preservando estrutura para análise"""
        text = text.lower()
        # Remover repetições óbvias mas preservar hesitações
        text = re.sub(r'\b(\w+)(\s+\1){3,}', r'\1', text)
        text = re.sub(r'[^a-záàâãéêíóôõúçñ\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def segment_by_time(self, text, minutes_per_segment=5):
        """Divide texto em segmentos temporais estimados"""
        # Estimar baseado em ~150 palavras por minuto
        words = text.split()
        words_per_segment = 150 * minutes_per_segment
        
        segments = []
        for i in range(0, len(words), words_per_segment):
            segment = ' '.join(words[i:i + words_per_segment])
            if len(segment.strip()) > 50:  # Apenas segmentos substantivos
                segments.append({
                    'time_range': f"{i//150:.0f}-{(i+words_per_segment)//150:.0f} min",
                    'start_minute': i//150,
                    'end_minute': (i+words_per_segment)//150,
                    'text': segment,
                    'word_count': len(segment.split())
                })
        return segments
    
    def extract_topics_enhanced(self, text, n_topics=5):
        """Extração melhorada de tópicos para análise"""
        # Dividir em chunks para simular múltiplos documentos
        words = text.split()
        chunk_size = len(words) // 10  # 10 chunks
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk) > 50:
                chunks.append(chunk)
        
        if len(chunks) < 3:
            return [], []
        
        try:
            vectorizer = CountVectorizer(max_features=30, min_df=1, max_df=0.8)
            doc_matrix = vectorizer.fit_transform(chunks)
            
            lda = LatentDirichletAllocation(n_components=min(n_topics, len(chunks)//2), 
                                          random_state=42, max_iter=10)
            lda.fit(doc_matrix)
            
            feature_names = vectorizer.get_feature_names_out()
            topics = []
            
            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[-8:][::-1]
                top_words = [feature_names[i] for i in top_words_idx]
                top_scores = [topic[i] for i in top_words_idx]
                
                topics.append({
                    'id': topic_idx,
                    'words': top_words,
                    'scores': top_scores,
                    'description': ' + '.join([f"{w}({s:.1f})" for w, s in zip(top_words[:4], top_scores[:4])])
                })
            
            # Distribuição no texto todo
            full_text_vector = vectorizer.transform([text])
            distribution = lda.transform(full_text_vector)[0]
            
            return topics, distribution
            
        except Exception as e:
            print(f"⚠️ Erro no topic modeling: {e}")
            return [], []
    
    def analyze_sentiment_simple(self, text):
        """Análise de sentimento básica usando listas de palavras"""
        words = text.lower().split()
        
        positive_count = sum(1 for word in words if any(pos in word for pos in self.positive_words))
        negative_count = sum(1 for word in words if any(neg in word for neg in self.negative_words))
        
        total_emotional = positive_count + negative_count
        if total_emotional == 0:
            return 0.0
        
        sentiment_score = (positive_count - negative_count) / total_emotional
        return sentiment_score
    
    def detect_contradictions(self, text, topics):
        """Detecta possíveis contradições/ambivalências no texto"""
        sentences = sent_tokenize(text, language='portuguese')
        contradictions = []
        
        # Para cada tópico, buscar sentenças com sentimentos opostos
        for topic in topics:
            topic_sentences = []
            topic_words = topic['words'][:5]
            
            for sentence in sentences:
                # Se a sentença contém palavras do tópico
                if any(word in sentence.lower() for word in topic_words):
                    sentiment = self.analyze_sentiment_simple(sentence)
                    topic_sentences.append({
                        'text': sentence,
                        'sentiment': sentiment
                    })
            
            # Buscar sentimentos opostos no mesmo tópico
            positive_sentences = [s for s in topic_sentences if s['sentiment'] > 0.3]
            negative_sentences = [s for s in topic_sentences if s['sentiment'] < -0.3]
            
            if positive_sentences and negative_sentences:
                contradiction_intensity = abs(
                    np.mean([s['sentiment'] for s in positive_sentences]) - 
                    np.mean([s['sentiment'] for s in negative_sentences])
                )
                
                contradictions.append({
                    'topic': topic['description'],
                    'topic_words': topic['words'][:3],
                    'positive_example': positive_sentences[0]['text'][:100] + '...',
                    'negative_example': negative_sentences[0]['text'][:100] + '...',
                    'intensity': contradiction_intensity,
                    'count': len(positive_sentences) + len(negative_sentences)
                })
        
        return sorted(contradictions, key=lambda x: x['intensity'], reverse=True)
    
    def analyze_linguistic_patterns_detailed(self, text, topics, segments):
        """Análise detalhada de padrões linguísticos"""
        words = text.lower().split()
        sentences = sent_tokenize(text, language='portuguese')
        
        # Contagem de hesitações
        hesitations = sum(1 for word in words if word in self.hesitation_markers)
        
        # Certeza vs incerteza
        certainty_count = sum(1 for word in words if any(cert in word for cert in self.certainty_words))
        uncertainty_count = sum(1 for word in words if any(unc in word for unc in self.uncertainty_words))
        
        # Complexidade das sentenças
        sentence_lengths = [len(sent.split()) for sent in sentences]
        avg_sentence_length = np.mean(sentence_lengths)
        
        # Análise por tópico com métricas individuais
        topic_patterns = {}
        for topic in topics:
            topic_words = topic['words'][:5]
            topic_sentences = [sent for sent in sentences 
                             if any(word in sent.lower() for word in topic_words)]
            
            if topic_sentences:
                topic_text = ' '.join(topic_sentences)
                topic_words_list = topic_text.split()
                
                # Cálculos específicos do tópico
                topic_hesitations = sum(1 for word in topic_words_list 
                                      if word in self.hesitation_markers)
                topic_uncertainty = sum(1 for word in topic_words_list 
                                      if any(unc in word for unc in self.uncertainty_words))
                topic_certainty = sum(1 for word in topic_words_list 
                                    if any(cert in word for cert in self.certainty_words))
                
                # Score de incerteza (0-100)
                uncertainty_score = (topic_uncertainty / (topic_uncertainty + topic_certainty + 1)) * 100
                
                # Tempo médio de resposta (baseado no comprimento)
                avg_response_length = len(topic_text.split()) / len(topic_sentences) if topic_sentences else 0
                response_time_estimate = avg_response_length / 2.5  # ~2.5 palavras por segundo
                
                topic_patterns[topic['description']] = {
                    'hesitations': topic_hesitations,
                    'uncertainty_markers': topic_uncertainty,
                    'certainty_markers': topic_certainty,
                    'uncertainty_score': uncertainty_score,
                    'avg_sentence_length': np.mean([len(sent.split()) for sent in topic_sentences]),
                    'sentence_count': len(topic_sentences),
                    'response_time_estimate': response_time_estimate,
                    'elaboration_level': 'muito elaborado' if response_time_estimate > 40 else 
                                       'elaborado' if response_time_estimate > 25 else
                                       'moderado' if response_time_estimate > 15 else
                                       'direto' if response_time_estimate > 10 else 'superficial'
                }
        
        return {
            'total_hesitations': hesitations,
            'certainty_count': certainty_count,
            'uncertainty_count': uncertainty_count,
            'certainty_ratio': certainty_count / (certainty_count + uncertainty_count + 1),
            'avg_sentence_length': avg_sentence_length,
            'topic_patterns': topic_patterns
        }
    
    def create_concept_network_enhanced(self, text, topics):
        """Cria rede de co-ocorrência de conceitos com análise"""
        # Extrair conceitos principais dos tópicos
        all_concepts = []
        for topic in topics:
            all_concepts.extend(topic['words'][:5])
        
        # Remover duplicatas
        concepts = list(set(all_concepts))
        
        # Calcular co-ocorrências (janela de 20 palavras)
        words = text.lower().split()
        co_occurrences = defaultdict(int)
        concept_contexts = defaultdict(list)
        
        for i, word in enumerate(words):
            if word in concepts:
                # Buscar outros conceitos na janela
                start = max(0, i - 10)
                end = min(len(words), i + 10)
                
                for j in range(start, end):
                    if j != i and words[j] in concepts:
                        pair = tuple(sorted([word, words[j]]))
                        co_occurrences[pair] += 1
                        # Capturar contexto
                        context_start = max(0, i - 5)
                        context_end = min(len(words), i + 5)
                        context = ' '.join(words[context_start:context_end])
                        concept_contexts[pair].append(context)
        
        # Criar lista ordenada de conexões
        connections = []
        for (concept1, concept2), count in co_occurrences.items():
            if count > 1:  # Apenas conexões significativas
                # Analisar sentimento dos contextos
                contexts = concept_contexts[(concept1, concept2)]
                avg_sentiment = np.mean([self.analyze_sentiment_simple(ctx) for ctx in contexts])
                
                connections.append({
                    'concept1': concept1,
                    'concept2': concept2,
                    'strength': count,
                    'normalized_strength': count / len(words) * 1000,
                    'sentiment': avg_sentiment,
                    'correlation_score': count / len(words) * 100
                })
        
        connections.sort(key=lambda x: x['strength'], reverse=True)
        return connections[:15]  # Top 15 conexões
    
    def get_sentiment_emoji(self, sentiment):
        """Retorna emoji apropriado para o sentimento"""
        if sentiment < -0.7:
            return "😢"  # Muito negativo
        elif sentiment < -0.4:
            return "😟"  # Negativo
        elif sentiment < -0.2:
            return "😔"  # Levemente negativo
        elif sentiment < 0.2:
            return "😐"  # Neutro
        elif sentiment < 0.4:
            return "🙂"  # Levemente positivo
        elif sentiment < 0.7:
            return "😊"  # Positivo
        else:
            return "😄"  # Muito positivo
    
    def create_narrative_blocks(self, segments, topics, topic_distribution):
        """Cria blocos narrativos estilo relatório da Ana"""
        narrative_blocks = []
        
        for i, segment in enumerate(segments):
            # Análise detalhada do segmento
            sentiment = self.analyze_sentiment_simple(segment['text'])
            words = segment['text'].split()
            hesitations = sum(1 for word in words if word in self.hesitation_markers)
            
            # Identificar tema dominante do segmento
            segment_topics = []
            for j, topic in enumerate(topics):
                topic_presence = sum(1 for word in words if word in topic['words']) / len(words) * 100
                if topic_presence > 5:  # Threshold de 5%
                    segment_topics.append({
                        'name': topic['words'][0],
                        'percentage': topic_presence,
                        'topic_id': j
                    })
            
            segment_topics.sort(key=lambda x: x['percentage'], reverse=True)
            
            # Determinar título do bloco
            if i == 0:
                block_title = "APRESENTAÇÃO E CONTEXTO INICIAL"
            elif i == len(segments) - 1:
                block_title = "CONCLUSÃO E PERSPECTIVAS"
            elif sentiment < -0.5 and any('problema' in t['name'] or 'difícil' in t['name'] for t in segment_topics):
                block_title = "MOMENTO CRÍTICO - PROCESSAMENTO EMOCIONAL"
            elif sentiment > 0.5:
                block_title = "RECURSOS E ASPECTOS POSITIVOS"
            elif segment_topics:
                main_topic = segment_topics[0]['name'].upper()
                if sentiment < -0.2:
                    block_title = f"{main_topic} - ASPECTOS NEGATIVOS"
                elif sentiment > 0.2:
                    block_title = f"{main_topic} - ASPECTOS POSITIVOS"
                else:
                    block_title = f"{main_topic} - EXPLORAÇÃO DO TEMA"
            else:
                block_title = "TRANSIÇÃO TEMÁTICA"
            
            # Criar nota interpretativa variada baseada no contexto
            notas_por_contexto = {
                'high_hesitation_negative': [
                    "Processamento emocional intenso, possível tema gatilho",
                    "Dificuldade evidente de verbalização, conteúdo sensível",
                    "Pausas frequentes sugerem impacto emocional do tema"
                ],
                'high_hesitation_positive': [
                    "Entusiasmo pode estar gerando agitação na fala",
                    "Excitação sobre o tema, busca por palavras adequadas",
                    "Elaboração cuidadosa de ideias positivas"
                ],
                'low_hesitation_negative': [
                    "Narrativa fluida sobre dificuldades, possível resignação",
                    "Familiaridade com o sofrimento, verbalização clara",
                    "Tema doloroso mas já processado anteriormente"
                ],
                'low_hesitation_positive': [
                    "Fala confiante e fluida, tema confortável",
                    "Expressão natural de contentamento",
                    "Segurança ao abordar aspectos positivos"
                ],
                'neutral': [
                    "Exploração reflexiva do tema",
                    "Processamento cognitivo em andamento",
                    "Transição entre ideias e conceitos"
                ],
                'multiple_themes': [
                    "Conexões complexas entre múltiplos temas",
                    "Pensamento associativo rico e elaborado",
                    "Integração de diferentes aspectos da experiência"
                ]
            }
            
            # Selecionar nota apropriada
            import random
            if hesitations > 10 and sentiment < -0.2:
                nota = random.choice(notas_por_contexto['high_hesitation_negative'])
            elif hesitations > 10 and sentiment > 0.2:
                nota = random.choice(notas_por_contexto['high_hesitation_positive'])
            elif hesitations < 5 and sentiment < -0.2:
                nota = random.choice(notas_por_contexto['low_hesitation_negative'])
            elif hesitations < 5 and sentiment > 0.2:
                nota = random.choice(notas_por_contexto['low_hesitation_positive'])
            elif len(segment_topics) > 2:
                nota = random.choice(notas_por_contexto['multiple_themes'])
            else:
                nota = random.choice(notas_por_contexto['neutral'])
            
            # Identificar picos emocionais
            is_emotional_peak = abs(sentiment) > 0.7
            
            # Determinar emoji baseado no sentimento
            sentiment_emoji = self.get_sentiment_emoji(sentiment)
            
            narrative_blocks.append({
                'block_number': i + 1,
                'time_range': segment['time_range'],
                'title': block_title,
                'themes': segment_topics[:3],  # Top 3 temas
                'sentiment': sentiment,
                'sentiment_label': 'Muito negativo' if sentiment < -0.5 else
                                 'Negativo' if sentiment < -0.2 else
                                 'Neutro' if abs(sentiment) <= 0.2 else
                                 'Positivo' if sentiment < 0.5 else
                                 'Muito positivo',
                'sentiment_emoji': sentiment_emoji,
                'hesitations': hesitations,
                'nota': nota,
                'is_emotional_peak': is_emotional_peak,
                'word_count': segment['word_count']
            })
        
        return narrative_blocks
    
    def generate_storyline(self, narrative_blocks):
        """Gera storyline da entrevista"""
        storyline = {
            'opening': None,
            'development': [],
            'crisis_points': [],
            'resolution_attempts': [],
            'closing': None,
            'emotional_journey': []
        }
        
        # Identificar momentos-chave
        for i, block in enumerate(narrative_blocks):
            if i == 0:
                storyline['opening'] = block
            elif i == len(narrative_blocks) - 1:
                storyline['closing'] = block
            elif block['is_emotional_peak'] and block['sentiment'] < -0.5:
                storyline['crisis_points'].append(block)
            elif i > 0 and narrative_blocks[i-1]['sentiment'] < -0.3 and block['sentiment'] > 0.1:
                storyline['resolution_attempts'].append(block)
            else:
                storyline['development'].append(block)
            
            # Trajetória emocional
            storyline['emotional_journey'].append({
                'time': block['time_range'],
                'sentiment': block['sentiment'],
                'label': block['sentiment_label']
            })
        
        return storyline
    
    def generate_hypotheses(self, analysis_results):
        """Gera hipóteses interpretativas com espaços para completar"""
        hypotheses = []
        
        # Hipóteses sobre temas dominantes
        if analysis_results['topics']:
            dominant_topic = max(enumerate(analysis_results['topic_distribution']), 
                               key=lambda x: x[1])[0]
            dominant_words = analysis_results['topics'][dominant_topic]['words'][:3]
            hypotheses.append({
                'category': 'TEMA CENTRAL',
                'observation': f"A predominância do tema '{', '.join(dominant_words)}' "
                             f"({analysis_results['topic_distribution'][dominant_topic]:.1%} do conteúdo)",
                'hypothesis': "sugere que o participante _______"
            })
        
        # Hipóteses sobre contradições
        if analysis_results['contradictions']:
            main_contradiction = analysis_results['contradictions'][0]
            hypotheses.append({
                'category': 'AMBIVALÊNCIA PRINCIPAL',
                'observation': f"Contradição sobre '{', '.join(main_contradiction['topic_words'])}' "
                             f"com intensidade {main_contradiction['intensity']:.1f}",
                'hypothesis': "pode indicar _______"
            })
        
        # Hipóteses sobre padrões linguísticos
        ling = analysis_results['linguistic_patterns']
        uncertainty_ratio = ling['uncertainty_count'] / (ling['certainty_count'] + 1)
        if uncertainty_ratio > 3:
            hypotheses.append({
                'category': 'PADRÃO COMUNICACIONAL',
                'observation': f"Alta proporção de incerteza linguística ({uncertainty_ratio:.1f}:1)",
                'hypothesis': "sugere possível _______"
            })
        
        # Hipóteses sobre trajetória emocional
        if analysis_results['storyline']['emotional_journey']:
            start_sentiment = analysis_results['storyline']['emotional_journey'][0]['sentiment']
            end_sentiment = analysis_results['storyline']['emotional_journey'][-1]['sentiment']
            change = end_sentiment - start_sentiment
            
            if abs(change) > 0.5:
                direction = "ascendente" if change > 0 else "descendente"
                hypotheses.append({
                    'category': 'PROCESSO EMOCIONAL',
                    'observation': f"Trajetória emocional {direction} (Δ={change:.2f})",
                    'hypothesis': f"indica processo de _______"
                })
        
        # Hipóteses sobre momentos críticos
        if analysis_results['storyline']['crisis_points']:
            crisis_themes = []
            for crisis in analysis_results['storyline']['crisis_points']:
                if crisis['themes']:
                    crisis_themes.extend([t['name'] for t in crisis['themes']])
            
            if crisis_themes:
                most_common_crisis_theme = max(set(crisis_themes), key=crisis_themes.count)
                hypotheses.append({
                    'category': 'PONTOS DE VULNERABILIDADE',
                    'observation': f"Momentos críticos associados principalmente a '{most_common_crisis_theme}'",
                    'hypothesis': "revela _______"
                })
        
        return hypotheses
    
    def generate_recommendations(self, analysis_results):
        """Gera recomendações para próximas entrevistas"""
        recommendations = {
            'explore_further': [],
            'timing': [],
            'approach': []
        }
        
        # Temas para explorar
        for contradiction in analysis_results['contradictions'][:2]:
            recommendations['explore_further'].append(
                f"Dinâmica específica sobre '{', '.join(contradiction['topic_words'])}' "
                f"(alta ambivalência detectada)"
            )
        
        # Timing otimizado
        if analysis_results['storyline']['crisis_points']:
            crisis_times = [int(block['time_range'].split('-')[0]) for block in 
                          analysis_results['storyline']['crisis_points']]
            avg_crisis_time = np.mean(crisis_times)
            recommendations['timing'].append(
                f"Temas sensíveis emergem após ~{avg_crisis_time:.0f} minutos "
                f"(aguardar estabelecimento de rapport)"
            )
        
        # Abordagem recomendada
        ling = analysis_results['linguistic_patterns']
        if ling['topic_patterns']:
            elaborated_topics = [topic for topic, patterns in ling['topic_patterns'].items()
                               if patterns['elaboration_level'] in ['muito elaborado', 'elaborado']]
            if elaborated_topics:
                recommendations['approach'].append(
                    f"Usar perguntas abertas para temas como {elaborated_topics[0][:30]}... "
                    f"(participante elabora bem)"
                )
        
        return recommendations
    
    def create_hierarchical_tree(self, topics, topic_distribution, concept_network):
        """Cria visualização hierárquica dos tópicos em ASCII"""
        tree_lines = []
        tree_lines.append("🌳 ÁRVORE HIERÁRQUICA DE TEMAS:")
        tree_lines.append("="*50)
        tree_lines.append("")
        tree_lines.append("TEMAS PRINCIPAIS")
        
        # Ordenar tópicos por relevância
        topic_weights = [(i, weight) for i, weight in enumerate(topic_distribution)]
        topic_weights.sort(key=lambda x: x[1], reverse=True)
        
        for idx, (topic_id, weight) in enumerate(topic_weights):
            topic = topics[topic_id]
            is_last_topic = idx == len(topic_weights) - 1
            
            # Linha principal do tópico
            prefix = "└── " if is_last_topic else "├── "
            tree_lines.append(f"{prefix}{topic['words'][0]} ({weight:.0%})")
            
            # Subpalavras do tópico
            sub_prefix = "    " if is_last_topic else "│   "
            for j, (word, score) in enumerate(zip(topic['words'][1:4], topic['scores'][1:4])):
                is_last_word = j == 2
                word_prefix = "└── " if is_last_word else "├── "
                
                # Determinar valência baseado nas conexões
                valence = ""
                for conn in concept_network:
                    if word in [conn['concept1'], conn['concept2']]:
                        if conn['sentiment'] > 0.2:
                            valence = " ✨"
                        elif conn['sentiment'] < -0.2:
                            valence = " ⚡"
                        break
                
                tree_lines.append(f"{sub_prefix}{word_prefix}{word} ({score:.1f}){valence}")
        
        return tree_lines
    
    def create_concept_map(self, concept_network, topics):
        """Cria mapa mental dos conceitos principais"""
        map_lines = []
        map_lines.append("🧠 MAPA MENTAL DE CONCEITOS:")
        map_lines.append("="*50)
        map_lines.append("")
        
        # Identificar conceito central (mais conexões)
        concept_counts = {}
        for conn in concept_network:
            concept_counts[conn['concept1']] = concept_counts.get(conn['concept1'], 0) + 1
            concept_counts[conn['concept2']] = concept_counts.get(conn['concept2'], 0) + 1
        
        if concept_counts:
            central_concept = max(concept_counts.items(), key=lambda x: x[1])[0]
            
            # Construir visualização
            map_lines.append(f"                 {central_concept.upper()}")
            map_lines.append(f"                    (CENTRAL)")
            map_lines.append(f"                   /    |    \\")
            
            # Encontrar conceitos conectados ao central
            connected = []
            for conn in concept_network[:8]:  # Top 8 conexões
                if conn['concept1'] == central_concept:
                    connected.append((conn['concept2'], conn['sentiment']))
                elif conn['concept2'] == central_concept:
                    connected.append((conn['concept1'], conn['sentiment']))
            
            if len(connected) >= 3:
                # Primeira linha de conexões
                line1 = f"           {connected[0][0]:>10}  {connected[1][0]:^10}  {connected[2][0]:<10}"
                map_lines.append(line1)
                
                # Símbolos de valência
                symbols = []
                for concept, sentiment in connected[:3]:
                    if sentiment > 0.2:
                        symbols.append("(+)")
                    elif sentiment < -0.2:
                        symbols.append("(-)")
                    else:
                        symbols.append("(~)")
                
                line2 = f"              {symbols[0]:>6}    {symbols[1]:^6}    {symbols[2]:<6}"
                map_lines.append(line2)
        
        return map_lines
    
    def create_emotional_timeline(self, narrative_blocks):
        """Cria timeline visual da jornada emocional"""
        timeline_lines = []
        timeline_lines.append("📈 JORNADA EMOCIONAL:")
        timeline_lines.append("="*50)
        timeline_lines.append("")
        
        # Criar gráfico de barras ASCII
        timeline_lines.append("Intensidade")
        timeline_lines.append("   +1.0 ┤")
        
        # Criar linhas do gráfico
        for level in [0.5, 0, -0.5, -1.0]:
            line = f"  {level:+.1f} ┤"
            
            for block in narrative_blocks:
                sentiment = block['sentiment']
                if level == 1.0 and sentiment >= 0.75:
                    line += "███ "
                elif level == 0.5 and 0.25 <= sentiment < 0.75:
                    line += "███ "
                elif level == 0 and -0.25 <= sentiment < 0.25:
                    line += "███ "
                elif level == -0.5 and -0.75 <= sentiment < -0.25:
                    line += "███ "
                elif level == -1.0 and sentiment < -0.75:
                    line += "███ "
                else:
                    line += "    "
            
            timeline_lines.append(line)
        
        # Eixo X
        timeline_lines.append("       └" + "────" * len(narrative_blocks))
        
        # Labels
        labels = "       "
        for block in narrative_blocks:
            labels += f"B{block['block_number']}  "
        timeline_lines.append(labels)
        
        # Linha de tendência
        timeline_lines.append("")
        timeline_lines.append("📊 Evolução:")
        
        for block in narrative_blocks:
            emoji = block['sentiment_emoji']
            time = block['time_range']
            desc = "↗️" if block['sentiment'] > 0.3 else "↘️" if block['sentiment'] < -0.3 else "→"
            timeline_lines.append(f"{emoji} {time}: {desc} {block['title'][:30]}...")
        
        return timeline_lines
    
    def calculate_global_metrics(self, analysis_results):
        """Calcula métricas globais da entrevista"""
        metrics = {}
        
        # Score de sentimento global
        all_sentiments = [block['sentiment'] for block in analysis_results['narrative_blocks']]
        metrics['global_sentiment'] = np.mean(all_sentiments)
        metrics['sentiment_variance'] = np.std(all_sentiments)
        
        # Coerência temática (quanto os temas se mantêm consistentes)
        theme_changes = 0
        prev_themes = []
        for block in analysis_results['narrative_blocks']:
            curr_themes = [t['name'] for t in block['themes']]
            if prev_themes and not any(t in prev_themes for t in curr_themes):
                theme_changes += 1
            prev_themes = curr_themes
        
        metrics['thematic_coherence'] = 1 - (theme_changes / len(analysis_results['narrative_blocks']))
        
        # Profundidade de elaboração
        avg_response_lengths = []
        for patterns in analysis_results['linguistic_patterns']['topic_patterns'].values():
            avg_response_lengths.append(patterns['response_time_estimate'])
        
        metrics['elaboration_depth'] = np.mean(avg_response_lengths) if avg_response_lengths else 0
        
        # Índice de conflito interno (baseado em contradições)
        if analysis_results['contradictions']:
            metrics['internal_conflict_index'] = np.mean([c['intensity'] 
                                                         for c in analysis_results['contradictions']])
        else:
            metrics['internal_conflict_index'] = 0
        
        # Abertura emocional (variação entre início e máxima expressão)
        sentiment_range = max(all_sentiments) - min(all_sentiments)
        metrics['emotional_openness'] = sentiment_range
        
        return metrics
    
    def generate_dual_report(self, text, participant_name="Participante"):
        """Gera relatório duplo: Análise técnica + Síntese narrativa"""
        print("🚀 GERANDO RELATÓRIO COMPLETO (ANÁLISE + SÍNTESE)...")
        print("=" * 80)
        
        # Preparação
        clean_text = self.clean_text(text)
        
        # Análises base
        segments = self.segment_by_time(clean_text, minutes_per_segment=5)
        print(f"📊 Texto dividido em {len(segments)} segmentos temporais")
        
        topics, topic_distribution = self.extract_topics_enhanced(clean_text)
        print(f"🎯 {len(topics)} tópicos principais identificados")
        
        # Análises complementares
        temporal_analysis = []
        for segment in segments:
            sentiment = self.analyze_sentiment_simple(segment['text'])
            temporal_analysis.append({
                'time_range': segment['time_range'],
                'sentiment': sentiment,
                'word_count': segment['word_count']
            })
        
        contradictions = self.detect_contradictions(clean_text, topics)
        linguistic_patterns = self.analyze_linguistic_patterns_detailed(clean_text, topics, segments)
        concept_network = self.create_concept_network_enhanced(clean_text, topics)
        
        # Análises narrativas
        narrative_blocks = self.create_narrative_blocks(segments, topics, topic_distribution)
        storyline = self.generate_storyline(narrative_blocks)
        
        # Compilar resultados
        analysis_results = {
            'participant': participant_name,
            'duration': f"{len(segments) * 5} minutos",
            'segments': segments,
            'topics': topics,
            'topic_distribution': topic_distribution,
            'temporal_analysis': temporal_analysis,
            'contradictions': contradictions,
            'linguistic_patterns': linguistic_patterns,
            'concept_network': concept_network,
            'narrative_blocks': narrative_blocks,
            'storyline': storyline
        }
        
        # Gerar visualizações
        analysis_results['visualizations'] = {
            'hierarchical_tree': self.create_hierarchical_tree(topics, topic_distribution, concept_network),
            'concept_map': self.create_concept_map(concept_network, topics),
            'emotional_timeline': self.create_emotional_timeline(narrative_blocks)
        }
        
        # Calcular métricas globais
        analysis_results['global_metrics'] = self.calculate_global_metrics(analysis_results)
        
        # Gerar hipóteses e recomendações
        hypotheses = self.generate_hypotheses(analysis_results)
        recommendations = self.generate_recommendations(analysis_results)
        
        analysis_results['hypotheses'] = hypotheses
        analysis_results['recommendations'] = recommendations
        
        # Imprimir relatório dual
        self.print_dual_report(analysis_results)
        
        return analysis_results
    
    def print_dual_report(self, results):
        """Imprime relatório em duas partes: Análise e Síntese"""
        
        # Cabeçalho
        print(f"\n{'='*80}")
        print(f"                    📋 RELATÓRIO DE ANÁLISE DA ENTREVISTA")
        print(f"                         Participante: {results['participant']}")
        print(f"                         Duração: {results['duration']}")
        print(f"{'='*80}")
        
        # PARTE 1: ANÁLISE TÉCNICA
        print(f"\n{'─'*80}")
        print(f"PARTE 1: ANÁLISE TÉCNICA E ESTRUTURAL")
        print(f"{'─'*80}")
        
        # 1.1 Análise Temática
        print(f"\n📊 ANÁLISE TEMÁTICA:")
        print(f"{'─'*40}")
        
        print(f"\n🧠 Tópicos Identificados:")
        for i, topic in enumerate(results['topics']):
            weight = results['topic_distribution'][i] if i < len(results['topic_distribution']) else 0
            print(f"├─ Tópico {i+1} ({weight:.1%}): {', '.join(topic['words'][:4])}")
        
        if results['topics']:
            dominant_idx = np.argmax(results['topic_distribution'])
            print(f"└─ Dominante: Tópico {dominant_idx+1} "
                  f"({results['topic_distribution'][dominant_idx]:.1%})")
        
        # 1.2 Análise Temporal Agrupada
        print(f"\n⏰ ANÁLISE TEMPORAL:")
        print(f"{'─'*40}")
        
        # Calcular médias por terços
        n_segments = len(results['temporal_analysis'])
        third_size = n_segments // 3
        
        inicio_sentiments = [s['sentiment'] for s in results['temporal_analysis'][:third_size]]
        meio_sentiments = [s['sentiment'] for s in results['temporal_analysis'][third_size:third_size*2]]
        fim_sentiments = [s['sentiment'] for s in results['temporal_analysis'][third_size*2:]]
        
        print(f"\n📈 Evolução Emocional por Fase:")
        print(f"├─ Início: {np.mean(inicio_sentiments):+.2f} (σ={np.std(inicio_sentiments):.2f})")
        print(f"├─ Meio:   {np.mean(meio_sentiments):+.2f} (σ={np.std(meio_sentiments):.2f})")
        print(f"└─ Fim:    {np.mean(fim_sentiments):+.2f} (σ={np.std(fim_sentiments):.2f})")
        
        # 1.3 Análise Linguística Agrupada
        print(f"\n🎭 ANÁLISE LINGUÍSTICA:")
        print(f"{'─'*40}")
        
        ling = results['linguistic_patterns']
        print(f"\n📏 Métricas Globais:")
        print(f"├─ Hesitações totais: {ling['total_hesitations']}")
        print(f"├─ Razão Incerteza/Certeza: {ling['uncertainty_count']}/{ling['certainty_count']} "
              f"({ling['uncertainty_count']/(ling['certainty_count']+1):.1f}:1)")
        print(f"└─ Complexidade média: {ling['avg_sentence_length']:.1f} palavras/frase")
        
        if ling['topic_patterns']:
            print(f"\n📊 Padrões por Tema:")
            for topic, patterns in ling['topic_patterns'].items():
                print(f"\n{topic[:40]}...")
                print(f"├─ Elaboração: {patterns['elaboration_level']} "
                      f"(~{patterns['response_time_estimate']:.0f}s/resposta)")
                print(f"├─ Incerteza: {patterns['uncertainty_score']:.0f}%")
                print(f"└─ Hesitações: {patterns['hesitations']} "
                      f"({patterns['hesitations']/patterns['sentence_count']:.1f}/frase)")
        
        # 1.4 Rede Conceitual
        print(f"\n🕸️ REDE CONCEITUAL:")
        print(f"{'─'*40}")
        
        if results['concept_network']:
            print(f"\n🔗 Conexões Mais Fortes:")
            for i, conn in enumerate(results['concept_network'][:5], 1):
                valence = "+" if conn['sentiment'] > 0 else "-"
                print(f"{i}. {conn['concept1']} ↔ {conn['concept2']} "
                      f"(força: {conn['strength']}, valência: {valence})")
        
        # PARTE 2: SÍNTESE NARRATIVA
        print(f"\n\n{'─'*80}")
        print(f"PARTE 2: SÍNTESE NARRATIVA E INTERPRETATIVA")
        print(f"{'─'*80}")
        
        # 2.1 Métricas Globais
        print(f"\n🌐 MÉTRICAS GLOBAIS DA ENTREVISTA:")
        print(f"{'─'*40}")
        
        metrics = results['global_metrics']
        
        # Sentimento global com interpretação
        sentiment_interpretation = ""
        if metrics['global_sentiment'] > 0.3:
            sentiment_interpretation = "predominantemente positiva"
        elif metrics['global_sentiment'] < -0.3:
            sentiment_interpretation = "predominantemente negativa"
        else:
            sentiment_interpretation = "equilibrada/ambivalente"
        
        print(f"📊 Score de Sentimento Global: {metrics['global_sentiment']:+.2f} ({sentiment_interpretation})")
        print(f"📈 Variabilidade Emocional: {metrics['sentiment_variance']:.2f} ", end="")
        if metrics['sentiment_variance'] > 0.5:
            print("(alta flutuação emocional)")
        else:
            print("(estável)")
        
        print(f"🔗 Coerência Temática: {metrics['thematic_coherence']:.1%} ", end="")
        if metrics['thematic_coherence'] > 0.7:
            print("(narrativa focada)")
        else:
            print("(narrativa dispersa)")
        
        print(f"📖 Profundidade de Elaboração: {metrics['elaboration_depth']:.0f}s/resposta ", end="")
        if metrics['elaboration_depth'] > 30:
            print("(muito detalhista)")
        elif metrics['elaboration_depth'] > 20:
            print("(elaborado)")
        else:
            print("(conciso)")
        
        print(f"⚖️ Índice de Conflito Interno: {metrics['internal_conflict_index']:.2f} ", end="")
        if metrics['internal_conflict_index'] > 0.8:
            print("(alto)")
        elif metrics['internal_conflict_index'] > 0.5:
            print("(moderado)")
        else:
            print("(baixo)")
        
        print(f"💭 Abertura Emocional: {metrics['emotional_openness']:.2f} ", end="")
        if metrics['emotional_openness'] > 1.5:
            print("(muito expressivo)")
        elif metrics['emotional_openness'] > 0.8:
            print("(expressivo)")
        else:
            print("(contido)")
        
        # 2.2 Visualizações
        print(f"\n\n{'─'*80}")
        print("VISUALIZAÇÕES DE DADOS")
        print(f"{'─'*80}")
        
        # Árvore hierárquica
        for line in results['visualizations']['hierarchical_tree']:
            print(line)
        
        print("")
        
        # Mapa mental
        for line in results['visualizations']['concept_map']:
            print(line)
        
        print("")
        
        # Timeline emocional
        for line in results['visualizations']['emotional_timeline']:
            print(line)
        
        # 2.3 Resumo Executivo Narrativo
        print(f"\n\n🎯 RESUMO EXECUTIVO:")
        print(f"{'─'*40}")
        
        # Calcular resumo
        dominant_themes = []
        for i, weight in enumerate(results['topic_distribution']):
            if weight > 0.15:
                dominant_themes.append(f"{results['topics'][i]['words'][0]} ({weight:.0%})")
        
        emotional_trajectory = "neutro"
        if results['storyline']['emotional_journey']:
            start = results['storyline']['emotional_journey'][0]['sentiment']
            end = results['storyline']['emotional_journey'][-1]['sentiment']
            if end > start + 0.3:
                emotional_trajectory = "ascendente (melhora ao longo da entrevista)"
            elif end < start - 0.3:
                emotional_trajectory = "descendente (piora ao longo da entrevista)"
            else:
                emotional_trajectory = "estável com flutuações"
        
        print(f"- Temas Dominantes: {', '.join(dominant_themes)}")
        print(f"- Evolução Emocional: {emotional_trajectory}")
        
        if results['contradictions']:
            main_contradiction = results['contradictions'][0]
            print(f"- Contradição Principal: Ambivalência sobre "
                  f"'{', '.join(main_contradiction['topic_words'])}'")
        
        # Nível de abertura
        avg_response_times = []
        for patterns in results['linguistic_patterns']['topic_patterns'].values():
            avg_response_times.append(patterns['response_time_estimate'])
        
        if avg_response_times:
            avg_response = np.mean(avg_response_times)
            openness = "Alto" if avg_response > 30 else "Médio" if avg_response > 20 else "Baixo"
            print(f"- Nível de Abertura: {openness} "
                  f"(tempo médio de resposta: {avg_response:.0f}s)")
        
        # 2.4 Linha do Tempo Narrativa
        print(f"\n📈 ANÁLISE TEMPORAL NARRATIVA (Blocos de 5 minutos):")
        print(f"{'─'*60}")
        
        for block in results['narrative_blocks']:
            # Cabeçalho do bloco com emoji
            print(f"\n{block['sentiment_emoji']} Bloco {block['block_number']} ({block['time_range']}): {block['title']}")
            
            # Temas
            theme_str = ""
            if block['themes']:
                theme_percentages = [f"{t['name']} ({t['percentage']:.0f}%)" 
                                   for t in block['themes']]
                theme_str = ', '.join(theme_percentages)
            else:
                theme_str = "transição temática"
            
            print(f"├─ Temas: {theme_str}")
            print(f"├─ Sentimento: {block['sentiment_label']} ({block['sentiment']:+.2f})", end="")
            
            if block['is_emotional_peak']:
                print(f" ⚠️ PICO EMOCIONAL", end="")
            print()
            
            print(f"├─ Hesitações: {block['hesitations']} ocorrências", end="")
            if block['hesitations'] > 10:
                print(f" (processamento intenso)", end="")
            print()
            
            print(f"└─ Nota: {block['nota']}")
        
        # 2.5 Contradições Contextualizadas
        if results['contradictions']:
            print(f"\n⚖️ CONTRADIÇÕES E AMBIVALÊNCIAS:")
            print(f"{'─'*40}")
            
            for i, contradiction in enumerate(results['contradictions'][:2], 1):
                intensity_label = "muito alta" if contradiction['intensity'] > 1.0 else \
                                "alta" if contradiction['intensity'] > 0.7 else "moderada"
                
                print(f"\n{'🔴' if i == 1 else '🟡'} CONTRADIÇÃO {i}: "
                      f"{', '.join(contradiction['topic_words']).title()}")
                print(f"├─ Visão Positiva: \"{contradiction['positive_example']}\"")
                print(f"├─ Visão Negativa: \"{contradiction['negative_example']}\"")
                print(f"├─ Intensidade: {contradiction['intensity']:.1f} ({intensity_label})")
                print(f"└─ Interpretação: _______")
        
        # 2.6 Hipóteses Interpretativas
        print(f"\n💭 HIPÓTESES INTERPRETATIVAS:")
        print(f"{'─'*40}")
        
        for hypothesis in results['hypotheses']:
            print(f"\n🔍 {hypothesis['category']}:")
            print(f"├─ Observação: {hypothesis['observation']}")
            print(f"└─ Hipótese: {hypothesis['hypothesis']}")
            print(f"   {'─' * 60}")
        
        # 2.7 Insights Emergentes
        print(f"\n🌟 INSIGHTS EMERGENTES:")
        print(f"{'─'*40}")
        
        # Temas não óbvios (aparecem em momentos críticos mas não são dominantes)
        crisis_themes = set()
        for crisis in results['storyline']['crisis_points']:
            if crisis['themes']:
                crisis_themes.update([t['name'] for t in crisis['themes']])
        
        dominant_theme_words = set()
        for topic, weight in zip(results['topics'], results['topic_distribution']):
            if weight > 0.2:
                dominant_theme_words.update(topic['words'][:3])
        
        hidden_themes = crisis_themes - dominant_theme_words
        if hidden_themes:
            print(f"\n🔍 Temas emergentes não óbvios:")
            for theme in list(hidden_themes)[:3]:
                print(f"├─ '{theme}' (aparece em momentos críticos)")
        
        # Padrões de enfrentamento
        if results['storyline']['resolution_attempts']:
            print(f"\n💪 Recursos identificados:")
            print(f"├─ {len(results['storyline']['resolution_attempts'])} "
                  f"tentativas de resolução emocional detectadas")
            print(f"└─ Capacidade de auto-regulação presente")
        
        # 2.8 Recomendações
        print(f"\n📋 RECOMENDAÇÕES PARA PRÓXIMAS SESSÕES:")
        print(f"{'─'*40}")
        
        if results['recommendations']['explore_further']:
            print(f"\n🎯 EXPLORAR MAIS PROFUNDAMENTE:")
            for rec in results['recommendations']['explore_further']:
                print(f"├─ {rec}")
        
        if results['recommendations']['timing']:
            print(f"\n⏰ TIMING OTIMIZADO:")
            for rec in results['recommendations']['timing']:
                print(f"├─ {rec}")
        
        if results['recommendations']['approach']:
            print(f"\n🗣️ ABORDAGEM RECOMENDADA:")
            for rec in results['recommendations']['approach']:
                print(f"├─ {rec}")
        
        # Rodapé
        print(f"\n{'='*80}")
        print(f"                            📊 FIM DO RELATÓRIO")
        print(f"{'='*80}")

def analyze_interview_narrative(filename, participant_name=None):
    """Função principal para análise narrativa"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        
        if not participant_name:
            participant_name = Path(filename).stem.replace('_', ' ').title()
        
        analyzer = NarrativeInterviewAnalyzer()
        results = analyzer.generate_dual_report(text, participant_name)
        
        return results
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {filename}")
        return None
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()
        return None




def default_sample_path():
    project_root = Path(__file__).resolve().parents[2]
    return project_root / "data" / "sample" / "estatistica_psicobio_aula_2024.txt"


def main(path=None, participant_name=None):
    print("🚀 ANALISADOR DE ENTREVISTAS - VERSÃO NARRATIVA")
    print("=" * 60)

    arquivo_transcricao = Path(path) if path else default_sample_path()
    nome_participante = participant_name or "Prof. Estatística (Aula 2024)"
    
    print(f"📁 Analisando: {arquivo_transcricao}")
    print(f"👤 Participante: {nome_participante}")
    print()
    
    # Executar análise
    resultado = analyze_interview_narrative(arquivo_transcricao, nome_participante)
    
    if resultado:
        print("\n✅ Análise concluída com sucesso!")
        print("💡 Relatório dividido em duas partes:")
        print("   1️⃣ ANÁLISE: Dados técnicos agrupados por tema")
        print("   2️⃣ SÍNTESE: Narrativa interpretativa com templates")
        print("📝 Complete os espaços '______' com suas interpretações.")
    else:
        print("\n❌ Falha na análise.")
        print("💡 Verifique se o arquivo existe e está na pasta correta.")


if __name__ == "__main__":
    main()
