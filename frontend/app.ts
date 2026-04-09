/**
 * Main entry point for the Universal Local Research Assistant frontend
 */

import { Dashboard } from './dashboard';
import { APIClient } from './api_client';

class App {
    private dashboard: Dashboard;
    private apiClient: APIClient;
    
    constructor() {
        this.apiClient = new APIClient();
        this.dashboard = new Dashboard(this.apiClient);
        this.init();
    }
    
    private init(): void {
        console.log('Initializing Universal Local Research Assistant...');
        
        // Initialize dashboard components
        this.dashboard.render();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Load initial data
        this.loadInitialData();
    }
    
    private setupEventListeners(): void {
        // Search form submission
        const searchForm = document.getElementById('search-form') as HTMLFormElement;
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => this.handleSearch(e));
        }
        
        // Document upload
        const uploadButton = document.getElementById('upload-button') as HTMLButtonElement;
        if (uploadButton) {
            uploadButton.addEventListener('click', () => this.handleUpload());
        }
    }
    
    private async handleSearch(e: Event): Promise<void> {
        e.preventDefault();
        const queryInput = document.getElementById('search-input') as HTMLInputElement;
        const query = queryInput.value.trim();
        
        if (!query) {
            alert('Please enter a search query');
            return;
        }
        
        try {
            const results = await this.apiClient.searchTopic(query);
            this.dashboard.updateSearchResults(results);
        } catch (error) {
            console.error('Search error:', error);
            alert('Error searching topics');
        }
    }
    
    private async handleUpload(): Promise<void> {
        // In a real implementation, this would open a file dialog
        // and upload the selected PDF file
        alert('PDF upload functionality would go here. In a real implementation, this would upload PDF files to the backend.');
    }
    
    private async loadInitialData(): Promise<void> {
        // Load recent documents
        try {
            const documents = await this.apiClient.getDocuments();
            this.dashboard.updateDocuments(documents);
        } catch (error) {
            console.error('Failed to load documents:', error);
        }
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new App();
});
