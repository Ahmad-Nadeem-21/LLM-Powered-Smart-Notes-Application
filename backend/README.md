# Smart Notes App - Backend

A FastAPI-based REST API backend for an intelligent document processing and note generation application. This backend handles file uploads, text extraction from multiple formats (PDF, DOCX, TXT), and AI-powered note generation using local LLM integration via Ollama.

## 🚀 Features

- **Multi-format File Support**: Upload and process PDF, DOCX, and TXT files
- **Intelligent Text Extraction**: Automatic text extraction from various document formats
- **AI-Powered Note Generation**: Generate structured study notes using local LLM (Ollama with Llama3)
- **Smart Caching**: Database-backed caching to avoid redundant LLM processing
- **RESTful API**: Clean, well-documented REST endpoints with automatic OpenAPI/Swagger docs
- **PostgreSQL Integration**: Robust database storage for files and generated notes
- **Map-Reduce Processing**: Efficient handling of large documents through chunking and summarization

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.127+
- **Python**: 3.14+
- **Database**: PostgreSQL (with psycopg2)
- **AI/LLM**: Ollama (local LLM server with Llama3 model)
- **File Processing**: 
  - `pdfplumber` for PDF extraction
  - `python-docx` for DOCX extraction
- **Package Manager**: `uv` (modern Python package manager)
- **Server**: Uvicorn (ASGI server)

## 📋 Prerequisites

Before running the backend, ensure you have:

1. **Python 3.14+** installed
2. **PostgreSQL** running (default port: 5433)
   - Database name: `notes_db`
   - User: `postgres`
3. **Ollama** installed and running
   - Model: `llama3` (must be pulled: `ollama pull llama3`)
   - Running on `http://localhost:11434`
4. **uv** package manager (install via: `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## 🔧 Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd "Notes App/backend"
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```
   
   This will:
   - Create a virtual environment
   - Install all dependencies from `pyproject.toml`
   - Generate a lock file (`uv.lock`)

3. **Alternative: Install using pip** (if not using uv):
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create a `.env` file** in the `backend` directory:
   ```env
   DB_PASSWORD=your_postgres_password
   ```

2. **Database Configuration** (in `app/database.py`):
   - Default database: `notes_db`
   - Default host: `localhost`
   - Default port: `5433`
   - Default user: `postgres`
   - Password: From `.env` file

3. **Ollama Configuration** (in `app/LLM_Integration.py`):
   - Default URL: `http://localhost:11434/api/chat`
   - Default model: `llama3`
   - Request timeout: 120 seconds

## 🏃 Running the Server

### Development Mode (with auto-reload):

```bash
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode:

```bash
uv run uvicorn app.app:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### API Documentation

Once the server is running, access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check endpoint |
| `POST` | `/upload` | Upload a file (PDF, DOCX, or TXT) |
| `GET` | `/file/{file_id}` | Download an uploaded file |
| `PUT` | `/file/{file_id}` | Update/replace an uploaded file |
| `DELETE` | `/file/{file_id}` | Delete an uploaded file |
| `POST` | `/notes/{file_id}` | Generate AI-powered notes from a file |

### Example Requests

**Upload a file:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

**Generate notes:**
```bash
curl -X POST "http://localhost:8000/notes/{file_id}"
```

## 🗄️ Database Setup

The application automatically creates the necessary tables on startup:

### Tables

1. **files**
   - `id` (SERIAL PRIMARY KEY)
   - `file_id` (VARCHAR, UNIQUE) - UUID-based file identifier
   - `filename` (VARCHAR) - Original filename
   - `upload_time` (TIMESTAMP) - Auto-generated upload timestamp

2. **notes**
   - `id` (SERIAL PRIMARY KEY)
   - `file_id` (VARCHAR, UNIQUE, FOREIGN KEY) - References files.file_id
   - `content` (TEXT) - Generated notes content
   - `model` (VARCHAR) - LLM model used (e.g., "llama3")
   - `created_at` (TIMESTAMP) - Auto-generated creation timestamp

### Manual Database Creation

If you need to create the database manually:

```sql
CREATE DATABASE notes_db;
```

The application will create tables automatically on first startup.

## 🤖 Ollama Setup

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)

2. **Start Ollama server**:
   ```bash
   ollama serve
   ```

3. **Pull the Llama3 model**:
   ```bash
   ollama pull llama3
   ```

4. **Verify installation**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

   You should see `llama3` in the models list.

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── app.py               # FastAPI application and routes
│   ├── database.py           # PostgreSQL connection and queries
│   ├── LLM_Integration.py   # Ollama client and note generation
│   ├── schemas.py            # Pydantic models
│   └── text_extracting.py    # File text extraction functions
├── uploads/                  # File storage directory (auto-created)
├── main.py                   # Application entry point
├── pyproject.toml            # Project dependencies (uv format)
├── requirements.txt          # Alternative dependency list
├── uv.lock                   # Dependency lock file
├── .env                      # Environment variables (create this)
└── README.md                 # This file
```

## 🔍 Key Features Explained

### Text Extraction
- **PDF**: Uses `pdfplumber` for page-by-page text extraction
- **DOCX**: Uses `python-docx` for paragraph extraction
- **TXT**: Direct UTF-8 text reading with error tolerance

### Note Generation
- **Short texts (< 500 chars)**: Direct single-pass generation
- **Long texts**: Map-reduce pattern:
  1. Split into 3000-character chunks
  2. Summarize each chunk independently
  3. Combine summaries into final structured notes

### Caching
- Notes are cached in the database by `file_id`
- Subsequent requests for the same file return cached notes instantly
- Cache is automatically updated when notes are regenerated

## 🐛 Troubleshooting

### Ollama Connection Issues
- **Error**: "Cannot connect to Ollama"
  - **Solution**: Ensure Ollama is running: `ollama serve`
  - Check if port 11434 is accessible: `curl http://localhost:11434/api/tags`

### Database Connection Issues
- **Error**: "Connection refused" or "Authentication failed"
  - **Solution**: Verify PostgreSQL is running and credentials in `.env` are correct
  - Check database exists: `psql -U postgres -l`

### Model Loading Slow
- **First request** after Ollama restart can take 30-60 seconds (model loading)
- This is normal behavior - subsequent requests will be faster

### Timeout Errors
- **Error**: "Ollama request timed out"
  - **Solution**: Increase `REQUEST_TIMEOUT` in `app/LLM_Integration.py`
  - Check system resources (CPU/RAM) - Ollama may be overloaded

## 🧪 Development

### Running Tests
```bash
uv run pytest
```

### Code Formatting
```bash
# Using black (if installed)
uv run black app/

# Using ruff (if installed)
uv run ruff check app/
```

### Adding New Dependencies
```bash
# Using uv (recommended)
uv add package-name

# Or manually edit pyproject.toml, then:
uv sync
```

## 📝 Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database
DB_PASSWORD=your_postgres_password

# Optional: Override defaults
# DB_HOST=localhost
# DB_PORT=5433
# DB_NAME=notes_db
# DB_USER=postgres
```

## 🔒 Security Notes

- **CORS**: Currently configured for localhost development. Update `allow_origins` in `app.py` for production.
- **File Storage**: Files are stored in `uploads/` directory. Consider implementing file size limits and validation.
- **Database**: Use strong passwords and consider connection pooling for production.
- **Authentication**: Currently not implemented. Consider adding JWT or OAuth2 for production use.



**Note**: This backend is designed to work with the React frontend. Make sure the frontend is configured to point to `http://localhost:8000` (or your backend URL).

