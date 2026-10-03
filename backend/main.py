"""
GitCompass Core Agent Harness
Powered by Open-Weight Models (Qwen 2.5 Coder & Llama 3.1)
Compliant with Agent Skill Open Standard
"""

import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

app = FastAPI(
    title="GitCompass - Open-Weight OSS Contributor Agent",
    description="Agent harness and skill for onboarding and triaging open-source repositories.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama-3.1-8b-instant")

SKILL_METADATA = {
    "$schema": "https://agentskills.org/v1/skill.json",
    "name": "gitcompass_triage",
    "version": "1.0.0",
    "description": "Analyzes open-source repo context and maps GitHub issues to file changes, test requirements, and PR blueprints.",
    "author": "GitCompass Contributors",
    "license": "MIT",
    "inputs": {
        "repo_name": {"type": "string", "description": "e.g., owner/repo"},
        "file_tree": {"type": "array", "items": {"type": "string"}},
        "issue_title": {"type": "string"},
        "issue_body": {"type": "string"}
    },
    "outputs": {
        "architecture_summary": {"type": "string"},
        "target_files": {"type": "array", "items": {"type": "string"}},
        "root_cause_or_design": {"type": "string"},
        "pr_gameplan": {"type": "array", "items": {"type": "string"}},
        "test_cases": {"type": "array", "items": {"type": "string"}},
        "commit_message": {"type": "string"}
    }
}

class TriageRequest(BaseModel):
    repo_name: str = Field(..., example="expressjs/express")
    file_tree: List[str] = Field(..., example=["lib/router/index.js", "lib/application.js", "test/app.test.js"])
    issue_title: str = Field(..., example="TypeError: Router.use() requires a middleware function")
    issue_body: str = Field(..., example="Passing undefined to app.use crashes instead of warning with a clear message.")

class TriageResponse(BaseModel):
    status: str
    model_used: str
    analysis: Dict[str, Any]

async def query_open_weight_model(prompt: str, system_prompt: str) -> str:
    """Connects to open-weight LLMs via Groq (Llama 3.1) or local Ollama (Qwen 2.5 Coder)."""
    if MODEL_PROVIDER == "groq":
        if not GROQ_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY environment variable is missing. Set it or set MODEL_PROVIDER=ollama."
            )
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": DEFAULT_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail=resp.text)
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    elif MODEL_PROVIDER == "ollama":
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": "qwen2.5-coder:7b" if DEFAULT_MODEL == "llama-3.1-8b-instant" else DEFAULT_MODEL,
            "prompt": f"{system_prompt}\n\nTask:\n{prompt}",
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.2}
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Failed to connect to local Ollama instance.")
            return resp.json()["response"]
    else:
        raise HTTPException(status_code=400, detail="Invalid MODEL_PROVIDER specified.")

@app.get("/skill")
def get_agent_skill_manifest():
    """Agent Skill Open Standard discovery endpoint."""
    return SKILL_METADATA

@app.post("/api/triage", response_model=TriageResponse)
async def triage_issue(req: TriageRequest):
    system_prompt = (
        "You are GitCompass, an elite open-source senior maintainer and triage agent. "
        "Analyze an open-source repository context and a contributor's issue, "
        "then provide an exact, actionable Pull Request gameplan. "
        "You MUST respond ONLY with valid JSON strictly adhering to the schema:\n"
        "{\n"
        '  "architecture_summary": "Short explanation of relevant components and dataflow",\n'
        '  "target_files": ["list", "of", "exact", "files", "to", "modify"],\n'
        '  "root_cause_or_design": "Detailed rationale for the fix or enhancement",\n'
        '  "pr_gameplan": ["Step 1...", "Step 2...", "Step 3..."],\n'
        '  "test_cases": ["Test 1 description and assertion", "Test 2 description"],\n'
        '  "commit_message": "Conventional commit style string (e.g. fix(router): validate middleware parameter)"\n'
        "}"
    )

    user_prompt = f"""Repository: {req.repo_name}
File Structure Overview:
{json.dumps(req.file_tree, indent=2)}

Issue Title: {req.issue_title}
Issue Description:
{req.issue_body}

Analyze which files to touch, outline the step-by-step PR implementation, identify tests that must be added, and generate a standardized conventional commit message."""

    raw_response = await query_open_weight_model(user_prompt, system_prompt)
    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Open-weight model did not return valid JSON.")

    return TriageResponse(
        status="success",
        model_used=DEFAULT_MODEL,
        analysis=parsed
    )

@app.get("/api/health")
def health_check():
    return {"status": "ok", "provider": MODEL_PROVIDER, "model": DEFAULT_MODEL}
