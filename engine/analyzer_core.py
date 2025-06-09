"""🔍 Engine de análise principal"""

import json
import os
import numpy as np

from pathlib import Path
from typing import Dict, List, Any, Optional

from .analyzers.word_frequency import WordFrequencyAnalyzer

class TranscriptAnalyzer:
    """Analisador principal de transcrições"""
    
    def __init__(self, config, resource_manager):
        self.config = config
        self.resources = resource_manager
        print(f"✅ TranscriptAnalyzer inicializado para projeto: {config.project_name}")
    
    def analyze_transcript(self, file_path: Path) -> Dict[str, Any]:
        """Análise completa de uma transcrição"""
        
        print(f"🔍 Iniciando análise de: {file_path.name}")
        
        try:
            # Ler arquivo
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if not text.strip():
                raise ValueError("Arquivo vazio ou inválido")
            
            # Calcular todas as análises primeiro
            word_frequencies = self._count_word_frequencies(text)
            temporal_analysis = self._analyze_temporal(text)
            topics, topic_distribution, topic_hierarchy = self._extract_simple_topics(text, word_frequencies)
            
            # ANÁLISE REAL (básica por enquanto)
            result = {
                'filename': file_path.name,
                'status': 'success',
                'global_metrics': self._calculate_global_metrics(text, temporal_analysis),
                'word_frequencies': word_frequencies,
                'temporal_analysis': temporal_analysis,
                'phases': self._extract_phases(temporal_analysis),
                'linguistic_patterns': self._detect_linguistic_patterns(text),
                'topics': topics,
                'topic_distribution': topic_distribution,
                'topic_hierarchy': topic_hierarchy,
                'contradictions': self._detect_contradictions(text, temporal_analysis),
                'concept_network': self._build_concept_network(text, word_frequencies)
            }
            
            print(f"✅ Análise concluída: {file_path.name}")
            return result
            
        except Exception as e:
            print(f"❌ Erro na análise de {file_path.name}: {e}")
            raise

    def _count_word_frequencies(self, text: str) -> Dict[str, int]:
        """Usa o novo sistema plugável de análise"""
        analyzer = WordFrequencyAnalyzer()
        result = analyzer.analyze(text)
        return result['word_frequencies']
    




    def _analyze_temporal(self, text: str) -> List[Dict[str, Any]]:
        """Divide texto em segmentos temporais e analisa evolução"""
        import re
        
        # Dividir em parágrafos (ou sentenças grandes)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Se muito poucos parágrafos, dividir por sentenças
        if len(paragraphs) < 5:
            sentences = re.split(r'[.!?]+', text)
            # Agrupar sentenças em blocos de 3-4
            paragraphs = []
            for i in range(0, len(sentences), 3):
                block = ' '.join(sentences[i:i+3]).strip()
                if block:
                    paragraphs.append(block)
        
        # Limitar a 20 segmentos no máximo
        if len(paragraphs) > 20:
            # Agrupar parágrafos para ter ~20 segmentos
            step = len(paragraphs) // 20
            temp = []
            for i in range(0, len(paragraphs), step):
                temp.append(' '.join(paragraphs[i:i+step]))
            paragraphs = temp[:20]
        
        # Analisar cada segmento
        temporal_data = []
        for i, paragraph in enumerate(paragraphs):
            if not paragraph:
                continue
                
            # Calcular métricas básicas
            words = paragraph.split()
            
            # Análise de sentimento básica com palavras-chave
            sentiment = 0.0
            paragraph_lower = paragraph.lower()
            
            # Palavras positivas
            positive_words = ['bom', 'ótimo', 'excelente', 'feliz', 'satisfeito', 'gosto', 
                            'adoro', 'maravilh', 'incrível', 'positiv', 'melhor', 'sucesso',
                            'consegui', 'aprendi', 'entendi', 'legal', 'bacana', 'top']
            
            # Palavras negativas  
            negative_words = ['ruim', 'péssimo', 'triste', 'difícil', 'problema', 'erro',
                            'não', 'nunca', 'medo', 'preocup', 'frustr', 'chato', 'cansado',
                            'complicado', 'confuso', 'dúvida']
            
            # Contar palavras positivas e negativas
            for word in positive_words:
                if word in paragraph_lower:
                    sentiment += 0.15
            
            for word in negative_words:
                if word in paragraph_lower:
                    sentiment -= 0.15
            
            # Ajustar por pontuação
            if '!' in paragraph:
                sentiment += 0.1
            if '?' in paragraph and any(neg in paragraph_lower for neg in ['não', 'como', 'por que']):
                sentiment -= 0.1
            
            # Variação para tornar mais interessante
            import random
            sentiment += random.uniform(-0.1, 0.1)
            
            # Detectar marcadores
            marker = "normal"
            if i == 0:
                marker = "INICIO"
            elif i == len(paragraphs) - 1:
                marker = "CONCLUSAO"
            elif "mas" in paragraph.lower() or "porém" in paragraph.lower():
                marker = "CONFLITO"
            elif "portanto" in paragraph.lower() or "assim" in paragraph.lower():
                marker = "SINTESE"
            
            temporal_data.append({
                'time': i * 5,  # Simular tempo em minutos
                'minute': i * 2.5,
                'sentiment': max(-1, min(1, sentiment)),  # Limitar entre -1 e 1
                'marker': marker,
                'phase': 'INICIO' if i < len(paragraphs) * 0.3 else 'DESENVOLVIMENTO' if i < len(paragraphs) * 0.7 else 'CONCLUSAO',
                'cognitive_load': len(words),
                'hesitations': paragraph.lower().count('né') + paragraph.lower().count('tipo')
            })
        
        return temporal_data
    

    def _extract_phases(self, temporal_data: List[Dict]) -> Dict[str, Dict]:
        """Extrai as fases da análise temporal"""
        if not temporal_data:
            return {}
        
        phases = {
            'INICIO': {
                'start': 0,
                'end': 0,
                'sentiment_avg': 0,
                'duration_minutes': 0,
                'color': '#B3E5FC'
            },
            'DESENVOLVIMENTO': {
                'start': 0,
                'end': 0,
                'sentiment_avg': 0,
                'duration_minutes': 0,
                'color': '#4FC3F7'
            },
            'CONCLUSAO': {
                'start': 0,
                'end': 0,
                'sentiment_avg': 0,
                'duration_minutes': 0,
                'color': '#E1BEE7'
            }
        }
        
        # Calcular métricas por fase
        for phase_name in phases:
            phase_data = [d for d in temporal_data if d.get('phase') == phase_name]
            if phase_data:
                phases[phase_name]['start'] = phase_data[0]['minute']
                phases[phase_name]['end'] = phase_data[-1]['minute']
                phases[phase_name]['duration_minutes'] = phases[phase_name]['end'] - phases[phase_name]['start']
                
                sentiments = [d['sentiment'] for d in phase_data]
                phases[phase_name]['sentiment_avg'] = sum(sentiments) / len(sentiments) if sentiments else 0
        
        return phases
    
    def _calculate_global_metrics(self, text: str, temporal_data: List[Dict]) -> Dict[str, float]:
        """Calcula métricas globais do texto"""
        # Sentimento global (média dos segmentos)
        sentiments = [d['sentiment'] for d in temporal_data] if temporal_data else [0]
        global_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
        # Variância do sentimento (abertura emocional)
        if len(sentiments) > 1:
            mean = sum(sentiments) / len(sentiments)
            variance = sum((s - mean) ** 2 for s in sentiments) / len(sentiments)
            sentiment_variance = variance
        else:
            sentiment_variance = 0.1
        
        # Hesitações totais
        total_hesitations = text.lower().count('né') + text.lower().count('tipo') + \
                          text.lower().count('assim') + text.lower().count('então')
        
        # Coerência temática (baseada em repetição de palavras-chave)
        words = text.lower().split()
        unique_words = len(set(words))
        total_words = len(words)
        coherence = 1 - (unique_words / total_words) if total_words > 0 else 0.5
        
        return {
            'global_sentiment': round(global_sentiment, 2),
            'thematic_coherence': round(coherence, 2),
            'emotional_openness': round(1 + sentiment_variance, 2),
            'sentiment_variance': round(sentiment_variance, 2),
            'total_hesitations': total_hesitations
        }
    
    def _detect_linguistic_patterns(self, text: str) -> Dict[str, Any]:
        """Detecta padrões linguísticos reais no texto"""
        import re
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Marcadores de certeza
        certainty_phrases = [
            'com certeza', 'obviamente', 'claramente', 'sem dúvida', 
            'definitivamente', 'certamente', 'claro que', 'evidente',
            'tenho certeza', 'absolutamente', 'seguramente'
        ]
        
        # Marcadores de incerteza
        uncertainty_phrases = [
            'talvez', 'acho que', 'não sei', 'pode ser', 'provavelmente',
            'me parece', 'acredito que', 'suponho', 'imagino que',
            'não tenho certeza', 'possivelmente', 'quem sabe'
        ]
        
        # Hesitações
        hesitation_words = ['né', 'tipo', 'assim', 'então', 'eh', 'ah', 'uhm', 'ahn']
        
        # Contar ocorrências
        certainty_count = sum(1 for phrase in certainty_phrases if phrase in text_lower)
        uncertainty_count = sum(1 for phrase in uncertainty_phrases if phrase in text_lower)
        
        # Hesitações por palavra
        hesitations_by_word = {}
        total_hesitations = 0
        
        for word in hesitation_words:
            count = text_lower.count(word)
            if count > 0:
                hesitations_by_word[word] = {
                    'count': count,
                    'percentage': (count / len(words)) * 100 if words else 0
                }
                total_hesitations += count
        
        # Complexidade das frases
        sentences = re.split(r'[.!?]+', text)
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        return {
            'certainty_markers': {
                'count': certainty_count,
                'examples': [p for p in certainty_phrases if p in text_lower][:5],
                'percentage': (certainty_count / len(sentences)) * 100 if sentences else 0
            },
            'uncertainty_markers': {
                'count': uncertainty_count,
                'examples': [p for p in uncertainty_phrases if p in text_lower][:5],
                'percentage': (uncertainty_count / len(sentences)) * 100 if sentences else 0,
                'ratio_to_certainty': uncertainty_count / certainty_count if certainty_count > 0 else uncertainty_count
            },
            'hesitations_by_word': hesitations_by_word,
            'hesitation_phrases': {word: text_lower.count(word) for word in hesitation_words if text_lower.count(word) > 0},
            'total_hesitations': total_hesitations,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'sentence_length_std': round(np.std(sentence_lengths), 1) if len(sentence_lengths) > 1 else 0,
            'complexity_by_topic': {}  # TODO: implementar quando tivermos tópicos
        }
    
    def _build_concept_network(self, text: str, word_freq: Dict[str, int]) -> List[Dict[str, Any]]:
        """Constrói rede de conceitos baseada em coocorrência"""
        import re
        from collections import defaultdict
        
        # Pegar top palavras mais frequentes
        top_words = list(word_freq.keys())[:30]
        
        # Dividir em sentenças
        sentences = re.split(r'[.!?]+', text.lower())
        
        # Contar coocorrências
        cooccurrence = defaultdict(int)
        
        for sentence in sentences:
            words_in_sentence = [w for w in sentence.split() if w in top_words]
            
            # Para cada par de palavras na sentença
            for i, word1 in enumerate(words_in_sentence):
                for word2 in words_in_sentence[i+1:]:
                    if word1 != word2:
                        # Ordenar para evitar duplicatas (a,b) e (b,a)
                        pair = tuple(sorted([word1, word2]))
                        cooccurrence[pair] += 1
        
        # Criar lista de conexões
        connections = []
        for (word1, word2), weight in sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)[:20]:
            if weight > 1:  # Apenas conexões significativas
                connections.append({
                    'word1': word1,
                    'word2': word2,
                    'weight': weight
                })
        
        return connections
    


    def _extract_simple_topics(self, text: str, word_freq: Dict[str, int]) -> tuple:
        """Extrai tópicos simples baseados em agrupamento de palavras"""
        # Agrupar palavras por categorias temáticas simples
        topic_keywords = {
            'Tecnologia': ['sistema', 'software', 'código', 'programa', 'computador', 'dados', 'tecnologia', 'digital', 'internet', 'aplicativo'],
            'Educação': ['curso', 'aula', 'professor', 'aluno', 'escola', 'ensino', 'aprendizagem', 'estudo', 'educação', 'conhecimento'],
            'Trabalho': ['trabalho', 'empresa', 'projeto', 'equipe', 'cliente', 'processo', 'resultado', 'meta', 'objetivo', 'prazo'],
            'Pessoal': ['vida', 'família', 'casa', 'tempo', 'dia', 'pessoa', 'gente', 'amigo', 'momento', 'experiência'],
            'Análise': ['problema', 'solução', 'questão', 'situação', 'caso', 'exemplo', 'forma', 'maneira', 'aspecto', 'ponto']
        }
        
        # Contar palavras por tópico
        topic_scores = {}
        text_lower = text.lower()
        
        for topic, keywords in topic_keywords.items():
            score = sum(text_lower.count(keyword) for keyword in keywords)
            if score > 0:
                topic_scores[topic] = score
        
        # Se nenhum tópico específico, usar genérico
        if not topic_scores:
            topic_scores['Geral'] = len(text.split())
        
        # Normalizar para distribuição
        total = sum(topic_scores.values())
        topic_distribution = [score/total for score in topic_scores.values()]
        
        # Criar estrutura de tópicos
        topics = []
        for i, (topic_name, score) in enumerate(topic_scores.items()):
            # Pegar palavras relevantes do word_freq que se relacionam
            relevant_words = []
            for word in word_freq.keys():
                if any(keyword in word for keyword in topic_keywords.get(topic_name, [])):
                    relevant_words.append(word)
            
            # Se não encontrou palavras relevantes, pegar as top do word_freq
            if not relevant_words:
                relevant_words = list(word_freq.keys())[i*8:(i+1)*8]
            
            topics.append({
                'id': f'topic_{i}',
                'words': relevant_words[:8],
                'weight': topic_distribution[i] if i < len(topic_distribution) else 0.1,
                'label': topic_name
            })
        
        # Criar hierarquia simples
        topic_hierarchy = {
            'central_theme': 'TEMAS PRINCIPAIS',
            'nodes': [{'id': 'central', 'label': 'TEMAS PRINCIPAIS', 'level': 0, 'size': 50}],
            'edges': []
        }
        
        for topic in topics:
            topic_hierarchy['nodes'].append({
                'id': topic['id'],
                'label': topic['label'],
                'level': 1,
                'size': int(topic['weight'] * 100)
            })
            topic_hierarchy['edges'].append({
                'source': 'central',
                'target': topic['id'],
                'weight': topic['weight']
            })
        
        return topics, topic_distribution, topic_hierarchy
    

    def _detect_contradictions(self, text: str, temporal_data: List[Dict]) -> List[Dict[str, Any]]:
        """Detecta possíveis contradições no texto"""
        import re
        
        contradictions = []
        
        # Dividir em sentenças
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Padrões de contradição comuns
        contradiction_patterns = [
            # Negação direta
            (r'\b(sempre|todos?|toda?s?|nunca|ninguém|nenhum)\b.*\b(mas|porém|entretanto|contudo)\b.*\b(às vezes|alguns?|alguma?s?|nem sempre)\b', 0.8),
            # Mudança de opinião
            (r'\b(acho|penso|acredito)\b.*\b(mas|porém)\b.*\b(não sei|talvez não|pensando bem)\b', 0.7),
            # Afirmação seguida de negação
            (r'\b(sim|concordo|certo|verdade)\b.*\b(mas|porém|no entanto)\b.*\b(não|errado|discordo)\b', 0.9),
            # Generalização seguida de exceção
            (r'\b(todos?|sempre|nunca)\b.*\b(exceto|menos|salvo|fora)\b', 0.6),
        ]
        
        # Buscar padrões em sentenças consecutivas
        for i in range(len(sentences) - 1):
            for j in range(i + 1, min(i + 5, len(sentences))):  # Olhar até 5 sentenças à frente
                sent1 = sentences[i].lower()
                sent2 = sentences[j].lower()
                
                # Verificar padrões de contradição
                for pattern, base_score in contradiction_patterns:
                    combined = f"{sent1} {sent2}"
                    if re.search(pattern, combined):
                        contradictions.append({
                            'text1': sentences[i][:100],
                            'text2': sentences[j][:100],
                            'score': base_score,
                            'topics': self._extract_keywords(combined),
                            'timestamp1': i * 2.5,  # Estimativa temporal
                            'timestamp2': j * 2.5
                        })
                        break
                
                # Verificar negações do mesmo conceito
                # Palavras-chave importantes em ambas as sentenças
                words1 = set(re.findall(r'\b\w{4,}\b', sent1))
                words2 = set(re.findall(r'\b\w{4,}\b', sent2))
                common_words = words1.intersection(words2)
                
                if common_words and len(common_words) > 2:
                    # Verificar se uma nega a outra
                    has_negation1 = bool(re.search(r'\b(não|nunca|nenhum|sem)\b', sent1))
                    has_negation2 = bool(re.search(r'\b(não|nunca|nenhum|sem)\b', sent2))
                    
                    if has_negation1 != has_negation2:  # Uma tem negação, outra não
                        # Variar o score baseado na quantidade de palavras em comum
                        score_variation = 0.5 + (len(common_words) * 0.05)
                        score_variation = min(score_variation, 0.85)  # Limitar máximo
                        
                        contradictions.append({
                            'text1': sentences[i][:100],
                            'text2': sentences[j][:100],
                            'score': score_variation,
                            'topics': list(common_words)[:5],
                            'timestamp1': i * 2.5,
                            'timestamp2': j * 2.5
                        })
        
        # Detectar mudanças de sentimento extremas
        if temporal_data and len(temporal_data) > 1:
            for i in range(len(temporal_data) - 1):
                current = temporal_data[i]
                next_seg = temporal_data[i + 1]
                
                # Mudança brusca de sentimento
                sentiment_change = abs(current['sentiment'] - next_seg['sentiment'])
                if sentiment_change > 1.0:  # Mudança significativa
                    contradictions.append({
                        'text1': f"Sentimento positivo no minuto {current['minute']:.1f}",
                        'text2': f"Sentimento negativo no minuto {next_seg['minute']:.1f}",
                        'score': min(sentiment_change / 2, 1.0),
                        'topics': ['mudança emocional', 'sentimento'],
                        'timestamp1': current['minute'],
                        'timestamp2': next_seg['minute']
                    })
        
        # Ordenar por score e retornar top contradições
        contradictions.sort(key=lambda x: x['score'], reverse=True)
        return contradictions[:5]  # Máximo 5 contradições
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai palavras-chave de um texto"""
        import re
        
        # Palavras importantes (substantivos, verbos principais)
        words = re.findall(r'\b\w{4,}\b', text.lower())
        
        # Filtrar stopwords básicas
        stopwords = {'para', 'mais', 'muito', 'mesmo', 'quando', 'onde', 'como', 'porque'}
        keywords = [w for w in words if w not in stopwords]
        
        # Retornar únicas
        return list(set(keywords))[:5]