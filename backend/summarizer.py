"""
Generates summaries of long documents
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
import re

router = APIRouter()

def extract_keywords(text: str, num_keywords: int = 10) -> List[str]:
    """Extract keywords from text (simplified implementation)"""
    # Simple keyword extraction - in a real implementation, this would be more sophisticated
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = {}
    for word in words:
        if len(word) > 3:  # Ignore short words
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:num_keywords]]

def simple_summarize(text: str, num_sentences: int = 3) -> Dict[str, any]:
    """Create a simple summary using sentence ranking"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Simple sentence splitting
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # For simplicity, we'll return first few sentences as summary
    summary_sentences = sentences[:num_sentences]
    summary = ' '.join(summary_sentences)
    
    # Extract keywords
    keywords = extract_keywords(text)
    
    return {
        "summary": summary,
        "keywords": keywords[:10],
        "sentence_count": len(sentences)
    }

@router.post("/document")
async def summarize_document(text: str):
    """Generate a summary for a document"""
    try:
        if not text:
            raise HTTPException(status_code=400, detail="No text provided for summarization")
        
        # Create a simple summary
        summary = simple_summarize(text)
        
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text")
async def summarize_text(text: str, num_sentences: int = 3):
    """Generate summary for provided text"""
    try:
        if not text:
            raise HTTPException(status_code=400, detail="No text provided for summarization")
        
        # Simple text summarization
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Get first few sentences as summary
        summary_sentences = sentences[:num_sentences]
        summary = ' '.join(summary_sentences)
        
        # Extract keywords
        keywords = extract_keywords(text, 10)
        
        return {
            "summary": summary,
            "keywords": keywords,
            "sentence_count": len(sentences)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
