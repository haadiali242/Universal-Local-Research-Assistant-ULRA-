"""
Handles the local knowledge base using SQLite
"""
import sqlite3
import os
from typing import List, Dict, Any
from contextlib import contextmanager

# Database file path
DB_PATH = "data/documents.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    """Initialize the database with required tables"""
    with get_db_connection() as conn:
        # Create documents table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                url TEXT,
                file_path TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create summaries table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                summary TEXT,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')
        
        # Create topics table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create document_topics table (many-to-many relationship)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS document_topics (
                document_id INTEGER,
                topic_id INTEGER,
                PRIMARY KEY (document_id, topic_id),
                FOREIGN KEY (document_id) REFERENCES documents (id),
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            )
        ''')
        
        # Create keywords table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create document_keywords table (many-to-many relationship)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS document_keywords (
                document_id INTEGER,
                keyword_id INTEGER,
                PRIMARY KEY (document_id, keyword_id),
                FOREIGN KEY (document_id) REFERENCES documents (id),
                FOREIGN KEY (keyword_id) REFERENCES keywords (id)
            )
        ''')
        
        conn.commit()

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    try:
        yield conn
    finally:
        conn.close()

def insert_document(document_data: Dict[str, Any]) -> int:
    """Insert a new document into the database"""
    with get_db_connection() as conn:
        cursor = conn.execute('''
            INSERT INTO documents (title, author, url, file_path, content)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            document_data.get('title'),
            document_data.get('author'),
            document_data.get('url'),
            document_data.get('file_path'),
            document_data.get('content')
        ))
        conn.commit()
        return cursor.lastrowid

def get_documents() -> List[Dict[str, Any]]:
    """Retrieve all documents from the database"""
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM documents ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]

def get_document_by_id(doc_id: int) -> Dict[str, Any]:
    """Retrieve a document by its ID"""
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM documents WHERE id = ?', (doc_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def insert_summary(summary_data: Dict[str, Any]) -> int:
    """Insert a new summary into the database"""
    with get_db_connection() as conn:
        cursor = conn.execute('''
            INSERT INTO summaries (document_id, summary, keywords)
            VALUES (?, ?, ?)
        ''', (
            summary_data.get('document_id'),
            summary_data.get('summary'),
            ','.join(summary_data.get('keywords', []))
        ))
        conn.commit()
        return cursor.lastrowid

def get_summary_by_document_id(doc_id: int) -> Dict[str, Any]:
    """Retrieve a summary by document ID"""
    with get_db_connection() as conn:
        cursor = conn.execute('''
            SELECT * FROM summaries WHERE document_id = ? ORDER BY created_at DESC LIMIT 1
        ''', (doc_id,))
        row = cursor.fetchone()
        if row:
            # Convert keywords from comma-separated string back to list
            summary_dict = dict(row)
            summary_dict['keywords'] = summary_dict['keywords'].split(',') if summary_dict['keywords'] else []
            return summary_dict
        return None

def add_topic(topic_name: str, description: str = None) -> int:
    """Add a new topic to the database"""
    with get_db_connection() as conn:
        cursor = conn.execute('''
            INSERT OR IGNORE INTO topics (name, description)
            VALUES (?, ?)
        ''', (topic_name, description))
        conn.commit()
        return cursor.lastrowid

def get_topics() -> List[Dict[str, Any]]:
    """Retrieve all topics from the database"""
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM topics ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]

def link_document_to_topic(doc_id: int, topic_id: int):
    """Link a document to a topic"""
    with get_db_connection() as conn:
        conn.execute('''
            INSERT OR IGNORE INTO document_topics (document_id, topic_id)
            VALUES (?, ?)
        ''', (doc_id, topic_id))
        conn.commit()

def add_keyword(keyword: str) -> int:
    """Add a keyword to the database"""
    with get_db_connection() as conn:
        cursor = conn.execute('''
            INSERT OR IGNORE INTO keywords (word)
            VALUES (?)
        ''', (keyword,))
        conn.commit()
        return cursor.lastrowid

def link_document_to_keyword(doc_id: int, keyword_id: int):
    """Link a document to a keyword"""
    with get_db_connection() as conn:
        conn.execute('''
            INSERT OR IGNORE INTO document_keywords (document_id, keyword_id)
            VALUES (?, ?)
        ''', (doc_id, keyword_id))
        conn.commit()
