import re

# Ler arquivo
with open('engine/analysis_orchestrator.py', 'r') as f:
    content = f.read()

# Localizar e substituir
old_pattern = r'''                if result:
                    results\[analyzer_key\] = result
                    self\.results_cache\[analyzer_key\] = result
                    successful_analyses \+= 1'''

new_pattern = '''                if result:
                    results[analyzer_key] = result
                    self.results_cache[analyzer_key] = result
                    
                    # CORREÇÃO: Expor dados internos no nível raiz para os gráficos
                    if isinstance(result, dict):
                        for key, value in result.items():
                            if key not in ['analysis_type', 'calibration_used']:
                                results[key] = value
                    
                    successful_analyses += 1'''

content = re.sub(old_pattern, new_pattern, content)

# Salvar
with open('engine/analysis_orchestrator.py', 'w') as f:
    f.write(content)

print("✅ Correção aplicada!")
