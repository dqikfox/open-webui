#!/usr/bin/env python3
"""Test LLM connection for all QA$Y$ tools"""
import sys
import asyncio
sys.path.insert(0, '/home/ultro/projects/openui/oasis/backend')

from oasis.qasy.llm_connector import llm_connector


async def test_connection():
    """Test Ollama connection"""
    print("🔍 Testing Ollama Connection...")
    print(f"URL: {llm_connector.ollama_url}")
    print()
    
    # Get available models
    models = llm_connector.get_models()
    print(f"✅ Available Models ({len(models)}):")
    for model in models:
        print(f"  - {model}")
    print()
    
    # Test generation
    print("🧪 Testing LLM Generation...")
    response = await llm_connector.generate(
        prompt="Say 'QA$Y$ is connected!' in one sentence.",
        model=llm_connector.default_model
    )
    print(f"Response: {response}")
    print()
    
    # Test chat
    print("🧪 Testing LLM Chat...")
    response = await llm_connector.chat(
        messages=[
            {"role": "user", "content": "What is QA$Y$?"}
        ],
        model=llm_connector.default_model
    )
    print(f"Response: {response}")
    print()
    
    print("✅ All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_connection())
