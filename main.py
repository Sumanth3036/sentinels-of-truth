from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.config import OUTPUT_DIR
from app.docgen import generate_docx
from app.executor import draft_content, execute_plan
from app.planner import create_plan

app = FastAPI(title="Autonomous Document Agent", version="1.0.0")


class AgentRequest(BaseModel):
    request: str = Field(..., min_length=1, description="Natural-language business document request")


class AgentResponse(BaseModel):
    plan: dict
    steps_executed: list[dict]
    document_path: str
    summary: str


@app.post("/agent", response_model=AgentResponse)
async def run_agent(body: AgentRequest) -> AgentResponse:
    plan = create_plan(body.request)
    steps_executed, context = execute_plan(plan)
    content = draft_content(plan, context)
    document_path = generate_docx(plan.get("title", "Document"), content)

    doc_type = plan.get("document_type", "document")
    title = plan.get("title", "Untitled")
    summary = (
        f"Generated a {doc_type.replace('_', ' ')} titled \"{title}\" "
        f"with {len(content.get('sections', []))} sections after executing {len(steps_executed)} planned steps."
    )

    return AgentResponse(
        plan=plan,
        steps_executed=steps_executed,
        document_path=document_path,
        summary=summary,
    )


@app.get("/agent/download/{filename}")
async def download_document(filename: str):
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    filepath = Path(OUTPUT_DIR) / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
