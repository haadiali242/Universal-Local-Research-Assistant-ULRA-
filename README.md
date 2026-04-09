# Universal Local Research Assistant (ULRA)

A desktop research assistant that runs locally on your computer and helps you find, organize, summarize, and manage research materials. This project demonstrates full-stack development with a multi-language architecture.

## Project Overview

The Universal Local Research Assistant is a local research management tool that helps researchers find, organize, and understand research materials. It can search topics, discover resources, extract metadata from PDFs, generate summaries, and build a searchable knowledge base.

## Architecture

The project uses a multi-language architecture:

- **Python Backend**: Main API server, scraping, summarization, and metadata extraction
- **Rust Engine**: Fast file indexing and local search engine
- **TypeScript Frontend**: Modern UI interface (React or Angular)

Communication happens through a local REST API.

## Features

- Topic search
- Automatic research material discovery
- PDF metadata extraction
- Automatic summaries
- Local document indexing
- Knowledge graph of topics
- Dashboard UI
- File management
- Offline mode
- Fast Rust search engine

## Project Structure

```
ulra/
│
├── backend/
│   ├── main.py              # Main API server using FastAPI
│   ├── search_api.py        # Search request handling
│   ├── summarizer.py        # Summary generation
│   ├── pdf_processor.py     # PDF metadata extraction
│   ├── web_scraper.py       # Online resource discovery
│   └── database.py          # Local SQLite database
│
├── rust_engine/
│   ├── main.rs              # Entry point and main search engine
│   ├── indexer.rs           # Document indexing functionality
│   └── search.rs            # Search query handling
│
├── frontend/
│   ├── app.ts               # Main entry point
│   ├── dashboard.ts         # Dashboard UI component
│   ├── api_client.ts        # API communication layer
│   └── styles.css           # UI styling
│
├── data/
│   └── documents.db         # SQLite database
│
└── README.md                # This file
```

## System Features

### Backend (Python)
- FastAPI server setup
- REST endpoints for search, PDF processing, and summarization
- SQLite database for local knowledge base
- Document and topic management
- Integration with search and indexing services

### Rust Engine
- Fast file indexing capabilities
- Full-text search engine
- Inverted index for efficient search
- Document retrieval and scoring

### Frontend (TypeScript)
- Modern UI dashboard
- Search interface
- Document listing
- Summary display
- Responsive design

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Rust (latest stable version)
- pip and npm

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Universal\ Local\ Research\ Assistant\ (ULRA)
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
cd frontend
npm install
```

4. Build Rust engine:
```bash
cd rust_engine
cargo build
```

### Running the Application

1. Start the Python backend:
```bash
cd backend
python main.py
```

2. Start the Rust engine (in a separate terminal):
```bash
cd rust_engine
cargo run
```

3. Start the frontend development server:
```bash
cd frontend
npm start
```

## API Endpoints

### Search API
- `POST /search/topic` - Search for research topics
- `GET /search/discover` - Discover additional resources

### PDF Processing
- `POST /pdf/process` - Process uploaded PDF files
- `POST /pdf/extract` - Extract metadata and information from PDFs

### Summarization
- `POST /summarize/document` - Generate document summaries
- `POST /summarize/text` - Summarize text content

### Documents
- `GET /documents` - Get all documents
- `GET /documents/{id}` - Get document by ID
- `GET /summary/{id}` - Get document summary

## Technologies Used

### Python Backend
- FastAPI for REST API
- PyMuPDF for PDF processing
- SQLite for the database
- BeautifulSoup for web scraping

### Rust Engine
- Actix-web or similar for HTTP server
- Efficient memory management and algorithms
- Fast search operations

### Frontend
- TypeScript for development
- Modern CSS (optional styling)
- Responsive UI components

## License

This project is available under the MIT License.

## Future Enhancements

- Advanced NLP for better summarization
- Machine learning for topic modeling
- More sophisticated document classification
- Collaboration features
- Cloud synchronization options
- Enhanced knowledge graph visualization
- Mobile application support

## Contributing

This project is part of a learning exercise and portfolio showcase. Contributions are welcome by following the standard GitHub fork, develop, and pull request workflow.

## Author

Haadi Ali - CrumWorld
