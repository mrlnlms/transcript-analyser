#!/bin/bash

# 🔍 Script de Refatoração - Transcript Analyzer
# Mapeia estrutura atual e cria arquitetura plugável

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE} $1 ${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Função para mapear código atual
map_current_structure() {
    print_header "MAPEAMENTO DA ESTRUTURA ATUAL"
    
    echo -e "${YELLOW}📁 Estrutura de arquivos principais:${NC}"
    echo "├── run_analysis.py ($(wc -l < run_analysis.py) linhas)"
    echo "├── engine/analyzer_core.py ($(wc -l < engine/analyzer_core.py) linhas)"
    echo "├── visuals/visualization_manager.py ($(wc -l < visuals/visualization_manager.py) linhas)"
    echo "└── visuals/dashboard_generator.py ($(wc -l < visuals/dashboard_generator.py) linhas)"
    echo ""
    
    echo -e "${YELLOW}🔍 Classes e funções em run_analysis.py:${NC}"
    grep -n "^class\|^def " run_analysis.py || echo "Nenhuma classe/função encontrada"
    echo ""
    
    echo -e "${YELLOW}🔍 Classes e funções em engine/analyzer_core.py:${NC}"
    grep -n "^class\|^def " engine/analyzer_core.py || echo "Nenhuma classe/função encontrada"
    echo ""
    
    echo -e "${YELLOW}🔍 Classes e funções em visuals/visualization_manager.py:${NC}"
    grep -n "^class\|^def " visuals/visualization_manager.py || echo "Nenhuma classe/função encontrada"
    echo ""
    
    echo -e "${YELLOW}📊 Análises identificadas (baseado em métodos do analyzer_core.py):${NC}"
    if [ -f "engine/analyzer_core.py" ]; then
        grep -n "def analyze_\|def calculate_\|def detect_\|def extract_" engine/analyzer_core.py | sed 's/^/  - /'
    fi
    echo ""
    
    echo -e "${YELLOW}📈 Visualizações identificadas (baseado em visualization_manager.py):${NC}"
    if [ -f "visuals/visualization_manager.py" ]; then
        grep -n "def create_\|def generate_" visuals/visualization_manager.py | sed 's/^/  - /'
    fi
    echo ""
    
    echo -e "${YELLOW}⚙️ Arquivos de configuração existentes:${NC}"
    find . -name "*.json" -not -path "./transcript_env/*" -not -path "./.git/*" | sed 's/^/  - /'
    echo ""
}

# Função para criar nova estrutura
create_new_structure() {
    print_header "CRIANDO NOVA ESTRUTURA PLUGÁVEL"
    
    # Criar diretórios
    echo "📁 Criando diretórios..."
    mkdir -p engine/analyzers
    mkdir -p visuals/charts  
    mkdir -p config/analysis_configs
    mkdir -p config/visualization_configs
    mkdir -p scripts/automation
    
    print_success "Diretórios criados"
    
    # Criar templates base
    echo "📄 Criando templates..."
    
    # Template BaseAnalyzer
    cat > engine/analyzers/__init__.py << 'EOF'
"""
Sistema de auto-descoberta de analisadores
"""
import importlib
import inspect
from pathlib import Path
from typing import Dict, Type
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """Classe base para todos os analisadores"""
    
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path) if config_path else {}
    
    def load_config(self, config_path: str) -> dict:
        """Carrega configuração específica do analisador"""
        import json
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config não encontrado: {config_path}")
            return {}
    
    @abstractmethod
    def analyze(self, text: str) -> Dict:
        """Executa a análise principal"""
        pass
    
    def get_calibration_params(self, text_length: int) -> Dict:
        """Retorna parâmetros calibrados baseado no tamanho do texto"""
        if text_length < 1000:  # Texto curto (~15min)
            return {"segments": 5, "smoothing": 0.1, "min_frequency": 2}
        elif text_length > 10000:  # Texto longo (~1h45+)
            return {"segments": 20, "smoothing": 0.3, "min_frequency": 5}
        else:  # Texto médio
            return {"segments": 10, "smoothing": 0.2, "min_frequency": 3}
    
    def get_name(self) -> str:
        """Retorna nome legível do analisador"""
        return self.__class__.__name__.replace('Analyzer', '').replace('_', ' ').title()

def discover_analyzers() -> Dict[str, Type[BaseAnalyzer]]:
    """Encontra automaticamente todos os analisadores disponíveis"""
    analyzers = {}
    analyzer_dir = Path(__file__).parent
    
    for file_path in analyzer_dir.glob("*.py"):
        if file_path.name.startswith("_") or file_path.name == "__init__.py":
            continue
            
        module_name = f"engine.analyzers.{file_path.stem}"
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BaseAnalyzer) and 
                    obj != BaseAnalyzer and
                    name.endswith("Analyzer")):
                    analyzers[name] = obj
        except ImportError as e:
            print(f"⚠️ Erro ao importar {module_name}: {e}")
    
    return analyzers
EOF

    # Template para novos analisadores
    cat > engine/analyzers/_template_analyzer.py << 'EOF'
"""
Template para criar novos analisadores
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseAnalyzer
from typing import Dict

class TemplateAnalyzer(BaseAnalyzer):
    """
    Template para novos analisadores
    
    Para criar um novo analisador:
    1. Copie este arquivo: cp _template_analyzer.py meu_analyzer.py
    2. Renomeie a classe: TemplateAnalyzer -> MeuAnalyzer  
    3. Implemente o método analyze()
    4. Crie arquivo de config em config/analysis_configs/
    """
    
    def analyze(self, text: str) -> Dict:
        """
        Implementar análise principal aqui
        
        Args:
            text: Texto da transcrição para analisar
            
        Returns:
            Dict com resultados da análise
        """
        # Exemplo de implementação:
        text_length = len(text)
        calibration = self.get_calibration_params(text_length)
        
        # Sua lógica de análise aqui
        results = {
            "analysis_type": self.get_name(),
            "text_length": text_length,
            "calibration_used": calibration,
            "results": {
                # Seus resultados aqui
            }
        }
        
        return results
    
    def get_calibration_params(self, text_length: int) -> Dict:
        """Sobrescrever se precisar de calibração específica"""
        base_params = super().get_calibration_params(text_length)
        
        # Adicionar parâmetros específicos da sua análise
        specific_params = {
            "my_parameter": "valor_baseado_no_tamanho"
        }
        
        return {**base_params, **specific_params}
EOF

    # Template BaseChart
    cat > visuals/charts/__init__.py << 'EOF'
"""
Sistema de auto-descoberta de gráficos
"""
import importlib
import inspect
from pathlib import Path
from typing import Dict, Type
from abc import ABC, abstractmethod

class BaseChart(ABC):
    """Classe base para todos os gráficos"""
    
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path) if config_path else {}
        self.backend = self.config.get("backend", "plotly")  # plotly, matplotlib, text
    
    def load_config(self, config_path: str) -> dict:
        """Carrega configuração específica do gráfico"""
        import json
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config não encontrado: {config_path}")
            return {}
    
    @abstractmethod
    def create(self, data: Dict, output_path: str) -> str:
        """Cria a visualização"""
        pass
    
    def adjust_for_data_size(self, data: Dict) -> Dict:
        """Ajusta parâmetros visuais baseado no volume de dados"""
        if isinstance(data, dict):
            # Estimar tamanho dos dados
            total_items = sum(len(v) if isinstance(v, (list, dict)) else 1 
                            for v in data.values())
        else:
            total_items = len(data) if hasattr(data, '__len__') else 1
        
        if total_items > 100:
            return {"downsample": True, "max_points": 50, "smoothing": 0.3}
        elif total_items > 50:
            return {"downsample": False, "max_points": 100, "smoothing": 0.1}
        else:
            return {"downsample": False, "smoothing": 0.0}
    
    def get_name(self) -> str:
        """Retorna nome legível do gráfico"""
        return self.__class__.__name__.replace('Chart', '').replace('_', ' ').title()

def discover_charts() -> Dict[str, Type[BaseChart]]:
    """Encontra automaticamente todos os gráficos disponíveis"""
    charts = {}
    chart_dir = Path(__file__).parent
    
    for file_path in chart_dir.glob("*.py"):
        if file_path.name.startswith("_") or file_path.name == "__init__.py":
            continue
            
        module_name = f"visuals.charts.{file_path.stem}"
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BaseChart) and 
                    obj != BaseChart and
                    name.endswith("Chart")):
                    charts[name] = obj
        except ImportError as e:
            print(f"⚠️ Erro ao importar {module_name}: {e}")
    
    return charts
EOF

    # Template para novos gráficos
    cat > visuals/charts/_template_chart.py << 'EOF'
"""
Template para criar novos gráficos
Copie este arquivo e implemente os métodos abstratos
"""
from . import BaseChart
from typing import Dict

class TemplateChart(BaseChart):
    """
    Template para novos gráficos
    
    Para criar um novo gráfico:
    1. Copie este arquivo: cp _template_chart.py meu_chart.py
    2. Renomeie a classe: TemplateChart -> MeuChart
    3. Implemente o método create()
    4. Crie arquivo de config em config/visualization_configs/
    """
    
    def create(self, data: Dict, output_path: str) -> str:
        """
        Implementar criação do gráfico aqui
        
        Args:
            data: Dados da análise para visualizar
            output_path: Caminho onde salvar o gráfico
            
        Returns:
            Caminho do arquivo criado
        """
        # Ajustar para tamanho dos dados
        adjustments = self.adjust_for_data_size(data)
        
        # Escolher backend baseado na configuração
        if self.backend == "plotly":
            return self._create_plotly(data, output_path, adjustments)
        elif self.backend == "matplotlib":
            return self._create_matplotlib(data, output_path, adjustments)
        else:
            return self._create_text(data, output_path, adjustments)
    
    def _create_plotly(self, data: Dict, output_path: str, adjustments: Dict) -> str:
        """Implementar versão Plotly do gráfico"""
        # Sua implementação Plotly aqui
        import plotly.graph_objects as go
        
        fig = go.Figure()
        # Adicionar seus dados ao gráfico
        
        html_path = output_path.replace('.png', '.html')
        fig.write_html(html_path)
        return html_path
    
    def _create_matplotlib(self, data: Dict, output_path: str, adjustments: Dict) -> str:
        """Implementar versão Matplotlib do gráfico"""
        # Sua implementação Matplotlib aqui
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        # Criar seu gráfico
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return output_path
    
    def _create_text(self, data: Dict, output_path: str, adjustments: Dict) -> str:
        """Implementar versão texto do gráfico (fallback)"""
        # Sua implementação texto aqui
        text_output = f"📊 {self.get_name()}\n"
        text_output += "=" * 40 + "\n"
        # Adicionar representação textual dos dados
        
        text_path = output_path.replace('.png', '.txt').replace('.html', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        return text_path
EOF

    # Configs templates
    cat > config/analysis_configs/_template.json << 'EOF'
{
    "enabled": true,
    "description": "Template para configuração de análise",
    "calibration": {
        "short_text": {
            "max_length": 1000,
            "parameters": {
                "segments": 5,
                "min_frequency": 2
            }
        },
        "medium_text": {
            "max_length": 10000,
            "parameters": {
                "segments": 10,
                "min_frequency": 3
            }
        },
        "long_text": {
            "parameters": {
                "segments": 20,
                "min_frequency": 5
            }
        }
    },
    "parameters": {
        "smoothing_factor": 0.2,
        "min_confidence": 0.1
    },
    "output": {
        "include_in_report": true,
        "export_raw_data": false,
        "create_visualization": true
    }
}
EOF

    cat > config/visualization_configs/_template.json << 'EOF'
{
    "enabled": true,
    "description": "Template para configuração de visualização",
    "backend": "plotly",
    "fallback_backends": ["matplotlib", "text"],
    "styling": {
        "width": 800,
        "height": 600,
        "theme": "plotly_white",
        "font_size": 12
    },
    "data_adjustments": {
        "max_data_points": 100,
        "downsample_threshold": 200,
        "smoothing": {
            "enabled": true,
            "factor": 0.1
        }
    },
    "export": {
        "formats": ["html", "png"],
        "dpi": 300,
        "interactive": true
    }
}
EOF

    # Config global
    cat > config/global_config.json << 'EOF'
{
    "version": "2.0",
    "system": {
        "auto_discovery": true,
        "parallel_processing": false,
        "cache_enabled": false
    },
    "defaults": {
        "analysis_backend": "real",
        "visualization_backend": "plotly",
        "output_format": "markdown"
    },
    "calibration": {
        "auto_adjust": true,
        "text_size_thresholds": {
            "short": 1000,
            "medium": 10000
        }
    }
}
EOF

    print_success "Templates criados"
}

# Função para criar scripts de automação
create_automation_scripts() {
    print_header "CRIANDO SCRIPTS DE AUTOMAÇÃO"
    
    # Script para criar nova análise
    cat > scripts/automation/nova_analise.sh << 'EOF'
#!/bin/bash
# Script para criar nova análise automaticamente

if [ -z "$1" ]; then
    echo "Uso: $0 <nome_analise> [descrição]"
    echo "Exemplo: $0 speech_velocity 'Análise de Velocidade de Fala'"
    exit 1
fi

NOME=$1
DESCRICAO=${2:-"Nova análise"}
SNAKE_CASE=$(echo "$NOME" | sed 's/[A-Z]/_&/g' | sed 's/^_//' | tr '[:upper:]' '[:lower:]')
CLASS_NAME=$(echo "$NOME" | sed 's/_\([a-z]\)/\U\1/g' | sed 's/^./\U&/')Analyzer

echo "🔧 Criando análise: $CLASS_NAME"
echo "📁 Arquivo: engine/analyzers/${SNAKE_CASE}.py"
echo "⚙️ Config: config/analysis_configs/${SNAKE_CASE}_config.json"

# Copiar e personalizar template
cp engine/analyzers/_template_analyzer.py engine/analyzers/${SNAKE_CASE}.py

# Corrigir para macOS (usar sed -i '')
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/TemplateAnalyzer/${CLASS_NAME}/g" engine/analyzers/${SNAKE_CASE}.py
    sed -i '' "s/Template para novos analisadores/${DESCRICAO}/g" engine/analyzers/${SNAKE_CASE}.py
else
    sed -i "s/TemplateAnalyzer/${CLASS_NAME}/g" engine/analyzers/${SNAKE_CASE}.py
    sed -i "s/Template para novos analisadores/${DESCRICAO}/g" engine/analyzers/${SNAKE_CASE}.py
fi

# Criar config personalizado
cp config/analysis_configs/_template.json config/analysis_configs/${SNAKE_CASE}_config.json

# Corrigir para macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/Template para configuração de análise/${DESCRICAO}/g" config/analysis_configs/${SNAKE_CASE}_config.json
else
    sed -i "s/Template para configuração de análise/${DESCRICAO}/g" config/analysis_configs/${SNAKE_CASE}_config.json
fi

echo "✅ Análise $CLASS_NAME criada!"
echo "📝 Próximo passo: editar engine/analyzers/${SNAKE_CASE}.py"
EOF

    # Script para criar novo gráfico
    cat > scripts/automation/novo_grafico.sh << 'EOF'
#!/bin/bash
# Script para criar novo gráfico automaticamente

if [ -z "$1" ]; then
    echo "Uso: $0 <nome_grafico> [descrição]"
    echo "Exemplo: $0 velocity_chart 'Gráfico de Velocidade'"
    exit 1
fi

NOME=$1
DESCRICAO=${2:-"Novo gráfico"}
SNAKE_CASE=$(echo "$NOME" | sed 's/[A-Z]/_&/g' | sed 's/^_//' | tr '[:upper:]' '[:lower:]')
CLASS_NAME=$(echo "$NOME" | sed 's/_\([a-z]\)/\U\1/g' | sed 's/^./\U&/')Chart

echo "🎨 Criando gráfico: $CLASS_NAME"
echo "📁 Arquivo: visuals/charts/${SNAKE_CASE}.py"
echo "⚙️ Config: config/visualization_configs/${SNAKE_CASE}_config.json"

# Copiar e personalizar template
cp visuals/charts/_template_chart.py visuals/charts/${SNAKE_CASE}.py
sed -i "s/TemplateChart/${CLASS_NAME}/g" visuals/charts/${SNAKE_CASE}.py
sed -i "s/Template para novos gráficos/${DESCRICAO}/g" visuals/charts/${SNAKE_CASE}.py

# Criar config personalizado
cp config/visualization_configs/_template.json config/visualization_configs/${SNAKE_CASE}_config.json
sed -i "s/Template para configuração de visualização/${DESCRICAO}/g" config/visualization_configs/${SNAKE_CASE}_config.json

echo "✅ Gráfico $CLASS_NAME criado!"
echo "📝 Próximo passo: editar visuals/charts/${SNAKE_CASE}.py"
EOF

    # Script para criar feature completa (análise + gráfico)
    cat > scripts/automation/nova_feature.sh << 'EOF'
#!/bin/bash
# Script para criar análise + gráfico de uma vez

if [ -z "$1" ]; then
    echo "Uso: $0 <nome_feature> [descrição]"
    echo "Exemplo: $0 emotion_phases 'Análise de Fases Emocionais'"
    exit 1
fi

NOME=$1
DESCRICAO=${2:-"Nova feature"}

echo "🚀 Criando feature completa: $NOME"
echo "📊 Análise + 📈 Gráfico"

# Criar análise
./scripts/automation/nova_analise.sh "${NOME}_analysis" "$DESCRICAO"

# Criar gráfico
./scripts/automation/novo_grafico.sh "${NOME}_chart" "Gráfico de $DESCRICAO"

echo ""
echo "✅ Feature $NOME criada completamente!"
echo "📝 Próximos passos:"
echo "   1. Editar engine/analyzers/${NOME}_analysis.py"
echo "   2. Editar visuals/charts/${NOME}_chart.py"
echo "   3. Testar: python run_analysis.py --test-analysis ${NOME}_analysis"
EOF

    chmod +x scripts/automation/*.sh
    
    print_success "Scripts de automação criados"
    echo "   📄 scripts/automation/nova_analise.sh"
    echo "   📄 scripts/automation/novo_grafico.sh"  
    echo "   📄 scripts/automation/nova_feature.sh"
}

# Função para validar estrutura
validate_structure() {
    print_header "VALIDANDO NOVA ESTRUTURA"
    
    echo "📁 Verificando diretórios criados..."
    for dir in "engine/analyzers" "visuals/charts" "config/analysis_configs" "config/visualization_configs" "scripts/automation"; do
        if [ -d "$dir" ]; then
            print_success "$dir ✓"
        else
            print_error "$dir ✗"
        fi
    done
    
    echo ""
    echo "📄 Verificando templates criados..."
    for file in "engine/analyzers/__init__.py" "engine/analyzers/_template_analyzer.py" "visuals/charts/__init__.py" "visuals/charts/_template_chart.py"; do
        if [ -f "$file" ]; then
            print_success "$file ✓"
        else
            print_error "$file ✗"
        fi
    done
    
    echo ""
    echo "⚙️ Verificando configs..."
    for file in "config/analysis_configs/_template.json" "config/visualization_configs/_template.json" "config/global_config.json"; do
        if [ -f "$file" ]; then
            print_success "$file ✓"
        else
            print_error "$file ✗"
        fi
    done
    
    echo ""
    echo "🛠️ Verificando scripts de automação..."
    for file in "scripts/automation/nova_analise.sh" "scripts/automation/novo_grafico.sh" "scripts/automation/nova_feature.sh"; do
        if [ -f "$file" ]; then
            print_success "$file ✓"
        else
            print_error "$file ✗"
        fi
    done
}

# Função principal
main() {
    clear
    print_header "REFATORAÇÃO TRANSCRIPT ANALYZER V2.0"
    echo "Este script vai mapear a estrutura atual e criar a nova arquitetura plugável"
    echo ""
    
    # Verificar se estamos no diretório correto
    if [ ! -f "run_analysis.py" ]; then
        print_error "Execute este script do diretório raiz do projeto (onde está run_analysis.py)"
        exit 1
    fi
    
    # Menu de opções
    echo "Escolha uma opção:"
    echo "1) Mapear estrutura atual"
    echo "2) Criar nova estrutura"
    echo "3) Fazer ambos (recomendado)"
    echo "4) Sair"
    
    read -p "Opção [1-4]: " opcao
    
    case $opcao in
        1)
            map_current_structure
            ;;
        2)
            create_new_structure
            create_automation_scripts
            validate_structure
            ;;
        3)
            map_current_structure
            echo ""
            read -p "Pressione Enter para continuar com a criação da nova estrutura..."
            create_new_structure
            create_automation_scripts
            validate_structure
            ;;
        4)
            echo "Saindo..."
            exit 0
            ;;
        *)
            print_error "Opção inválida"
            exit 1
            ;;
    esac
    
    echo ""
    print_header "PRÓXIMOS PASSOS"
    echo "1. ✅ Estrutura plugável criada"
    echo "2. 🔄 Migrar código existente para novos módulos"
    echo "3. 🧪 Testar se tudo funciona"
    echo "4. 🚀 Começar a usar scripts de automação"
    echo ""
    echo "📝 Para criar nova análise: ./scripts/automation/nova_analise.sh minha_analise"
    echo "🎨 Para criar novo gráfico: ./scripts/automation/novo_grafico.sh meu_grafico"
    echo "🚀 Para criar feature completa: ./scripts/automation/nova_feature.sh minha_feature"
}

# Executar script
main "$@"