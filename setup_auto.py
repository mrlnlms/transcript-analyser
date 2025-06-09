#!/usr/bin/env python3
"""
🚀 TRANSCRIPT ANALYZER - SETUP AUTOMATIZADO
Para Mac, Windows e Linux - Detecta SO e instala dependências corretas
"""

import subprocess
import sys
import platform
import os
from pathlib import Path


def detect_system():
    """Detecta sistema operacional"""
    system = platform.system().lower()
    print(f"🖥️ Sistema detectado: {platform.system()} {platform.release()}")
    return system


def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ necessário")
        return False
    
    print("✅ Versão do Python adequada")
    return True


def setup_virtual_environment():
    """Configura ambiente virtual se não existir"""
    
    venv_path = Path("transcript_env")
    
    if venv_path.exists():
        print("📦 Ambiente virtual já existe")
        return True
    
    print("📦 Criando ambiente virtual...")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "transcript_env"], 
                      check=True, capture_output=True)
        print("✅ Ambiente virtual criado")
        
        # Instruções de ativação
        if sys.platform == "win32":
            activate_cmd = "transcript_env\\Scripts\\activate"
        else:
            activate_cmd = "source transcript_env/bin/activate"
        
        print(f"\n🔧 Para ativar o ambiente virtual:")
        print(f"   {activate_cmd}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        return False


def install_dependencies_smart():
    """Instala dependências de forma inteligente baseada no SO"""
    
    system = detect_system()
    
    # Verificar se estamos no ambiente virtual
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Ambiente virtual ativo")
    else:
        print("⚠️ Ambiente virtual não detectado - continuando...")
    
    print("\n📦 INSTALANDO DEPENDÊNCIAS...")
    print("=" * 50)
    
    # Atualizar pip
    print("🔧 Atualizando pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✅ pip atualizado")
    except:
        print("⚠️ Erro ao atualizar pip, continuando...")
    
    # Dependências por categoria
    if system == "darwin":  # macOS
        return install_macos_dependencies()
    elif system == "windows":
        return install_windows_dependencies()
    else:  # Linux
        return install_linux_dependencies()


def install_macos_dependencies():
    """Instalação específica para macOS"""
    
    print("🍎 Instalação otimizada para macOS")
    
    # Grupo 1: Científicas (com flags especiais para Mac)
    mac_scientific = [
        "--only-binary=all", "numpy>=1.21.0",
        "--only-binary=all", "scipy>=1.9.0", 
        "--only-binary=all", "scikit-learn>=1.0.0"
    ]
    
    # Grupo 2: Visualizações (sempre funcionam)
    viz_packages = [
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0", 
        "plotly>=5.10.0",
        "networkx>=2.8.0",
        "wordcloud>=1.9.0"
    ]
    
    # Grupo 3: Análise de dados
    data_packages = [
        "pandas>=1.5.0",
        "nltk>=3.7",
        "textblob>=0.17.1"
    ]
    
    # Grupo 4: Utilitários
    utils = [
        "tqdm>=4.64.0",
        "pyyaml>=6.0",
        "pathlib2>=2.3.7"
    ]
    
    # Instalar em grupos
    package_groups = [
        ("🔬 Pacotes científicos (Mac)", mac_scientific),
        ("📊 Visualizações", viz_packages), 
        ("📈 Análise de dados", data_packages),
        ("🛠️ Utilitários", utils)
    ]
    
    success_count = 0
    total_groups = len(package_groups)
    
    for group_name, packages in package_groups:
        print(f"\n{group_name}...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + packages,
                         check=True, capture_output=True, text=True)
            print(f"✅ {group_name} - OK")
            success_count += 1
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ {group_name} - Alguns pacotes falharam")
            # Tentar instalar um por um
            for package in packages:
                if not package.startswith("--"):
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", package],
                                     check=True, capture_output=True)
                        print(f"  ✅ {package}")
                    except:
                        print(f"  ❌ {package}")
    
    # Pacotes opcionais (podem falhar)
    optional_packages = ["gensim", "spacy"]
    
    print(f"\n🔍 Tentando pacotes opcionais...")
    for package in optional_packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True, timeout=300)
            print(f"✅ {package} (opcional)")
        except:
            print(f"⚠️ {package} falhou (normal no Mac)")
    
    return success_count >= (total_groups - 1)  # OK se pelo menos 3/4 grupos funcionaram


def install_windows_dependencies():
    """Instalação para Windows"""
    
    print("🪟 Instalação para Windows")
    
    # Windows geralmente funciona melhor com pip normal
    all_packages = [
        "pandas>=1.5.0", "numpy>=1.21.0", "scipy>=1.9.0",
        "matplotlib>=3.5.0", "seaborn>=0.11.0", "plotly>=5.10.0", 
        "networkx>=2.8.0", "wordcloud>=1.9.0", "scikit-learn>=1.0.0",
        "nltk>=3.7", "textblob>=0.17.1", "tqdm>=4.64.0", "pyyaml>=6.0"
    ]
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install"] + all_packages,
                     check=True, capture_output=True)
        print("✅ Todas as dependências instaladas")
        return True
    except:
        print("⚠️ Instalação em lote falhou, tentando individualmente...")
        return install_individual_packages(all_packages)


def install_linux_dependencies():
    """Instalação para Linux"""
    
    print("🐧 Instalação para Linux")
    
    # Linux geralmente funciona bem
    all_packages = [
        "pandas>=1.5.0", "numpy>=1.21.0", "scipy>=1.9.0",
        "matplotlib>=3.5.0", "seaborn>=0.11.0", "plotly>=5.10.0", 
        "networkx>=2.8.0", "wordcloud>=1.9.0", "scikit-learn>=1.0.0",
        "nltk>=3.7", "textblob>=0.17.1", "tqdm>=4.64.0", "pyyaml>=6.0",
        "gensim>=4.2.0"  # Geralmente funciona no Linux
    ]
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install"] + all_packages,
                     check=True, capture_output=True)
        print("✅ Todas as dependências instaladas")
        return True
    except:
        print("⚠️ Instalação em lote falhou, tentando individualmente...")
        return install_individual_packages(all_packages)


def install_individual_packages(packages):
    """Instala pacotes individualmente se instalação em lote falhar"""
    
    success_count = 0
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package],
                         check=True, capture_output=True)
            print(f"  ✅ {package}")
            success_count += 1
        except:
            print(f"  ❌ {package}")
    
    return success_count >= len(packages) * 0.8  # OK se 80% funcionaram


def test_installation():
    """Testa se instalação funcionou"""
    
    print("\n🧪 TESTANDO INSTALAÇÃO...")
    print("=" * 40)
    
    # Testes essenciais
    essential_tests = [
        ("pandas", "import pandas"),
        ("numpy", "import numpy"), 
        ("matplotlib", "import matplotlib"),
        ("seaborn", "import seaborn"),
        ("plotly", "import plotly"),
        ("networkx", "import networkx"),
        ("wordcloud", "import wordcloud"),
        ("sklearn", "import sklearn"),
        ("nltk", "import nltk"),
        ("textblob", "import textblob")
    ]
    
    success_count = 0
    
    for name, import_stmt in essential_tests:
        try:
            subprocess.run([sys.executable, "-c", import_stmt], 
                         check=True, capture_output=True)
            print(f"✅ {name}")
            success_count += 1
        except:
            print(f"❌ {name}")
    
    # Teste do sistema
    try:
        result = subprocess.run([sys.executable, "run_analysis.py", "--list-projects"], 
                              capture_output=True, text=True, timeout=30)
        if "Projetos disponíveis" in result.stdout:
            print("✅ Sistema principal funcionando")
            success_count += 1
        else:
            print("⚠️ Sistema principal com problemas")
    except:
        print("⚠️ Sistema principal não testado")
    
    total_tests = len(essential_tests) + 1
    success_rate = (success_count / total_tests) * 100
    
    print(f"\n📊 Taxa de sucesso: {success_rate:.0f}% ({success_count}/{total_tests})")
    
    if success_rate >= 80:
        print("🎉 INSTALAÇÃO BEM-SUCEDIDA!")
        return True
    else:
        print("⚠️ Instalação parcial - sistema pode funcionar com limitações")
        return False


def create_quick_start_guide():
    """Cria guia de início rápido"""
    
    system = detect_system()
    
    if system == "darwin":
        activate_cmd = "source transcript_env/bin/activate"
    else:
        activate_cmd = "transcript_env\\Scripts\\activate"
    
    guide = f"""
# 🚀 TRANSCRIPT ANALYZER - GUIA RÁPIDO

## ✅ Instalação concluída!

### 🔧 Como usar:

1. **Ativar ambiente virtual:**
   ```bash
   {activate_cmd}
   ```

2. **Listar projetos:**
   ```bash
   python3 run_analysis.py --list-projects
   ```

3. **Criar novo projeto:**
   ```bash
   python3 run_analysis.py --create-project meu_projeto
   ```

4. **Executar análise:**
   ```bash
   python3 run_analysis.py --project nome_projeto
   ```

5. **Testar visualizações:**
   ```bash
   python3 run_analysis.py --test-visuals
   ```

### 📁 Estrutura:
- `projects/nome_projeto/arquivos/` → Adicione arquivos .txt aqui
- `projects/nome_projeto/output/` → Resultados aparecem aqui
- `resources/` → Léxicos editáveis
- `config/` → Configurações globais

### 🎯 Backends disponíveis:
- **Plotly**: Gráficos interativos (HTML)
- **Matplotlib**: Gráficos estáticos (PNG/PDF) 
- **Text**: Fallback em texto

### 💡 Próximos passos:
1. Adicione arquivos .txt em projects/exemplo_docentes/arquivos/
2. Execute análise: `python3 run_analysis.py --project exemplo_docentes`
3. Veja resultados em projects/exemplo_docentes/output/

---
🎉 **Sistema pronto para uso!**
"""
    
    with open("QUICK_START.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("📚 Guia criado: QUICK_START.md")


def main():
    """Função principal do setup automatizado"""
    
    print("🚀 TRANSCRIPT ANALYZER - SETUP AUTOMATIZADO")
    print("=" * 60)
    print()
    
    # Verificações iniciais
    if not check_python_version():
        return False
    
    system = detect_system()
    print()
    
    # Setup do ambiente virtual
    if not setup_virtual_environment():
        print("⚠️ Continuando sem ambiente virtual...")
    
    print()
    
    # Instalação inteligente
    success = install_dependencies_smart()
    
    print()
    
    # Testes
    test_success = test_installation()
    
    # Guia de início
    create_quick_start_guide()
    
    print("\n" + "=" * 60)
    if success and test_success:
        print("🎉 SETUP AUTOMATIZADO CONCLUÍDO COM SUCESSO!")
        print("\n📖 Consulte QUICK_START.md para começar a usar")
        print(f"\n💡 Lembre-se de ativar o ambiente virtual:")
        if system == "darwin":
            print("   source transcript_env/bin/activate")
        else:
            print("   transcript_env\\Scripts\\activate")
    else:
        print("⚠️ Setup concluído com algumas limitações")
        print("💡 Sistema básico deve funcionar normalmente")
    
    return success


if __name__ == "__main__":
    main()