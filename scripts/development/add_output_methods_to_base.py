#!/usr/bin/env python3
"""Adiciona métodos de interpretação e formatação ao BaseAnalyzer"""

# Código para adicionar após get_config_schema
NEW_METHODS = '''
    def interpret_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpreta resultados numéricos em insights qualitativos
        
        Exemplo:
            {'sentiment': -0.5} → {'sentiment': -0.5, 'sentiment_label': 'Negativo moderado'}
        
        Override este método em cada analyzer para interpretações específicas
        """
        return results
    
    def get_insights(self, results: Dict[str, Any]) -> List[str]:
        """
        Gera insights textuais baseados nos resultados
        
        Returns:
            Lista de insights em linguagem natural
        """
        return []
    
    def format_output(self, results: Dict[str, Any], format_type: str = 'markdown') -> str:
        """
        Formata resultados para diferentes tipos de saída
        
        Args:
            results: Resultados da análise
            format_type: 'markdown', 'json', 'html', 'text'
        
        Returns:
            String formatada no tipo solicitado
        """
        interpreted = self.interpret_results(results)
        
        if format_type == 'markdown':
            return self._format_markdown(interpreted)
        elif format_type == 'json':
            import json
            return json.dumps(interpreted, indent=2, ensure_ascii=False)
        elif format_type == 'text':
            return self._format_text(interpreted)
        else:
            return str(interpreted)
    
    def _format_markdown(self, results: Dict[str, Any]) -> str:
        """Formata resultados como Markdown"""
        # Implementação base - override em analyzers específicos
        lines = [f"## {self.__class__.__name__} Results\n"]
        for key, value in results.items():
            if not key.startswith('_'):
                lines.append(f"- **{key}**: {value}")
        return '\n'.join(lines)
    
    def _format_text(self, results: Dict[str, Any]) -> str:
        """Formata resultados como texto simples"""
        lines = []
        for key, value in results.items():
            if not key.startswith('_'):
                lines.append(f"{key}: {value}")
        return '\n'.join(lines)
'''

# Ler arquivo
with open('engine/analyzers/base_analyzer.py', 'r') as f:
    content = f.read()

# Adicionar imports necessários
if 'from typing import Dict, Any' not in content:
    content = content.replace('from typing import Dict', 'from typing import Dict, List')

# Encontrar onde inserir (após validate_config)
lines = content.split('\n')
insert_index = None

for i, line in enumerate(lines):
    if 'def validate_config' in line:
        # Encontrar o fim do método
        for j in range(i+1, len(lines)):
            if lines[j].strip() and not lines[j].startswith(' '):
                insert_index = j
                break
            elif j == len(lines) - 1:
                insert_index = j
                break
        break

if insert_index:
    # Inserir os novos métodos
    lines.insert(insert_index, NEW_METHODS)
    
    # Salvar
    with open('engine/analyzers/base_analyzer.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Métodos de output adicionados ao BaseAnalyzer!")
else:
    print("❌ Não encontrei onde inserir os métodos")
