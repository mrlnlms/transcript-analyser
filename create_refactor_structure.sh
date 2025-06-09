#!/bin/bash

echo "🏗️ Criando estrutura para refatoração..."

# Backup primeiro (sempre!)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p backups
cp run_analysis.py "backups/run_analysis_pre_refactor_$TIMESTAMP.py"
echo "✅ Backup criado: backups/run_analysis_pre_refactor_$TIMESTAMP.py"

# Criar novos módulos
touch cli_manager.py
touch project_manager.py
touch analysis_runner.py

echo "✅ Módulos criados!"
echo ""
echo "�� Próximos passos:"
echo "1. cli_manager.py - Gerenciamento de CLI"
echo "2. project_manager.py - Gerenciamento de projetos"
echo "3. analysis_runner.py - Execução de análises"
echo "4. run_analysis.py - Apenas entry point"

