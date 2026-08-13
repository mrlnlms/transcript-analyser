#!/usr/bin/env python3
"""
🎯 TRANSCRIPT ANALYZER V2.0 - Entry Point
Sistema modular de análise de transcrições
"""

import sys
import logging
from pathlib import Path

# Imports dos módulos
from core.managers.cli_manager import CLIManager
from core.managers.project_manager import ProjectManager
from core.managers.analysis_runner import AnalysisRunner
# from core.visuals.visualization_manager import test_visualization_system


def setup_logging(verbose: bool = False):
    """Configura o sistema de logging"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


def main():
    """Função principal - orquestra todos os módulos"""
    # CLI Manager
    cli = CLIManager()
    args = cli.parse_args()
    
    # Validar argumentos
    if not cli.validate_args(args):
        sys.exit(1)
    
    # Setup logging
    setup_logging(args.verbose if hasattr(args, 'verbose') else False)
    
    # Project Manager
    project_manager = ProjectManager()
    
    # Obter comando
    command, params = cli.get_command(args)
    
    # Executar comando apropriado
    if command == 'create':
        # Criar novo projeto
        success = project_manager.create_project(params)
        sys.exit(0 if success else 1)
        
    elif command == 'list':
        # Listar projetos
        project_manager.print_projects_table()
        sys.exit(0)
        
    elif command == 'analyze':
        # Analisar projeto
        valid, message = project_manager.validate_project(params)
        if not valid:
            print(f"❌ {message}")
            sys.exit(1)
            
        print(message)
        
        # Executar análise
        runner = AnalysisRunner()
        project_path = Path("projects") / params
        success = runner.analyze_project(project_path)
        
        if success:
            print(f"\n✅ Análise concluída!")
            print(f"📁 Resultados em: {project_path / 'output'}")
        
        sys.exit(0 if success else 1)
        
    elif command == 'compare':
        # TODO: Implementar comparação
        print("⚠️  Comparação ainda não implementada na nova versão")
        sys.exit(1)
        
    elif command == 'test':
        # Testar visualizações
        from core.visuals.visualization_manager import create_visualization_manager
        viz = create_visualization_manager()
        # Teste básico
        print("✅ Sistema de visualização carregado")
    else:
        print("❌ Comando não reconhecido")
        sys.exit(1)


if __name__ == "__main__":
    main()
