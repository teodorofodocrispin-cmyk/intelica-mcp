"""
Tests para Intelica MCP Server
Correr con: pytest tests/ -v
"""
import pytest
import json
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_demo_analyze_returns_json():
    """demo_analyze debe retornar JSON válido."""
    from server import demo_analyze

    mock_response = {
        "source": "demo",
        "analysis": {
            "company_or_product": "Linear",
            "confidence": "high",
        }
    }

    class MockResp:
        status_code = 200
        def json(self): return mock_response

    class MockClient:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): pass
        async def post(self, *a, **kw): return MockResp()

    with patch("httpx.AsyncClient", return_value=MockClient()):
        result = await demo_analyze(text="Linear is a project management tool")
        data = json.loads(result)
        assert "source" in data or "analysis" in data or "error" in data


@pytest.mark.asyncio
async def test_demo_analyze_empty_text():
    """demo_analyze debe retornar error si no hay texto."""
    from server import demo_analyze
    result = await demo_analyze(text="")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_batch_analyze_empty_items():
    """batch_analyze debe retornar error si items está vacío."""
    from server import batch_analyze
    result = await batch_analyze(items=[])
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_batch_analyze_too_many_items():
    """batch_analyze debe retornar error si hay más de 10 items."""
    from server import batch_analyze
    items = [{"text": f"Company {i}"} for i in range(11)]
    result = await batch_analyze(items=items)
    data = json.loads(result)
    assert "error" in data
    assert "10" in data.get("message", "")


@pytest.mark.asyncio
async def test_analyze_competitor_missing_input():
    """analyze_competitor debe retornar error si no hay url ni text."""
    from server import analyze_competitor
    result = await analyze_competitor()
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
async def test_get_pricing_returns_json():
    """get_pricing debe retornar JSON con campos de precio."""
    from server import get_pricing

    mock_response = {
        "single": {"price": "$0.05 USDC"},
        "batch": {"price": "$0.20 USDC"},
        "protocol": "x402",
        "network": "eip155:8453",
    }

    class MockResp:
        def json(self): return mock_response

    class MockClient:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): pass
        async def get(self, *a, **kw): return MockResp()

    with patch("httpx.AsyncClient", return_value=MockClient()):
        result = await get_pricing()
        data = json.loads(result)
        assert isinstance(data, dict)


def test_server_imports():
    """El servidor debe importar sin errores."""
    import server
    assert hasattr(server, 'mcp')
    assert hasattr(server, 'analyze_competitor')
    assert hasattr(server, 'batch_analyze')
    assert hasattr(server, 'demo_analyze')
    assert hasattr(server, 'get_pricing')


def test_server_has_4_tools():
    """El servidor debe tener exactamente 4 tools."""
    import server
    # FastMCP registra tools en _tool_manager
    tools = server.mcp._tool_manager.list_tools()
    assert len(tools) == 4
    tool_names = {t.name for t in tools}
    assert "analyze_competitor" in tool_names
    assert "batch_analyze" in tool_names
    assert "demo_analyze" in tool_names
    assert "get_pricing" in tool_names
