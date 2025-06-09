#!/bin/bash
echo "🔧 Corrigindo problemas de orquestração..."

# 1. Corrigir auto-discovery para ignorar BaseAnalyzer
sed -i.bak "s/if name.endswith('Analyzer') and not name.startswith('_'):/if name.endswith('Analyzer') and not name.startswith('_') and name != 'BaseAnalyzer':/" engine/analysis_orchestrator.py

# 2. Mover ChartOrchestrator para local correto
mv engine/analyzers/chart_orchestrator.py visuals/ 2>/dev/null || echo "ChartOrchestrator já no local correto"

# 3. Atualizar importação
sed -i.bak 's/from engine.analyzers.chart_orchestrator/from visuals.chart_orchestrator/' run_analysis.py

# 4. Corrigir NetworkChart
sed -i.bak 's/connections = data\[.concept_network.\]\[:10\]/if isinstance(data["concept_network"], list):\n        connections = data["concept_network"][:10]\n    else:\n        connections = list(data["concept_network"].items())[:10] if isinstance(data["concept_network"], dict) else []/' visuals/charts/network_chart.py

echo "✅ Correções aplicadas!"
echo "🧪 Teste agora: ./scripts/teste_automatico.sh"
