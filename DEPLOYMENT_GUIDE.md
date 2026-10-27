# QA$Y$ Deployment Guide
## Complete Setup & Installation

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- CUDA 12.1+ (optional, for GPU)
- 8GB+ RAM

---

## Quick Install (5 minutes)

```bash
# 1. Clone repository
cd /home/ultro/projects/openui/oasis

# 2. Run installation script
./scripts/install_qasy.sh

# 3. Start OASIS
docker-compose up -d

# 4. Test QA$Y$
curl http://localhost:8080/api/oasis/status
```

---

## Manual Installation

### Step 1: Install Dependencies

```bash
# Install QA$Y$ requirements
pip install -r requirements-qasy.txt

# Install NeMo Agent Toolkit
pip install nemo-agent-toolkit

# Verify installation
python3 -c "import nemo_agent; print('✅ NeMo installed')"
```

### Step 2: Configure Environment

```bash
# Create .env file
cat > .env << EOF
# QA$Y$ Configuration
QASY_ENABLED=True
QASY_TOOLS_DIR=./backend/oasis/qasy/tools
QASY_MEMORY_SIZE=100
QASY_MINIMAX_ENABLED=True

# NeMo Configuration
QASY_NEMO_ENABLED=True
NEMO_MODEL_PATH=/models/nemo
NEMO_GPU_ENABLED=True

# MiniMax API
MINIMAX_API_KEY=your_api_key_here
MINIMAX_GROUP_ID=your_group_id_here
EOF
```

### Step 3: Generate Assets

```bash
# Generate Ultron-themed assets
python3 scripts/generate_ultron_assets.py

# Assets will be saved to:
# static/assets/ultron/background.png
# static/assets/ultron/logo.png
# static/assets/ultron/circuit_pattern.png
```

### Step 4: Start Services

```bash
# Start with Docker Compose
docker-compose up -d

# Or start manually
cd backend
python -m oasis.main
```

---

## Docker Deployment

### Standard Deployment

```bash
# Build image
docker build -t qasy:latest .

# Run container
docker run -d \
  -p 8080:8080 \
  -v qasy-data:/app/backend/data \
  -e QASY_ENABLED=True \
  --name qasy \
  qasy:latest
```

### GPU-Enabled Deployment

```bash
# Build with CUDA support
docker build -f Dockerfile.cuda -t qasy:cuda .

# Run with GPU
docker run -d \
  -p 8080:8080 \
  --gpus all \
  -v qasy-data:/app/backend/data \
  -e QASY_ENABLED=True \
  -e NEMO_GPU_ENABLED=True \
  --name qasy-gpu \
  qasy:cuda
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  qasy:
    image: qasy:latest
    ports:
      - "8080:8080"
    environment:
      - QASY_ENABLED=True
      - QASY_NEMO_ENABLED=True
    volumes:
      - qasy-data:/app/backend/data
      - ./static/assets:/app/static/assets
    restart: unless-stopped

volumes:
  qasy-data:
```

---

## Kubernetes Deployment

### Basic Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qasy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: qasy
  template:
    metadata:
      labels:
        app: qasy
    spec:
      containers:
      - name: qasy
        image: qasy:latest
        ports:
        - containerPort: 8080
        env:
        - name: QASY_ENABLED
          value: "True"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
```

### GPU Deployment

```yaml
# k8s/deployment-gpu.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qasy-gpu
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: qasy
        image: qasy:cuda
        resources:
          limits:
            nvidia.com/gpu: 1
```

---

## Testing

### API Tests

```bash
# Test status
curl http://localhost:8080/api/oasis/status

# Test command execution
curl -X POST http://localhost:8080/api/oasis/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "test hello"}'

# Test tools
curl http://localhost:8080/api/oasis/tools

# Test NeMo
curl http://localhost:8080/api/oasis/nemo/status
```

### Frontend Tests

```bash
# Open browser
open http://localhost:8080

# Navigate to QA$Y$ section
# Test chat interface
# Test tool panel
```

---

## Monitoring

### Health Checks

```bash
# QA$Y$ health
curl http://localhost:8080/api/oasis/status

# OASIS health
curl http://localhost:8080/health

# Database health
curl http://localhost:8080/health/db
```

### Logs

```bash
# Docker logs
docker logs qasy -f

# Application logs
tail -f backend/logs/qasy.log

# NeMo logs
tail -f backend/logs/nemo.log
```

### Metrics

```bash
# Memory usage
curl http://localhost:8080/api/oasis/memory | jq '.messages | length'

# Agent status
curl http://localhost:8080/api/oasis/status | jq '.agent'

# NeMo agents
curl http://localhost:8080/api/oasis/nemo/agents | jq '.agents | length'
```

---

## Troubleshooting

### NeMo Not Found

```bash
# Install NeMo
pip install nemo-agent-toolkit

# Verify
python3 -c "import nemo_agent"
```

### CUDA Errors

```bash
# Check CUDA
nvidia-smi

# Install CUDA toolkit
conda install cudatoolkit=12.1
```

### Port Conflicts

```bash
# Check port usage
lsof -i :8080

# Kill process
kill -9 $(lsof -t -i:8080)
```

### Memory Issues

```bash
# Reduce memory size
export QASY_MEMORY_SIZE=50

# Clear memory
curl -X DELETE http://localhost:8080/api/oasis/memory
```

---

## Production Checklist

- [ ] Environment variables configured
- [ ] SSL/TLS certificates installed
- [ ] Database backups configured
- [ ] Monitoring setup (Prometheus/Grafana)
- [ ] Log aggregation (ELK/Loki)
- [ ] Auto-scaling configured
- [ ] Load balancer setup
- [ ] CDN for static assets
- [ ] Rate limiting enabled
- [ ] Security headers configured

---

## Performance Tuning

### Database

```bash
# Optimize PostgreSQL
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';
```

### Caching

```bash
# Enable Redis caching
export REDIS_URL=redis://localhost:6379
```

### GPU Optimization

```bash
# Set GPU memory fraction
export CUDA_VISIBLE_DEVICES=0
export TF_FORCE_GPU_ALLOW_GROWTH=true
```

---

## Backup & Recovery

### Backup

```bash
# Backup database
docker exec qasy pg_dump -U postgres > backup.sql

# Backup assets
tar -czf assets-backup.tar.gz static/assets/
```

### Restore

```bash
# Restore database
docker exec -i qasy psql -U postgres < backup.sql

# Restore assets
tar -xzf assets-backup.tar.gz -C static/
```

---

## Scaling

### Horizontal Scaling

```bash
# Scale replicas
kubectl scale deployment qasy --replicas=5

# Or with Docker Compose
docker-compose up -d --scale qasy=5
```

### Vertical Scaling

```bash
# Increase resources
docker update qasy --memory=8g --cpus=4
```

---

## Security

### SSL/TLS

```bash
# Generate certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout key.pem -out cert.pem

# Configure nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

### Authentication

```bash
# Enable API key authentication
export ENABLE_API_KEY=True
export API_KEY_ALLOWED_ENDPOINTS=/api/oasis/*
```

---

## Support

- Documentation: `QASY_README.md`
- NeMo Guide: `QASY_NEMO_INTEGRATION.md`
- Integration: `INTEGRATION_COMPLETE.md`
- GitHub: https://github.com/oasis/oasis

---

**Status**: ✅ PRODUCTION READY
**Version**: 1.0.0
**Last Updated**: 2025-01-16
