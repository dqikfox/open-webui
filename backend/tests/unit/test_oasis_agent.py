import pytest
import asyncio
from unittest.mock import Mock, patch
from open_webui.oasis.agent_core import OasisAgent

@pytest.fixture
def agent():
    return OasisAgent()

@pytest.mark.asyncio
async def test_agent_initialization(agent):
    assert agent.config == {}
    assert agent.tools == {}
    assert agent.memory == []
    assert agent.active == False

@pytest.mark.asyncio
async def test_execute_test_command(agent):
    result = await agent.execute_command("test arg1 arg2")
    assert result["status"] == "success"
    assert result["action"] == "test"
    assert result["args"] == ["arg1", "arg2"]

@pytest.mark.asyncio
async def test_execute_empty_command(agent):
    result = await agent.execute_command("")
    assert "error" in result
    assert result["error"] == "Empty command"

@pytest.mark.asyncio
async def test_execute_unknown_command(agent):
    result = await agent.execute_command("unknown_action")
    assert "error" in result
    assert "Unknown action" in result["error"]

@pytest.mark.asyncio
async def test_tool_registration(agent):
    mock_tool = Mock()
    mock_tool.execute = Mock(return_value={"result": "success"})
    
    agent.register_tool("test_tool", mock_tool)
    assert "test_tool" in agent.tools
    assert agent.tools["test_tool"] == mock_tool

def test_get_status(agent):
    status = agent.get_status()
    assert "active" in status
    assert "tools_count" in status
    assert "memory_size" in status
    assert "version" in status
    assert status["tools_count"] == 0
    assert status["memory_size"] == 0