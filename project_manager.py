#!/usr/bin/env python3
"""
Project Manager - Gerenciamento de projetos
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class ProjectManager:
    """Gerencia projetos de análise"""
    
    def __init__(self, base_path: str = "projects"):
        self.base_path = Path(base_path)
        self.logger = logging.getLogger(__name__)
        
    def create_project(self, name: str) -> bool:
        """Cria um novo projeto com estrutura padrão"""
        try:
            project_dir = self.base_path / name
            
            if project_dir.exists():
                print(f"❌ Projeto '{name}' já existe!")
                return False
            
            # Criar estrutura
            project_dir.mkdir(parents=True)
            (project_dir / "arquivos").mkdir()
            (project_dir / "output").mkdir()
            
            # Criar configuração padrão
            config = {
                "project_name": name,
                "created_at": datetime.now().isoformat(),
                "analysis_config": {
                    "word_frequency": {"min_frequency": 2},
                    "temporal_analysis": {"segments": 10},
                    "topic_modeling": {"n_topics": 5}
                }
            }
            
            config_path = project_dir / "config_analise.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Projeto '{name}' criado com sucesso!")
            print(f"📁 Adicione arquivos .txt em: {project_dir / 'arquivos'}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao criar projeto: {e}")
            return False
    
    def list_projects(self) -> List[str]:
        """Lista todos os projetos disponíveis"""
        if not self.base_path.exists():
            return []
        
        projects = []
        for item in self.base_path.iterdir():
            if item.is_dir() and (item / "config_analise.json").exists():
                projects.append(item.name)
        
        return sorted(projects)
    
    def get_project_info(self, name: str) -> Optional[Dict]:
        """Obtém informações de um projeto"""
        project_dir = self.base_path / name
        
        if not project_dir.exists():
            return None
            
        info = {
            "name": name,
            "path": str(project_dir),
            "files": [],
            "has_output": False
        }
        
        # Contar arquivos
        arquivos_dir = project_dir / "arquivos"
        if arquivos_dir.exists():
            info["files"] = [f.name for f in arquivos_dir.glob("*.txt")]
        
        # Verificar se tem output
        output_dir = project_dir / "output"
        if output_dir.exists() and any(output_dir.iterdir()):
            info["has_output"] = True
            
        # Ler config se existir
        config_path = project_dir / "config_analise.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    info["config"] = json.load(f)
            except:
                pass
                
        return info
    
    def validate_project(self, name: str) -> tuple[bool, str]:
        """Valida se um projeto está pronto para análise"""
        project_dir = self.base_path / name
        
        if not project_dir.exists():
            return False, f"Projeto '{name}' não encontrado"
            
        if not (project_dir / "config_analise.json").exists():
            return False, f"Arquivo de configuração não encontrado"
            
        arquivos_dir = project_dir / "arquivos"
        if not arquivos_dir.exists():
            return False, f"Pasta 'arquivos' não encontrada"
            
        txt_files = list(arquivos_dir.glob("*.txt"))
        if not txt_files:
            return False, f"Nenhum arquivo .txt encontrado em 'arquivos'"
            
        return True, f"✅ {len(txt_files)} arquivo(s) encontrado(s)"
    
    def print_projects_table(self):
        """Imprime tabela formatada com os projetos"""
        projects = self.list_projects()
        
        if not projects:
            print("📭 Nenhum projeto encontrado.")
            print("💡 Use --create-project NOME para criar um novo projeto.")
            return
            
        print(f"\n📁 {len(projects)} projeto(s) encontrado(s):\n")
        print(f"{'Nome':<30} {'Arquivos':<10} {'Status':<20}")
        print("-" * 60)
        
        for proj_name in projects:
            info = self.get_project_info(proj_name)
            if info:
                n_files = len(info['files'])
                status = "✅ Analisado" if info['has_output'] else "⏳ Pendente"
                print(f"{proj_name:<30} {n_files:<10} {status:<20}")


# Teste rápido
if __name__ == "__main__":
    pm = ProjectManager()
    print("✅ Project Manager funcionando!")
    
    # Teste de listagem
    print("\n📋 Projetos existentes:")
    pm.print_projects_table()
