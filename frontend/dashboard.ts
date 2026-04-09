/**
 * Dashboard component for the Universal Local Research Assistant
 */

import { APIClient } from './api_client';

interface Document {
    id: number;
    title: string;
    author: string;
    url: string;
    file_path: string;
    created_at: string;
}

interface SearchResult {
    query: string;
    results: any[];
    total_results: number;
}

interface Summary {
    summary: string;
    keywords: string[];
}

export class Dashboard {
    private apiClient: APIClient;
    private searchResults: any[] = [];
    private documents: Document[] = [];
    
    constructor(apiClient: APIClient) {
        this.apiClient = apiClient;
        this.init();
    }
    
    private init(): void {
        console.log('Dashboard initialized');
    }
    
    public render(): void {
        const appContainer = document.getElementById('app') || document.body;
        
        appContainer.innerHTML = `
            <div class="dashboard">
                <header class="dashboard-header">
                    <h1>Universal Local Research Assistant</h1>
                    <p>Search, organize, and manage research materials locally</p>
                </header>
                
                <main class="dashboard-main">
                    <!-- Search Section -->
                    <section class="search-section">
                        <h2>Search Research Topic</h2>
                        <form id="search-form">
                            <input type="text" id="search-input" placeholder="Enter topic to search..." required>
                            <button type="submit">Search</button>
                        </form>
                    </section>
                    
                    <!-- Documents Section -->
                    <section class="documents-section">
                        <h2>Documents Found</h2>
                        <div id="documents-list" class="documents-list">
                            <div class="loading">Loading documents...</div>
                        </div>
                    </section>
                    
                    <!-- Search Results Section -->
                    <section class="search-results-section">
                        <h2>Search Results</h2>
                        <div id="search-results" class="search-results">
                            <div class="no-results">No search results yet. Try searching above.</div>
                        </div>
                    </section>
                    
                    <!-- Knowledge Graph Section -->
                    <section class="knowledge-graph-section">
                        <h2>Knowledge Graph of Topics</h2>
                        <div id="knowledge-graph" class="knowledge-graph">
                            <div class="placeholder">Knowledge graph visualization would appear here</div>
                        </div>
                    </section>
                </main>
                
                <footer class="dashboard-footer">
                    <p>Universal Local Research Assistant v1.0</p>
                </footer>
            </div>
        `;
        
        // Add styles
        this.addStyles();
    }
    
    private addStyles(): void {
        const style = document.createElement('style');
        style.textContent = `
            .dashboard {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f5f5;
                min-height: 100vh;
            }
            
            .dashboard-header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background-color: #2c3e50;
                color: white;
                border-radius: 8px;
            }
            
            .dashboard-main {
                display: flex;
                flex-direction: column;
                gap: 30px;
            }
            
            .search-section {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .search-section h2 {
                margin-top: 0;
                color: #2c3e50;
            }
            
            #search-form {
                display: flex;
                gap: 10px;
            }
            
            #search-input {
                flex: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
            }
            
            button {
                padding: 12px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            
            button:hover {
                background-color: #2980b9;
            }
            
            .documents-section, .search-results-section, .knowledge-graph-section {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .documents-section h2, .search-results-section h2, .knowledge-graph-section h2 {
                margin-top: 0;
                color: #2c3e50;
            }
            
            .documents-list {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }
            
            .document-card {
                border: 1px solid #eee;
                border-radius: 8px;
                padding: 15px;
                background-color: #f9f9f9;
            }
            
            .document-card h3 {
                margin-top: 0;
                color: #3498db;
            }
            
            .document-card p {
                margin: 5px 0;
                font-size: 14px;
            }
            
            .search-results {
                margin-top: 15px;
            }
            
            .search-result {
                border: 1px solid #eee;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                background-color: #f9f9f9;
            }
            
            .search-result h3 {
                margin-top: 0;
                color: #2c3e50;
            }
            
            .search-result .excerpt {
                color: #666;
                font-size: 14px;
            }
            
            .knowledge-graph {
                height: 300px;
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: #f0f0f0;
                border-radius: 8px;
            }
            
            .placeholder {
                color: #999;
                text-align: center;
            }
            
            .loading, .no-results {
                text-align: center;
                padding: 20px;
                color: #999;
            }
            
            .dashboard-footer {
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                color: #7f8c8d;
                font-size: 14px;
            }
        `;
        document.head.appendChild(style);
    }
    
    public updateDocuments(documents: Document[]): void {
        this.documents = documents;
        const documentsList = document.getElementById('documents-list');
        
        if (!documentsList) return;
        
        if (documents.length === 0) {
            documentsList.innerHTML = '<div class="no-results">No documents found.</div>';
            return;
        }
        
        documentsList.innerHTML = documents.map(doc => `
            <div class="document-card">
                <h3>${doc.title}</h3>
                <p><strong>Author:</strong> ${doc.author || 'Unknown'}</p>
                <p><strong>Created:</strong> ${doc.created_at}</p>
                <p><strong>File:</strong> ${doc.file_path || 'N/A'}</p>
            </div>
        `).join('');
    }
    
    public updateSearchResults(results: SearchResult): void {
        const searchResults = document.getElementById('search-results');
        
        if (!searchResults) return;
        
        if (!results || results.results.length === 0) {
            searchResults.innerHTML = '<div class="no-results">No search results found.</div>';
            return;
        }
        
        searchResults.innerHTML = results.results.map(result => `
            <div class="search-result">
                <h3>${result.title}</h3>
                <p class="excerpt">${result.excerpt}</p>
                <p><strong>Type:</strong> ${result.type || 'Article'}</p>
                <a href="${result.url}" target="_blank">View Source</a>
            </div>
        `).join('');
    }
}
