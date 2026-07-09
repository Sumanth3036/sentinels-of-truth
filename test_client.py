"""Send the two required test requests and save returned documents."""

import json
import sys
from pathlib import Path

import httpx

BASE_URL = "http://127.0.0.1:8000"

TEST_REQUESTS = [
    {
        "name": "standard_meeting_minutes",
        "request": (
            "Create meeting minutes for a product sync between engineering and design "
            "about the Q3 mobile app redesign."
        ),
    },
    {
        "name": "complex_ambiguous",
        "request": "We need something for the new client about our platform, make it look professional.",
    },
]


def run_tests(base_url: str = BASE_URL) -> None:
    output_dir = Path("test_outputs")
    output_dir.mkdir(exist_ok=True)

    for i, test in enumerate(TEST_REQUESTS, 1):
        print(f"\n{'=' * 60}")
        print(f"Test {i}: {test['name']}")
        print(f"Request: {test['request']}")
        print("=" * 60)

        response = httpx.post(
            f"{base_url}/agent",
            json={"request": test["request"]},
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()

        result_path = output_dir / f"{test['name']}_response.json"
        result_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Response saved to {result_path}")

        print(f"\nDocument type: {data['plan'].get('document_type')}")
        print(f"Title: {data['plan'].get('title')}")
        print(f"Assumptions: {data['plan'].get('assumptions')}")
        print(f"Summary: {data['summary']}")
        print(f"Document: {data['document_path']}")

        doc_filename = Path(data["document_path"]).name
        download = httpx.get(f"{base_url}/agent/download/{doc_filename}", timeout=30.0)
        download.raise_for_status()
        saved_doc = output_dir / doc_filename
        saved_doc.write_bytes(download.content)
        print(f"Downloaded doc to {saved_doc}")


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    run_tests(url)
