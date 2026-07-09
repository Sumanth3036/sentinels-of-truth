import json
from typing import Any

from app.llm import call_llm
from app.tools import TOOL_REGISTRY

DRAFTER_SYSTEM = """You are a professional business document writer.
Given a document plan and collected tool results, produce document content as JSON.

Return ONLY valid JSON matching this schema:
{
  "sections": [
    {"heading": "string", "body": "string"},
    {"heading": "string", "bullets": ["item1", "item2"]}
  ]
}

Each section must have either "body" (paragraph text) or "bullets" (list of strings), not both.
Write professional, specific content using the provided data. Include 4-8 sections appropriate for the document_type.
If assumptions were made, include an early section noting them briefly."""


def _call_tool(tool_name: str, tool_input: Any) -> Any:
    if tool_name == "get_current_date":
        return TOOL_REGISTRY["get_current_date"]()
    if tool_name == "search_mock_data":
        query = tool_input if isinstance(tool_input, str) else str(tool_input or "")
        return TOOL_REGISTRY["search_mock_data"](query)
    if tool_name == "estimate_effort":
        task = tool_input if isinstance(tool_input, str) else str(tool_input or "")
        return TOOL_REGISTRY["estimate_effort"](task)
    return TOOL_REGISTRY[tool_name](tool_input)


def execute_plan(plan: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    steps_executed: list[dict[str, Any]] = []
    context: dict[str, Any] = {}

    for step in plan.get("steps", []):
        tool_name = step.get("tool")
        step_record: dict[str, Any] = {
            "name": step.get("name", "Unnamed step"),
            "tool_used": tool_name,
            "result": None,
        }

        if tool_name:
            if tool_name not in TOOL_REGISTRY:
                step_record["result"] = f"Unknown tool: {tool_name}"
            else:
                try:
                    result = _call_tool(tool_name, step.get("tool_input"))
                    context[step.get("name", tool_name)] = result
                    step_record["result"] = result
                except Exception as exc:
                    step_record["result"] = f"Tool error: {exc}"
        else:
            step_record["result"] = step.get("purpose", "Reasoning step — no tool execution.")

        steps_executed.append(step_record)

    return steps_executed, context


def draft_content(plan: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    user_payload = {
        "document_type": plan.get("document_type"),
        "title": plan.get("title"),
        "assumptions": plan.get("assumptions", []),
        "tool_results": context,
    }

    try:
        return call_llm(
            system=DRAFTER_SYSTEM,
            user=json.dumps(user_payload, indent=2, default=str),
            json_mode=True,
        )
    except Exception:
        return {
            "sections": [
                {
                    "heading": "Overview",
                    "body": f"This {plan.get('document_type', 'document')} titled \"{plan.get('title', 'Untitled')}\" "
                    f"was generated based on the user request. Assumptions: {'; '.join(plan.get('assumptions', []))}",
                },
                {
                    "heading": "Key Points",
                    "bullets": [
                        "Document generated with fallback content due to drafting service unavailability.",
                        "Refer to the execution log for tool results.",
                    ],
                },
                {
                    "heading": "Collected Data",
                    "body": json.dumps(context, indent=2, default=str)[:2000],
                },
            ]
        }
