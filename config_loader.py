#!/usr/bin/env python3
"""
🎯 TRANSCRIPT ANALYZER - ESTRUTURA MODULAR
📁 Desktop/transcript-analyser/

Arquitetura centralizada para análise de entrevistas qualitativas
com configurações externalizadas e módulos independentes.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ProjectConfig:
    """Classe para configurações de projeto - versão flexível"""
    project_name: str
    topic_modeling: Dict[str, Any]
    emotion: Dict[str, Any]
    linguistic: Dict[str, Any]
    output: Dict[str, Any]
    
    # Campos opcionais
    description: Optional[str] = None
    created_date: Optional[str] = None
    version: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None
    visualizations: Optional[Dict[str, Any]] = None
    export: Optional[Dict[str, Any]] = None
    quality_control: Optional[Dict[str, Any]] = None
    advanced: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validação após inicialização"""
        if not self.project_name:
            raise ValueError("Nome do projeto é obrigatório")
        
        # Compatibilidade com configs antigos
        if not hasattr(self, 'advanced') or self.advanced is None:
            self.advanced = {
                "contradiction_detection": True,
                "concept_network": True,
                "temporal_analysis": True,
                "comparative_mode": False
            }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Cria ProjectConfig a partir de dicionário, ignorando campos extras"""
        
        # Campos obrigatórios
        required_fields = {
            'project_name': data.get('project_name'),
            'topic_modeling': data.get('topic_modeling', {}),
            'emotion': data.get('emotion', {}),
            'linguistic': data.get('linguistic', {}),
            'output': data.get('output', {}),
        }
        
        # Campos opcionais
        optional_fields = {
            'description': data.get('description'),
            'created_date': data.get('created_date'),
            'version': data.get('version'),
            'analysis': data.get('analysis'),
            'visualizations': data.get('visualizations'),
            'export': data.get('export'),
            'quality_control': data.get('quality_control'),
            'advanced': data.get('advanced'),
        }
        
        # Combinar campos
        all_fields = {**required_fields, **optional_fields}
        
        return cls(**all_fields)

class ConfigLoader:
    """🔧 Carregador universal de configurações"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.projects_dir = self.base_path / "projects"
        self.resources_dir = self.base_path / "resources"
        
        # Criar diretórios se não existirem
        self.projects_dir.mkdir(exist_ok=True)
        self.resources_dir.mkdir(exist_ok=True)
    
    # Substitua o método load_project_config na classe ConfigLoader:

    def load_project_config(self, project_name: str) -> ProjectConfig:
        """🎛️ Carrega configuração específica do projeto"""
        config_path = self.projects_dir / project_name / "config_analise.json"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuração não encontrada: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Usar método from_dict para lidar com campos extras
        return ProjectConfig.from_dict(config_data)
    
    def load_resource_file(self, filename: str) -> List[str]:
        """📚 Carrega arquivo de recurso (stopwords, dicionários, etc.)"""
        file_path = self.resources_dir / filename
        
        if not file_path.exists():
            print(f"⚠️ Arquivo de recurso não encontrado: {filename}")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            if filename.endswith('.json'):
                return json.load(f)
            else:
                return [line.strip() for line in f if line.strip()]
    
    def load_all_lexicons(self) -> Dict[str, List[str]]:
        """📖 Carrega todos os léxicos da pasta resources/"""
        lexicons = {}
        
        # Mapear arquivos para chaves
        lexicon_files = {
            'stopwords_custom': 'stopwords_custom.txt',
            'modalizadores_certeza': 'modalizadores_certeza.txt',
            'hesitacao_termos': 'hesitacao_termos.txt',
            'emocionais_positivos': 'emocionais_positivos.txt',
            'emocionais_negativos': 'emocionais_negativos.txt',
            'conectores_discursivos': 'conectores_discursivos.txt'
        }
        
        for key, filename in lexicon_files.items():
            lexicons[key] = self.load_resource_file(filename)
        
        # Carregar pesos específicos
        lexicons['pesos_formula'] = self.load_resource_file('pesos_formula_linguistica.json')
        
        return lexicons
    
    def create_default_project(self, project_name: str):
        """🛠️ Cria projeto padrão com estrutura completa"""
        project_dir = self.projects_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        # Criar subdiretórios
        (project_dir / "arquivos").mkdir(exist_ok=True)
        (project_dir / "output").mkdir(exist_ok=True)
        
        # Configuração padrão
        default_config = {
            "project_name": project_name,
            "topic_modeling": {
                "n_topics": 5,
                "auto_adjust": True,
                "min_topics": 3,
                "max_topics": 10,
                "coherence_threshold": 0.4
            },
            "emotion": {
                "block_size": 10,
                "smoothing": True,
                "sentiment_threshold": 0.2,
                "peak_detection": True
            },
            "linguistic": {
                "use_stemming": True,
                "extra_stopwords": ["tipo", "então", "né", "assim"],
                "hesitation_weight": 1.5,
                "certainty_weight": 2.0,
                "min_sentence_length": 3
            },
            "output": {
                "generate_markdown": True,
                "generate_visuals": True,
                "save_raw_data": False,
                "create_summary": True,
                "dashboard_style": "premium"
            },
            "advanced": {
                "contradiction_detection": True,
                "concept_network": True,
                "temporal_analysis": True,
                "comparative_mode": False
            }
        }
        
        # Salvar configuração
        config_path = project_dir / "config_analise.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Projeto '{project_name}' criado em: {project_dir}")
        return project_dir


class ResourceManager:
    """📚 Gerenciador dinâmico de recursos lexicais"""
    
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self._lexicons = None
    
    @property
    def lexicons(self) -> Dict[str, List[str]]:
        """💾 Carregamento lazy dos léxicos"""
        if self._lexicons is None:
            self._lexicons = self.config_loader.load_all_lexicons()
        return self._lexicons
    
    def get_stopwords(self, extra_words: List[str] = None) -> List[str]:
        """🛑 Retorna stopwords personalizadas + extras"""
        stopwords = self.lexicons['stopwords_custom'].copy()
        if extra_words:
            stopwords.extend(extra_words)
        return list(set(stopwords))
    
    def get_emotional_words(self) -> Dict[str, List[str]]:
        """😊😢 Retorna dicionários emocionais"""
        return {
            'positivas': self.lexicons['emocionais_positivos'],
            'negativas': self.lexicons['emocionais_negativos']
        }
    
    def get_linguistic_markers(self) -> Dict[str, List[str]]:
        """🎭 Retorna marcadores linguísticos"""
        return {
            'certeza': self.lexicons['modalizadores_certeza'],
            'hesitacao': self.lexicons['hesitacao_termos'],
            'conectores': self.lexicons['conectores_discursivos']
        }
    
    def get_formula_weights(self) -> Dict[str, float]:
        """⚖️ Retorna pesos para fórmulas de cálculo"""
        weights = self.lexicons.get('pesos_formula', {})
        
        # Pesos padrão caso arquivo não exista
        default_weights = {
            'hesitation_penalty': -0.1,
            'certainty_boost': 0.2,
            'emotional_intensity': 1.5,
            'topic_coherence': 0.3,
            'sentence_length_factor': 0.05
        }
        
        return {**default_weights, **weights}
