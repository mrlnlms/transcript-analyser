#!/usr/bin/env python3
"""
Markdown Report Generator
Gera relatórios em Markdown a partir dos resultados de análise
"""
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from engine.analyzers.global_metrics import GlobalMetricsAnalyzer
from engine.analyzers.temporal_analysis import TemporalAnalysisAnalyzer
from datetime import datetime

logger = logging.getLogger(__name__)


class MarkdownReportGenerator:
    """Gera relatórios em formato Markdown"""
    
    def __init__(self):
        """Inicializa o gerador"""
        self.analyzers_cache = {}
        
    def get_analyzer(self, analyzer_name: str):
        """Obtém instância do analyzer para usar interpret_results"""
        if analyzer_name not in self.analyzers_cache:
            analyzer_map = {
                'global_metrics': GlobalMetricsAnalyzer(),
                'temporal_analysis': TemporalAnalysisAnalyzer(),
            }
            self.analyzers_cache[analyzer_name] = analyzer_map.get(analyzer_name)
        return self.analyzers_cache.get(analyzer_name)
    
    def generate_report(self, result: Dict[str, Any], output_path: Path, 
                       filename: str) -> Optional[Path]:
        """Gera relatório em Markdown"""
        try:
            logger.info("📝 Gerando relatório Markdown...")
            
            content = self._create_content(result)
            
            report_name = f"report_{Path(filename).stem}.md"
            report_path = output_path / report_name
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Relatório salvo: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_content(self, result: Dict[str, Any]) -> str:
        """Cria o conteúdo completo do relatório"""
        sections = []
        
        sections.append(self._create_header(result))
        sections.append(self._create_executive_summary(result))
        
        if 'global_metrics' in result:
            sections.append(self._create_global_metrics_section(result['global_metrics']))
        
        if 'temporal_analysis' in result:
            sections.append(self._create_temporal_section(result['temporal_analysis']))
        
        if 'topics' in result:
            sections.append(self._create_topics_section(result))
        
        if 'concept_network' in result:
            sections.append(self._create_network_section(result['concept_network']))
        
        if 'linguistic_patterns' in result:
            sections.append(self._create_patterns_section(result['linguistic_patterns']))
        
        if 'contradictions' in result:
            sections.append(self._create_contradictions_section(result['contradictions']))
        
        if 'word_frequencies' in result:
            sections.append(self._create_frequency_section(result['word_frequencies']))
        
        sections.append(self._create_footer())
        
        return '\n\n'.join(filter(None, sections))
    
    def _create_header(self, result: Dict[str, Any]) -> str:
        """Cria cabeçalho do relatório"""
        filename = result.get('filename', 'Arquivo')
        timestamp = result.get('analysis_timestamp', datetime.now().isoformat())
        
        return f"""# 📊 Relatório de Análise - {filename}

**Data da análise**: {timestamp}
**Versão**: Transcript Analyzer v2.1
"""
    
    def _create_executive_summary(self, result: Dict[str, Any]) -> str:
        """Cria sumário executivo"""
        summary_parts = ["## 📋 Sumário Executivo\n"]
        
        if 'global_metrics' in result:
            sentiment = result['global_metrics'].get('global_sentiment', 0)
            if sentiment > 0.3:
                summary_parts.append("😊 **Sentimento predominantemente positivo**")
            elif sentiment < -0.3:
                summary_parts.append("😔 **Sentimento predominantemente negativo**")
            else:
                summary_parts.append("😐 **Sentimento neutro/misto**")
        
        return '\n'.join(summary_parts)
    
    def _create_global_metrics_section(self, metrics: Dict[str, Any]) -> str:
        """Cria seção de métricas globais"""
        if not metrics:
            return ""
        
        content = ["## 📊 Métricas Globais\n"]
        
        sentiment = metrics.get('global_sentiment', 0)
        sentiment_label = "Positivo" if sentiment > 0.1 else "Negativo" if sentiment < -0.1 else "Neutro"
        content.append(f"- **Sentimento Global**: {sentiment:.3f} ({sentiment_label})")
        
        coherence = metrics.get('thematic_coherence', 0)
        content.append(f"- **Coerência Temática**: {coherence:.2f}")
        
        openness = metrics.get('emotional_openness', 0)
        content.append(f"- **Abertura Emocional**: {openness:.2f}")
        
        hesitations = metrics.get('total_hesitations', 0)
        content.append(f"- **Total de Hesitações**: {hesitations}")
        
        return '\n'.join(content)
    
    def _create_temporal_section(self, temporal_data) -> str:
        """Cria seção de análise temporal"""
        if not temporal_data:
            return ""
        
        content = ["## 📈 Análise Temporal\n"]
        
        if isinstance(temporal_data, list):
            content.append(f"- **Total de Segmentos**: {len(temporal_data)}")
            return '\n'.join(content)
        
        if isinstance(temporal_data, dict):
            total_segments = temporal_data.get('total_segments', 0)
            content.append(f"- **Total de Segmentos**: {total_segments}")
        
        return '\n'.join(content)
    
    def _create_topics_section(self, result: Dict[str, Any]) -> str:
        """Cria seção de tópicos"""
        if 'topics' not in result:
            return ""
        
        content = ["## 🎯 Tópicos Identificados\n"]
        
        topics = result.get('topics', [])
        if isinstance(topics, list):
            for i, topic in enumerate(topics[:5]):
                if isinstance(topic, dict):
                    words = ', '.join(topic.get('words', [])[:5])
                    weight = topic.get('weight', 0)
                    content.append(f"**Tópico {i+1}** ({weight:.2%}): {words}")
        
        return '\n'.join(content)
    
    def _create_network_section(self, network_data) -> str:
        """Cria seção de rede de conceitos"""
        if not network_data:
            return ""
        
        content = ["## 🕸️ Rede de Conceitos\n"]
        
        if isinstance(network_data, list):
            content.append(f"- **Total de Conexões**: {len(network_data)}")
            return '\n'.join(content)
        
        if isinstance(network_data, dict):
            total_connections = network_data.get('significant_connections', 0)
            words_analyzed = network_data.get('words_analyzed', 0)
            
            content.append(f"- **Palavras Analisadas**: {words_analyzed}")
            content.append(f"- **Conexões Significativas**: {total_connections}")
        
        return '\n'.join(content)
    
    def _create_patterns_section(self, patterns_data) -> str:
        """Cria seção de padrões linguísticos"""
        if not patterns_data:
            return ""
        
        content = ["## 🔍 Padrões Linguísticos\n"]
        
        if isinstance(patterns_data, dict):
            certainty = len(patterns_data.get('certainty_markers', []))
            uncertainty = len(patterns_data.get('uncertainty_markers', []))
            hesitations = len(patterns_data.get('hesitation_phrases', []))
            
            content.append(f"- **Marcadores de Certeza**: {certainty}")
            content.append(f"- **Marcadores de Incerteza**: {uncertainty}")
            content.append(f"- **Frases de Hesitação**: {hesitations}")
            
            avg_sentence = patterns_data.get('avg_sentence_length', 0)
            content.append(f"- **Comprimento Médio de Frase**: {avg_sentence:.1f} palavras")
        
        return '\n'.join(content)
    
    def _create_contradictions_section(self, contradictions) -> str:
        """Cria seção de contradições"""
        if not contradictions:
            return ""
        
        content = ["## ⚡ Contradições Detectadas\n"]
        
        if not isinstance(contradictions, list) or len(contradictions) == 0:
            content.append("*Nenhuma contradição significativa detectada*")
        else:
            for i, cont in enumerate(contradictions[:3]):
                if isinstance(cont, dict):
                    sent1 = cont.get('sentence1', '')
                    sent2 = cont.get('sentence2', '')
                    score = cont.get('contradiction_score', 0)
                    content.append(f"**Contradição {i+1}** (Score: {score:.2f})")
                    content.append(f"- Frase 1: \"{sent1[:100]}...\"")
                    content.append(f"- Frase 2: \"{sent2[:100]}...\"")
                    content.append("")
        
        return '\n'.join(content)
    
    def _create_frequency_section(self, frequencies) -> str:
        """Cria seção de frequência de palavras"""
        if not frequencies:
            return ""
        
        content = ["## 📊 Palavras Mais Frequentes\n"]
        
        if isinstance(frequencies, dict):
            sorted_words = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:10]
            for word, freq in sorted_words:
                content.append(f"- **{word}**: {freq} ocorrências")
        
        return '\n'.join(content)
    
    def _create_footer(self) -> str:
        """Cria rodapé do relatório"""
        return f"""---

*Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*  
*Transcript Analyzer v2.1*
"""
