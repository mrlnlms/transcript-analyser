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

class EnhancedInterviewAnalyzer:
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
                    'positive_example': positive_sentences[0]['text'][:100] + '...',
                    'negative_example': negative_sentences[0]['text'][:100] + '...',
                    'intensity': contradiction_intensity,
                    'count': len(positive_sentences) + len(negative_sentences)
                })
        
        return contradictions
    
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
        avg_sentence_length = np.mean([len(sent.split()) for sent in sentences])
        
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
                
                topic_patterns[topic['description']] = {
                    'hesitations': topic_hesitations,
                    'uncertainty_markers': topic_uncertainty,
                    'certainty_markers': topic_certainty,
                    'uncertainty_score': uncertainty_score,
                    'avg_sentence_length': np.mean([len(sent.split()) for sent in topic_sentences]),
                    'sentence_count': len(topic_sentences)
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
                    'sentiment': avg_sentiment
                })
        
        connections.sort(key=lambda x: x['strength'], reverse=True)
        return connections[:15]  # Top 15 conexões
    
    def analyze_temporal_phases(self, segments):
        """Analisa padrões nas fases temporais (início, meio, fim)"""
        if len(segments) < 3:
            return {}
        
        # Dividir em três fases
        phase_size = len(segments) // 3
        phases = {
            'início': segments[:phase_size],
            'meio': segments[phase_size:phase_size*2],
            'fim': segments[phase_size*2:]
        }
        
        phase_analysis = {}
        for phase_name, phase_segments in phases.items():
            if phase_segments:
                sentiments = [self.analyze_sentiment_simple(seg['text']) for seg in phase_segments]
                phase_text = ' '.join([seg['text'] for seg in phase_segments])
                words = phase_text.split()
                
                # Calcular métricas da fase
                hesitations = sum(1 for word in words if word in self.hesitation_markers)
                uncertainty = sum(1 for word in words if any(unc in word for unc in self.uncertainty_words))
                
                phase_analysis[phase_name] = {
                    'avg_sentiment': np.mean(sentiments),
                    'sentiment_std': np.std(sentiments),
                    'hesitations': hesitations,
                    'uncertainty_count': uncertainty,
                    'word_count': len(words)
                }
        
        return phase_analysis
    
    def generate_insights_templates(self, analysis_results):
        """Gera templates de insights para interpretação"""
        insights = []
        
        # Insights sobre tópicos dominantes
        if analysis_results['topics']:
            dominant_topic = max(analysis_results['topics'], 
                               key=lambda x: analysis_results['topic_distribution'][x['id']])
            insights.append({
                'category': 'tópico_dominante',
                'template': f"📊 Tópico dominante '{dominant_topic['description']}' ({analysis_results['topic_distribution'][dominant_topic['id']]:.1%} do conteúdo) sugere que _______"
            })
        
        # Insights sobre contradições
        if analysis_results['contradictions']:
            max_contradiction = max(analysis_results['contradictions'], key=lambda x: x['intensity'])
            insights.append({
                'category': 'ambivalência',
                'template': f"⚖️ Alta ambivalência sobre '{max_contradiction['topic']}' (intensidade: {max_contradiction['intensity']:.1f}) pode indicar _______"
            })
        
        # Insights sobre trajetória temporal
        if analysis_results['phase_analysis']:
            phases = analysis_results['phase_analysis']
            if 'início' in phases and 'fim' in phases:
                sentiment_change = phases['fim']['avg_sentiment'] - phases['início']['avg_sentiment']
                if abs(sentiment_change) > 0.3:
                    direction = "ascendente" if sentiment_change > 0 else "descendente"
                    insights.append({
                        'category': 'trajetória',
                        'template': f"📈 Trajetória emocional {direction} (Δ = {sentiment_change:.2f}) sugere _______"
                    })
        
        # Insights sobre padrões linguísticos
        ling = analysis_results['linguistic_patterns']
        if ling['uncertainty_count'] > ling['certainty_count'] * 2:
            insights.append({
                'category': 'incerteza',
                'template': f"🤔 Predomínio de marcadores de incerteza ({ling['uncertainty_count']} vs {ling['certainty_count']} certeza) indica _______"
            })
        
        # Insights sobre rede conceitual
        if analysis_results['concept_network']:
            strongest = analysis_results['concept_network'][0]
            insights.append({
                'category': 'conexão',
                'template': f"🔗 Forte associação entre '{strongest['concept1']}' e '{strongest['concept2']}' (força: {strongest['strength']}) sugere _______"
            })
            
            # Conexões com valência emocional
            positive_connections = [c for c in analysis_results['concept_network'][:5] 
                                  if c['sentiment'] > 0.3]
            negative_connections = [c for c in analysis_results['concept_network'][:5] 
                                  if c['sentiment'] < -0.3]
            
            if positive_connections:
                pc = positive_connections[0]
                insights.append({
                    'category': 'conexão_positiva',
                    'template': f"😊 Associação positiva entre '{pc['concept1']}' e '{pc['concept2']}' pode significar _______"
                })
        
        return insights
    
    def generate_auto_insights(self, analysis_results):
        """Gera insights automáticos diretos (mantém formato original)"""
        insights = []
        
        # Insights sobre tópicos
        if analysis_results['topics']:
            dominant_topic = max(analysis_results['topics'], 
                               key=lambda x: analysis_results['topic_distribution'][x['id']])
            insights.append(f"📊 Tópico dominante: '{dominant_topic['description']}' "
                          f"({analysis_results['topic_distribution'][dominant_topic['id']]:.1%} do conteúdo)")
        
        # Insights sobre contradições
        if analysis_results['contradictions']:
            max_contradiction = max(analysis_results['contradictions'], key=lambda x: x['intensity'])
            insights.append(f"⚖️ Maior ambivalência detectada em: '{max_contradiction['topic']}' "
                          f"(intensidade: {max_contradiction['intensity']:.1f})")
        
        # Insights linguísticos
        ling = analysis_results['linguistic_patterns']
        if ling['uncertainty_count'] > ling['certainty_count'] * 2:
            insights.append("🤔 Alto nível de incerteza linguística detectado - "
                          "possível baixa autoconfiança ou processamento de temas complexos")
        
        if ling['total_hesitations'] > len(analysis_results['segments']) * 3:
            insights.append("⏸️ Muitas hesitações detectadas - indica processamento emocional "
                          "intenso ou dificuldade de verbalização")
        
        # Insights sobre trajetória emocional
        temporal = analysis_results['temporal_analysis']
        sentiment_trend = [seg['sentiment'] for seg in temporal]
        if len(sentiment_trend) > 2:
            if sentiment_trend[-1] > sentiment_trend[0]:
                insights.append("📈 Trajetória emocional ascendente - processo de elaboração "
                              "bem-sucedido durante a conversa")
            elif sentiment_trend[-1] < sentiment_trend[0]:
                insights.append("📉 Trajetória emocional descendente - possível fadiga emocional "
                              "ou abordagem de temas difíceis")
        
        # Insights sobre rede conceitual
        if analysis_results['concept_network']:
            strongest_connection = analysis_results['concept_network'][0]
            insights.append(f"🔗 Conexão conceitual mais forte: "
                          f"'{strongest_connection['concept1']}' ↔ '{strongest_connection['concept2']}' "
                          f"(força: {strongest_connection['strength']})")
        
        return insights
    
    def generate_enhanced_report(self, text, participant_name="Participante"):
        """Gera relatório completo com insights automáticos e templates"""
        print("🚀 GERANDO RELATÓRIO COMPLETO E APRIMORADO...")
        print("=" * 80)
        
        # Limpeza básica
        clean_text = self.clean_text(text)
        
        # 1. Segmentação temporal
        segments = self.segment_by_time(clean_text, minutes_per_segment=5)
        print(f"📊 Texto dividido em {len(segments)} segmentos temporais")
        
        # 2. Extração de tópicos
        topics, topic_distribution = self.extract_topics_enhanced(clean_text)
        print(f"🎯 {len(topics)} tópicos principais identificados")
        
        # 3. Análise temporal de sentimento
        temporal_analysis = []
        for segment in segments:
            sentiment = self.analyze_sentiment_simple(segment['text'])
            temporal_analysis.append({
                'time_range': segment['time_range'],
                'sentiment': sentiment,
                'word_count': segment['word_count']
            })
        
        # 4. Detecção de contradições
        contradictions = self.detect_contradictions(clean_text, topics)
        
        # 5. Padrões linguísticos detalhados
        linguistic_patterns = self.analyze_linguistic_patterns_detailed(clean_text, topics, segments)
        
        # 6. Rede de conceitos aprimorada
        concept_network = self.create_concept_network_enhanced(clean_text, topics)
        
        # 7. Análise de fases temporais
        phase_analysis = self.analyze_temporal_phases(segments)
        
        # Compilar resultados
        analysis_results = {
            'participant': participant_name,
            'segments': segments,
            'topics': topics,
            'topic_distribution': topic_distribution,
            'temporal_analysis': temporal_analysis,
            'contradictions': contradictions,
            'linguistic_patterns': linguistic_patterns,
            'concept_network': concept_network,
            'phase_analysis': phase_analysis
        }
        
        # 8. Gerar insights automáticos e templates
        auto_insights = self.generate_auto_insights(analysis_results)
        analysis_results['auto_insights'] = auto_insights
        
        insight_templates = self.generate_insights_templates(analysis_results)
        analysis_results['insight_templates'] = insight_templates
        
        # Gerar relatório formatado
        self.print_enhanced_report(analysis_results)
        
        return analysis_results
    
    def print_enhanced_report(self, results):
        """Imprime relatório completo com seções originais + templates"""
        
        print(f"\n{'='*80}")
        print(f"📋 RELATÓRIO COMPLETO DE ANÁLISE - {results['participant']}")
        print(f"{'='*80}")
        
        # RESUMO EXECUTIVO (mantém formato original)
        print(f"\n🎯 RESUMO EXECUTIVO:")
        print(f"────────────────────")
        for insight in results['auto_insights']:
            print(f"• {insight}")
        
        # TÓPICOS IDENTIFICADOS
        print(f"\n🧠 TÓPICOS PRINCIPAIS IDENTIFICADOS:")
        print(f"─────────────────────────────────────")
        for i, topic in enumerate(results['topics']):
            weight = results['topic_distribution'][i] if i < len(results['topic_distribution']) else 0
            print(f"📌 Tópico {i+1} ({weight:.1%}): {topic['description']}")
            print(f"   Palavras-chave: {', '.join(topic['words'][:6])}")
        
        # Template de interpretação para tópicos
        topic_templates = [t for t in results['insight_templates'] if t['category'] == 'tópico_dominante']
        if topic_templates:
            print(f"\n   💡 Interpretação:")
            for template in topic_templates:
                print(f"   └─ {template['template']}")
        
        # ANÁLISE TEMPORAL (formato original)
        print(f"\n⏰ EVOLUÇÃO TEMPORAL (Segmentos de ~5 minutos):")
        print(f"──────────────────────────────────────────────")
        for segment in results['temporal_analysis']:
            sentiment_emoji = "😊" if segment['sentiment'] > 0.2 else "😐" if segment['sentiment'] > -0.2 else "😔"
            print(f"{segment['time_range']:>12} | {sentiment_emoji} Sentimento: {segment['sentiment']:+.2f} | "
                  f"Palavras: {segment['word_count']:>4}")
        
        # Análise de fases com templates
        if results['phase_analysis']:
            print(f"\n📊 ANÁLISE POR FASES:")
            print(f"────────────────────")
            for phase, metrics in results['phase_analysis'].items():
                sentiment_emoji = "😊" if metrics['avg_sentiment'] > 0.2 else "😐" if metrics['avg_sentiment'] > -0.2 else "😔"
                print(f"\n{phase.upper()}:")
                print(f"  {sentiment_emoji} Sentimento médio: {metrics['avg_sentiment']:+.2f} (σ={metrics['sentiment_std']:.2f})")
                print(f"  ⏸️  Hesitações: {metrics['hesitations']} ({metrics['hesitations']/metrics['word_count']*100:.1f} por 100 palavras)")
                print(f"  🤔 Marcadores de incerteza: {metrics['uncertainty_count']}")
            
            # Templates de trajetória
            trajectory_templates = [t for t in results['insight_templates'] if t['category'] == 'trajetória']
            if trajectory_templates:
                print(f"\n  💡 Interpretação da trajetória:")
                for template in trajectory_templates:
                    print(f"  └─ {template['template']}")
        
        # CONTRADIÇÕES DETECTADAS
        if results['contradictions']:
            print(f"\n⚖️ CONTRADIÇÕES/AMBIVALÊNCIAS DETECTADAS:")
            print(f"─────────────────────────────────────────")
            for contradiction in results['contradictions'][:3]:  # Top 3
                print(f"🔄 Sobre: {contradiction['topic']}")
                print(f"   ➕ Positivo: {contradiction['positive_example']}")
                print(f"   ➖ Negativo: {contradiction['negative_example']}")
                print(f"   📊 Intensidade: {contradiction['intensity']:.2f}")
            
            # Templates de ambivalência
            ambiv_templates = [t for t in results['insight_templates'] if t['category'] == 'ambivalência']
            if ambiv_templates:
                print(f"\n   💡 Interpretação:")
                for template in ambiv_templates:
                    print(f"   └─ {template['template']}")
        
        # REDE DE CONCEITOS
        if results['concept_network']:
            print(f"\n🕸️ REDE DE CONCEITOS (Top 10 conexões):")
            print(f"─────────────────────────────────────────")
            for i, connection in enumerate(results['concept_network'][:10], 1):
                strength_bar = "█" * min(int(connection['strength']), 10)
                sentiment_indicator = "+" if connection['sentiment'] > 0 else "-"
                print(f"{i:>2}. {connection['concept1']:>12} ↔ {connection['concept2']:<12} "
                      f"{strength_bar} ({connection['strength']}) [{sentiment_indicator}]")
            
            # Templates de conexões
            connection_templates = [t for t in results['insight_templates'] 
                                  if t['category'] in ['conexão', 'conexão_positiva']]
            if connection_templates:
                print(f"\n   💡 Interpretação das conexões:")
                for template in connection_templates:
                    print(f"   └─ {template['template']}")
        
        # PADRÕES LINGUÍSTICOS
        print(f"\n🎭 PADRÕES LINGUÍSTICOS:")
        print(f"──────────────────────")
        ling = results['linguistic_patterns']
        print(f"• Hesitações totais: {ling['total_hesitations']}")
        print(f"• Razão Certeza/Incerteza: {ling['certainty_ratio']:.2f}")
        print(f"• Comprimento médio de frase: {ling['avg_sentence_length']:.1f} palavras")
        
        # Templates linguísticos
        ling_templates = [t for t in results['insight_templates'] if t['category'] == 'incerteza']
        if ling_templates:
            print(f"\n💡 Interpretação:")
            for template in ling_templates:
                print(f"└─ {template['template']}")
        
        if ling['topic_patterns']:
            print(f"\n📊 Padrões por tópico:")
            for topic, patterns in ling['topic_patterns'].items():
                print(f"\n   • {topic[:40]}...")
                print(f"     ├─ Hesitações: {patterns['hesitations']} "
                      f"({patterns['hesitations']/patterns['sentence_count']:.1f} por frase)")
                print(f"     ├─ Incerteza: {patterns['uncertainty_score']:.1f}% "
                      f"({patterns['uncertainty_markers']} marcadores)")
                print(f"     └─ Complexidade: {patterns['avg_sentence_length']:.1f} palavras/frase")
                
                # Template específico do tópico se houver padrão significativo
                if patterns['uncertainty_score'] > 70:
                    print(f"        💡 Alta incerteza neste tópico ({patterns['uncertainty_score']:.0f}%) sugere _______")
        
        # SÍNTESE FINAL COM TEMPLATES
        print(f"\n{'='*80}")
        print(f"💡 TEMPLATES PARA INTERPRETAÇÃO QUALITATIVA:")
        print(f"{'='*80}")
        
        # Agrupar todos os templates por categoria
        template_categories = {
            'Visão Geral': ['tópico_dominante', 'trajetória'],
            'Dinâmicas Emocionais': ['ambivalência', 'conexão_positiva'],
            'Padrões Comunicacionais': ['incerteza', 'conexão']
        }
        
        for category_name, category_types in template_categories.items():
            relevant_templates = [t for t in results['insight_templates'] 
                                if t['category'] in category_types]
            if relevant_templates:
                print(f"\n📌 {category_name}:")
                for i, template in enumerate(relevant_templates, 1):
                    print(f"\n{i}. {template['template']}")
                    print(f"   " + "─" * 70)
        
        print(f"\n{'='*80}")
        print(f"📊 RELATÓRIO CONCLUÍDO")
        print(f"{'='*80}")

def analyze_interview_enhanced(filename, participant_name=None):
    """Função principal para análise aprimorada"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        
        if not participant_name:
            participant_name = Path(filename).stem.replace('_', ' ').title()
        
        analyzer = EnhancedInterviewAnalyzer()
        results = analyzer.generate_enhanced_report(text, participant_name)
        
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
    print("🚀 ANALISADOR DE ENTREVISTAS - VERSÃO COMPLETA COM TEMPLATES")
    print("=" * 60)

    arquivo_transcricao = Path(path) if path else default_sample_path()
    nome_participante = participant_name or "Prof. Estatística (Aula 2024)"
    
    print(f"📁 Analisando: {arquivo_transcricao}")
    print(f"👤 Participante: {nome_participante}")
    print()
    
    # Executar análise
    resultado = analyze_interview_enhanced(arquivo_transcricao, nome_participante)
    
    if resultado:
        print("\n✅ Análise concluída com sucesso!")
        print("💡 Este relatório combina insights automáticos com templates para interpretação.")
        print("📝 Complete os espaços '______' com sua análise qualitativa.")
    else:
        print("\n❌ Falha na análise.")
        print("💡 Verifique se o arquivo existe e está na pasta correta.")


if __name__ == "__main__":
    main()
