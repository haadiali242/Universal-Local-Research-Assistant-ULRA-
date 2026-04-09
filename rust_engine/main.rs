//! Rust search engine for Universal Local Research Assistant
//! 
//! This module provides fast indexing and search capabilities for the ULRA system.

mod indexer;
mod search;

use std::collections::HashMap;
use std::fs;
use std::path::Path;

// Basic document structure
#[derive(Debug, Clone)]
pub struct Document {
    pub id: String,
    pub title: String,
    pub content: String,
    pub metadata: HashMap<String, String>,
}

// Search result structure
#[derive(Debug, Clone)]
pub struct SearchResult {
    pub document_id: String,
    pub title: String,
    pub score: f32,
    pub excerpt: String,
}

// Main search engine struct
pub struct SearchEngine {
    documents: HashMap<String, Document>,
    inverted_index: HashMap<String, Vec<String>>,
}

impl SearchEngine {
    /// Create a new search engine instance
    pub fn new() -> Self {
        SearchEngine {
            documents: HashMap::new(),
            inverted_index: HashMap::new(),
        }
    }

    /// Index a document
    pub fn index_document(&mut self, document: Document) {
        let doc_id = document.id.clone();
        let mut terms = Vec::new();
        
        // Tokenize and index content
        let content = document.content.to_lowercase();
        for term in content.split_whitespace() {
            // Simple tokenization - remove punctuation
            let clean_term = term.trim_matches(|c| !c.is_alphanumeric());
            if !clean_term.is_empty() {
                terms.push(clean_term.to_string());
                self.inverted_index
                    .entry(clean_term.to_string())
                    .or_insert_with(Vec::new)
                    .push(doc_id.clone());
            }
        }
        
        // Store the document
        self.documents.insert(doc_id, document);
    }

    /// Perform a search query
    pub fn search(&self, query: &str) -> Vec<SearchResult> {
        let mut query_terms = Vec::new();
        
        // Tokenize query
        for term in query.to_lowercase().split_whitespace() {
            let clean_term = term.trim_matches(|c| !c.is_alphanumeric());
            if !clean_term.is_empty() {
                query_terms.push(clean_term.to_string());
            }
        }
        
        // Find documents that contain all query terms
        let mut term_document_scores: HashMap<String, f32> = HashMap::new();
        
        for term in &query_terms {
            if let Some(doc_ids) = self.inverted_index.get(term) {
                for doc_id in doc_ids {
                    *term_document_scores.entry(doc_id.clone()).or_insert(0.0) += 1.0;
                }
            }
        }
        
        // Calculate final scores and prepare results
        let mut results: Vec<SearchResult> = term_document_scores
            .into_iter()
            .filter(|(_, score)| *score > 0.0)
            .map(|(doc_id, score)| {
                // Get the document
                if let Some(doc) = self.documents.get(&doc_id) {
                    // Create excerpt from the document content
                    let excerpt_length = 150;
                    let excerpt = if doc.content.len() > excerpt_length {
                        format!("{}...", &doc.content[..excerpt_length])
                    } else {
                        doc.content.clone()
                    };
                    
                    SearchResult {
                        document_id: doc_id,
                        title: doc.title.clone(),
                        score,
                        excerpt,
                    }
                } else {
                    SearchResult {
                        document_id: doc_id,
                        title: "Unknown".to_string(),
                        score,
                        excerpt: "Content not available".to_string(),
                    }
                }
            })
            .collect();
            
        // Sort by score (descending)
        results.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap());
        
        results
    }
    
    /// Get a document by ID
    pub fn get_document(&self, id: &str) -> Option<&Document> {
        self.documents.get(id)
    }
    
    /// Get total number of documents
    pub fn document_count(&self) -> usize {
        self.documents.len()
    }
}

/// Test function to demonstrate basic functionality
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_search_engine_creation() {
        let engine = SearchEngine::new();
        assert!(engine.documents.is_empty());
        assert!(engine.inverted_index.is_empty());
    }

    #[test]
    fn test_document_indexing() {
        let mut engine = SearchEngine::new();
        let doc = Document {
            id: "test1".to_string(),
            title: "Test Document".to_string(),
            content: "This is a test document for indexing".to_string(),
            metadata: HashMap::new(),
        };
        
        engine.index_document(doc);
        assert_eq!(engine.documents.len(), 1);
        assert!(!engine.inverted_index.is_empty());
    }
}

// Example usage
fn main() {
    println!("Universal Local Research Assistant - Rust Engine");
    println!("Starting search engine...");
    
    // You would start the actual search engine service here
    // This might involve:
    // 1. Starting a local server 
    // 2. Listening for indexing requests
    // 3. Listening for search queries
    // 4. Communicating with the Python backend
    
    let mut engine = SearchEngine::new();
    
    // Add some test documents
    let doc1 = Document {
        id: "1".to_string(),
        title: "Climate Change Impact".to_string(),
        content: "Research on how climate change affects agriculture and environment".to_string(),
        metadata: HashMap::new(),
    };
    
    let doc2 = Document {
        id: "2".to_string(),
        title: "Agricultural Sustainability".to_string(),
        content: "Sustainable farming practices and their impact on climate change".to_string(),
        metadata: HashMap::new(),
    };
    
    engine.index_document(doc1);
    engine.index_document(doc2);
    
    // Perform a search
    let results = engine.search("climate change");
    println!("Search results for 'climate change':");
    for result in results {
        println!("- {} (score: {})", result.title, result.score);
    }
}
