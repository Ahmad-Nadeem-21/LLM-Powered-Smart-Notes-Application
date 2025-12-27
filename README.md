# Smart Notes App

An intelligent full-stack web application that automatically generates structured study notes from uploaded documents using AI. Upload PDF, DOCX, or TXT files and get beautifully formatted notes powered by local LLM technology.

![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20PostgreSQL%20%7C%20Ollama-blue)
![Python](https://img.shields.io/badge/Python-3.14+-green)
![React](https://img.shields.io/badge/React-18.3-blue)

## Features

- 📄 **Multi-format Support**: Upload and process PDF, DOCX, and TXT files
- 🤖 **AI-Powered Note Generation**: Generate structured study notes using local LLM (Ollama with Llama3)
- ⚡ **Smart Caching**: Database-backed caching for instant note retrieval
- 🎨 **Modern UI**: Beautiful, responsive React frontend with intuitive design
- 🔄 **Map-Reduce Processing**: Efficient handling of large documents through intelligent chunking
- 📊 **RESTful API**: Clean, well-documented API with automatic OpenAPI/Swagger documentation
- 💾 **PostgreSQL Integration**: Robust database storage for files and generated notes



## Tech Stack

### Frontend
- **React 18.3** - Modern UI library
- **Vite 6.0** - Fast build tool and dev server
- **CSS3** - Custom styling with modern design patterns

### Backend
- **FastAPI 0.127+** - High-performance Python web framework
- **Python 3.14+** - Modern Python features
- **Uvicorn** - ASGI server
- **uv** - Modern Python package manager

### Database
- **PostgreSQL** - Relational database for file and note storage
- **psycopg2** - PostgreSQL adapter

### AI/LLM
- **Ollama** - Local LLM server
- **Llama3** - Large language model for note generation

### File Processing
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX text extraction

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Node.js 18+** and **npm** (for frontend)
2. **Python 3.14+** (for backend)
3. **PostgreSQL** (running on port 5433)
4. **Ollama** (with Llama3 model)
5. **uv** package manager (optional but recommended)

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd "Notes App"
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
uv sync
# OR
pip install -r requirements.txt

# Create .env file
echo "DB_PASSWORD=your_postgres_password" > .env

# Start the server
uv run uvicorn app.app:app --reload
```

The backend will run on `http://localhost:8000`

**See [backend/README.md](backend/README.md) for detailed backend documentation.**

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173`

**See [frontend/README.md](frontend/README.md) for detailed frontend documentation.**

### 4. Ollama Setup

```bash
# Install Ollama from https://ollama.ai

# Start Ollama server
ollama serve

# Pull the Llama3 model
ollama pull llama3

# Verify installation
curl http://localhost:11434/api/tags
```

### 5. Database Setup

```sql
-- Create database
CREATE DATABASE notes_db;

-- The application will create tables automatically on startup
```

## Usage

1. **Start all services**:
   - PostgreSQL (port 5433)
   - Ollama server (port 11434)
   - Backend server (port 8000)
   - Frontend dev server (port 5173)

2. **Open the application**: Navigate to `http://localhost:5173`

3. **Upload a file**: 
   - Click "Choose a file" or drag & drop
   - Supported formats: PDF, DOCX, TXT
   - Click "Upload to server"

4. **Generate notes**:
   - Click "Generate notes"
   - Wait for AI processing (first request may take 30-60 seconds)
   - View your structured notes!

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload a file |
| `GET` | `/file/{file_id}` | Download a file |
| `PUT` | `/file/{file_id}` | Update a file |
| `DELETE` | `/file/{file_id}` | Delete a file |
| `POST` | `/notes/{file_id}` | Generate notes |

**Full API documentation**: `http://localhost:8000/docs` (Swagger UI)



## How It Works

### Document Processing Pipeline

1. **File Upload**: User uploads a document (PDF/DOCX/TXT)
2. **Text Extraction**: Backend extracts text using format-specific libraries
3. **Intelligent Processing**:
   - **Short texts** (< 500 chars): Direct single-pass generation
   - **Long texts**: Map-reduce pattern:
     - Split into 3000-character chunks
     - Summarize each chunk independently
     - Combine summaries into final structured notes
4. **Caching**: Notes are stored in PostgreSQL for instant retrieval
5. **Display**: Frontend renders formatted notes to the user

### Note Generation Flow

```
Upload File → Extract Text → Check Cache → [If not cached] → 
Chunk Text → Summarize Chunks → Combine Summaries → 
Generate Final Notes → Save to Database → Return to User
```

## Key Features Explained

### Smart Caching
- Notes are cached by `file_id` in the database
- Subsequent requests return instantly from cache
- Cache is automatically updated when notes are regenerated

### Map-Reduce Processing
- Large documents are split into manageable chunks
- Each chunk is processed independently
- Summaries are combined intelligently for final output

### Multi-Format Support
- **PDF**: Page-by-page extraction using `pdfplumber`
- **DOCX**: Paragraph extraction using `python-docx`
- **TXT**: Direct UTF-8 reading with error tolerance

## Troubleshooting

### Backend Issues
- **Database connection failed**: Check PostgreSQL is running and `.env` has correct password
- **Ollama timeout**: Ensure Ollama is running and `llama3` model is installed
- **Import errors**: Run `uv sync` to ensure all dependencies are installed

### Frontend Issues
- **CORS errors**: Ensure backend CORS is configured for your frontend URL
- **API connection failed**: Check backend is running on `http://localhost:8000`
- **Build errors**: Delete `node_modules` and run `npm install` again

### Ollama Issues
- **Model not found**: Run `ollama pull llama3`
- **Connection refused**: Start Ollama with `ollama serve`
- **Slow responses**: First request after restart takes 30-60 seconds (normal)

**See [backend/README.md](backend/README.md) for detailed troubleshooting.**

## Security Considerations

- **CORS**: Currently configured for localhost development. Update for production.
- **File Storage**: Files stored in `uploads/` directory. Consider size limits and validation.
- **Database**: Use strong passwords. Consider connection pooling for production.
- **Authentication**: Not currently implemented. Consider JWT/OAuth2 for production.

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Multi-user support with user-specific files
- [ ] File preview functionality
- [ ] Notes editing capabilities
- [ ] Export notes (PDF, DOCX, Markdown)
- [ ] Multiple LLM model support
- [ ] Streaming responses for long operations
- [ ] File size limits and validation
- [ ] Docker containerization
- [ ] Unit and integration tests
- [ ] Production deployment guides

## Environment Variables

### Backend (`.env` in `backend/` directory)
```env
DB_PASSWORD=your_postgres_password
```

### Frontend (optional `.env` in `frontend/` directory)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Development

### Running Tests
```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests (if configured)
cd frontend
npm test
```

### Code Formatting
```bash
# Backend
cd backend
uv run black app/
uv run ruff check app/

# Frontend
cd frontend
npm run lint
```

## Documentation

- [Backend README](backend/README.md) - Detailed backend documentation
- [Frontend README](frontend/README.md) - Frontend setup and usage
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when server is running)
