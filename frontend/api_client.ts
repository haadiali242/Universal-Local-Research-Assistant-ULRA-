/**
 * API client for communicating with the ULRA backend
 */

interface Document {
    id: number;
    title: string;
    author: string;
    url: string;
    file_path: string;
    content: string;
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

export class APIClient {
    private baseUrl: string;
    
    constructor() {
        // In production, this would be configurable
        this.baseUrl = 'http://localhost:8000';
    }
    
    // Search functionality
    public async searchTopic(query: string): Promise<SearchResult> {
        try {
            const response = await fetch(`${this.baseUrl}/search/topic`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Search API error:', error);
            throw error;
        }
    }
    
    // Document management
    public async getDocuments(): Promise<Document[]> {
        try {
            const response = await fetch(`${this.baseUrl}/documents`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Documents API error:', error);
            throw error;
        }
    }
    
    public async getDocument(id: number): Promise<Document> {
        try {
            const response = await fetch(`${this.baseUrl}/documents/${id}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Document API error:', error);
            throw error;
        }
    }
    
    public async uploadPDF(file: File): Promise<any> {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`${this.baseUrl}/pdf/process`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Upload API error:', error);
            throw error;
        }
    }
    
    // Summarization
    public async getSummary(documentId: number): Promise<Summary> {
        try {
            const response = await fetch(`${this.baseUrl}/summarize/document`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    document_id: documentId 
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Summary API error:', error);
            throw error;
        }
    }
}
