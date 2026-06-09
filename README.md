# Intelica MCP Server

[![Glama](https://glama.ai/mcp/servers/badge)](https://glama.ai/mcp/servers/teodorofodocrispin-cmyk/intelica-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![x402](https://img.shields.io/badge/payments-x402-orange.svg)](https://x402.org)

Competitive intelligence for AI agents — pay $0.05 USDC per analysis, no accounts required.

Analyze any URL or text description and get back structured JSON: market positioning, user pain points, detected competitors, and unique market angles. Payments handled automatically via the [x402 protocol](https://x402.org) on Base mainnet.

---

## Quick Start

### Claude Desktop

Add to your `claude_desktop_config.json`:

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

Connect directly to the hosted endpoint:

```
https://api.intelica.dev/mcp
```

---

## Tools

### `analyze_competitor` — $0.05 USDC

Analyzes a single competitor URL or text description.

**Parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | One of url/text | Full URL to analyze (e.g. `https://notion.so`) |
| `text` | string | One of url/text | Text description (min 50 chars) |
| `context` | string | No | Your product context for better `unique_angle` |

**Returns:**
```json
{
  "source": "https://notion.so",
  "analysis": {
    "company_or_product": "Notion",
    "positioning_summary": "All-in-one workspace combining notes, databases, and project management...",
    "target_customer": "Knowledge workers and product teams seeking unified workspace solutions",
    "core_value_props": [
      "Eliminates tool switching and fragmentation",
      "Highly customizable database system",
      "Real-time collaborative editing"
    ],
    "user_pain_points": [
      "Complex for new users",
      "Slow on large pages",
      "Inefficient designer-to-developer handoff"
    ],
    "detected_competitors": ["Obsidian", "Coda", "Confluence", "Linear", "Asana"],
    "unique_angle": "Developer-focused simplicity gap — Notion targets everyone, leaving power users underserved",
    "tone": "professional",
    "confidence": "high"
  },
  "cached": false,
  "response_ms": 4821,
  "price_paid_usdc": "0.05"
}
```

**Example:**
```
analyze_competitor(url="https://linear.app", context="Building a project management tool for remote teams")
```

---

### `batch_analyze` — $0.20 USDC

Analyzes up to 10 competitors in parallel in one call.

**Parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `items` | list[dict] | Yes | Up to 10 items, each with `url`, `text`, `context`, and optional `id` |

**Example:**
```python
batch_analyze(items=[
    {"url": "https://notion.so", "id": "notion"},
    {"url": "https://coda.io", "id": "coda"},
    {"text": "Obsidian is a local-first note-taking app", "id": "obsidian"},
    {"url": "https://roamresearch.com", "id": "roam"},
])
```

**Returns:** Array of analysis results, one per item.

---

### `demo_analyze` — Free

Free analysis, 300 character text limit, no URL support.

```
demo_analyze(text="Stripe is a payment processing platform for developers")
```

---

### `get_pricing` — Free

Returns current pricing, network configuration, and wallet addresses.

```
get_pricing()
```

---

## Configuration

| Variable | Required | Description |
|---|---|---|
| `EVM_PRIVATE_KEY` | Yes (paid tools) | Base mainnet private key for x402 payments |
| `INTELICA_BASE_URL` | No | Override API base URL (default: `https://api.intelica.dev`) |

**Getting a Base mainnet wallet:**
- [MetaMask](https://metamask.io) — add Base network, export private key
- [Coinbase Wallet](https://www.coinbase.com/wallet) — supports Base natively
- Minimum balance: ~$0.10 USDC + small ETH for gas

---

## Installation

### With uvx (recommended)

```bash
uvx intelica-mcp
```

### With pip

```bash
pip install intelica-mcp
python server.py
```

### With x402 payment support

```bash
pip install "intelica-mcp[x402]"
EVM_PRIVATE_KEY=0x_your_key python server.py
```

### Run locally for development

```bash
git clone https://github.com/teodorofodocrispin-cmyk/intelica-mcp
cd intelica-mcp
pip install -e ".[x402]"
EVM_PRIVATE_KEY=0x_your_key python server.py --transport streamable-http --port 8080
```

---

## Payment Architecture

Intelica uses the [x402 protocol](https://x402.org) for payments:

1. Agent calls `analyze_competitor` or `batch_analyze`
2. Server responds HTTP 402 with payment envelope (price, wallet, network)
3. x402 client signs USDC transfer on Base mainnet
4. PayAI facilitator verifies and settles payment on-chain
5. Server delivers analysis

**No accounts. No API keys. No subscriptions. USDC settles directly to the Intelica wallet.**

Payment network: Base mainnet (`eip155:8453`)  
Payment asset: USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)  
Facilitator: [PayAI](https://facilitator.payai.network)

---

## API Reference

Full REST API documentation: **https://api.intelica.dev/docs**

x402 manifest: **https://api.intelica.dev/.well-known/x402.json**

---

## Use Cases

**Outreach agents** — Personalize cold emails by understanding the prospect's positioning before writing.

**Due diligence agents** — Evaluate startups and vendors automatically with structured competitive data.

**Content agents** — Research competitive landscape before writing articles or landing pages.

**Product intelligence** — Monitor 10 competitors weekly via `batch_analyze` for $0.20/week.

---

## Verified On-Chain

Intelica has confirmed transactions on Base mainnet:  
[View on Basescan](https://basescan.org/address/0x1d6bA7ac2461fd0E17D6A4C7bc1c9Ce365EfC4FF#tokentxns)

---

## License

MIT — see [LICENSE](LICENSE)
