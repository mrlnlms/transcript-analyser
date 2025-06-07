import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
from difflib import SequenceMatcher
import numpy as np
from collections import Counter
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

class TranscriptComparisonAnalyzer:
    def __init__(self):
        self.stemmer = RSLPStemmer()
        self.stop_words = set(stopwords.words('portuguese'))
        self.stop_words.update(['né', 'eh', 'tá', 'ó', 'ah', 'oh', 'um', 'uma'])
        
        # Dicionário para interpretação automática de tópicos
        self.topic_patterns = {
            'metodologia_ensino': {
                'keywords': ['curs', 'aul', 'vai', 'gent', 'faz', 'métod', 'ensn', 'aprend', 'explc'],
                'description': '📚 Metodologia e Condução do Curso',
                'explanation': 'Professor explicando como o curso funciona, metodologia de ensino'
            },
            'teoria_conceitos': {
                'keywords': ['teor', 'conceitul', 'defin', 'princip', 'fundament', 'bas', 'import'],
                'description': '🧠 Fundamentação Teórica',
                'explanation': 'Apresentação de conceitos teóricos e definições fundamentais'
            },
            'medicao_estatistica': {
                'keywords': ['med', 'númer', 'estatist', 'vari', 'dad', 'anál', 'calcul'],
                'description': '📊 Conceitos de Medição e Estatística',
                'explanation': 'Explicação sobre medidas, números, análise de dados'
            },
            'atributos_propriedades': {
                'keywords': ['atribut', 'propriedad', 'caract', 'qualidad', 'isomórf', 'isomorf'],
                'description': '🔍 Atributos e Propriedades',
                'explanation': 'Discussão sobre atributos, características e propriedades (isomorfismo)'
            },
            'fenomenos_objetos': {
                'keywords': ['fenômen', 'objet', 'real', 'mund', 'observ', 'estud'],
                'description': '🌍 Fenômenos e Objetos de Estudo',
                'explanation': 'Análise de fenômenos reais e objetos de investigação'
            },
            'exemplos_praticos': {
                'keywords': ['exempl', 'cas', 'prát', 'situaç', 'aqui', 'dess', 'faz'],
                'description': '💡 Exemplos e Aplicações Práticas',
                'explanation': 'Demonstrações práticas e exemplos concretos'
            },
            'psicologia_comportamento': {
                'keywords': ['psicolog', 'comportament', 'person', 'indivídu', 'human'],
                'description': '🧑‍🎓 Aspectos Psicológicos',
                'explanation': 'Discussão sobre psicologia e comportamento humano'
            },
            'interface_tecnologia': {
                'keywords': ['interfac', 'tecnolog', 'sistem', 'comput', 'digital'],
                'description': '💻 Interface e Tecnologia',
                'explanation': 'Aspectos tecnológicos e interfaces de sistemas'
            },
            'validacao_confiabilidade': {
                'keywords': ['val', 'valid', 'confiabl', 'precis', 'error', 'qual'],
                'description': '✅ Validação e Confiabilidade',
                'explanation': 'Discussão sobre validade, confiabilidade e qualidade das medições'
            },
            'escalas_ordenacao': {
                'keywords': ['escal', 'ord', 'nivel', 'hierarqu', 'classific'],
                'description': '📏 Escalas e Ordenação',
                'explanation': 'Tipos de escalas de medição e sistemas de ordenação'
            }
        }
    
    def interpret_topic(self, words_list, scores_list):
        """Interpreta automaticamente um tópico baseado nas palavras-chave"""
        # Converter palavras para stemmed para comparação
        words_stemmed = [self.stemmer.stem(word.lower()) for word in words_list]
        
        best_match = None
        best_score = 0
        
        # Testar cada padrão
        for pattern_name, pattern_data in self.topic_patterns.items():
            pattern_keywords = pattern_data['keywords']
            
            # Calcular sobreposição com as palavras do tópico
            matches = 0
            total_weight = 0
            
            for i, word in enumerate(words_stemmed):
                if word in pattern_keywords:
                    matches += 1
                    # Dar mais peso para palavras com score alto
                    if i < len(scores_list):
                        total_weight += scores_list[i]
            
            # Score baseado em: número de matches + peso dos scores
            pattern_score = matches + (total_weight / 100)  # Normalizar scores
            
            if pattern_score > best_score:
                best_score = pattern_score
                best_match = pattern_data
        
        # Se não encontrou padrão bom, criar interpretação genérica
        if best_match is None or best_score < 1:
            # Tentar identificar categoria baseada na palavra principal
            main_word = words_list[0] if words_list else "tema"
            return {
                'description': f'📋 Tópico: {main_word.title()}',
                'explanation': f'Discussão centrada em torno de: {", ".join(words_list[:3])}'
            }
        
        return best_match
    
    def clean_text(self, text):
        """Limpa e normaliza o texto da transcrição com stemming"""
        text = text.lower()
        
        # Remover padrões específicos de transcrições
        text = re.sub(r'\b(\w+)(\s+\1){2,}', r'\1', text)
        
        ruidos_transcricao = [
            'né', 'eh', 'ah', 'oh', 'tá', 'ó', 'um', 'uma', 'tipo', 'assim',
            'então', 'aí', 'né pessoal', 'tá bom', 'certo', 'ok', 'beleza'
        ]
        
        for ruido in ruidos_transcricao:
            text = re.sub(r'\b' + re.escape(ruido) + r'\b', ' ', text)
        
        text = re.sub(r'[^a-záàâãéêíóôõúçñ\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        try:
            tokens = word_tokenize(text, language='portuguese')
        except:
            tokens = text.split()
        
        cleaned_tokens = []
        for token in tokens:
            if (token not in self.stop_words and 
                len(token) > 2 and 
                not token.isdigit()):
                try:
                    stemmed = self.stemmer.stem(token)
                    if len(stemmed) > 1:
                        cleaned_tokens.append(stemmed)
                except:
                    cleaned_tokens.append(token)
        
        return ' '.join(cleaned_tokens)
    
    def clean_text_no_stemming(self, text):
        """Limpa texto SEM aplicar stemming - para contexto"""
        text = text.lower()
        
        text = re.sub(r'\b(\w+)(\s+\1){2,}', r'\1', text)
        
        ruidos_transcricao = [
            'né', 'eh', 'ah', 'oh', 'tá', 'ó', 'um', 'uma', 'tipo', 'assim',
            'então', 'aí', 'né pessoal', 'tá bom', 'certo', 'ok', 'beleza'
        ]
        
        for ruido in ruidos_transcricao:
            text = re.sub(r'\b' + re.escape(ruido) + r'\b', ' ', text)
        
        text = re.sub(r'[^a-záàâãéêíóôõúçñ\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        try:
            tokens = word_tokenize(text, language='portuguese')
        except:
            tokens = text.split()
        
        cleaned_tokens = []
        for token in tokens:
            if (token not in self.stop_words and 
                len(token) > 2 and 
                not token.isdigit()):
                cleaned_tokens.append(token)
        
        return ' '.join(cleaned_tokens)
    
    def extract_key_phrases_simple(self, text, n_phrases=20):
        """Versão SIMPLES que funcionava - extrai frases-chave usando frequência"""
        print(f"🔍 Processando texto com {len(text)} caracteres...")
        
        # Limpeza básica primeiro
        cleaned_text = self.clean_text(text)
        print(f"🔍 Após limpeza: {len(cleaned_text)} caracteres")
        
        if len(cleaned_text.strip()) < 100:
            print("⚠️  Texto muito pequeno após limpeza")
            return []
        
        # Abordagem simples: análise de frequência de palavras/bigramas
        words = cleaned_text.split()
        print(f"🔍 Total de palavras após limpeza: {len(words)}")
        
        # Contar palavras individuais
        word_freq = Counter(words)
        
        # Contar bigramas (pares de palavras)
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        bigram_freq = Counter(bigrams)
        
        # Combinar resultados
        all_phrases = []
        
        # Top palavras (filtrar palavras muito comuns ou muito raras)
        for word, freq in word_freq.most_common(n_phrases):
            if freq > 2 and len(word) > 3:  # Pelo menos 3 ocorrências e 4+ caracteres
                score = freq / len(words)  # Frequência relativa
                all_phrases.append((word, score))
        
        # Top bigramas
        for bigram, freq in bigram_freq.most_common(n_phrases // 2):
            if freq > 1:  # Pelo menos 2 ocorrências
                score = freq / len(bigrams)
                all_phrases.append((bigram, score))
        
        # Ordenar por score e remover duplicatas
        all_phrases = list(set(all_phrases))  # Remove duplicatas
        all_phrases.sort(key=lambda x: x[1], reverse=True)
        
        result = all_phrases[:n_phrases]
        print(f"✅ Extraídas {len(result)} frases-chave")
        
        return result
    
    def extract_topics_lda_with_smart_interpretation(self, text, n_topics=5, n_words=10):
        """Extrai tópicos com LDA E interpretação automática inteligente"""
        print(f"🧠 Extraindo {n_topics} tópicos com interpretação inteligente...")
        
        # Limpar texto
        cleaned_text = self.clean_text(text)
        cleaned_no_stem = self.clean_text_no_stemming(text)
        
        if len(cleaned_text.strip()) < 500:
            print("⚠️  Texto muito pequeno para Topic Modeling confiável")
            return [], []
        
        # Dividir por chunks (solução para transcrições)
        chunk_size = 500
        chunks_stem = []
        chunks_no_stem = []
        
        for i in range(0, len(cleaned_text), chunk_size):
            chunk_stem = cleaned_text[i:i + chunk_size]
            chunk_no_stem = cleaned_no_stem[i:i + chunk_size]
            if len(chunk_stem.strip()) > 100:
                chunks_stem.append(chunk_stem)
                chunks_no_stem.append(chunk_no_stem)
        
        print(f"📝 Processando {len(chunks_stem)} chunks...")
        
        # Criar mapeamento stem -> original
        stem_to_original = {}
        words_stem = cleaned_text.split()
        words_no_stem = cleaned_no_stem.split()
        
        min_len = min(len(words_stem), len(words_no_stem))
        for i in range(min_len):
            stem = words_stem[i]
            original = words_no_stem[i]
            if stem in stem_to_original:
                stem_to_original[stem].add(original)
            else:
                stem_to_original[stem] = {original}
        
        try:
            # Vectorizer para LDA
            vectorizer = CountVectorizer(
                max_features=50,
                min_df=1,
                max_df=0.9,
                ngram_range=(1, 2)
            )
            
            doc_term_matrix = vectorizer.fit_transform(chunks_stem)
            feature_names = vectorizer.get_feature_names_out()
            
            # LDA
            actual_topics = min(n_topics, len(chunks_stem) // 2, len(feature_names) // 3)
            
            lda = LatentDirichletAllocation(
                n_components=actual_topics,
                random_state=42,
                max_iter=10,
                learning_method='batch'
            )
            
            lda.fit(doc_term_matrix)
            
            # Extrair tópicos COM interpretação inteligente
            topics = []
            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[-min(n_words, len(feature_names)):][::-1]
                top_words_stem = [feature_names[i] for i in top_words_idx]
                top_scores = [topic[i] for i in top_words_idx]
                
                # Mapear para palavras originais
                top_words_original = []
                for stem_word in top_words_stem:
                    originals = list(stem_to_original.get(stem_word, {stem_word}))
                    original_word = originals[0] if originals else stem_word
                    top_words_original.append(original_word)
                
                # NOVA FUNCIONALIDADE: Interpretação automática
                interpretation = self.interpret_topic(top_words_original, top_scores)
                
                # Criar descrição do tópico (versão stem)
                topic_words_stem = [f"{word}({score:.1f})" for word, score in zip(top_words_stem[:5], top_scores[:5])]
                topic_description = " + ".join(topic_words_stem)
                
                # Criar descrição com palavras originais
                topic_words_original = [f"{word}" for word in top_words_original[:5]]
                topic_context = " + ".join(topic_words_original)
                
                topics.append({
                    'id': topic_idx,
                    'words_stem': top_words_stem,
                    'words_original': top_words_original,
                    'scores': top_scores,
                    'description': topic_description,
                    'context': topic_context,
                    'interpretation': interpretation  # NOVO!
                })
            
            # Calcular distribuição de tópicos
            doc_topic_probs = lda.transform(doc_term_matrix)
            topic_distribution = np.mean(doc_topic_probs, axis=0)
            
            print(f"✅ {len(topics)} tópicos extraídos e interpretados com sucesso")
            return topics, topic_distribution
            
        except Exception as e:
            print(f"❌ Erro no Topic Modeling: {e}")
            return [], []
    
    def compare_topic_distributions(self, dist1, dist2, topics1, topics2):
        """Compara distribuições de tópicos entre dois textos"""
        if len(dist1) == 0 or len(dist2) == 0:
            return 0.0, []
        
        # Pad distributions para ter mesmo tamanho
        max_len = max(len(dist1), len(dist2))
        dist1_padded = np.pad(dist1, (0, max_len - len(dist1)), 'constant')
        dist2_padded = np.pad(dist2, (0, max_len - len(dist2)), 'constant')
        
        # Similaridade coseno entre distribuições
        similarity = cosine_similarity([dist1_padded], [dist2_padded])[0][0]
        
        # Encontrar tópicos mais próximos
        topic_matches = []
        for i, topic1 in enumerate(topics1):
            if i < len(dist1):
                best_match = None
                best_score = 0
                
                for j, topic2 in enumerate(topics2):
                    if j < len(dist2):
                        # Comparar palavras dos tópicos
                        words1 = set(topic1['words_stem'][:5])
                        words2 = set(topic2['words_stem'][:5])
                        word_overlap = len(words1.intersection(words2)) / len(words1.union(words2))
                        
                        if word_overlap > best_score:
                            best_score = word_overlap
                            best_match = j
                
                if best_match is not None and best_score > 0.1:
                    topic_matches.append({
                        'topic1_id': i,
                        'topic2_id': best_match,
                        'overlap': best_score,
                        'weight1': dist1[i],
                        'weight2': dist2[best_match] if best_match < len(dist2) else 0,
                        'interpretation1': topic1.get('interpretation', {}),
                        'interpretation2': topics2[best_match].get('interpretation', {}) if best_match < len(topics2) else {}
                    })
        
        return similarity, topic_matches
    
    def calculate_similarity_metrics(self, text1, text2):
        """Calcula múltiplas métricas de similaridade"""
        results = {}
        
        # Similaridade de sequência básica
        results['sequence_similarity'] = SequenceMatcher(None, text1, text2).ratio()
        
        # Limpeza dos textos
        clean_text1 = self.clean_text(text1)
        clean_text2 = self.clean_text(text2)
        
        # Similaridade após limpeza
        results['clean_sequence_similarity'] = SequenceMatcher(None, clean_text1, clean_text2).ratio()
        
        # Similaridade coseno com TF-IDF
        if clean_text1.strip() and clean_text2.strip():
            vectorizer = TfidfVectorizer()
            try:
                tfidf_matrix = vectorizer.fit_transform([clean_text1, clean_text2])
                cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                results['cosine_similarity'] = cosine_sim
            except:
                results['cosine_similarity'] = 0.0
        else:
            results['cosine_similarity'] = 0.0
        
        # Similaridade de palavras-chave
        words1 = set(clean_text1.split())
        words2 = set(clean_text2.split())
        if words1 and words2:
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            results['jaccard_similarity'] = len(intersection) / len(union)
        else:
            results['jaccard_similarity'] = 0.0
        
        return results
    
    def analyze_content_structure(self, text1, text2):
        """Analisa a estrutura do conteúdo com interpretação inteligente de tópicos"""
        print("\n" + "="*60)
        print("🔍 ANÁLISE DE CONTEÚDO COM INTERPRETAÇÃO INTELIGENTE")
        print("="*60)
        
        # 1. Análise de frases-chave (versão SIMPLES que funciona)
        print("\n📊 EXTRAÇÃO DE TERMOS FREQUENTES:")
        phrases1 = self.extract_key_phrases_simple(text1)
        phrases2 = self.extract_key_phrases_simple(text2)
        
        print("\n--- TEXTO 1 ---")
        if len(phrases1) > 0:
            for phrase, score in phrases1[:8]:
                print(f"• {phrase}: {score:.3f}")
        else:
            print("⚠️  Nenhum termo frequente extraído do Texto 1")
        
        print("\n--- TEXTO 2 ---")
        if len(phrases2) > 0:
            for phrase, score in phrases2[:8]:
                print(f"• {phrase}: {score:.3f}")
        else:
            print("⚠️  Nenhum termo frequente extraído do Texto 2")
        
        # 2. Topic Modeling com interpretação inteligente
        print(f"\n🧠 TOPIC MODELING COM INTERPRETAÇÃO AUTOMÁTICA:")
        print("-" * 50)
        
        topics1, dist1 = self.extract_topics_lda_with_smart_interpretation(text1, n_topics=5)
        topics2, dist2 = self.extract_topics_lda_with_smart_interpretation(text2, n_topics=5)
        
        if topics1 and topics2:
            print("\n🎯 TEMAS IDENTIFICADOS NO TEXTO 1:")
            for i, topic in enumerate(topics1):
                weight = dist1[i] if i < len(dist1) else 0
                interpretation = topic.get('interpretation', {})
                
                print(f"\n   {interpretation.get('description', f'Tópico {i+1}')} ({weight:.1%})")
                print(f"   📝 Palavras-chave: {topic['context']}")
                print(f"   🔍 Interpretação: {interpretation.get('explanation', 'Tema não identificado')}")
            
            print("\n🎯 TEMAS IDENTIFICADOS NO TEXTO 2:")
            for i, topic in enumerate(topics2):
                weight = dist2[i] if i < len(dist2) else 0
                interpretation = topic.get('interpretation', {})
                
                print(f"\n   {interpretation.get('description', f'Tópico {i+1}')} ({weight:.1%})")
                print(f"   📝 Palavras-chave: {topic['context']}")
                print(f"   🔍 Interpretação: {interpretation.get('explanation', 'Tema não identificado')}")
            
            # Comparar distribuições de tópicos
            topic_similarity, topic_matches = self.compare_topic_distributions(
                dist1, dist2, topics1, topics2
            )
            
            print(f"\n🔄 SIMILARIDADE TEMÁTICA GERAL: {topic_similarity:.1%}")
            
            if topic_matches:
                print("\n🎯 TEMAS RELACIONADOS ENTRE OS TEXTOS:")
                for match in topic_matches:
                    interp1 = match['interpretation1']
                    interp2 = match['interpretation2']
                    
                    desc1 = interp1.get('description', f"Tópico {match['topic1_id']+1}")
                    desc2 = interp2.get('description', f"Tópico {match['topic2_id']+1}")
                    
                    print(f"\n   🔗 RELAÇÃO TEMÁTICA (overlap: {match['overlap']:.1%}):")
                    print(f"   📖 Texto 1: {desc1}")
                    print(f"   📖 Texto 2: {desc2}")
                    
                    if match['overlap'] > 0.3:
                        print(f"   ✅ Temas muito similares - indicam mesmo conteúdo")
                    elif match['overlap'] > 0.2:
                        print(f"   🟡 Temas relacionados - conteúdo complementar")
                    else:
                        print(f"   🔍 Temas parcialmente relacionados")
        else:
            topic_similarity = 0.0
            print("⚠️  Topic Modeling não pôde ser aplicado (textos muito pequenos)")
        
        # 3. Análise de sobreposição de termos
        phrases1_set = set([phrase for phrase, _ in phrases1]) if phrases1 else set()
        phrases2_set = set([phrase for phrase, _ in phrases2]) if phrases2 else set()
        
        common_phrases = phrases1_set.intersection(phrases2_set)
        total_unique_phrases = len(phrases1_set.union(phrases2_set))
        
        if total_unique_phrases > 0:
            phrase_overlap = len(common_phrases) / total_unique_phrases
        else:
            phrase_overlap = 0.0
        
        print(f"\n📝 TERMOS FREQUENTES EM COMUM:")
        print(f"Sobreposição: {phrase_overlap:.1%} ({len(common_phrases)} de {total_unique_phrases})")
        
        if common_phrases and phrases1 and phrases2:
            phrases1_dict = {phrase: score for phrase, score in phrases1}
            phrases2_dict = {phrase: score for phrase, score in phrases2}
            
            print("\nTermos comuns mais importantes:")
            common_sorted = sorted(common_phrases, key=lambda x: phrases1_dict.get(x, 0), reverse=True)
            
            for phrase in common_sorted[:8]:
                score1 = phrases1_dict.get(phrase, 0)
                score2 = phrases2_dict.get(phrase, 0)
                avg_score = (score1 + score2) / 2
                print(f"   • {phrase}: {avg_score:.3f}")
        
        return {
            'phrase_overlap': phrase_overlap,
            'common_phrases': list(common_phrases),
            'total_phrases_text1': len(phrases1) if phrases1 else 0,
            'total_phrases_text2': len(phrases2) if phrases2 else 0,
            'topic_similarity': topic_similarity,
            'topics1': topics1,
            'topics2': topics2,
            'topic_distribution1': dist1.tolist() if len(dist1) > 0 else [],
            'topic_distribution2': dist2.tolist() if len(dist2) > 0 else []
        }

    def create_visualizations(self, analysis_results, nome1, nome2, output_dir=None):
        """Create a compact visual summary of the topic comparison."""
        topics1 = analysis_results.get('topics1', [])
        topics2 = analysis_results.get('topics2', [])
        dist1 = np.array(analysis_results.get('topic_distribution1', []))
        dist2 = np.array(analysis_results.get('topic_distribution2', []))

        if not topics1 or not topics2 or len(dist1) == 0 or len(dist2) == 0:
            print("⚠️  Não é possível criar visualizações sem tópicos válidos")
            return None

        project_root = Path(__file__).resolve().parents[2]
        output_path = Path(output_dir) if output_dir else project_root / "output" / "visualizations"
        output_path.mkdir(parents=True, exist_ok=True)

        print("📊 Gerando visualizações...")

        n_topics = min(len(dist1), len(dist2), len(topics1), len(topics2))
        topic_labels = [f"T{i + 1}" for i in range(n_topics)]
        x_pos = np.arange(n_topics)
        width = 0.35

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f"Análise Visual de Tópicos\n{nome1} vs {nome2}", fontsize=16, fontweight="bold")

        ax1 = axes[0, 0]
        bars1 = ax1.bar(x_pos - width / 2, dist1[:n_topics], width, label=nome1[:18], alpha=0.8, color="skyblue")
        bars2 = ax1.bar(x_pos + width / 2, dist2[:n_topics], width, label=nome2[:18], alpha=0.8, color="lightcoral")
        ax1.set_xlabel("Tópicos")
        ax1.set_ylabel("Peso (%)")
        ax1.set_title("Distribuição de Tópicos por Documento")
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(topic_labels)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        for bar in list(bars1) + list(bars2):
            height = bar.get_height()
            if height > 0:
                ax1.annotate(
                    f"{height:.1%}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

        ax2 = axes[0, 1]
        all_words = []
        for topic in topics1[:n_topics] + topics2[:n_topics]:
            all_words.extend(topic.get("words_stem", topic.get("words", []))[:5])
        all_words = list(dict.fromkeys(all_words))[:15]

        if all_words:
            matrix_data = []
            topic_names = []
            for label, topics in [(nome1, topics1), (nome2, topics2)]:
                for i, topic in enumerate(topics[:n_topics]):
                    topic_names.append(f"{label[:8]}-T{i + 1}")
                    words = topic.get("words_stem", topic.get("words", []))
                    topic_words = {word: score for word, score in zip(words, topic["scores"])}
                    matrix_data.append([topic_words.get(word, 0) for word in all_words])

            sns.heatmap(
                matrix_data,
                xticklabels=all_words,
                yticklabels=topic_names,
                annot=False,
                cmap="Blues",
                ax=ax2,
                cbar_kws={"label": "Importância"},
            )
            ax2.set_title("Importância das Palavras por Tópico")
            ax2.set_xlabel("Palavras-chave")
            ax2.set_ylabel("Tópicos")
            plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
        else:
            ax2.text(0.5, 0.5, "Dados insuficientes\npara heatmap", transform=ax2.transAxes, ha="center", va="center")
            ax2.set_title("Heatmap - Dados Insuficientes")

        ax3 = axes[1, 0]
        all_topic_words = {}
        for topic in topics1 + topics2:
            words = topic.get("words_stem", topic.get("words", []))
            for word, score in zip(words[:10], topic["scores"][:10]):
                all_topic_words[word] = all_topic_words.get(word, 0) + score

        if all_topic_words:
            try:
                wordcloud = WordCloud(width=400, height=300, background_color="white", max_words=50, colormap="viridis")
                ax3.imshow(wordcloud.generate_from_frequencies(all_topic_words), interpolation="bilinear")
                ax3.axis("off")
                ax3.set_title("Nuvem de Palavras - Termos Principais")
            except Exception as exc:
                ax3.text(0.5, 0.5, f"WordCloud não disponível\n{str(exc)[:30]}...", transform=ax3.transAxes, ha="center", va="center")
                ax3.set_title("Nuvem de Palavras - Não Disponível")
                ax3.axis("off")
        else:
            ax3.text(0.5, 0.5, "Dados insuficientes\npara WordCloud", transform=ax3.transAxes, ha="center", va="center")
            ax3.set_title("WordCloud - Dados Insuficientes")
            ax3.axis("off")

        ax4 = axes[1, 1]
        similarity_matrix = np.zeros((n_topics, n_topics))
        for i, topic1 in enumerate(topics1[:n_topics]):
            for j, topic2 in enumerate(topics2[:n_topics]):
                words1 = set(topic1.get("words_stem", topic1.get("words", []))[:10])
                words2 = set(topic2.get("words_stem", topic2.get("words", []))[:10])
                if words1 and words2:
                    similarity_matrix[i][j] = len(words1.intersection(words2)) / len(words1.union(words2))

        im = ax4.imshow(similarity_matrix, cmap="Reds", interpolation="nearest")
        ax4.set_xticks(range(n_topics))
        ax4.set_yticks(range(n_topics))
        ax4.set_xticklabels([f"T2-{i + 1}" for i in range(n_topics)])
        ax4.set_yticklabels([f"T1-{i + 1}" for i in range(n_topics)])
        ax4.set_xlabel(f"Tópicos - {nome2[:15]}")
        ax4.set_ylabel(f"Tópicos - {nome1[:15]}")
        ax4.set_title("Similaridade entre Tópicos")

        for i in range(n_topics):
            for j in range(n_topics):
                ax4.text(
                    j,
                    i,
                    f"{similarity_matrix[i, j]:.2f}",
                    ha="center",
                    va="center",
                    color="black" if similarity_matrix[i, j] < 0.5 else "white",
                    fontsize=8,
                )

        plt.colorbar(im, ax=ax4, label="Similaridade")
        plt.tight_layout()

        filename = output_path / f"topic_analysis_{nome1.replace(' ', '_')}_vs_{nome2.replace(' ', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"📊 Visualizações salvas em: {filename}")
        return filename
    
    def compare_two_texts(self, text1, text2, nome1="Texto 1", nome2="Texto 2"):
        """Compara dois textos e retorna análise completa"""
        print(f"\n{'='*80}")
        print(f"🔄 COMPARANDO: {nome1} ↔ {nome2}")
        print(f"{'='*80}")
        
        print("=== ESTATÍSTICAS BÁSICAS ===")
        print(f"{nome1}: {len(text1)} caracteres, {len(text1.split())} palavras")
        print(f"{nome2}: {len(text2)} caracteres, {len(text2.split())} palavras")
        
        print("\n=== MÉTRICAS DE SIMILARIDADE ===")
        similarity_metrics = self.calculate_similarity_metrics(text1, text2)
        
        for metric, value in similarity_metrics.items():
            percentage = value * 100
            print(f"{metric.replace('_', ' ').title()}: {percentage:.1f}%")
        
        print("\n=== ANÁLISE DE CONTEÚDO ===")
        content_analysis = self.analyze_content_structure(text1, text2)
        visualization_path = self.create_visualizations(content_analysis, nome1, nome2)
        
        print(f"\nSobreposição de frases-chave: {content_analysis['phrase_overlap']*100:.1f}%")
        
        # Análise final
        print("\n=== INTERPRETAÇÃO DETALHADA ===")
        cosine_score = similarity_metrics['cosine_similarity']
        phrase_overlap = content_analysis['phrase_overlap']
        topic_similarity = content_analysis.get('topic_similarity', 0)
        
        print(f"📊 INDICADORES PRINCIPAIS:")
        print(f"• Cosine Similarity: {cosine_score*100:.1f}% (vocabulário técnico)")
        print(f"• Sobreposição Termos: {phrase_overlap*100:.1f}% (termos em comum)")
        print(f"• Similaridade Tópicos: {topic_similarity*100:.1f}% (temas latentes)")
        print(f"• Jaccard Similarity: {similarity_metrics['jaccard_similarity']*100:.1f}% (palavras únicas)")
        
        # EXPLICAÇÃO DA PONDERAÇÃO
        print(f"\n🎯 CÁLCULO DO SCORE PONDERADO:")
        print(f"• Cosine (40%): {cosine_score*100:.1f}% × 0.4 = {cosine_score*40:.1f}")
        print(f"• Tópicos (30%): {topic_similarity*100:.1f}% × 0.3 = {topic_similarity*30:.1f}")  
        print(f"• Termos (20%): {phrase_overlap*100:.1f}% × 0.2 = {phrase_overlap*20:.1f}")
        print(f"• Jaccard (10%): {similarity_metrics['jaccard_similarity']*100:.1f}% × 0.1 = {similarity_metrics['jaccard_similarity']*10:.1f}")
        
        # Peso maior para métricas mais importantes
        weighted_similarity = (
            cosine_score * 0.4 +           # 40% - vocabulário técnico
            topic_similarity * 0.3 +       # 30% - tópicos descobertos  
            phrase_overlap * 0.2 +         # 20% - termos frequentes
            similarity_metrics['jaccard_similarity'] * 0.1  # 10% - palavras únicas
        )
        
        print(f"\n🎯 SCORE PONDERADO FINAL: {weighted_similarity*100:.1f}%")
        
        if weighted_similarity > 0.75:
            interpretation = "🟢 ALTA similaridade - Conteúdo muito similar"
            confidence = "Alta confiança"
        elif weighted_similarity > 0.6:
            interpretation = "🟡 MÉDIA-ALTA similaridade - Temas relacionados"
            confidence = "Boa confiança"
        elif weighted_similarity > 0.4:
            interpretation = "🟠 MÉDIA similaridade - Alguma sobreposição temática"
            confidence = "Confiança moderada"
        else:
            interpretation = "🔴 BAIXA similaridade - Conteúdos diferentes"
            confidence = "Alta confiança"
        
        print(f"\n🎯 CONCLUSÃO: {interpretation}")
        print(f"Nível de confiança: {confidence}")
        
        # Insights específicos
        print(f"\n💡 INSIGHTS:")
        if cosine_score > 0.8:
            print("• Alto vocabulário compartilhado indica mesmo domínio/área")
        if topic_similarity > 0.6:
            print("• Tópicos latentes similares sugerem estrutura temática parecida")  
        if phrase_overlap > 0.4:
            print("• Muitos termos frequentes em comum")
        
        num_topics1 = len(content_analysis.get('topics1', []))
        num_topics2 = len(content_analysis.get('topics2', []))
        if num_topics1 > 0 and num_topics2 > 0:
            print(f"• Topic Modeling identificou {num_topics1} e {num_topics2} temas principais")
        
        return {
            'similarity_metrics': similarity_metrics,
            'content_analysis': content_analysis,
            'weighted_similarity': weighted_similarity,
            'interpretation': interpretation,
            'confidence': confidence,
            'visualization_path': str(visualization_path) if visualization_path else None,
            'nome1': nome1,
            'nome2': nome2
        }

def load_transcript(path):
    """Carrega uma transcrição de um arquivo .txt"""
    try:
        with open(path, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {path}")
        return None
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return None

def compare_files(paths):
    """Compara múltiplos arquivos entre si"""
    print(f"🔍 Carregando {len(paths)} arquivos...")
    
    # Carregar todos os textos
    textos = {}
    for arquivo in paths:
        texto = load_transcript(arquivo)
        if texto:
            textos[arquivo] = texto
            print(f"✅ Carregado: {arquivo} ({len(texto)} caracteres)")
        else:
            print(f"❌ Falha ao carregar: {arquivo}")
    
    if len(textos) < 2:
        print("❌ Precisa de pelo menos 2 arquivos válidos!")
        return []
    
    print(f"\n📊 Realizando {len(textos) * (len(textos) - 1) // 2} comparações...")
    
    analyzer = TranscriptComparisonAnalyzer()
    resultados = []
    
    # Comparar todos os pares
    arquivos_validos = list(textos.keys())
    for i, arquivo1 in enumerate(arquivos_validos):
        for j, arquivo2 in enumerate(arquivos_validos[i+1:], i+1):
            nome1 = Path(arquivo1).stem
            nome2 = Path(arquivo2).stem
            
            resultado = analyzer.compare_two_texts(
                textos[arquivo1], 
                textos[arquivo2], 
                nome1, 
                nome2
            )
            resultados.append(resultado)
    
    return resultados

def print_summary(resultados):
    """Gera relatório consolidado de todas as comparações"""
    if not resultados:
        return
    
    print(f"\n\n{'='*80}")
    print(f"📋 RELATÓRIO CONSOLIDADO - {len(resultados)} COMPARAÇÕES")
    print(f"{'='*80}")
    
    # Ordenar por similaridade ponderada
    resultados_ordenados = sorted(
        resultados, 
        key=lambda x: x.get('weighted_similarity', x['similarity_metrics']['cosine_similarity']), 
        reverse=True
    )
    
    print("\n🏆 RANKING DE SIMILARIDADE (Score Ponderado):")
    print("-" * 80)
    
    for i, resultado in enumerate(resultados_ordenados, 1):
        score_ponderado = resultado.get('weighted_similarity', 0) * 100
        cosine = resultado['similarity_metrics']['cosine_similarity'] * 100
        topic_sim = resultado['content_analysis'].get('topic_similarity', 0) * 100
        overlap = resultado['content_analysis']['phrase_overlap'] * 100
        
        if score_ponderado > 75:
            emoji = "🟢"
        elif score_ponderado > 60:
            emoji = "🟡"
        elif score_ponderado > 40:
            emoji = "🟠"
        else:
            emoji = "🔴"
        
        print(f"{i:2d}. {emoji} {resultado['nome1']} ↔ {resultado['nome2']}")
        print(f"    Score: {score_ponderado:.1f}% | Cosine: {cosine:.1f}% | Tópicos: {topic_sim:.1f}% | Termos: {overlap:.1f}%")
    
    return resultados_ordenados

def default_sample_paths():
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "data" / "sample"
    return [
        data_dir / "estatistica_psicobio_aula_2024.txt",
        data_dir / "estatistica_psicobio_teoria_medida_2025.txt",
    ]


def main(paths=None):
    arquivos_para_comparar = paths or default_sample_paths()
    
    print("🚀 ANALISADOR FINAL COM VISUALIZAÇÕES")
    print("=" * 60)
    print(f"📁 Arquivos configurados: {len(arquivos_para_comparar)}")
    for i, arquivo in enumerate(arquivos_para_comparar, 1):
        print(f"   {i}. {arquivo}")
    
    # Executar análise
    resultados = compare_files(arquivos_para_comparar)
    
    if resultados:
        print_summary(resultados)
    else:
        print("❌ Nenhuma comparação foi realizada.")


if __name__ == "__main__":
    main()
