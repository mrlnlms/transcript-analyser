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

class TranscriptComparisonAnalyzer:
    def __init__(self):
        self.stemmer = RSLPStemmer()
        self.stop_words = set(stopwords.words('portuguese'))
        # Adicionar palavras específicas de transcrições
        self.stop_words.update(['né', 'eh', 'tá', 'ó', 'ah', 'oh', 'um', 'uma'])
        
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
    
    def extract_topics_lda_with_context(self, text, n_topics=5, n_words=10):
        """Extrai tópicos com LDA E mostra palavras completas para contexto"""
        print(f"🧠 Extraindo {n_topics} tópicos com LDA...")
        
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
            
            # Extrair tópicos COM contexto
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
                
                # Criar descrição do tópico (versão stem)
                topic_words_stem = [f"{word}({score:.2f})" for word, score in zip(top_words_stem[:5], top_scores[:5])]
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
                    'context': topic_context
                })
            
            # Calcular distribuição de tópicos
            doc_topic_probs = lda.transform(doc_term_matrix)
            topic_distribution = np.mean(doc_topic_probs, axis=0)
            
            print(f"✅ {len(topics)} tópicos extraídos com sucesso")
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
                        'context1': topic1['context'],
                        'context2': topics2[best_match]['context'] if best_match < len(topics2) else ""
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
        """Analisa a estrutura do conteúdo incluindo Topic Modeling MELHORADO"""
        print("\n" + "="*60)
        print("🔍 ANÁLISE DE CONTEÚDO DETALHADA")
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
        
        # 2. Topic Modeling MELHORADO com contexto
        print(f"\n🧠 TOPIC MODELING COM CONTEXTO:")
        print("-" * 40)
        
        topics1, dist1 = self.extract_topics_lda_with_context(text1, n_topics=5)
        topics2, dist2 = self.extract_topics_lda_with_context(text2, n_topics=5)
        
        if topics1 and topics2:
            print("\n🎯 TÓPICOS DESCOBERTOS NO TEXTO 1:")
            for i, topic in enumerate(topics1):
                weight = dist1[i] if i < len(dist1) else 0
                print(f"   Tópico {i+1} ({weight:.1%}): {topic['description']}")
                print(f"   💡 Contexto: {topic['context']}")
            
            print("\n🎯 TÓPICOS DESCOBERTOS NO TEXTO 2:")
            for i, topic in enumerate(topics2):
                weight = dist2[i] if i < len(dist2) else 0
                print(f"   Tópico {i+1} ({weight:.1%}): {topic['description']}")
                print(f"   💡 Contexto: {topic['context']}")
            
            # Comparar distribuições de tópicos
            topic_similarity, topic_matches = self.compare_topic_distributions(
                dist1, dist2, topics1, topics2
            )
            
            print(f"\n🔄 SIMILARIDADE DE TÓPICOS: {topic_similarity:.1%}")
            
            if topic_matches:
                print("\n🎯 TÓPICOS RELACIONADOS:")
                for match in topic_matches:
                    print(f"   • T1-{match['topic1_id']+1} ↔ T2-{match['topic2_id']+1} "
                          f"(overlap: {match['overlap']:.1%})")
                    print(f"     📝 Texto 1: {match['context1']}")
                    print(f"     📝 Texto 2: {match['context2']}")
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
    
    # Análise de grupos
    print(f"\n🔍 ANÁLISE DE GRUPOS:")
    print("-" * 50)
    
    mais_similar = resultados_ordenados[0]
    score_max = mais_similar.get('weighted_similarity', 0) * 100
    
    print(f"✨ Par mais similar ({score_max:.1f}%):")
    print(f"   • {mais_similar['nome1']}")
    print(f"   • {mais_similar['nome2']}")
    
    grupos_alta_similaridade = [r for r in resultados_ordenados 
                                if r.get('weighted_similarity', 0) > 0.6]
    
    if len(grupos_alta_similaridade) > 1:
        print(f"\n🎯 {len(grupos_alta_similaridade)} pares com alta similaridade (>60%):")
        for resultado in grupos_alta_similaridade:
            score = resultado.get('weighted_similarity', 0) * 100
            print(f"   • {resultado['nome1']} ↔ {resultado['nome2']} ({score:.1f}%)")
    
    # Insights de Topic Modeling
    print(f"\n🧠 INSIGHTS DE TOPIC MODELING:")
    print("-" * 50)
    
    textos_com_topics = [r for r in resultados if len(r['content_analysis'].get('topics1', [])) > 0]
    
    if textos_com_topics:
        print(f"✅ Topic Modeling aplicado em {len(textos_com_topics)} comparações")
        avg_topic_sim = np.mean([r['content_analysis'].get('topic_similarity', 0) 
                                for r in textos_com_topics])
        print(f"📊 Similaridade média de tópicos: {avg_topic_sim:.1%}")
        
        # Identificar o par com maior similaridade de tópicos
        best_topic_match = max(textos_com_topics, 
                              key=lambda x: x['content_analysis'].get('topic_similarity', 0))
        best_topic_score = best_topic_match['content_analysis']['topic_similarity']
        
        if best_topic_score > 0.5:
            print(f"🎯 Maior similaridade temática ({best_topic_score:.1%}):")
            print(f"   • {best_topic_match['nome1']} ↔ {best_topic_match['nome2']}")
    else:
        print("⚠️  Topic Modeling não pôde ser aplicado (textos muito pequenos)")
    
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
    
    print("🚀 ANALISADOR FINAL DE TRANSCRIÇÕES")
    print("=" * 50)
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
