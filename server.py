"""
Intelica MCP Server — Competitive Intelligence for AI Agents

Exposes competitive intelligence analysis as MCP tools.
Payments are handled automatically via the x402 protocol (USDC on Base mainnet).
No API keys required — agents pay $0.05 USDC per analysis autonomously.

Endpoint: https://intelica.onrender.com/mcp
Transport: Streamable HTTP (MCP 2024-11-05)
"""

import os
import json
import httpx
from typing import Optional
from mcp.server.fastmcp import FastMCP

# ── Config ────────────────────────────────────────────────────────────────────
INTELICA_BASE_URL = os.environ.get("INTELICA_BASE_URL", "https://intelica.onrender.com")
EVM_PRIVATE_KEY   = os.environ.get("EVM_PRIVATE_KEY", "")   # Required for paid tools

# ── FastMCP Server ────────────────────────────────────────────────────────────
mcp = FastMCP(
    name="Intelica",
    instructions="""
Intelica provides competitive intelligence analysis for AI agents.

Send any URL or text description of a product, company, or service and receive
structured intelligence: market positioning, user pain points, detected competitors,
and unique market angles.

Pricing:
- analyze_competitor: $0.05 USDC per call (Base mainnet, via x402)
- batch_analyze: $0.20 USDC for up to 10 analyses in parallel
- get_pricing: Free

Payments are handled automatically via the x402 protocol if EVM_PRIVATE_KEY
is configured. No accounts, no API keys, no subscriptions required.

Best for:
- Research agents building competitive reports
- Outreach agents personalizing messages before contacting prospects
- Due diligence agents evaluating startups or vendors
- Product intelligence agents monitoring competitor positioning
""",
    stateless_http=True,
    json_response=True,
)


# ── x402 Payment helper ───────────────────────────────────────────────────────
async def _call_intelica(endpoint: str, payload: dict) -> dict:
    """
    Makes an x402-authenticated request to the Intelica API.

    If EVM_PRIVATE_KEY is set, handles payment automatically via x402.
    Falls back to direct call (will return 402 if payment required).
    """
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
            pass  # Fall through to direct call

    # Direct call without payment (for testing or if x402 not installed)
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        if response.status_code == 402:
            return {
                "error": "Payment required",
                "message": "Set EVM_PRIVATE_KEY environment variable to enable automatic x402 payments.",
                "price": "$0.05 USDC on Base mainnet",
                "docs": f"{INTELICA_BASE_URL}/docs",
            }
        return response.json()


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
async def analyze_competitor(
    url: Optional[str] = None,
    text: Optional[str] = None,
    context: Optional[str] = None,
) -> str:
    """
    Analyzes a competitor's URL or text description and returns structured
    competitive intelligence as JSON.

    Cost: $0.05 USDC per call, paid automatically via x402 on Base mainnet.
    Response time: 2-5 seconds (first call), <1 second (cached within 6 hours).

    Returns a JSON object with these fields:
    - company_or_product (str): Identified name of the company or product
    - positioning_summary (str): 2-3 sentence description of market positioning
    - target_customer (str): Primary customer segment being targeted
    - core_value_props (list[str]): Top 3 value propositions
    - user_pain_points (list[str]): Top 3 problems users experience
    - detected_competitors (list[str]): Up to 6 detected competitors
    - unique_angle (str): One specific differentiator or exploitable gap
    - tone (str): Brand tone — "professional", "casual", "technical", or "aggressive"
    - confidence (str): Analysis confidence — "high", "medium", or "low"

    Parameters:
    - url: Full URL of the product or company to analyze (e.g. "https://notion.so").
      The server fetches and parses the page automatically.
    - text: Raw text description to analyze (alternative to url).
      Minimum 50 characters for reliable results.
    - context: Optional context about your own product or use case.
      Example: "I'm building a note-taking app for developers."
      Providing context improves the relevance of unique_angle.

    At least one of url or text is required.

    Example usage:
    - analyze_competitor(url="https://linear.app")
    - analyze_competitor(text="Figma is a collaborative design tool for product teams")
    - analyze_competitor(url="https://notion.so", context="Building a wiki tool for engineers")

    Note: Results are cached for 6 hours. Repeated calls for the same input
    return instantly at the same price.
    """
    if not url and not text:
        return json.dumps({
            "error": "Missing input",
            "message": "Provide either 'url' or 'text' parameter.",
        })

    payload = {}
    if url:
        payload["url"] = url
    if text:
        payload["text"] = text
    if context:
        payload["context"] = context

    result = await _call_intelica("/intel", payload)
    return json.dumps(result, indent=2)


@mcp.tool()
async def batch_analyze(
    items: list[dict],
) -> str:
    """
    Analyzes up to 10 competitors in parallel in a single call.

    Cost: $0.20 USDC flat for the entire batch (regardless of item count),
    paid automatically via x402 on Base mainnet. More efficient than calling
    analyze_competitor 10 times ($0.50 USDC).

    Each item in the batch is processed in parallel, so total time is similar
    to a single analysis (2-5 seconds) regardless of batch size.

    Returns a JSON object with:
    - results (list): Array of analysis results, one per item
      - id (str): The id you provided, or the item index as string
      - source (str): The url or "provided_text"
      - analysis (object): Same structure as analyze_competitor output
      - cached (bool): Whether this result was served from cache
    - total (int): Number of items processed
    - cached (int): Number of items served from cache
    - response_ms (int): Total processing time in milliseconds
    - price_paid_usdc (str): Total price paid ("0.20")

    Parameters:
    - items (list[dict]): List of up to 10 analysis requests. Each item can have:
      - url (str, optional): URL to analyze
      - text (str, optional): Text description to analyze
      - context (str, optional): Your product context for relevance
      - id (str, optional): Identifier to track items in the response

    Example usage:
    batch_analyze(items=[
        {"url": "https://notion.so", "id": "notion"},
        {"url": "https://coda.io", "id": "coda"},
        {"text": "Obsidian is a local-first note-taking app", "id": "obsidian"},
    ])

    Best for:
    - Due diligence: analyze all competitors in a market in one call
    - Weekly monitoring: check 5-10 competitors every Monday
    - Market mapping: build a full competitive landscape in seconds
    """
    if not items:
        return json.dumps({
            "error": "Missing items",
            "message": "Provide a list of items to analyze.",
        })

    if len(items) > 10:
        return json.dumps({
            "error": "Too many items",
            "message": f"Maximum 10 items per batch. You provided {len(items)}.",
        })

    result = await _call_intelica("/batch", {"items": items})
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_pricing() -> str:
    """
    Returns current pricing, available endpoints, network configuration,
    and wallet addresses for the Intelica API.

    Free to call — no payment required.

    Returns a JSON object with:
    - single (object): Pricing for POST /intel (single analysis)
      - price (str): "$0.05 USDC"
      - max_items (int): 1
    - batch (object): Pricing for POST /batch (batch analysis)
      - price (str): "$0.20 USDC"
      - max_items (int): 10
    - demo (object): Pricing for POST /demo (free demo)
      - price (str): "free"
      - limit (str): "300 chars, no URL"
    - network (str): Payment network in CAIP-2 format ("eip155:8453" = Base mainnet)
    - pay_to (str): EVM wallet address receiving payments
    - asset (str): Payment asset ("USDC")
    - protocol (str): Payment protocol ("x402")

    Use this tool to:
    - Verify current prices before making calls
    - Get the wallet address for manual payment verification
    - Confirm network and asset configuration

    Example usage:
    get_pricing()
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{INTELICA_BASE_URL}/pricing")
        return json.dumps(response.json(), indent=2)


@mcp.tool()
async def demo_analyze(text: str) -> str:
    """
    Runs a free competitive intelligence analysis on a short text description.

    No payment required. Limited to 300 characters of text input.
    Does not support URL fetching (use analyze_competitor for URLs).
    Results may be cached from previous calls.

    Returns the same JSON structure as analyze_competitor:
    - company_or_product, positioning_summary, target_customer,
      core_value_props, user_pain_points, detected_competitors,
      unique_angle, tone, confidence

    Parameters:
    - text (str): Text description of the product or company to analyze.
      Maximum 300 characters. For longer texts or URL analysis, use
      analyze_competitor (paid, $0.05 USDC).

    Example usage:
    demo_analyze(text="Linear is a fast project management tool for software teams")
    demo_analyze(text="Stripe is a payment processing platform for developers")

    Note: This is a demonstration endpoint. For production agent workflows,
    use analyze_competitor or batch_analyze with x402 payment.
    """
    if not text:
        return json.dumps({
            "error": "Missing text",
            "message": "Provide a text description to analyze.",
        })

    if len(text) > 300:
        text = text[:300]

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{INTELICA_BASE_URL}/demo",
            json={"text": text},
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
        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
        )
