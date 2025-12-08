# Open WebUI - Development Guidelines

## Code Quality Standards

### Import Organization
- **Standard library imports first**, followed by third-party imports, then local imports
- Group imports logically with blank lines between groups
- Example pattern:
  ```python
  import json
  import logging
  import os
  
  from fastapi import Request, HTTPException
  from pydantic import BaseModel
  
  from open_webui.models.users import Users
  from open_webui.config import CACHE_DIR
  ```

### Naming Conventions
- **SCREAMING_SNAKE_CASE** for constants and environment variables
  - Examples: `CACHE_DIR`, `ENABLE_WEB_SEARCH`, `RAG_EMBEDDING_MODEL`
- **snake_case** for functions, variables, and module names
  - Examples: `get_embedding_function`, `process_web_search`, `user_id`
- **PascalCase** for classes and Pydantic models
  - Examples: `PersistentConfig`, `SearchForm`, `UserModel`
- **Prefix private/internal** with single underscore
  - Examples: `_get_docs_info`, `__event_emitter__`

### Type Annotations
- Use type hints extensively for function parameters and return types
- Leverage `Optional[T]` for nullable values
- Use `Union` types when multiple types are acceptable
- Example:
  ```python
  def get_ef(
      engine: str,
      embedding_model: str,
      auto_update: bool = False,
  ) -> Optional[SentenceTransformer]:
  ```

### Documentation
- Use docstrings for complex functions, especially public APIs
- Include parameter descriptions and return value documentation
- Example:
  ```python
  def search_web(request: Request, engine: str, query: str) -> list[SearchResult]:
      """Search the web using a search engine and return the results.
      
      Args:
          request: FastAPI request object
          engine: Search engine identifier
          query: The query to search for
          
      Returns:
          List of SearchResult objects
      """
  ```

## Semantic Patterns

### Configuration Management Pattern
**Frequency: Very High** - Used throughout the codebase

The project uses a sophisticated `PersistentConfig` pattern for managing configuration:

```python
# Define configuration with environment variable fallback
ENABLE_WEB_SEARCH = PersistentConfig(
    "ENABLE_WEB_SEARCH",
    "rag.web.search.enable",
    os.getenv("ENABLE_WEB_SEARCH", "False").lower() == "true",
)

# Access configuration value
if request.app.state.config.ENABLE_WEB_SEARCH:
    # Use the configuration
```

**Key characteristics:**
- Three-parameter initialization: env name, config path, default value
- Automatic persistence to database
- Centralized in `config.py`
- Access via `request.app.state.config.PROPERTY_NAME`

### Request State Pattern
**Frequency: Very High** - Core to the application architecture

Application state is stored on the FastAPI request object:

```python
# Accessing application state
embedding_model = request.app.state.config.RAG_EMBEDDING_MODEL
embedding_function = request.app.state.EMBEDDING_FUNCTION
vector_db = request.app.state.VECTOR_DB_CLIENT

# Setting application state (typically in startup)
request.app.state.ef = get_ef(engine, model)
request.app.state.rf = get_rf(reranking_model)
```

**Key characteristics:**
- Configuration accessed via `request.app.state.config`
- Shared resources via `request.app.state.RESOURCE_NAME`
- Enables dependency injection without explicit parameters

### Async/Await Pattern
**Frequency: High** - Used for I/O operations

Consistent use of async/await for I/O-bound operations:

```python
async def process_web_search(
    request: Request, form_data: SearchForm, user=Depends(get_verified_user)
):
    # Concurrent task execution
    search_tasks = [
        run_in_threadpool(search_web, request, engine, query)
        for query in form_data.queries
    ]
    search_results = await asyncio.gather(*search_tasks)
    
    # Async loading
    docs = await loader.aload()
```

**Key characteristics:**
- Use `async def` for async functions
- `await` for async operations
- `asyncio.gather()` for concurrent execution
- `run_in_threadpool()` for CPU-bound operations

### Dependency Injection Pattern
**Frequency: High** - FastAPI standard

FastAPI's dependency injection for authentication and validation:

```python
@router.post("/process/file")
def process_file(
    request: Request,
    form_data: ProcessFileForm,
    user=Depends(get_verified_user),
):
    # user is automatically injected and validated
```

**Common dependencies:**
- `get_verified_user` - Authenticated user
- `get_admin_user` - Admin-only access
- `Depends()` - FastAPI dependency injection

### Error Handling Pattern
**Frequency: High** - Consistent error handling

Structured error handling with logging and HTTP exceptions:

```python
try:
    result = save_docs_to_vector_db(request, docs, collection_name)
    if result:
        return {"status": True, "collection_name": collection_name}
except Exception as e:
    log.exception(e)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.DEFAULT(e),
    )
```

**Key characteristics:**
- Always log exceptions with `log.exception(e)`
- Use `HTTPException` for API errors
- Centralized error messages in `ERROR_MESSAGES`
- Return structured responses with `status` field

### Event Emitter Pattern
**Frequency: Medium** - Real-time communication

WebSocket-based event emission for real-time updates:

```python
event_emitter = get_event_emitter(metadata)

await event_emitter({
    "type": "status",
    "data": {
        "action": "web_search",
        "description": "Searching the web",
        "done": False,
    },
})
```

**Key characteristics:**
- Get emitter from metadata: `get_event_emitter(metadata)`
- Structured event data with `type` and `data` fields
- Used for progress updates, status changes, and streaming
- Async emission with `await`

### Pydantic Model Validation
**Frequency: High** - Data validation

Pydantic models for request/response validation:

```python
class ProcessFileForm(BaseModel):
    file_id: str
    content: Optional[str] = None
    collection_name: Optional[str] = None

@router.post("/process/file")
def process_file(request: Request, form_data: ProcessFileForm):
    # form_data is automatically validated
```

**Key characteristics:**
- Inherit from `BaseModel`
- Use `Optional[T]` for nullable fields
- Provide defaults with `= None` or `= value`
- Automatic validation and serialization

### Logging Pattern
**Frequency: Very High** - Comprehensive logging

Structured logging with module-level loggers:

```python
import logging
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])

# Usage
log.debug(f"Processing file: {file_id}")
log.info(f"Updating embedding model: {old} to {new}")
log.exception(e)  # Logs exception with traceback
log.error(f"Error: {error_message}")
```

**Key characteristics:**
- Module-level logger: `log = logging.getLogger(__name__)`
- Configurable log levels via `SRC_LOG_LEVELS`
- Use f-strings for log messages
- `log.exception()` for exception logging

### Database Access Pattern
**Frequency: High** - Data persistence

Direct model access for database operations:

```python
# Get operations
user = Users.get_user_by_id(user_id)
file = Files.get_file_by_id(file_id)

# Update operations
Files.update_file_data_by_id(file_id, {"content": text_content})
Chats.upsert_message_to_chat_by_id_and_message_id(chat_id, message_id, data)

# Delete operations
VECTOR_DB_CLIENT.delete_collection(collection_name)
```

**Key characteristics:**
- Static methods on model classes
- Descriptive method names: `get_X_by_Y`, `update_X_by_Y`
- Direct database access without repositories
- Use `upsert` for insert-or-update operations

### Vector Database Pattern
**Frequency: Medium** - RAG operations

Consistent vector database operations:

```python
# Check collection existence
if VECTOR_DB_CLIENT.has_collection(collection_name):
    # Query collection
    result = VECTOR_DB_CLIENT.query(
        collection_name=collection_name,
        filter={"hash": metadata["hash"]},
    )
    
# Insert documents
VECTOR_DB_CLIENT.insert(
    collection_name=collection_name,
    items=items,
)
```

**Key characteristics:**
- Global `VECTOR_DB_CLIENT` instance
- Check existence before operations
- Use filters for targeted queries
- Batch insert with `items` list

### Template Processing Pattern
**Frequency: Medium** - Dynamic content generation

Template variable replacement for prompts:

```python
def prompt_template(template: str, user_name: Optional[str] = None) -> str:
    current_date = datetime.now().strftime("%Y-%m-%d")
    template = template.replace("{{CURRENT_DATE}}", current_date)
    template = template.replace("{{USER_NAME}}", user_name or "Unknown")
    return template
```

**Key characteristics:**
- Use `{{VARIABLE}}` syntax for placeholders
- Replace with `.replace()` method
- Provide fallback values for optional variables
- Chain replacements for multiple variables

### Middleware Pattern
**Frequency: Medium** - Request/response processing

Complex middleware for chat processing:

```python
async def process_chat_payload(request, form_data, user, metadata, model):
    # Get event emitters
    event_emitter = get_event_emitter(metadata)
    event_call = get_event_call(metadata)
    
    # Build extra params
    extra_params = {
        "__event_emitter__": event_emitter,
        "__event_call__": event_call,
        "__user__": user.model_dump(),
        "__metadata__": metadata,
    }
    
    # Process through pipeline
    form_data = await process_pipeline_inlet_filter(request, form_data, user, models)
    
    return form_data, metadata, events
```

**Key characteristics:**
- Build context dictionaries with `__prefix__` convention
- Pass through multiple processing stages
- Return modified data and metadata
- Use async for I/O operations

## Best Practices

### Environment Variable Handling
- Always provide defaults for environment variables
- Use `.lower() == "true"` for boolean environment variables
- Centralize in `config.py` using `PersistentConfig`
- Example:
  ```python
  ENABLE_FEATURE = os.environ.get("ENABLE_FEATURE", "False").lower() == "true"
  ```

### API Route Organization
- Group related routes in router modules
- Use FastAPI's `APIRouter` for modular routing
- Prefix routes logically (e.g., `/process/`, `/query/`)
- Include route documentation in docstrings

### State Management
- Store shared resources on `request.app.state`
- Initialize in application startup
- Access via `request.app.state.RESOURCE_NAME`
- Don't mutate state in request handlers

### Async Best Practices
- Use `async def` for I/O-bound operations
- Use `run_in_threadpool()` for CPU-bound operations
- Leverage `asyncio.gather()` for concurrent tasks
- Always `await` async operations

### Error Messages
- Use centralized `ERROR_MESSAGES` constants
- Provide context in error messages
- Log exceptions before raising HTTP exceptions
- Return structured error responses

### Testing Considerations
- Write testable code with dependency injection
- Separate business logic from route handlers
- Use type hints for better IDE support
- Mock external dependencies in tests

### Performance Optimization
- Use batch operations when possible
- Leverage async for concurrent I/O
- Cache expensive computations
- Use connection pooling for databases

### Security Practices
- Always validate user input with Pydantic
- Use dependency injection for authentication
- Sanitize user-provided content
- Log security-relevant events
- Never expose sensitive data in logs

## Code Examples

### Complete Route Handler Example
```python
@router.post("/process/file")
def process_file(
    request: Request,
    form_data: ProcessFileForm,
    user=Depends(get_verified_user),
):
    try:
        # Get file from database
        file = Files.get_file_by_id(form_data.file_id)
        
        # Process file content
        text_content = file.data.get("content", "")
        
        # Save to vector database
        if not request.app.state.config.BYPASS_EMBEDDING_AND_RETRIEVAL:
            result = save_docs_to_vector_db(
                request,
                docs=docs,
                collection_name=collection_name,
                user=user,
            )
            
            if result:
                return {
                    "status": True,
                    "collection_name": collection_name,
                    "content": text_content,
                }
    except Exception as e:
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )
```

### Async Processing Example
```python
async def process_web_search(request: Request, form_data: SearchForm):
    # Create concurrent tasks
    search_tasks = [
        run_in_threadpool(search_web, request, engine, query)
        for query in form_data.queries
    ]
    
    # Execute concurrently
    search_results = await asyncio.gather(*search_tasks)
    
    # Process results
    urls = [item.link for result in search_results for item in result]
    
    return {"status": True, "urls": urls}
```

### Configuration Access Example
```python
def get_config_value(request: Request):
    # Access configuration
    chunk_size = request.app.state.config.CHUNK_SIZE
    embedding_model = request.app.state.config.RAG_EMBEDDING_MODEL
    
    # Access shared resources
    embedding_function = request.app.state.EMBEDDING_FUNCTION
    
    return {
        "chunk_size": chunk_size,
        "embedding_model": embedding_model,
    }
```
