<p align="center">
  <img src="https://raw.githubusercontent.com/teodorofodocrispin-cmyk/Intelica-docs/main/ChatGPT%20Image%207%20jun%202026%2C%2003_21_28%20p.m..png" alt="Intelica Logo" width="200"/>
</p>

# Intelica MCP Server

[![Glama](https://glama.ai/mcp/servers/teodorofodocrispin-cmyk/intelica-mcp/badges/score.svg)](https://glama.ai/mcp/servers/teodorofodocrispin-cmyk/intelica-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

**Competitive intelligence for autonomous AI agents — pay $0.05–$1.00 USDC per analysis via x402. No accounts, no API keys.**

Analyze any URL or company description and get structured JSON with market positioning, competitors, battlecard, verified sources, and executable Market Score.

## Quick Start

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "intelica": {
      "command": "uvx",
      "args": ["intelica-mcp"],
      "env": {
        "EVM_PRIVATE_KEY": "0x_your_base_mainnet_private_key"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add intelica uvx intelica-mcp --env EVM_PRIVATE_KEY=0x_your_key
```

### Remote MCP (no install)

```json
{
  "mcpServers": {
    "intelica": {
      "url": "https://api.intelica.dev/mcp"
    }
  }
}
```

## Tools

### `analyze_competitor` — $0.05–$1.00 USDC

Analyzes a single competitor URL or text description.

```python
# Standard analysis ($0.05)
analyze_competitor(url="https://notion.so", mode="competitive")

# Sales battlecard ($1.00)
analyze_competitor(text="Notion workspace", mode="sales_enablement")

# DeFi protocol ($0.05)
analyze_competitor(text="Uniswap v4 AMM", mode="crypto_protocol", force_refresh=True)

# HTML report for humans ($0.50)
analyze_competitor(url="https://competitor.com", format="report")

# Regulatory compliance ($1.00)
analyze_competitor(text="Clearview AI biometric database", mode="regulatory_compliance")
```

**Available modes:**

| Mode | Price | Use case |
|------|-------|----------|
| `competitive` | $0.05 | General market analysis |
| `fundraising` | $0.05 | Investor narrative, TAM |
| `partnership` | $0.05 | Strategic fit evaluation |
| `acquisition` | $0.05 | M&A due diligence |
| `market_entry` | $0.05 | Market gaps, barriers |
| `crypto_protocol` | $0.05 | DeFi moat, tokenomics |
| `venture_screening` | $1.00 | Investment thesis + deal-breakers |
| `regulatory_compliance` | $1.00 | EU AI Act, GDPR, HIPAA |
| `risk_assessment` | $1.00 | Business model risk |
| `sales_enablement` | $1.00 | Battlecard + objections |

**Response includes:**

```json
{
  "analysis": {
    "company_or_product": "Notion",
    "positioning_summary": "...",
    "detected_competitors": ["Confluence", "Asana", "ClickUp"],
    "unique_angle": "...",
    "sources": ["https://...", "https://..."],
    "battlecard": {
      "headline": "...",
      "their_weakness": "...",
      "your_angle": "...",
      "proof_point": "...",
      "objection_handler": "..."
    },
    "market_score": {
      "threat_level": "high",
      "moat_strength": 0.72,
      "market_maturity": "mature",
      "agent_recommendation": "counter"
    }
  }
}
```

### `batch_analyze` — $0.20 USDC

Analyzes up to 10 competitors in parallel.

```python
batch_analyze(items=[
    {"url": "https://notion.so", "id": "notion", "mode": "competitive"},
    {"url": "https://coda.io", "id": "coda"},
    {"text": "Obsidian local-first notes", "id": "obsidian"},
])
```

### `demo_analyze` — Free

Free analysis, 300 character limit.

```python
demo_analyze(text="Stripe is a payment API for developers", mode="competitive")
```

### `get_pricing` — Free

```python
get_pricing()
```

## Payment Architecture

```
Agent calls analyze_competitor
  → Server responds HTTP 402 with payment challenge
  → x402 client signs USDC transfer (Base or Solana mainnet)
  → PayAI/CDP facilitator verifies payment on-chain
  → Server delivers analysis
```

**Networks:** Base mainnet + Solana mainnet  
**Asset:** USDC  
**Facilitators:** PayAI (primary) + Coinbase CDP (fallback)

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `EVM_PRIVATE_KEY` | Yes (paid) | Base mainnet private key |
| `INTELICA_BASE_URL` | No | Override API URL (default: `https://api.intelica.dev`) |

## Installation

```bash
# With uvx (recommended)
uvx intelica-mcp

# With pip
pip install intelica-mcp
python server.py

# With x402 payment support
pip install "intelica-mcp[x402]"
EVM_PRIVATE_KEY=0x_your_key python server.py
```

## Links

- **Live API:** https://api.intelica.dev
- **Free demo:** https://api.intelica.dev/demo
- **OpenAPI:** https://api.intelica.dev/openapi.json
- **x402 manifest:** https://api.intelica.dev/.well-known/x402.json
- **Glama MCP:** https://glama.ai/mcp/servers/teodorofodocrispin-cmyk/intelica-mcp
- **Glama Connector:** https://glama.ai/mcp/connectors/com.onrender.intelica/intelica
- **Docs:** https://github.com/teodorofodocrispin-cmyk/Intelica-docs
- **AGENTS.md:** https://github.com/teodorofodocrispin-cmyk/Intelica-docs/blob/main/AGENTS.md

---

*Built by a solo developer in Bogotá, Colombia.*  
*From the same builder behind [TrustBoost PII Sanitizer](https://api.trustboost.dev).*
