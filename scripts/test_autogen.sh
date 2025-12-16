#!/bin/bash

echo "🤖 Testing AutoGen Studio Integration..."

API_BASE="http://localhost:8080/api/oasis"

echo ""
echo "1️⃣ Getting Enhancement Suggestions..."
curl -X POST "$API_BASE/autogen/suggest" \
  -H "Content-Type: application/json" \
  -d '{"context": "OASIS QA$Y$ System"}' | jq .

echo ""
echo "2️⃣ Analyzing Sample Code..."
curl -X POST "$API_BASE/autogen/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/test/sample.py",
    "content": "def hello():\n    print(\"Hello World\")\n    return True"
  }' | jq .

echo ""
echo "3️⃣ Auto-Implementing Feature..."
curl -X POST "$API_BASE/autogen/implement" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_request": "Add error handling to the hello function",
    "file_context": {}
  }' | jq .

echo ""
echo "✅ AutoGen Studio tests complete!"
