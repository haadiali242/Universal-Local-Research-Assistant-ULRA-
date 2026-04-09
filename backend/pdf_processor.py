"""
Extracts information from research papers
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, List
import fitz  # PyMuPDF
import os
import tempfile

router = APIRouter()

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file"""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")
    return text

def extract_metadata_from_pdf(file_path: str) -> Dict[str, any]:
    """Extract metadata from a PDF file"""
    try:
        doc = fitz.open(file_path)
        metadata = doc.metadata
        doc.close()
        
        # Extract key metadata fields
        return {
            "title": metadata.get("title", "Unknown"),
            "author": metadata.get("author", "Unknown"),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "creation_date": metadata.get("creationDate", ""),
            "mod_date": metadata.get("modDate", ""),
            "pages": fitz.open(file_path).page_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting metadata: {str(e)}")

@router.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    """Process an uploaded PDF file and extract information"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            # Write uploaded file to temporary file
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Extract metadata
        metadata = extract_metadata_from_pdf(tmp_file_path)
        
        # Extract text content
        text = extract_text_from_pdf(tmp_file_path)
        
        # Cleanup temporary file
        os.unlink(tmp_file_path)
        
        return {
            "metadata": metadata,
            "text": text[:1000] + "..." if len(text) > 1000 else text,
            "text_length": len(text)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract")
async def extract_info(file: UploadFile = File(...)):
    """Extract specific information from a PDF (title, authors, references)"""
    try:
        # This is a simplified version - in a full implementation this would:
        # 1. Extract title from PDF metadata or first page
        # 2. Extract author information
        # 3. Parse references/citations
        # 4. Extract key sections
        
        # For now, we'll just return basic metadata plus dummy results
        result = await process_pdf(file)
        
        return {
            "title": result["metadata"]["title"],
            "authors": [result["metadata"]["author"]] if result["metadata"]["author"] else [],
            "abstract": "Abstract would be extracted from first paragraph",
            "keywords": ["keyword1", "keyword2", "keyword3"],
            "references": ["Reference 1", "Reference 2", "Reference 3"],
            "sections": ["Introduction", "Methodology", "Results", "Conclusion"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
