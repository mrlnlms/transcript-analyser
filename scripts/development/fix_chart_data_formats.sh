#!/bin/bash
echo "🔧 Corrigindo formatos de dados dos gráficos..."

# 1. Corrigir NetworkChart - tratar concept_network como lista
sed -i.bak 's/connections = data\[.concept_network.\]\[:10\]/concept_data = data["concept_network"]\
        connections = concept_data[:10] if isinstance(concept_data, list) else []/' visuals/charts/network_chart.py

# 2. Corrigir TimelineChart - garantir que seg é dict
sed -i.bak 's/x_data = \[seg.get(.timestamp., f"{i}%") for i, seg in enumerate(temporal_data)\]/x_data = [seg.get("timestamp", f"{i}%") if isinstance(seg, dict) else f"{i}%" for i, seg in enumerate(temporal_data)]/' visuals/charts/timeline_chart.py

sed -i.bak 's/y_data = \[seg\[.sentiment.\] for seg in temporal_data\]/y_data = [seg.get("sentiment", 0) if isinstance(seg, dict) else 0 for seg in temporal_data]/' visuals/charts/timeline_chart.py

echo "✅ Correções aplicadas!"
echo "🧪 Testando..."
