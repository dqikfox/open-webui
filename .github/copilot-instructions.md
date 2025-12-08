# Open WebUI - AI Agent Instructions

## Architecture Overview

**Open WebUI** is a self-hosted full-stack AI platform combining a **FastAPI backend** with a **SvelteKit frontend**, supporting LLM providers (Ollama, OpenAI-compatible APIs) with built-in RAG capabilities.

### Core Stack
- **Backend**: FastAPI + SQLAlchemy (primary) + Peewee (legacy migrations), uvicorn server
- **Frontend**: SvelteKit + Svelte 4 + Tailwind CSS 4, static adapter with SPA fallback
- **Database**: Supports SQLite (default), PostgreSQL, MySQL via SQLAlchemy. Uses Alembic for migrations (with Peewee compatibility layer)
- **Real-time**: Socket.IO for WebSocket communication (`/ws/socket.io` path)
- **AI Integration**: Pipelines plugin framework for extending LLM capabilities with custom Python logic

### Key Components

#### Backend Structure (`backend/open_webui/`)
- **`main.py`**: FastAPI app initialization, middleware setup, router registration
- **`routers/`**: API endpoints organized by domain (chats, users, models, retrieval, pipelines, etc.)
- **`models/`**: SQLAlchemy ORM models + Pydantic schemas (e.g., `Chat` class for DB, `ChatModel` for validation)
- **`functions.py`**: Python function calling framework - load, execute, and manage user-defined tools
- **`internal/db.py`**: Database engine configuration, handles both Alembic (SQLAlchemy) and Peewee migrations
- **`config.py`**: Centralized configuration with env vars, runs Alembic migrations on startup
- **`env.py`**: Environment variable parsing, logging setup, device detection (CPU/CUDA/MPS)

#### Frontend Structure (`src/`)
- **`routes/`**: SvelteKit file-based routing (`+layout.svelte`, `(app)/`, `auth/`)
- **`lib/stores/`**: Svelte stores for global state (user, config, models, chats, socket)
- **`lib/apis/`**: TypeScript API client modules organized by resource (mirrors backend routers)
- **`lib/components/`**: Reusable Svelte components
- **Socket.IO client** initialized in `+layout.svelte` with token auth and reconnection logic

#### Pipelines Plugin Framework
External Python plugins that extend LLM behavior via filter/action hooks:
- **Filter pipelines**: Intercept requests/responses (inlet/outlet) to modify payloads before/after LLM calls
- **Manifold pipes**: A single function that exposes multiple sub-models dynamically
- Configured via `OPENAI_API_BASE_URLS` and `OPENAI_API_KEYS` environment variables
- See `backend/open_webui/routers/pipelines.py` for implementation details

#### RAG System (`backend/open_webui/retrieval/`)
- Supports multiple vector databases: ChromaDB (default), Milvus, Qdrant, OpenSearch, Pinecone
- Embedding models via sentence-transformers (default: `all-MiniLM-L6-v2`)
- Optional reranking with Colbert
- Document processing: PDF, DOCX, PPTX, Markdown via `unstructured` library

## Development Workflows

### Local Development
```bash
# Frontend dev server (port 5173)
npm run dev

# Backend dev server (port 8080, auto-reload)
cd backend && ./dev.sh
```

Frontend proxies API calls to backend via Vite config. Frontend runs on port 5173, backend on 8080.

### Docker Development
```bash
# Build and run with docker-compose
make install  # or: docker compose up -d

# Update and rebuild
make update
```

Primary compose file: `docker-compose.yaml` (includes Ollama service)

### Database Migrations
- **Alembic** (SQLAlchemy): Primary migration system
  - Migrations in `backend/open_webui/migrations/versions/`
  - Auto-run on app startup via `config.py:run_migrations()`
  - Manual: `alembic upgrade head`
- **Peewee**: Legacy compatibility handled via `internal/db.py:handle_peewee_migration()`

### Testing
- **E2E**: Cypress (`npm run cy:open`, specs in `cypress/e2e/`)
- **Frontend unit**: Vitest (`npm run test:frontend`)
- **Backend lint**: `npm run lint:backend` (pylint)

## Project-Specific Conventions

### Backend Patterns

#### Router Organization
All routers follow this structure in `backend/open_webui/routers/*.py`:
```python
from fastapi import APIRouter
router = APIRouter()

@router.get("/", response_model=list[ItemResponse])
async def get_items(user=Depends(get_verified_user)):
    # Implementation
```
Routers registered in `main.py` with prefix pattern: `/api/v1/{resource}` (e.g., `/api/v1/chats`)

#### Model Pattern (Dual Schema)
```python
# SQLAlchemy ORM model (database)
class Chat(Base):
    __tablename__ = "chat"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    # ... other columns

# Pydantic model (validation/serialization)
class ChatModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    # ... mirrors Chat fields
```

#### Authentication Flow
- JWT tokens stored in `localStorage.token`
- Auth dependency: `get_verified_user` / `get_admin_user` in `utils/auth.py`
- Socket.IO auth via `auth: { token: localStorage.token }`

### Frontend Patterns

#### API Client Convention
API modules in `src/lib/apis/` export async functions that mirror backend routes:
```typescript
export const getChats = async (token: string) => {
  const res = await fetch(`${WEBUI_API_BASE_URL}/chats/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return res.json();
};
```

#### Svelte Store Usage
Global stores in `src/lib/stores/index.ts`:
- `user`: Current user session
- `config`: Backend configuration
- `models`: Available LLM models
- `socket`: Socket.IO connection
- `chats`: Chat history

Access pattern: `import { user } from '$lib/stores'` then `$user` in templates

#### Environment Variables
- Backend: `backend/open_webui/env.py` - parses env vars with defaults
- Frontend: Vite defines (`APP_VERSION`, `APP_BUILD_HASH`) in `vite.config.ts`

### Configuration Hierarchy
1. Environment variables (`.env` file loaded by `dotenv`)
2. Database config table (managed via `backend/open_webui/config.py`)
3. Hardcoded defaults in `env.py`

Key env vars:
- `DATABASE_URL`: Connection string (default: SQLite in `DATA_DIR`)
- `OLLAMA_BASE_URL`: Ollama API endpoint
- `OPENAI_API_KEY`: For OpenAI models
- `WEBUI_SECRET_KEY`: JWT signing key (auto-generated if missing)

## Integration Points

### Adding a New Backend Endpoint
1. Create router file in `backend/open_webui/routers/new_resource.py`
2. Define `router = APIRouter()`
3. Add route handlers with Pydantic models
4. Register in `main.py`: `app.include_router(new_resource.router, prefix="/api/v1/new_resource")`
5. Create matching API client in `src/lib/apis/new_resource/index.ts`

### Adding a Database Model
1. Create SQLAlchemy model in `backend/open_webui/models/new_model.py` extending `Base`
2. Create Pydantic schema for validation
3. Generate migration: `alembic revision --autogenerate -m "add new_model table"`
4. Review and edit migration in `backend/open_webui/migrations/versions/`
5. Migration auto-runs on next app start

### Extending with Functions/Tools
Functions are Python code snippets stored in DB and executed at runtime:
- Stored via `backend/open_webui/models/functions.py` (Functions table)
- Loaded dynamically by `utils/plugin.py:load_function_module_by_id()`
- Must define specific attributes: `valves` (config), `pipes` (manifold), or call methods
- Accessed by LLMs via OpenAI function calling protocol

### WebSocket Events
Socket events defined in `backend/open_webui/socket/main.py`:
- `user-count`: Broadcast active user count
- `usage`: Track model usage in real-time
- Connect/disconnect handlers manage state

## Common Pitfalls

- **Migration order**: Peewee migrations run before Alembic (handled in `internal/db.py`)
- **Docker volumes**: Always mount `-v open-webui:/app/backend/data` to persist database
- **Environment mismatch**: Backend runs on port 8080, frontend dev on 5173 - ensure proxy is configured
- **Embedding model changes**: Changing `USE_EMBEDDING_MODEL` requires re-embedding all documents
- **Socket.IO path**: WebSocket endpoint is `/ws/socket.io`, not default `/socket.io/`
