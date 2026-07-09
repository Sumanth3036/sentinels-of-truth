import json
from typing import Any

from app.llm import call_llm

PLANNER_SYSTEM = """You are a business document planning agent.
Given a user request, produce a JSON plan for generating a professional document.

Return ONLY valid JSON matching this schema:
{
  "document_type": "proposal | meeting_minutes | project_plan | business_report | technical_design | sop | product_spec | generic",
  "title": "string",
  "assumptions": ["list any assumptions made because the request was vague or incomplete"],
  "steps": [
    {"name": "string", "tool": "tool_name or null", "tool_input": "string or object or null", "purpose": "1-line reason for this step"}
  ]
}

Available tools (reference by exact name, or null for reasoning-only steps):
- search_mock_data: query string to fetch relevant business data (attendees, timelines, budgets, platform info)
- get_current_date: no input needed (use null or empty string)
- estimate_effort: task description string

If the request is ambiguous, still produce a complete plan. Fill assumptions explaining what you guessed and why.
Include 4-7 steps. Use tools where real data would help the document."""

FALLBACK_PLAN: dict[str, Any] = {
    "document_type": "generic",
    "title": "Business Report",
    "assumptions": [
        "Request details were unclear; defaulting to a generic three-section business report.",
        "Using placeholder structure due to planning service unavailability.",
    ],
    "steps": [
        {
            "name": "Gather context",
            "tool": "search_mock_data",
            "tool_input": "platform overview business data",
            "purpose": "Collect baseline business information for the report.",
        },
        {
            "name": "Set document date",
            "tool": "get_current_date",
            "tool_input": None,
            "purpose": "Anchor the report with today's date.",
        },
        {
            "name": "Outline executive summary",
            "tool": None,
            "tool_input": None,
            "purpose": "Plan the high-level overview section.",
        },
        {
            "name": "Outline key findings",
            "tool": None,
            "tool_input": None,
            "purpose": "Plan the analysis section.",
        },
        {
            "name": "Outline recommendations",
            "tool": None,
            "tool_input": None,
            "purpose": "Plan the actionable next steps section.",
        },
    ],
}


def _validate_plan(plan: dict[str, Any]) -> bool:
    required = ("document_type", "title", "assumptions", "steps")
    if not all(k in plan for k in required):
        return False
    if not isinstance(plan["steps"], list) or len(plan["steps"]) == 0:
        return False
    for step in plan["steps"]:
        if not isinstance(step, dict) or "name" not in step:
            return False
    return True


def create_plan(user_request: str) -> dict[str, Any]:
    try:
        plan = call_llm(
            system=PLANNER_SYSTEM,
            user=f"User request:\n{user_request}",
            json_mode=True,
        )
        if _validate_plan(plan):
            return plan
    except Exception:
        pass

    try:
        plan = call_llm(
            system=PLANNER_SYSTEM + "\n\nIMPORTANT: Return ONLY the JSON object, no markdown.",
            user=f"User request:\n{user_request}",
            json_mode=True,
        )
        if _validate_plan(plan):
            return plan
    except Exception:
        pass

    fallback = json.loads(json.dumps(FALLBACK_PLAN))
    fallback["assumptions"].append(f"Original request: {user_request[:200]}")
    return fallback
