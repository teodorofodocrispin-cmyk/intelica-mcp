"""
Intelica MCP Server — Competitive Intelligence for AI Agents

Exposes competitive intelligence analysis as MCP tools.
Payments are handled automatically via the x402 protocol (USDC on Base mainnet).
No API keys required — agents pay $0.05 USDC per analysis autonomously.

Endpoint: https://api.intelica.dev/mcp
Transport: Streamable HTTP (MCP 2024-11-05)
"""

import os
import json
import httpx
from typing import Optional, Literal
from mcp.server.fastmcp import FastMCP

# ── Config ────────────────────────────────────────────────────────────────────
INTELICA_BASE_URL = os.environ.get("INTELICA_BASE_URL", "https://api.intelica.dev")
EVM_PRIVATE_KEY   = os.environ.get("EVM_PRIVATE_KEY", "")   # Required for paid tools

# ── FastMCP Server ────────────────────────────────────────────────────────────
mcp = FastMCP(
    name="Intelica",
    instructions="""
Intelica provides competitive intelligence for autonomous AI agents.

Send any URL or text description and receive structured JSON with market positioning,
pain points, competitors, battlecard, verified sources, and executable Market Score.

Pricing:
- analyze_competitor: $0.05 USDC (standard modes) or $1.00 USDC (elite modes)
- analyze_competitor with format=report: $0.50 USDC (HTML report for humans)
- batch_analyze: $0.20 USDC for up to 10 analyses
- demo_analyze: Free (300 char limit)

Standard modes ($0.05): competitive, fundraising, partnership, acquisition, market_entry, crypto_protocol
Elite modes ($1.00): venture_screening, regulatory_compliance, risk_assessment, sales_enablement

Payments via x402 on Base mainnet or Solana mainnet.
""",
    stateless_http=True,
    json_response=True,
)


# ── x402 Payment helper ───────────────────────────────────────────────────────
async def _call_intelica(endpoint: str, payload: dict) -> dict:
    url = f"{INTELICA_BASE_URL}{endpoint}"

    if EVM_PRIVATE_KEY:
        try:
            from x402 import x402Client
            from x402.http.clients import x402HttpxClient
            from x402.mechanisms.evm import EthAccountSigner
            from x402.mechanisms.evm.exact.register import register_exact_evm_client
            from eth_account import Account

            account = Account.from_key(EVM_PRIVATE_KEY)
            client = x402Client()
            register_exact_evm_client(client, EthAccountSigner(account))

            async with x402HttpxClient(client) as http:
                response = await http.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                await response.aread()
                return response.json()
        except ImportError:
            pass

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        if response.status_code == 402:
            return {
                "error": "Payment required",
                "message": "Set EVM_PRIVATE_KEY environment variable to enable automatic x402 payments.",
                "price": "$0.05–$1.00 USDC on Base or Solana mainnet",
                "docs": f"{INTELICA_BASE_URL}/docs",
            }
        return response.json()


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
async def analyze_competitor(
    url: Optional[str] = None,
    text: Optional[str] = None,
    context: Optional[str] = None,
    mode: Optional[str] = "competitive",
    format: Optional[str] = "json",
    force_refresh: Optional[bool] = False,
) -> str:
    """
    Analyzes a competitor URL or text and returns structured competitive intelligence.

    Cost:
    - Standard modes (competitive, fundraising, partnership, acquisition,
      market_entry, crypto_protocol): $0.05 USDC
    - Elite modes (venture_screening, regulatory_compliance, risk_assessment,
      sales_enablement): $1.00 USDC
    - format=report (HTML for humans): $0.50 USDC

    Returns JSON with:
    - company_or_product, positioning_summary, target_customer
    - core_value_props, user_pain_points, detected_competitors
    - unique_angle, tone, confidence
    - sources[] — verified URLs from Exa web search
    - battlecard (sales_enablement mode only): headline, their_weakness,
      your_angle, proof_point, objection_handler
    - market_score: threat_level, moat_strength, market_maturity, agent_recommendation
    - trend: status (new/stable/changed) + changes[]

    Parameters:
    - url: Full URL to analyze (e.g. "https://notion.so")
    - text: Text description (min 50 chars, alternative to url)
    - context: Your product context for better unique_angle
    - mode: Analysis mode — see options below
    - format: "json" (default, for agents) or "report" (HTML for humans)
    - force_refresh: True to bypass 6h cache for fast-moving markets

    Available modes:
    Standard ($0.05): competitive, fundraising, partnership, acquisition,
                      market_entry, crypto_protocol
    Elite ($1.00): venture_screening, regulatory_compliance,
                   risk_assessment, sales_enablement

    Examples:
    - analyze_competitor(url="https://linear.app", mode="competitive")
    - analyze_competitor(text="Uniswap is a DEX on Ethereum", mode="crypto_protocol")
    - analyze_competitor(url="https://notion.so", mode="sales_enablement")
    - analyze_competitor(text="OpenAI GPT-4", mode="venture_screening")
    - analyze_competitor(text="Clearview AI", mode="regulatory_compliance")
    - analyze_competitor(url="https://competitor.com", format="report")
    """
    if not url and not text:
        return json.dumps({"error": "Provide either 'url' or 'text'."})

    payload = {}
    if url:
        payload["url"] = url
    if text:
        payload["text"] = text
    if context:
        payload["context"] = context
    if mode:
        payload["mode"] = mode
    if format:
        payload["format"] = format
    if force_refresh:
        payload["force_refresh"] = force_refresh

    result = await _call_intelica("/intel", payload)
    return json.dumps(result, indent=2)


@mcp.tool()
async def batch_analyze(items: list[dict]) -> str:
    """
    Analyzes up to 10 competitors in parallel for $0.20 USDC flat.

    Each item can have: url, text, context, mode, id
    Returns array of analysis results with market_score per item.

    Example:
    batch_analyze(items=[
        {"url": "https://notion.so", "id": "notion", "mode": "competitive"},
        {"url": "https://coda.io", "id": "coda", "mode": "sales_enablement"},
        {"text": "Obsidian local-first notes", "id": "obsidian"},
    ])
    """
    if not items:
        return json.dumps({"error": "Provide a list of items."})
    if len(items) > 10:
        return json.dumps({"error": f"Max 10 items. You provided {len(items)}."})

    result = await _call_intelica("/batch", {"items": items})
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_pricing() -> str:
    """
    Returns current pricing, endpoints, network config, and wallet addresses.
    Free — no payment required.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{INTELICA_BASE_URL}/pricing")
        return json.dumps(response.json(), indent=2)


@mcp.tool()
async def demo_analyze(text: str, mode: Optional[str] = "competitive") -> str:
    """
    Free competitive intelligence analysis. 300 character limit. No URL support.

    All 10 modes available in demo:
    competitive, fundraising, partnership, acquisition, market_entry,
    crypto_protocol, venture_screening, regulatory_compliance,
    risk_assessment, sales_enablement

    Example:
    demo_analyze(text="Stripe is a payment API for developers", mode="competitive")
    demo_analyze(text="Uniswap v4 decentralized exchange", mode="crypto_protocol")
    """
    if not text:
        return json.dumps({"error": "Provide text to analyze."})

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{INTELICA_BASE_URL}/demo",
            json={"text": text[:300], "mode": mode or "competitive"},
        )
        return json.dumps(response.json(), indent=2)


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Intelica MCP Server")
    parser.add_argument("--transport", default="streamable-http", choices=["stdio", "streamable-http"])
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
