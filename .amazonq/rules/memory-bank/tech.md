# Open WebUI - Technology Stack

## Programming Languages

### Backend
- **Python 3.11-3.12**: Primary backend language
  - Required: `>= 3.11, < 3.13.0a1`
  - Recommended: Python 3.11 for pip installation

### Frontend
- **TypeScript/JavaScript**: Frontend development
  - TypeScript 5.5.4+
  - ES Modules (type: "module")
- **Svelte 4.2.18**: UI framework
- **HTML/CSS**: Markup and styling

### Scripting
- **Bash**: Shell scripts for automation
- **Node.js**: Build tooling and scripts
  - Required: `>=18.13.0 <=22.x.x`
  - npm: `>=6.0.0`

## Core Frameworks & Libraries

### Backend Stack
- **FastAPI 0.115.7**: Modern async web framework
- **Uvicorn 0.34.2**: ASGI server with standard extras
- **Pydantic 2.10.6**: Data validation and settings management
- **SQLAlchemy 2.0.38**: SQL toolkit and ORM
- **Alembic 1.14.0**: Database migration tool
- **Peewee 3.18.1**: Alternative lightweight ORM
- **Python-SocketIO 5.13.0**: WebSocket communication
- **Starlette-Compress 1.6.0**: Response compression middleware

### Frontend Stack
- **SvelteKit 2.5.20+**: Full-stack Svelte framework
- **Vite 5.4.14+**: Build tool and dev server
- **Tailwind CSS 4.0.0**: Utility-first CSS framework
- **Socket.IO Client 4.2.0**: Real-time bidirectional communication
- **Pyodide 0.27.3**: Python runtime in WebAssembly

## AI & Machine Learning

### LLM Integration
- **OpenAI**: OpenAI API client
- **Anthropic**: Claude API integration
- **Google GenAI 1.15.0**: Google AI services
- **Google Generative AI 0.8.5**: Gemini integration
- **Tiktoken**: Token counting for OpenAI models

### RAG & Vector Databases
- **LangChain 0.3.24**: LLM application framework
- **LangChain Community 0.3.23**: Community integrations
- **ChromaDB 0.6.3**: Vector database
- **Milvus 2.5.0**: Vector database (pymilvus)
- **Qdrant Client 1.12.0**: Vector search engine
- **OpenSearch 2.8.0**: Search and analytics
- **Elasticsearch 9.0.1**: Search engine
- **Pinecone 6.0.2**: Vector database service

### ML Models & Processing
- **Transformers**: Hugging Face transformers library
- **Sentence-Transformers 4.1.0**: Sentence embeddings
- **Accelerate**: PyTorch training acceleration
- **ColBERT-AI 0.2.21**: Neural search
- **ONNX Runtime 1.20.1**: ML inference
- **Faster-Whisper 1.1.1**: Speech recognition

## Database Support

### SQL Databases
- **PostgreSQL**: Via psycopg2-binary 2.9.9 + pgvector 0.4.0
- **MySQL**: Via PyMySQL 1.1.1
- **SQLite**: Built-in support

### NoSQL Databases
- **MongoDB**: Via pymongo
- **Redis**: Caching and session storage

### Cloud Storage
- **AWS S3**: Via boto3 1.35.53
- **Google Cloud Storage 2.19.0**: GCS integration
- **Azure Blob Storage 12.24.1**: Azure storage

## Document Processing

### File Format Support
- **PDF**: pypdf 4.3.1, fpdf2 2.8.2
- **Word**: docx2txt 0.8
- **PowerPoint**: python-pptx 1.0.2
- **Excel**: pandas 2.2.3, openpyxl 3.1.5, pyxlsb 1.0.10, xlrd 2.0.1
- **Markdown**: Markdown 3.7, pymdown-extensions 10.14.2
- **Pandoc**: pypandoc 1.15
- **Unstructured 0.16.17**: Universal document loader

### Text & NLP
- **NLTK 3.9.1**: Natural language processing
- **SentencePiece**: Text tokenization
- **FTFY 6.2.3**: Text fixing

### Image Processing
- **Pillow 11.2.1**: Image manipulation
- **OpenCV 4.11.0.86**: Computer vision (headless)
- **RapidOCR 1.4.4**: OCR capabilities
- **Azure Document Intelligence 1.0.2**: Document analysis

## Frontend Libraries

### UI Components & Styling
- **Bits-UI 0.21.15**: Headless UI components
- **Paneforge 0.0.6**: Resizable panes
- **Svelte-Sonner 0.3.19**: Toast notifications
- **Svelte-Confetti 1.3.2**: Confetti effects
- **Tippy.js 6.3.7**: Tooltips and popovers
- **Focus-Trap 7.6.4**: Keyboard navigation

### Rich Text Editing
- **TipTap 2.11.9**: Rich text editor
- **CodeMirror 6.0.1**: Code editor
- **ProseMirror**: Document editing framework

### Data Visualization & Flow
- **XYFlow Svelte 0.1.19**: Node-based diagrams
- **Mermaid 11.6.0**: Diagram generation
- **Panzoom 9.4.3**: Pan and zoom functionality

### Content Processing
- **Marked 9.1.0**: Markdown parser
- **KaTeX 0.16.22**: LaTeX math rendering
- **Highlight.js 11.9.0**: Syntax highlighting
- **DOMPurify 3.2.5**: HTML sanitization
- **Turndown 7.2.0**: HTML to Markdown conversion

### Utilities
- **Day.js 1.11.10**: Date manipulation
- **Fuse.js 7.0.0**: Fuzzy search
- **UUID 9.0.1**: UUID generation
- **File-Saver 2.0.5**: File downloads
- **HTML2Canvas Pro 1.5.8**: Screenshot generation
- **jsPDF 3.0.0**: PDF generation
- **YAML 2.7.1**: YAML parsing

### Internationalization
- **i18next 23.10.0**: i18n framework
- **i18next-browser-languagedetector 7.2.0**: Language detection
- **i18next-resources-to-backend 1.2.0**: Dynamic resource loading

### AI in Browser
- **Hugging Face Transformers 3.0.0**: ML models in browser
- **MediaPipe Tasks Vision 0.10.17**: Vision tasks
- **PyScript Core 0.4.32**: Python in browser

## Authentication & Security

### Auth Libraries
- **Python-JOSE 3.4.0**: JWT handling
- **PyJWT 2.10.1**: JWT with crypto support
- **Passlib 1.7.4**: Password hashing (bcrypt)
- **Bcrypt 4.3.0**: Password hashing
- **Argon2-CFFI 23.1.0**: Argon2 password hashing
- **Authlib 1.4.1**: OAuth/OIDC client

### Identity Providers
- **Azure MSAL Browser 4.5.0**: Microsoft authentication
- **LDAP3 2.9.1**: LDAP authentication
- **Azure Identity 1.20.0**: Azure authentication

### Security
- **RestrictedPython 8.0**: Sandboxed Python execution
- **Validators 0.35.0**: Data validation

## Development Tools

### Code Quality
- **Black 25.1.0**: Python code formatter
- **Pylint**: Python linter
- **ESLint 8.56.0**: JavaScript/TypeScript linter
- **Prettier 3.3.3**: Code formatter
- **Svelte-Check 3.8.5**: Svelte type checking

### Testing
- **Pytest 8.3.2**: Python testing framework
- **Pytest-Docker 3.1.1**: Docker fixtures for tests
- **Cypress 13.15.0**: E2E testing
- **Vitest 1.6.1**: Unit testing for Vite

### Build Tools
- **Hatchling**: Python build backend
- **Vite 5.4.14**: Frontend build tool
- **PostCSS 8.4.31**: CSS processing
- **Sass-Embedded 1.81.0**: Sass compilation
- **i18next-Parser 9.0.1**: i18n extraction

## Monitoring & Observability

### Tracing & Monitoring
- **Langfuse 2.44.0**: LLM observability
- **OpenTelemetry**: Distributed tracing
  - API 1.32.1
  - SDK 1.32.1
  - OTLP Exporter 1.32.1
  - Instrumentation for FastAPI, SQLAlchemy, Redis, Requests, HTTPX, AIOHTTP

### Logging
- **Loguru 0.7.3**: Python logging

## Task Scheduling
- **APScheduler 3.10.4**: Background task scheduling

## Web Scraping & Search
- **Playwright 1.49.1**: Browser automation
- **DuckDuckGo Search 8.0.2**: Web search
- **Firecrawl 1.12.0**: Web scraping
- **YouTube Transcript API 1.1.0**: YouTube transcripts
- **PyTube 15.0.0**: YouTube video downloads
- **Fake-UserAgent 2.1.0**: User agent spoofing

## Audio Processing
- **PyDub**: Audio manipulation
- **SoundFile 0.13.1**: Audio file I/O
- **Kokoro-JS 1.1.1**: Audio processing

## Containerization & Orchestration
- **Docker 7.1.0**: Container management
- **Docker Compose**: Multi-container orchestration
- **Kubernetes**: Production orchestration (Helm, Kustomize)

## Development Commands

### Frontend
```bash
npm run dev              # Start dev server
npm run build            # Production build
npm run preview          # Preview production build
npm run check            # Type checking
npm run lint             # Run all linters
npm run format           # Format code
npm run test:frontend    # Run frontend tests
npm run cy:open          # Open Cypress
```

### Backend
```bash
pip install open-webui   # Install package
open-webui serve         # Start server
python -m pytest         # Run tests
black .                  # Format code
pylint backend/          # Lint code
```

### Docker
```bash
docker compose up -d     # Start services
docker compose down      # Stop services
docker compose logs      # View logs
```

## Environment Variables
Key configuration via environment variables:
- `OLLAMA_BASE_URL`: Ollama server URL
- `OPENAI_API_KEY`: OpenAI API key
- `HF_HUB_OFFLINE`: Offline mode flag
- Database connection strings
- Storage configuration
- Authentication settings

## Package Managers
- **npm**: Frontend dependencies
- **pip**: Python packages
- **uv**: Fast Python package installer (uv.lock present)
