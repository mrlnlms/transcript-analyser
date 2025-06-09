#!/bin/bash
echo "🔄 Migrando de 'resultados' para 'output'..."

# 1. Backup dos arquivos
echo "📦 Criando backups..."
cp run_analysis.py run_analysis.py.backup
cp config_loader.py config_loader.py.backup

# 2. Atualizar Python files
echo "📝 Atualizando arquivos Python..."

# run_analysis.py
sed -i '' 's/"resultados"/"output"/g' run_analysis.py

# config_loader.py
sed -i '' 's/"resultados"/"output"/g' config_loader.py

# setup_auto.py (só nos comentários/prints)
sed -i '' 's|/resultados/|/output/|g' setup_auto.py

# cleanup_project.py (documentação)
sed -i '' 's|resultados/|output/|g' visuals/cleanup_project.py

# 3. Atualizar scripts shell
echo "📝 Atualizando scripts..."
for script in scripts/*.sh; do
    sed -i '' 's|/resultados/|/output/|g' "$script"
done

# 4. Atualizar .gitignore
echo "📝 Atualizando .gitignore..."
sed -i '' 's|/resultados/|/output/|g' .gitignore

# 5. Atualizar docs
echo "📝 Atualizando documentação..."
for doc in docs/*.md; do
    sed -i '' 's|/resultados/|/output/|g' "$doc"
done

# 6. Migrar pastas existentes
echo "📁 Migrando pastas existentes..."
for project in projects/*/; do
    if [ -d "$project/resultados" ]; then
        echo "  Migrando: $project"
        mv "$project/resultados" "$project/output"
    fi
done

echo "✅ Migração completa!"
echo ""
echo "🔍 Verificando..."
grep -r "resultados" --include="*.py" --include="*.sh" . | grep -v "__pycache__" | grep -v "backup"