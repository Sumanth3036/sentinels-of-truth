from datetime import date
from typing import Any, Callable

MOCK_DATA: dict[str, dict[str, Any]] = {
    "meeting_attendees": {
        "title": "Product Sync Attendees",
        "attendees": [
            {"name": "Sarah Chen", "role": "Engineering Lead", "team": "Engineering"},
            {"name": "Marcus Rivera", "role": "Senior Designer", "team": "Design"},
            {"name": "Priya Patel", "role": "Product Manager", "team": "Product"},
            {"name": "Alex Kim", "role": "Mobile Engineer", "team": "Engineering"},
            {"name": "Jordan Lee", "role": "UX Researcher", "team": "Design"},
        ],
        "meeting_date": "2026-07-08",
        "location": "Conference Room B / Zoom",
    },
    "q3_mobile_redesign": {
        "project": "Q3 Mobile App Redesign",
        "timeline": [
            {"phase": "Discovery & Research", "start": "2026-07-01", "end": "2026-07-21"},
            {"phase": "Wireframes & Prototypes", "start": "2026-07-22", "end": "2026-08-18"},
            {"phase": "Development Sprint 1", "start": "2026-08-19", "end": "2026-09-15"},
            {"phase": "QA & Beta Launch", "start": "2026-09-16", "end": "2026-09-30"},
        ],
        "budget_usd": 185000,
        "key_goals": [
            "Reduce onboarding drop-off by 25%",
            "Improve navigation clarity based on user testing",
            "Ship dark mode and accessibility improvements",
        ],
    },
    "platform_overview": {
        "product_name": "CloudSync Platform",
        "tagline": "Unified workflow automation for modern teams",
        "features": [
            "Real-time collaboration dashboards",
            "Automated workflow orchestration",
            "Enterprise-grade security (SOC 2 Type II)",
            "API integrations with 50+ tools",
        ],
        "pricing_tiers": [
            {"name": "Starter", "price": "$29/user/mo", "seats": "Up to 10"},
            {"name": "Business", "price": "$59/user/mo", "seats": "Up to 100"},
            {"name": "Enterprise", "price": "Custom", "seats": "Unlimited"},
        ],
        "clients_served": 2400,
        "uptime_sla": "99.9%",
    },
    "project_budget": {
        "total_budget_usd": 450000,
        "allocated": {
            "engineering": 220000,
            "design": 85000,
            "infrastructure": 70000,
            "marketing": 45000,
            "contingency": 30000,
        },
        "fiscal_year": "FY2026",
    },
}


def search_mock_data(query: str) -> dict[str, Any]:
    """Return plausible fake business data matching the query."""
    query_lower = query.lower()
    results: list[dict[str, Any]] = []

    keyword_map = {
        "attendee": "meeting_attendees",
        "meeting": "meeting_attendees",
        "sync": "meeting_attendees",
        "mobile": "q3_mobile_redesign",
        "redesign": "q3_mobile_redesign",
        "q3": "q3_mobile_redesign",
        "timeline": "q3_mobile_redesign",
        "platform": "platform_overview",
        "client": "platform_overview",
        "product": "platform_overview",
        "pricing": "platform_overview",
        "budget": "project_budget",
        "cost": "project_budget",
    }

    matched_keys: set[str] = set()
    for keyword, key in keyword_map.items():
        if keyword in query_lower:
            matched_keys.add(key)

    if not matched_keys:
        matched_keys = set(MOCK_DATA.keys())

    for key in matched_keys:
        results.append({"source": key, "data": MOCK_DATA[key]})

    return {"query": query, "matches": results}


def get_current_date() -> str:
    return date.today().isoformat()


def estimate_effort(task: str) -> str:
    task_lower = task.lower()
    if any(w in task_lower for w in ("research", "discovery", "analysis")):
        return "Medium — 2-3 weeks (80-120 hours)"
    if any(w in task_lower for w in ("design", "prototype", "wireframe")):
        return "Medium-High — 3-4 weeks (120-160 hours)"
    if any(w in task_lower for w in ("develop", "implement", "build", "code")):
        return "High — 4-6 weeks (160-240 hours)"
    if any(w in task_lower for w in ("test", "qa", "review")):
        return "Low-Medium — 1-2 weeks (40-80 hours)"
    return "Medium — 2-4 weeks (80-160 hours)"


TOOL_REGISTRY: dict[str, Callable[..., Any]] = {
    "search_mock_data": search_mock_data,
    "get_current_date": get_current_date,
    "estimate_effort": estimate_effort,
}
