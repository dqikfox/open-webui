#!/bin/bash

echo "🧪 Testing OASIS QA$Y$ System..."
echo ""

# Test Ollama
echo "1️⃣ Testing Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama running"
    curl -s http://localhost:11434/api/tags | jq -r '.models[].name' | head -3
else
    echo "❌ Ollama not running"
fi

echo ""

# Test LLM generation
echo "2️⃣ Testing LLM generation..."
/usr/local/bin/python3 << 'EOF'
import sys
sys.path.insert(0, '/home/ultro/projects/openui/oasis/backend')

try:
    from open_webui.qasy.llm_connector import LLMConnector
    import asyncio
    
    async def test():
        llm = LLMConnector()
        response = await llm.generate("Say 'Hello from QA$Y$' in 5 words", model="llama3")
        print(f"✅ LLM Response: {response[:100]}")
    
    asyncio.run(test())
except Exception as e:
    print(f"❌ LLM Error: {e}")
EOF

echo ""

# Test AutoGen Studio
echo "3️⃣ Testing AutoGen Studio..."
/usr/local/bin/python3 << 'EOF'
import sys
sys.path.insert(0, '/home/ultro/projects/openui/oasis/backend')

try:
    from open_webui.qasy.autogen_studio import AutoGenStudio
    studio = AutoGenStudio()
    print(f"✅ AutoGen: {len(studio.agents)} agents initialized")
except Exception as e:
    print(f"❌ AutoGen Error: {e}")
EOF

echo ""

# Test Function Registry
echo "4️⃣ Testing Function Registry..."
/usr/local/bin/python3 << 'EOF'
import sys
sys.path.insert(0, '/home/ultro/projects/openui/oasis/backend')

try:
    from open_webui.qasy.function_registry import FunctionRegistry
    from open_webui.qasy.llm_connector import LLMConnector
    
    llm = LLMConnector()
    registry = FunctionRegistry(llm)
    registry.register_all_functions()
    
    functions = registry.list_functions()
    print(f"✅ Function Registry: {len(functions)} functions")
except Exception as e:
    print(f"❌ Registry Error: {e}")
EOF

echo ""

# Test Workflows
echo "5️⃣ Testing Workflows..."
/usr/local/bin/python3 << 'EOF'
import sys
sys.path.insert(0, '/home/ultro/projects/openui/oasis/backend')

try:
    from open_webui.qasy.agent_orchestrator import AgentOrchestrator
    from open_webui.qasy.autogen_studio import AutoGenStudio
    from open_webui.qasy import QasyAgent, QasyToolLoader
    from open_webui.qasy.llm_connector import llm_connector
    
    studio = AutoGenStudio()
    agent = QasyAgent()
    loader = QasyToolLoader(llm_connector=llm_connector)
    orchestrator = AgentOrchestrator(studio, agent, loader)
    
    workflows = orchestrator.list_workflows()
    print(f"✅ Workflows: {len(workflows)} available")
except Exception as e:
    print(f"❌ Workflow Error: {e}")
EOF

echo ""

# Test Knowledge Base
echo "6️⃣ Testing Knowledge Base..."
/usr/local/bin/python3 << 'EOF'
import sys
sys.path.insert(0, '/home/ultro/projects/openui/oasis/backend')

try:
    from open_webui.qasy.knowledge_base import knowledge_base
    
    stats = knowledge_base.get_stats()
    print(f"✅ Knowledge Base: {stats['total']} items")
except Exception as e:
    print(f"❌ Knowledge Base Error: {e}")
EOF

echo ""

# Test CUDA
echo "7️⃣ Testing CUDA..."
/usr/local/bin/python3 << 'EOF'
import sys
sys.path.insert(0, '/home/ultro/projects/openui/oasis/backend')

try:
    from open_webui.utils.cuda_utils import cuda_manager
    status = cuda_manager.get_status()
    
    if status.get('available'):
        print(f"✅ CUDA: {status['device_count']} GPU(s)")
    else:
        print("⚠️  CUDA: Not available (CPU mode)")
except Exception as e:
    print(f"⚠️  CUDA: {e}")
EOF

echo ""
echo "✅ All tests complete!"
