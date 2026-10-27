# OASIS - Project Structure

## Architecture Overview
OASIS follows a full-stack architecture with a Python FastAPI backend and a Svelte/SvelteKit frontend. The project is designed as a monorepo containing both frontend and backend code with clear separation of concerns.

## Directory Structure

### Root Level
```
oasis/
├── backend/           # Python FastAPI backend application
├── src/              # Svelte frontend application
├── static/           # Static assets (images, fonts, themes)
├── cypress/          # End-to-end testing
├── kubernetes/       # K8s deployment manifests (helm, kustomize)
├── scripts/          # Build and utility scripts
├── docs/             # Documentation files
└── test/             # Test files and fixtures
```

### Backend (`/backend/`)
Python-based FastAPI application handling API, database, and business logic.

```
backend/
├── oasis/
│   ├── routers/          # API route handlers (REST endpoints)
│   ├── models/           # Database models (SQLAlchemy/Peewee)
│   ├── utils/            # Utility functions and helpers
│   ├── socket/           # WebSocket/Socket.IO handlers
│   ├── retrieval/        # RAG and document retrieval logic
│   ├── internal/         # Internal services and helpers
│   ├── migrations/       # Database migration scripts (Alembic)
│   ├── storage/          # File storage management
│   ├── static/           # Backend static files
│   ├── test/             # Backend unit tests
│   ├── config.py         # Configuration management
│   ├── constants.py      # Application constants
│   ├── main.py           # FastAPI application entry point
│   ├── tasks.py          # Background task definitions
│   └── functions.py      # Function calling implementations
├── data/                 # Runtime data directory
└── requirements.txt      # Python dependencies
```

### Frontend (`/src/`)
Svelte/SvelteKit application providing the user interface.

```
src/
├── lib/
│   ├── apis/             # API client functions
│   ├── components/       # Reusable Svelte components
│   ├── stores/           # Svelte stores (state management)
│   ├── utils/            # Frontend utility functions
│   ├── i18n/             # Internationalization files
│   ├── types/            # TypeScript type definitions
│   ├── workers/          # Web Workers
│   ├── pyodide/          # Python runtime in browser
│   └── constants.ts      # Frontend constants
├── routes/               # SvelteKit file-based routing
│   ├── (app)/            # Main application routes
│   ├── auth/             # Authentication routes
│   ├── error/            # Error pages
│   ├── s/                # Shared/public routes
│   └── watch/            # Watch mode routes
├── app.css               # Global styles
├── app.html              # HTML template
└── tailwind.css          # Tailwind CSS imports
```

### Static Assets (`/static/`)
```
static/
├── assets/
│   ├── emojis/           # Emoji assets
│   ├── fonts/            # Custom fonts
│   └── images/           # Image assets
├── audio/                # Audio files (notifications, greetings)
├── themes/               # Custom CSS themes
├── pyodide/              # Pyodide runtime files
└── static/               # Public static files (favicons, manifests)
```

### Testing (`/cypress/`)
End-to-end testing with Cypress framework.

```
cypress/
├── e2e/                  # E2E test specifications
│   ├── chat.cy.ts
│   ├── documents.cy.ts
│   ├── registration.cy.ts
│   └── settings.cy.ts
├── support/              # Test support files
└── data/                 # Test fixtures
```

### Deployment (`/kubernetes/`)
```
kubernetes/
├── helm/                 # Helm charts for K8s deployment
└── manifest/
    ├── base/             # Base Kustomize manifests
    └── gpu/              # GPU-enabled configurations
```

## Core Components & Relationships

### Backend Components
1. **API Layer** (`routers/`): REST endpoints for frontend communication
2. **Database Layer** (`models/`): ORM models for data persistence (SQLAlchemy/Peewee)
3. **Real-time Layer** (`socket/`): WebSocket connections for live updates
4. **RAG Engine** (`retrieval/`): Document processing and retrieval logic
5. **Middleware** (`utils/middleware.py`): Request/response processing
6. **Task Queue** (`tasks.py`): Background job processing (APScheduler)

### Frontend Components
1. **State Management** (`stores/`): Svelte stores for global state
2. **API Client** (`apis/`): Backend communication layer
3. **UI Components** (`components/`): Reusable interface elements
4. **Routing** (`routes/`): SvelteKit file-based routing system
5. **Workers** (`workers/`): Background processing in browser
6. **Pyodide Integration** (`pyodide/`): Python runtime for client-side execution

### Data Flow
```
User Interface (Svelte)
    ↕ (HTTP/WebSocket)
API Routes (FastAPI)
    ↕
Business Logic (Services/Utils)
    ↕
Database (SQLAlchemy/Peewee)
    ↕
Storage (Files/Vectors)
```

## Architectural Patterns

### Backend Patterns
- **Layered Architecture**: Clear separation between routes, business logic, and data access
- **Dependency Injection**: FastAPI's dependency system for shared resources
- **Repository Pattern**: Database access abstraction through models
- **Middleware Pipeline**: Request/response processing chain
- **Background Tasks**: Async task processing with APScheduler

### Frontend Patterns
- **Component-Based Architecture**: Reusable Svelte components
- **Store Pattern**: Centralized state management with Svelte stores
- **API Abstraction**: Dedicated API client layer
- **File-Based Routing**: SvelteKit's convention-based routing
- **Progressive Enhancement**: PWA capabilities for offline support

### Integration Patterns
- **RESTful API**: Standard HTTP methods for CRUD operations
- **WebSocket Communication**: Real-time bidirectional communication
- **Event-Driven**: Socket.IO for real-time events
- **Plugin System**: Pipelines framework for extensibility

## Configuration Files
- `package.json`: Frontend dependencies and npm scripts
- `pyproject.toml`: Python project metadata and dependencies
- `requirements.txt`: Python package requirements
- `docker-compose.yaml`: Docker orchestration
- `Dockerfile`: Container image definition
- `svelte.config.js`: SvelteKit configuration
- `vite.config.ts`: Vite build configuration
- `tailwind.config.js`: Tailwind CSS configuration
- `tsconfig.json`: TypeScript configuration
- `.env.example`: Environment variable template

## Build & Deployment
- **Frontend Build**: Vite bundler with SvelteKit adapter
- **Backend Packaging**: Hatchling for Python package distribution
- **Container Images**: Multi-stage Docker builds with variants (`:main`, `:cuda`, `:ollama`)
- **Orchestration**: Docker Compose for local development, Kubernetes for production
