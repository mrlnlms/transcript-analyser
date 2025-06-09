import sys

with open('run_analysis.py', 'r') as f:
    lines = f.readlines()

# Encontrar e corrigir a linha
for i, line in enumerate(lines):
    if '_generate_markdown_report(results, project_dir' in line:
        indent = len(line) - len(line.lstrip())
        # Substituir a linha única por um loop
        lines[i] = ' ' * indent + 'for result in results:\n'
        lines.insert(i + 1, ' ' * (indent + 4) + 'self._generate_markdown_report(result, project_dir / "output")\n')
        break

# Salvar
with open('run_analysis.py', 'w') as f:
    f.writelines(lines)

print("✅ Correção aplicada!")
