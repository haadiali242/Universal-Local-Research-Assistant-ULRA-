//! Indexer for the Rust search engine
//! 
//! This module provides functionality for indexing documents stored on disk.

use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::io::Read;

use crate::Document;

/// Indexer for documents
pub struct Indexer {
    engine: crate::SearchEngine,
}

impl Indexer {
    /// Create a new indexer
    pub fn new(engine: crate::SearchEngine) -> Self {
        Indexer { engine }
    }

    /// Index a single file by reading its content
    pub fn index_file(&mut self, file_path: &str, title: &str) -> Result<(), Box<dyn std::error::Error>> {
        // Read the file content
        let content = fs::read_to_string(file_path)?;
        
        // Create a document
        let doc = Document {
            id: file_path.to_string(),
            title: title.to_string(),
            content,
            metadata: HashMap::new(),
        };
        
        // Add to search engine
        self.engine.index_document(doc);
        
        Ok(())
    }

    /// Index all PDF files in a directory
    pub fn index_directory(&mut self, dir_path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let path = Path::new(dir_path);
        
        if !path.exists() {
            return Err("Directory does not exist".into());
        }
        
        // Walk through directory
        for entry in fs::read_dir(path)? {
            let entry = entry?;
            let path = entry.path();
            
            if path.is_file() {
                // Check if it's a PDF file
                if let Some(extension) = path.extension() {
                    if extension == "pdf" {
                        let file_name = path.file_name().unwrap().to_string_lossy().to_string();
                        println!("Indexing PDF: {}", file_name);
                        self.index_file(&path.to_string_lossy(), &file_name)?;
                    }
                }
            }
        }
        
        Ok(())
    }

    /// Get the current number of indexed documents
    pub fn get_document_count(&self) -> usize {
        self.engine.documents.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::SearchEngine;

    #[test]
    fn test_indexer_creation() {
        let engine = SearchEngine::new();
        let indexer = Indexer::new(engine);
        assert_eq!(indexer.get_document_count(), 0);
    }
}
