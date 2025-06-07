import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
import numpy as np
from collections import Counter
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
    
    def extract_key_phrases_with_context(self, text, n_phrases=20):
        """Extrai frases-chave E versão com stemming, mostrando ambas"""
        print(f"Processando texto com {len(text)} caracteres...")
        
        # Versão SEM stemming para contexto
        text_clean_no_stem = self.clean_text_no_stemming(text)
        words_no_stem = text_clean_no_stem.split()
        
        # Versão COM stemming para agrupamento
        text_clean_stem = self.clean_text(text)
        words_stem = text_clean_stem.split()
        
        print(f"Após limpeza: {len(text_clean_stem)} caracteres, {len(words_stem)} palavras")
        
        if len(text_clean_stem.strip()) < 100:
            return []
        
        # Mapear stems para palavras originais
        stem_to_original = {}
        for original, stemmed in zip(words_no_stem, words_stem):
            if stemmed in stem_to_original:
                stem_to_original[stemmed].add(original)
            else:
                stem_to_original[stemmed] = {original}
        
        # Contar com stemming para agrupamento
        word_freq = Counter(words_stem)
        bigrams = [f"{words_stem[i]} {words_stem[i+1]}" for i in range(len(words_stem)-1)]
        bigram_freq = Counter(bigrams)
        
        # Combinar resultados com contexto
        all_phrases = []
        
        # Top palavras
        for stem_word, freq in word_freq.most_common(n_phrases):
            if freq > 2 and len(stem_word) > 3:
                score = freq / len(words_stem)
                original_words = list(stem_to_original.get(stem_word, {stem_word}))
                context = "/".join(sorted(original_words)[:3])
                all_phrases.append((stem_word, score, context))
        
        # Top bigramas
        for bigram, freq in bigram_freq.most_common(n_phrases // 2):
            if freq > 1:
                score = freq / len(bigrams)
                stem_words = bigram.split()
                original_bigram_parts = []
                for stem_part in stem_words:
                    originals = list(stem_to_original.get(stem_part, {stem_part}))
                    original_bigram_parts.append(originals[0])
                context = " ".join(original_bigram_parts)
                all_phrases.append((bigram, score, context))
        
        # Ordenar e remover duplicatas
        seen = set()
        unique_phrases = []
        for phrase, score, context in all_phrases:
            if phrase not in seen:
                unique_phrases.append((phrase, score, context))
                seen.add(phrase)
        
        unique_phrases.sort(key=lambda x: x[1], reverse=True)
        result = unique_phrases[:n_phrases]
        
        print(f"Extraídas {len(result)} frases-chave")
        return result
    
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
        """Analisa a estrutura do conteúdo das aulas"""
        phrases1 = self.extract_key_phrases_with_context(text1)
        phrases2 = self.extract_key_phrases_with_context(text2)
        
        print("=== FRASES-CHAVE DO TEXTO 1 ===")
        for phrase, score, context in phrases1[:10]:
            print(f"{phrase} ({context}): {score:.3f}")
        
        print("\n=== FRASES-CHAVE DO TEXTO 2 ===")
        for phrase, score, context in phrases2[:10]:
            print(f"{phrase} ({context}): {score:.3f}")
        
        # Calcular sobreposição
        phrases1_set = set([phrase for phrase, _, _ in phrases1])
        phrases2_set = set([phrase for phrase, _, _ in phrases2])
        
        common_phrases = phrases1_set.intersection(phrases2_set)
        total_unique_phrases = len(phrases1_set.union(phrases2_set))
        
        if total_unique_phrases > 0:
            phrase_overlap = len(common_phrases) / total_unique_phrases
        else:
            phrase_overlap = 0.0
        
        print(f"\n=== FRASES COMUNS ({len(common_phrases)} de {total_unique_phrases}) ===")
        
        phrases1_dict = {phrase: (score, context) for phrase, score, context in phrases1}
        phrases2_dict = {phrase: (score, context) for phrase, score, context in phrases2}
        
        for phrase in sorted(common_phrases):
            score1, context1 = phrases1_dict.get(phrase, (0, ""))
            score2, context2 = phrases2_dict.get(phrase, (0, ""))
            avg_score = (score1 + score2) / 2
            
            all_contexts = set([context1, context2])
            combined_context = "/".join(sorted(all_contexts))
            
            print(f"- {phrase} ({combined_context}): {avg_score:.3f}")
        
        return {
            'phrase_overlap': phrase_overlap,
            'common_phrases': list(common_phrases),
            'total_phrases_text1': len(phrases1),
            'total_phrases_text2': len(phrases2)
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
        
        print(f"📊 INDICADORES PRINCIPAIS:")
        print(f"• Cosine Similarity: {cosine_score*100:.1f}% (vocabulário técnico)")
        print(f"• Sobreposição Tópicos: {phrase_overlap*100:.1f}% (temas em comum)")
        print(f"• Jaccard Similarity: {similarity_metrics['jaccard_similarity']*100:.1f}% (palavras únicas)")
        
        if cosine_score > 0.8 and phrase_overlap > 0.4:
            interpretation = "🟢 ALTA similaridade - Mesma aula/roteiro"
            confidence = "Alta confiança"
        elif cosine_score > 0.7 and phrase_overlap > 0.3:
            interpretation = "🟡 MÉDIA-ALTA similaridade - Mesmo tema, execução diferente"
            confidence = "Boa confiança"
        elif cosine_score > 0.5 or phrase_overlap > 0.2:
            interpretation = "🟠 MÉDIA similaridade - Temas relacionados"
            confidence = "Confiança moderada"
        else:
            interpretation = "🔴 BAIXA similaridade - Conteúdos diferentes"
            confidence = "Alta confiança"
        
        print(f"\n🎯 CONCLUSÃO: {interpretation}")
        print(f"Nível de confiança: {confidence}")
        
        return {
            'similarity_metrics': similarity_metrics,
            'content_analysis': content_analysis,
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
    for path in paths:
        texto = load_transcript(path)
        if texto:
            textos[path] = texto
            print(f"✅ Carregado: {path} ({len(texto)} caracteres)")
        else:
            print(f"❌ Falha ao carregar: {path}")
    
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
    
    # Ordenar por similaridade coseno
    resultados_ordenados = sorted(
        resultados, 
        key=lambda x: x['similarity_metrics']['cosine_similarity'], 
        reverse=True
    )
    
    print("\n🏆 RANKING DE SIMILARIDADE (por Cosine Similarity):")
    print("-" * 80)
    
    for i, resultado in enumerate(resultados_ordenados, 1):
        cosine = resultado['similarity_metrics']['cosine_similarity'] * 100
        overlap = resultado['content_analysis']['phrase_overlap'] * 100
        
        if cosine > 80:
            emoji = "🟢"
        elif cosine > 60:
            emoji = "🟡"
        elif cosine > 40:
            emoji = "🟠"
        else:
            emoji = "🔴"
        
        print(f"{i:2d}. {emoji} {resultado['nome1']} ↔ {resultado['nome2']}")
        print(f"    Cosine: {cosine:.1f}% | Sobreposição: {overlap:.1f}% | {resultado['confidence']}")
    
    # Análise de grupos
    print(f"\n🔍 ANÁLISE DE GRUPOS:")
    print("-" * 50)
    
    mais_similar = resultados_ordenados[0]
    cosine_max = mais_similar['similarity_metrics']['cosine_similarity'] * 100
    
    print(f"✨ Par mais similar ({cosine_max:.1f}%):")
    print(f"   • {mais_similar['nome1']}")
    print(f"   • {mais_similar['nome2']}")
    
    grupos_alta_similaridade = [r for r in resultados_ordenados 
                                if r['similarity_metrics']['cosine_similarity'] > 0.7]
    
    if len(grupos_alta_similaridade) > 1:
        print(f"\n🎯 {len(grupos_alta_similaridade)} pares com alta similaridade (>70%):")
        for resultado in grupos_alta_similaridade:
            print(f"   • {resultado['nome1']} ↔ {resultado['nome2']}")
    
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
    
    print("🚀 ANALISADOR DE MÚLTIPLAS TRANSCRIÇÕES")
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
