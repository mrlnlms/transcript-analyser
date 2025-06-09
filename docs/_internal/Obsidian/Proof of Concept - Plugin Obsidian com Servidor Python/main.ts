// main.ts - Proof of Concept para Transcript Analyzer + Obsidian
import { App, Plugin, PluginSettingTab, Setting, Notice, Modal, MarkdownView } from 'obsidian';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

interface TranscriptAnalyzerSettings {
    serverInstalled: boolean;
    serverPath: string;
    autoStartServer: boolean;
}

const DEFAULT_SETTINGS: TranscriptAnalyzerSettings = {
    serverInstalled: false,
    serverPath: '',
    autoStartServer: false
}

export default class TranscriptAnalyzerPlugin extends Plugin {
    settings: TranscriptAnalyzerSettings;
    private server: ChildProcess | null = null;
    private serverRunning: boolean = false;

    async onload() {
        await this.loadSettings();

        // Adiciona comando principal
        this.addCommand({
            id: 'analyze-transcript',
            name: 'Analisar transcrição',
            callback: () => this.analyzeCurrentNote()
        });

        // Adiciona ribbon icon
        this.addRibbonIcon('mic', 'Transcript Analyzer', () => {
            this.analyzeCurrentNote();
        });

        // Settings
        this.addSettingTab(new TranscriptAnalyzerSettingTab(this.app, this));

        // Verifica se é primeira vez
        if (!this.settings.serverInstalled) {
            // Delay para garantir que plugin carregou
            setTimeout(() => {
                new WelcomeModal(this.app, this).open();
            }, 1000);
        }
    }

    async analyzeCurrentNote() {
        const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (!activeView) {
            new Notice('❌ Nenhuma nota ativa!');
            return;
        }

        const content = activeView.editor.getValue();
        new Notice('🔍 Analisando transcrição...');

        try {
            // Tenta análise avançada primeiro
            if (this.settings.serverInstalled) {
                await this.ensureServerRunning();
                const results = await this.analyzeWithPython(content);
                this.showDashboard(results);
            } else {
                // Fallback para análise básica
                const results = this.analyzeBasic(content);
                this.showDashboard(results);
            }
        } catch (error) {
            console.error('Erro na análise:', error);
            new Notice('❌ Erro na análise. Usando modo básico...');
            const results = this.analyzeBasic(content);
            this.showDashboard(results);
        }
    }

    analyzeBasic(content: string): any {
        // Análise básica em JS
        const words = content.split(/\s+/).filter(w => w.length > 0);
        const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0);
        
        // Análise de sentimento super básica
        const positiveWords = ['bom', 'ótimo', 'excelente', 'feliz', 'adorei', 'incrível'];
        const negativeWords = ['ruim', 'péssimo', 'horrível', 'triste', 'odeio', 'terrível'];
        
        let sentiment = 0;
        words.forEach(word => {
            if (positiveWords.includes(word.toLowerCase())) sentiment++;
            if (negativeWords.includes(word.toLowerCase())) sentiment--;
        });

        return {
            basic: true,
            wordCount: words.length,
            sentenceCount: sentences.length,
            avgWordsPerSentence: Math.round(words.length / sentences.length),
            sentiment: sentiment > 0 ? 'Positivo' : sentiment < 0 ? 'Negativo' : 'Neutro',
            sentimentScore: sentiment,
            readingTime: Math.ceil(words.length / 200),
            message: 'Análise básica - Instale o servidor para análise completa!'
        };
    }

    async analyzeWithPython(content: string): Promise<any> {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: content })
        });

        if (!response.ok) {
            throw new Error('Server error');
        }

        return await response.json();
    }

    showDashboard(results: any) {
        // Cria HTML do dashboard
        const html = `
            <div style="padding: 20px; font-family: var(--font-interface);">
                <h1>📊 Análise de Transcrição</h1>
                
                ${results.message ? `<div style="background: #ff6b6b; color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px;">${results.message}</div>` : ''}
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px;">
                    <div style="background: var(--background-secondary); padding: 20px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 2em; font-weight: bold; color: var(--text-accent);">${results.wordCount}</div>
                        <div style="color: var(--text-muted);">Palavras</div>
                    </div>
                    
                    <div style="background: var(--background-secondary); padding: 20px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 2em; font-weight: bold; color: var(--text-accent);">${results.sentiment}</div>
                        <div style="color: var(--text-muted);">Sentimento</div>
                    </div>
                    
                    <div style="background: var(--background-secondary); padding: 20px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 2em; font-weight: bold; color: var(--text-accent);">${results.readingTime}min</div>
                        <div style="color: var(--text-muted);">Tempo de Leitura</div>
                    </div>
                </div>
                
                ${results.basic ? '' : `
                    <h2>🎯 Análise Avançada</h2>
                    <div style="background: var(--background-secondary); padding: 20px; border-radius: 10px;">
                        <h3>Tópicos Principais</h3>
                        ${results.topics ? results.topics.map((t: any) => `<div>• ${t}</div>`).join('') : '<div>Processando...</div>'}
                    </div>
                `}
                
                <div style="margin-top: 30px; text-align: center;">
                    <button onclick="navigator.clipboard.writeText('${JSON.stringify(results)}')">📋 Copiar Resultados</button>
                </div>
            </div>
        `;

        // Abre em nova aba
        const leaf = this.app.workspace.getLeaf('tab');
        const view = new DashboardView(leaf, html);
        leaf.open(view);
    }

    async ensureServerRunning() {
        if (this.serverRunning) return;

        new Notice('🚀 Iniciando servidor de análise...');
        
        // Aqui entraria a lógica real de iniciar o servidor
        // Por enquanto, simula
        this.serverRunning = true;
        
        // Agenda desligamento em 5 minutos
        setTimeout(() => {
            this.serverRunning = false;
            new Notice('💤 Servidor de análise pausado');
        }, 5 * 60 * 1000);
    }

    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }
}

// Modal de Boas-vindas
class WelcomeModal extends Modal {
    plugin: TranscriptAnalyzerPlugin;

    constructor(app: App, plugin: TranscriptAnalyzerPlugin) {
        super(app);
        this.plugin = plugin;
    }

    onOpen() {
        const { contentEl } = this;
        
        contentEl.createEl('h2', { text: '🎙️ Bem-vindo ao Transcript Analyzer!' });
        
        contentEl.createEl('p', { text: 'Este plugin oferece análise poderosa de transcrições.' });
        
        const featuresDiv = contentEl.createDiv();
        featuresDiv.createEl('h3', { text: '✅ Disponível Agora:' });
        featuresDiv.createEl('li', { text: 'Contagem de palavras e sentenças' });
        featuresDiv.createEl('li', { text: 'Análise básica de sentimento' });
        featuresDiv.createEl('li', { text: 'Tempo estimado de leitura' });
        
        const advancedDiv = contentEl.createDiv();
        advancedDiv.createEl('h3', { text: '🚀 Com Servidor Python (Opcional):' });
        advancedDiv.createEl('li', { text: 'Análise profunda de sentimentos' });
        advancedDiv.createEl('li', { text: 'Modelagem de tópicos (LDA)' });
        advancedDiv.createEl('li', { text: 'Redes semânticas' });
        advancedDiv.createEl('li', { text: 'Visualizações interativas' });
        
        const buttonDiv = contentEl.createDiv('modal-button-container');
        
        const installBtn = buttonDiv.createEl('button', {
            text: 'Instalar Servidor Avançado',
            cls: 'mod-cta'
        });
        installBtn.onclick = () => this.installServer();
        
        const skipBtn = buttonDiv.createEl('button', {
            text: 'Usar Versão Básica'
        });
        skipBtn.onclick = () => this.close();
    }

    async installServer() {
        const { contentEl } = this;
        contentEl.empty();
        
        contentEl.createEl('h3', { text: '📥 Instalando Servidor...' });
        
        const progressEl = contentEl.createEl('progress');
        progressEl.max = 100;
        progressEl.value = 0;
        
        // Simula download
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressEl.value = progress;
            
            if (progress >= 100) {
                clearInterval(interval);
                this.plugin.settings.serverInstalled = true;
                this.plugin.settings.serverPath = '/path/to/server';
                this.plugin.saveSettings();
                
                new Notice('✅ Servidor instalado com sucesso!');
                this.close();
            }
        }, 200);
    }
}

// View customizada para o Dashboard
class DashboardView {
    leaf: any;
    html: string;

    constructor(leaf: any, html: string) {
        this.leaf = leaf;
        this.html = html;
    }

    async open() {
        await this.leaf.setViewState({
            type: 'markdown',
            state: { mode: 'preview' }
        });

        // Injeta HTML customizado
        const view = this.leaf.view;
        if (view.previewMode) {
            view.previewMode.renderer.sizerEl.innerHTML = this.html;
        }
    }
}

// Settings Tab
class TranscriptAnalyzerSettingTab extends PluginSettingTab {
    plugin: TranscriptAnalyzerPlugin;

    constructor(app: App, plugin: TranscriptAnalyzerPlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display(): void {
        const { containerEl } = this;
        containerEl.empty();

        containerEl.createEl('h2', { text: 'Transcript Analyzer - Configurações' });

        // Status do servidor
        const statusDiv = containerEl.createDiv('setting-item');
        statusDiv.createEl('div', { 
            text: this.plugin.settings.serverInstalled ? 
                '✅ Servidor Python instalado' : 
                '❌ Servidor Python não instalado',
            cls: 'setting-item-info'
        });

        if (!this.plugin.settings.serverInstalled) {
            new Setting(containerEl)
                .setName('Instalar Servidor')
                .setDesc('Baixa e instala o servidor Python para análises avançadas')
                .addButton(button => button
                    .setButtonText('Instalar')
                    .setCta()
                    .onClick(() => {
                        new WelcomeModal(this.app, this.plugin).open();
                    }));
        }

        new Setting(containerEl)
            .setName('Auto-iniciar servidor')
            .setDesc('Inicia o servidor automaticamente quando necessário')
            .addToggle(toggle => toggle
                .setValue(this.plugin.settings.autoStartServer)
                .onChange(async (value) => {
                    this.plugin.settings.autoStartServer = value;
                    await this.plugin.saveSettings();
                }));
    }
}