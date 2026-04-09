//! Search functionality for the Rust search engine
//! 
//! This module provides search query handling for the ULRA system.

use crate::SearchResult;
use crate::SearchEngine;

/// Search handler for the Rust engine
pub struct SearchHandler {
    engine: SearchEngine,
}

impl SearchHandler {
    /// Create a new search handler
    pub fn new(engine: SearchEngine) -> Self {
        SearchHandler { engine }
    }

    /// Perform a search with a query string
    pub fn search(&self, query: &str) -> Vec<SearchResult> {
        self.engine.search(query)
    }

    /// Perform a search with additional parameters
    pub fn search_with_params(&self, query: &str, limit: usize) -> Vec<SearchResult> {
        let mut results = self.engine.search(query);
        results.truncate(limit);
        results
    }

    /// Search for documents with specific topic
    pub fn search_by_topic(&self, topic: &str) -> Vec<SearchResult> {
        // This would be more sophisticated in a real implementation
        // Currently just doing a general search for the topic
        self.engine.search(topic)
    }

    /// Get document details by ID
    pub fn get_document(&self, id: &str) -> Option<crate::Document> {
        self.engine.get_document(id).cloned()
    }

    /// Get search statistics
    pub fn get_stats(&self) -> SearchStats {
        SearchStats {
            total_documents: self.engine.documents.len(),
            total_terms: self.engine.inverted_index.len(),
        }
    }
}

/// Statistics about the search engine
#[derive(Debug, Clone)]
pub struct SearchStats {
    pub total_documents: usize,
    pub total_terms: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_search_handler_creation() {
        let engine = crate::SearchEngine::new();
        let handler = SearchHandler::new(engine);
        let stats = handler.get_stats();
        assert_eq!(stats.total_documents, 0);
        assert_eq!(stats.total_terms, 0);
    }

    #[test]
    fn test_search_functionality() {
        let mut engine = crate::SearchEngine::new();
        
        // Add a test document
        let doc = crate::Document {
            id: "test1".to_string(),
            title: "Test Document".to_string(),
            content: "This is a test document for searching".to_string(),
            metadata: std::collections::HashMap::new(),
        };
        
        engine.index_document(doc);
        let handler = SearchHandler::new(engine);
        let results = handler.search("test");
        
        assert!(!results.is_empty());
    }
}
