#!/bin/bash

echo "🔧 Corrigindo todos os caminhos..."

# 1. Corrigir o markdown_generator.py
echo "📝 Ajustando nome do relatório..."
sed -i '' "/report_path = output_path \/ 'relatorio.md'/c\\
            # Salvar arquivo com nome do arquivo original\\
            filename_base = result.get('filename', 'arquivo').replace('.txt', '')\\
            report_path = output_path / f'report_{filename_base}.md'" markdown_generator.py

# 2. Ver o mapeamento atual no ChartOrchestrator
echo "🔍 Verificando mapeamentos atuais..."
grep -A20 "chart_mappings = {" visuals/chart_orchestrator.py | grep "filename"

# 3. Remover subpastas dos mapeamentos
echo "🔧 Removendo subpastas dos caminhos..."
# Procurar por padrões como 'Novo Codex DEV Pleno/arquivo.html' e mudar para apenas 'arquivo.html'
sed -i '' "s|'filename': '[^/]*/\([^']*\)'|'filename': '\1'|g" visuals/chart_orchestrator.py

# 4. Garantir que não há Path.mkdir em charts individuais
echo "🔍 Verificando criação de pastas nos charts..."
for chart in visuals/charts/*.py; do
    if grep -q "mkdir" "$chart"; then
        echo "  ⚠️  Removendo mkdir de $chart"
        sed -i '' '/\.mkdir(/d' "$chart"
    fi
done

echo "✅ Correções aplicadas!"
echo ""
echo "🧪 Para testar:"
echo "   rm -rf projects/teste_real_*"
echo "   ./scripts/teste_real_simples.sh"
