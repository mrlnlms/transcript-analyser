#!/usr/bin/env python3
"""
Markdown Report Generator
Gera relatórios em Markdown a partir dos resultados de análise
"""

import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class MarkdownReportGenerator:
    """Gerador de relatórios em Markdown com interpretações automáticas"""
    
    def __init__(self):
        self.logger = logger
        
    def generate_report(self, result: Dict[str, Any], output_path: Path) -> str:
        """
        Gera relatório completo em Markdown
        
        Args:
            result: Resultados da análise
            output_path: Caminho para salvar o relatório
            
        Returns:
            Caminho do arquivo gerado
        """
        try:
            self.logger.info("�� Gerando relatório Markdown...")
            
            # Criar conteúdo
            content = self._create_content(result)
            
            # Salvar arquivo
            # Salvar arquivo com nome do arquivo original
            filename_base = result.get('filename', 'arquivo').replace('.txt', '')
            report_path = output_path / f'report_{filename_base}.md'
            report_path.write_text(content, encoding='utf-8')
            
            self.logger.info(f"✅ Relatório salvo em: {report_path}")
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar relatório: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def _create_content(self, result: Dict[str, Any]) -> str:
        """Cria conteúdo completo do relatório"""
        sections = []
        
        # Cabeçalho
        sections.append(self._create_header(result))
        
        # Resumo executivo
        sections.append(self._create_executive_summary(result))
        
        # Métricas globais
        if 'global_metrics' in result:
            sections.append(self._create_global_metrics_section(result['global_metrics']))
        
        # Análise temporal
        if 'temporal_analysis' in result:
            sections.append(self._create_temporal_section(result['temporal_analysis']))
        
        # Tópicos
        if 'topics' in result:
            sections.append(self._create_topics_section(result))
        
        # Rede conceitual
        if 'concept_network' in result:
            sections.append(self._create_network_section(result['concept_network']))
        
        # Padrões linguísticos
        if 'linguistic_patterns' in result:
            sections.append(self._create_patterns_section(result['linguistic_patterns']))
        
        # Contradições
        if 'contradictions' in result:
            sections.append(self._create_contradictions_section(result['contradictions']))
        
        # Palavras frequentes
        if 'word_frequencies' in result:
            sections.append(self._create_frequency_section(result['word_frequencies']))
        
        # Rodapé
        sections.append(self._create_footer())
        
        return '\n\n'.join(filter(None, sections))
    
    def _create_header(self, result: Dict[str, Any]) -> str:
        """Cria cabeçalho do relatório"""
        filename = result.get('filename', 'arquivo')
        return f"""# 📊 Relatório de Análise - {filename}

**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}  
**Arquivo**: {filename}
"""
    
    def _create_executive_summary(self, result: Dict[str, Any]) -> str:
        """Cria resumo executivo com interpretações principais"""
        summary_parts = ["## 📋 Resumo Executivo\n"]
        
        # Sentimento dominante
        if 'global_metrics' in result:
            sentiment = result['global_metrics'].get('global_sentiment', 0)
            if sentiment > 0.1:
                summary_parts.append("✅ **Sentimento geral positivo** - A transcrição apresenta tom otimista")
            elif sentiment < -0.1:
                summary_parts.append("⚠️ **Sentimento geral negativo** - Tons de preocupação ou crítica detectados")
            else:
                summary_parts.append("🔵 **Sentimento neutro** - Discurso equilibrado e objetivo")
        
        # Tópicos principais
        if 'topics' in result and result['topics']:
            top_topic = result['topics'][0]
            summary_parts.append(f"🎯 **Tópico principal**: {top_topic.get('label', 'N/A')}")
        
        # Padrões notáveis
        if 'linguistic_patterns' in result:
            patterns = result['linguistic_patterns']
            hesitations = patterns.get('total_hesitations', 0)
            if hesitations > 5:
                summary_parts.append("💭 **Alta hesitação detectada** - Possível incerteza ou reflexão profunda")
        
        return '\n'.join(summary_parts)
    
    def _create_global_metrics_section(self, metrics: Dict[str, Any]) -> str:
        """Seção de métricas globais"""
        return f"""## 📊 Métricas Globais

- **Sentimento Global**: {metrics.get('global_sentiment', 0):.3f} {self._interpret_sentiment(metrics.get('global_sentiment', 0))}
- **Coerência Temática**: {metrics.get('thematic_coherence', 0):.2f} {self._interpret_coherence(metrics.get('thematic_coherence', 0))}
- **Abertura Emocional**: {metrics.get('emotional_openness', 0):.2f} {self._interpret_openness(metrics.get('emotional_openness', 0))}
"""
    
    def _create_temporal_section(self, temporal: List[Dict]) -> str:
        """Seção de análise temporal"""
        if not temporal:
            return ""
            
        content = ["## 📈 Análise Temporal\n"]
        
        # Estatísticas gerais
        sentiments = [seg.get('sentiment', 0) for seg in temporal]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
        content.append(f"**Sentimento médio ao longo do tempo**: {avg_sentiment:.3f}")
        content.append(f"**Total de segmentos analisados**: {len(temporal)}")
        
        # Encontrar picos e vales
        if len(sentiments) > 2:
            max_idx = sentiments.index(max(sentiments))
            min_idx = sentiments.index(min(sentiments))
            content.append(f"\n🔺 **Pico emocional**: Segmento {max_idx + 1} (sentimento: {sentiments[max_idx]:.3f})")
            content.append(f"🔻 **Vale emocional**: Segmento {min_idx + 1} (sentimento: {sentiments[min_idx]:.3f})")
        
        return '\n'.join(content)
    
    def _create_topics_section(self, result: Dict[str, Any]) -> str:
        """Seção de tópicos"""
        topics = result.get('topics', [])
        distribution = result.get('topic_distribution', [])
        
        if not topics:
            return ""
            
        content = ["## 🎯 Tópicos Identificados\n"]
        
        for i, topic in enumerate(topics[:5]):  # Top 5 tópicos
            label = topic.get('label', f'Tópico {i+1}')
            words = ', '.join(topic.get('words', [])[:5])
            
            if i < len(distribution):
                percentage = distribution[i] * 100
                content.append(f"### {label} ({percentage:.1f}%)")
            else:
                content.append(f"### {label}")
                
            content.append(f"**Palavras-chave**: {words}\n")
        
        return '\n'.join(content)
    
    def _create_network_section(self, network: List[Dict]) -> str:
        """Seção de rede conceitual"""
        if not network:
            return ""
            
        content = ["## 🕸️ Rede de Conceitos\n"]
        
        # Ordenar por peso (corrigindo o erro de comparação de dicts)
        try:
            # Filtrar apenas dicts válidos com 'weight'
            valid_connections = [conn for conn in network if isinstance(conn, dict) and 'weight' in conn]
            
            if valid_connections:
                # Ordenar por peso
                sorted_network = sorted(valid_connections, key=lambda x: x.get('weight', 0), reverse=True)
                
                content.append("**Conexões mais fortes**:")
                for conn in sorted_network[:10]:  # Top 10 conexões
                    word1 = conn.get('word1', 'N/A')
                    word2 = conn.get('word2', 'N/A')
                    weight = conn.get('weight', 0)
                    content.append(f"- {word1} ↔️ {word2} (força: {weight})")
            else:
                content.append("*Nenhuma conexão válida encontrada*")
                
        except Exception as e:
            self.logger.warning(f"Erro ao processar rede: {e}")
            content.append("*Erro ao processar conexões da rede*")
        
        return '\n'.join(content)
    
    def _create_patterns_section(self, patterns: Dict[str, Any]) -> str:
        """Seção de padrões linguísticos"""
        content = ["## 💬 Padrões Linguísticos\n"]
        
        # Hesitações
        hesitations = patterns.get('hesitation_phrases', {})
        total_hesitations = patterns.get('total_hesitations', 0)
        
        if total_hesitations > 0:
            content.append(f"**Total de hesitações**: {total_hesitations}")
            if isinstance(hesitations, dict) and hesitations:
                content.append("**Tipos de hesitação**:")
                for phrase, count in list(hesitations.items())[:5]:
                    content.append(f"- '{phrase}': {count} vezes")
        
        # Certeza vs Incerteza
        uncertainty = patterns.get('uncertainty_markers', {}).get('count', 0)
        certainty = patterns.get('certainty_markers', {}).get('count', 0)
        
        if uncertainty + certainty > 0:
            certainty_ratio = certainty / (certainty + uncertainty) * 100
            content.append(f"\n**Índice de certeza**: {certainty_ratio:.1f}%")
        
        # Comprimento médio
        avg_length = patterns.get('avg_sentence_length', 0)
        if avg_length > 0:
            content.append(f"**Comprimento médio das sentenças**: {avg_length:.1f} palavras")
        
        return '\n'.join(content)
    
    def _create_contradictions_section(self, contradictions: List[Dict]) -> str:
        """Seção de contradições"""
        if not contradictions:
            return ""
            
        content = ["## ⚡ Contradições Detectadas\n"]
        
        # Filtrar e ordenar contradições válidas
        valid_contradictions = [c for c in contradictions if isinstance(c, dict) and 'score' in c]
        
        if valid_contradictions:
            sorted_contradictions = sorted(valid_contradictions, key=lambda x: x.get('score', 0), reverse=True)
            
            for i, contradiction in enumerate(sorted_contradictions[:5], 1):
                score = contradiction.get('score', 0)
                text1 = contradiction.get('text1', 'N/A')
                text2 = contradiction.get('text2', 'N/A')
                
                content.append(f"### Contradição {i} (confiança: {score:.2f})")
                content.append(f"- **Afirmação 1**: \"{text1}\"")
                content.append(f"- **Afirmação 2**: \"{text2}\"\n")
        else:
            content.append("*Nenhuma contradição significativa detectada*")
        
        return '\n'.join(content)
    
    def _create_frequency_section(self, frequencies: Dict[str, int]) -> str:
        """Seção de palavras frequentes"""
        if not frequencies:
            return ""
            
        content = ["## 📝 Palavras Mais Frequentes\n"]
        
        # Ordenar por frequência
        sorted_words = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        
        for word, count in sorted_words[:15]:  # Top 15
            content.append(f"- **{word}**: {count} ocorrências")
        
        return '\n'.join(content)
    
    def _create_footer(self) -> str:
        """Rodapé do relatório"""
        return """---

📊 *Relatório gerado automaticamente pelo Transcript Analyzer V2.0*  
🔍 *Para análises mais detalhadas, consulte as visualizações interativas*"""
    
    # Métodos auxiliares de interpretação
    def _interpret_sentiment(self, value: float) -> str:
        """Interpreta valor de sentimento"""
        if value > 0.3:
            return "😊 Muito positivo"
        elif value > 0.1:
            return "🙂 Positivo"
        elif value > -0.1:
            return "😐 Neutro"
        elif value > -0.3:
            return "😕 Negativo"
        else:
            return "😔 Muito negativo"
    
    def _interpret_coherence(self, value: float) -> str:
        """Interpreta coerência temática"""
        if value > 0.8:
            return "🎯 Excelente foco"
        elif value > 0.6:
            return "✅ Boa estrutura"
        elif value > 0.4:
            return "📊 Estrutura razoável"
        else:
            return "⚠️ Disperso"
    
    def _interpret_openness(self, value: float) -> str:
        """Interpreta abertura emocional"""
        if value > 2:
            return "💖 Muito expressivo"
        elif value > 1:
            return "💬 Expressivo"
        elif value > 0.5:
            return "🔵 Moderado"
        else:
            return "🔒 Reservado"
