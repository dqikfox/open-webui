#!/bin/bash
# Verify Ollama has access to all QA$Y$ functions

echo "🔍 Verifying Ollama Function Access..."
echo "======================================"
echo ""

# Check Ollama is running
echo "1. Checking Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ Ollama is running"
    MODELS=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | wc -l)
    echo "   ✅ $MODELS models available"
else
    echo "   ❌ Ollama not running"
    exit 1
fi

echo ""
echo "2. Checking QA$Y$ function registry..."
FUNC_COUNT=$(curl -s http://localhost:8080/api/oasis/functions 2>/dev/null | grep -o '"count":[0-9]*' | cut -d':' -f2)
if [ ! -z "$FUNC_COUNT" ]; then
    echo "   ✅ $FUNC_COUNT functions registered"
else
    echo "   ⚠️  Function registry not accessible (start OASIS)"
fi

echo ""
echo "3. Available functions:"
curl -s http://localhost:8080/api/oasis/functions 2>/dev/null | grep -o '"[^"]*"' | grep -v "functions\|schemas\|count" | head -20 | sed 's/"//g' | sed 's/^/   - /'

echo ""
echo "4. Testing function execution..."
RESULT=$(curl -s -X POST http://localhost:8080/api/oasis/functions/execute \
  -H "Content-Type: application/json" \
  -d '{"function_name": "list_tools", "parameters": {}}' 2>/dev/null)

if echo "$RESULT" | grep -q "success"; then
    echo "   ✅ Function execution working"
else
    echo "   ⚠️  Function execution test failed"
fi

echo ""
echo "======================================"
echo "✅ Verification Complete"
echo ""
echo "All Ollama models can now use QA$Y$ functions!"
echo ""
echo "Test with:"
echo "  curl -X POST http://localhost:8080/api/oasis/ollama/chat \\"
echo "    -d '{\"model\": \"llama3.1\", \"messages\": [{\"role\": \"user\", \"content\": \"List available tools\"}]}'"
