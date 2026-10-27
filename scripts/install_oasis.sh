#!/bin/bash
# QA$Y$ Installation Script

echo "🤖 Installing QA$Y$ (Quality Assurance System)"
echo "=============================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install QA$Y$ requirements
echo ""
echo "📦 Installing QA$Y$ dependencies..."
pip install -r requirements-qasy.txt

# Check if NeMo installed successfully
if python3 -c "import importlib.util; exit(0 if importlib.util.find_spec('nemo_agent') else 1)" 2>/dev/null; then
    echo "✅ NeMo Agent Toolkit installed successfully"
else
    echo "⚠️  NeMo Agent Toolkit not found"
    echo "   Install manually: pip install nemo-agent-toolkit"
fi

# Generate QA$Y$ assets with MiniMax
echo ""
echo "🎨 Generating QA$Y$ assets with MiniMax AI..."
python3 scripts/generate_ultron_assets.py

echo ""
echo "✅ QA$Y$ installation complete!"
echo ""
echo "Quick Start:"
echo "  1. Start OASIS: docker-compose up -d"
echo "  2. Test QA$Y$: curl http://localhost:8080/api/oasis/status"
echo "  3. Access UI: http://localhost:8080"
echo ""
echo "Documentation:"
echo "  - QASY_README.md"
echo "  - QASY_NEMO_INTEGRATION.md"
echo "  - INTEGRATION_COMPLETE.md"
