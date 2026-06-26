<p align="center">
  <img src="https://raw.githubusercontent.com/teodorofodocrispin-cmyk/Intelica-docs/main/ChatGPT%20Image%207%20jun%202026%2C%2003_21_28%20p.m..png" alt="Intelica Logo" width="200"/>
</p>

# Intelica MCP Server

[![Glama](https://glama.ai/mcp/servers/teodorofodocrispin-cmyk/intelica-mcp/badges/score.svg)](https://glama.ai/mcp/servers/teodorofodocrispin-cmyk/intelica-mcp)
[![Smithery](https://smithery.ai/badge/@teodorofodocrispin-cmyk/intelica-mcp)](https://smithery.ai/server/@teodorofodocrispin-cmyk/intelica-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

**Competitive intelligence for autonomous AI agents — pay $0.05–$1.00 USDC per analysis via x402. No accounts, no API keys.**

Analyze any URL or company description and get structured JSON with market positioning, competitors, moat scoring (IMI), and an **executable action plan** — all in one call.

## What you get per call

```json
{
  "trace_id": "uuid-v4",
  "span_metadata": { "service.name": "intelica", "intelica.latency_ms": 1240, "..." },
  "intelica_moat_index": 0.72,
  "decision_recommendation": { "action": "partner", "confidence_score": 0.85, "risk_level": "medium" },
  "action_plan": {
    "objective": "Structure partnership with Stripe within 21 days",
    "steps": [
      { "step": 1, "action": "Run partnership analysis", "owner": "bd", "deadline_days": 7, "tool_hint": "POST /intel mode=partnership" },
      { "step": 2, "action": "Define integration surface", "owner": "product", "deadline_days": 14 }
    ],
    "sop_version": "1.0"
  },
  "next_action_trigger": { "recheck_in_days": 21, "pulse_available": true }
}
```

## Quick start — no wallet needed

```bash
# 1. Get a free trial key (5 calls)
curl https://api.intelica.dev/api-keys/trial

# 2. Analyze any company
curl -X POST https://api.intelica.dev/intel \
  -H "X-API-KEY: ikey_trial_..." \
  -H "Content-Type: application/json" \
  -d '{"text": "Stripe payment API for developers", "mode": "competitive"}'
```

## Install via Smithery

```bash
npx -y @smithery/cli install @teodorofodocrispin-cmyk/intelica-mcp
```

## MCP endpoint

```
https://api.intelica.dev/mcp
```

Transport: HTTP JSON-RPC 2.0. Tools: `intel_analyze`, `intel_batch`, `intel_demo`.

## Pricing

| Mode | Price | Model |
|---|---|---|
| Standard (competitive, market_entry, fundraising…) | $0.05 USDC | claude-haiku |
| Elite (regulatory_compliance, venture_screening, risk_assessment…) | $1.00 USDC | claude-sonnet |
| Batch (up to 10 companies) | $0.20 USDC | claude-haiku |
| Trial | Free (5 calls) | claude-haiku |

## Payment methods

- **x402** — autonomous USDC on Base or Solana (agents pay per call, no setup)
- **X-API-KEY** — pre-loaded USDC balance (best for pipelines)
- **Trial key** — 5 free calls, no wallet: `GET https://api.intelica.dev/api-keys/trial`

## Enterprise features (v4.5.6)

- `trace_id` — UUID v4 per request for log correlation
- `span_metadata` — OpenTelemetry-compatible (Datadog, Honeycomb, Grafana-ready)
- `action_plan` — SOP with actionable steps, owners, deadlines per decision
- `decision_recommendation` — enter / avoid / monitor / acquire / partner
- `next_action_trigger` — tells agents when to re-call
- `sources_cited` — verified URLs for every claim
- Competitive Graph — 3,744+ companies benchmarked

## Links

- API: https://api.intelica.dev
- Docs: https://api.intelica.dev/llms-full.txt
- Demo: https://teodorofodocrispin-cmyk.github.io/Intelica-docs/startup-validator/demo.html
- x402 spec: https://x402.org
