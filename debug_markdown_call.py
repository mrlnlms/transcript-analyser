import ast
import re

# Ler o arquivo
with open('run_analysis.py', 'r') as f:
    content = f.read()

# Encontrar onde _generate_markdown_report é chamado
matches = re.finditer(r'self\._generate_markdown_report\((.*?)\)', content, re.DOTALL)

print("🔍 Chamadas para _generate_markdown_report encontradas:\n")
for i, match in enumerate(matches, 1):
    print(f"Chamada {i}:")
    print(f"  Argumentos: {match.group(1)}")
    print(f"  Contexto: ...{content[max(0, match.start()-100):match.end()+50]}...")
    print("-" * 80)
