# Open WebUI - Product Overview

## Purpose
Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform designed to operate entirely offline. It serves as a powerful AI deployment solution that supports various LLM runners like Ollama and OpenAI-compatible APIs, with a built-in inference engine for Retrieval Augmented Generation (RAG).

## Value Proposition
- **Self-hosted & Offline**: Complete control over AI infrastructure with no external dependencies required
- **Versatile Integration**: Works with multiple LLM providers (Ollama, OpenAI, LMStudio, GroqCloud, Mistral, OpenRouter)
- **Enterprise-Ready**: Granular permissions, RBAC, user groups, and SLA support available
- **Extensible Platform**: Plugin system via Pipelines framework for custom logic and Python libraries

## Key Features

### Core Capabilities
- **Effortless Setup**: Docker/Kubernetes deployment with support for `:ollama` and `:cuda` tagged images
- **Multi-Model Conversations**: Engage with various models simultaneously for optimal responses
- **Responsive Design**: Seamless experience across desktop, laptop, and mobile devices
- **Progressive Web App (PWA)**: Native app-like mobile experience with offline access

### AI & LLM Integration
- **Ollama/OpenAI API Integration**: Flexible API connections with customizable endpoints
- **Model Builder**: Create custom Ollama models via Web UI with character/agent customization
- **Native Python Function Calling**: Built-in code editor for pure Python functions with BYOF (Bring Your Own Function)
- **Image Generation**: Integration with AUTOMATIC1111, ComfyUI (local), and DALL-E (external)

### Advanced Features
- **Local RAG Integration**: Document interactions with chat using `#` command for document library access
- **Web Search for RAG**: Multiple provider support (SearXNG, Google PSE, Brave, DuckDuckGo, Tavily, Bing, etc.)
- **Web Browsing**: Incorporate websites directly into conversations using `#` command + URL
- **Voice/Video Calls**: Hands-free communication with integrated voice and video features
- **Full Markdown & LaTeX Support**: Rich content rendering for technical and mathematical content

### Security & Access Control
- **Role-Based Access Control (RBAC)**: Restricted permissions with granular user roles
- **User Groups**: Detailed permission management for secure environments
- **Admin Controls**: Exclusive model creation/pulling rights for administrators

### Developer Features
- **Pipelines Plugin Framework**: Custom logic integration with examples for:
  - Function calling
  - Rate limiting
  - Usage monitoring (Langfuse integration)
  - Live translation (LibreTranslate)
  - Toxic message filtering
- **Multilingual Support (i18n)**: International language support with active community contributions

## Target Users

### Primary Users
- **AI Enthusiasts**: Individuals wanting self-hosted AI solutions with privacy control
- **Developers**: Teams building AI-powered applications requiring flexible LLM integration
- **Enterprises**: Organizations needing secure, on-premise AI deployment with compliance requirements
- **Researchers**: Academic and research teams requiring offline AI capabilities

### Use Cases
- Private AI assistant deployment for individuals and teams
- Enterprise knowledge management with RAG capabilities
- Custom AI application development with plugin extensibility
- Offline AI inference for secure/air-gapped environments
- Multi-model experimentation and comparison
- Document analysis and question-answering systems
- AI-powered customer support systems
- Educational AI platforms with controlled access

## Technical Highlights
- **Version**: 0.6.15
- **License**: Open WebUI License (revised BSD-3-Clause with branding preservation)
- **Deployment**: Docker, Kubernetes (kubectl, kustomize, helm), Python pip
- **Platform Support**: Linux, Windows, macOS with GPU acceleration support (CUDA)
- **Community**: Active Discord community and GitHub sponsorship program
