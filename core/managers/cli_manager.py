#!/usr/bin/env python3
"""
CLI Manager - Gerenciamento de linha de comando
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List


class CLIManager:
    """Gerencia argumentos e comandos da CLI"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Cria o parser de argumentos"""
        parser = argparse.ArgumentParser(
            description='🎯 Transcript Analyzer - Análise automatizada de transcrições',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemplos de uso:
  %(prog)s --create-project meu_estudo
  %(prog)s --project meu_estudo
  %(prog)s --compare projeto1 projeto2 projeto3
  %(prog)s --list-projects
  %(prog)s --test-visuals
            """
        )
        
        # Grupo de ações mutuamente exclusivas
        action = parser.add_mutually_exclusive_group(required=True)
        
        action.add_argument(
            '--create-project',
            metavar='NOME',
            help='Criar novo projeto de análise'
        )
        
        action.add_argument(
            '--project', '-p',
            metavar='NOME',
            help='Executar análise de um projeto'
        )
        
        action.add_argument(
            '--compare', '-c',
            nargs='+',
            metavar='PROJ',
            help='Comparar múltiplos projetos'
        )
        
        action.add_argument(
            '--list-projects', '-l',
            action='store_true',
            help='Listar projetos disponíveis'
        )
        
        action.add_argument(
            '--test-visuals',
            action='store_true',
            help='Testar sistema de visualizações'
        )
        
        # Opções adicionais
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Modo verboso com mais informações'
        )
        
        parser.add_argument(
            '--force', '-f',
            action='store_true',
            help='Forçar execução sem confirmações'
        )
        
        return parser
    
    def parse_args(self, args=None):
        """Parse dos argumentos da linha de comando"""
        return self.parser.parse_args(args)
    
    def validate_args(self, args) -> bool:
        """Valida os argumentos fornecidos"""
        # Validação básica de nomes de projeto
        if args.create_project:
            if not self._is_valid_project_name(args.create_project):
                print("❌ Nome de projeto inválido. Use apenas letras, números e underscore.")
                return False
                
        if args.compare and len(args.compare) < 2:
            print("❌ Comparação requer pelo menos 2 projetos.")
            return False
            
        return True
    
    def _is_valid_project_name(self, name: str) -> bool:
        """Verifica se o nome do projeto é válido"""
        import re
        return bool(re.match(r'^[a-zA-Z0-9_]+$', name))
    
    def get_command(self, args) -> tuple:
        """Retorna o comando e seus parâmetros"""
        if args.create_project:
            return ('create', args.create_project)
        elif args.project:
            return ('analyze', args.project)
        elif args.compare:
            return ('compare', args.compare)
        elif args.list_projects:
            return ('list', None)
        elif args.test_visuals:
            return ('test', None)
        else:
            return (None, None)


# Teste rápido
if __name__ == "__main__":
    cli = CLIManager()
    args = cli.parse_args(['--create-project', 'teste'])
    print(f"✅ CLI Manager funcionando!")
    print(f"📋 Comando: {cli.get_command(args)}")
