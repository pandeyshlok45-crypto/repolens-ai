# RepoLens AI 🧭
> **Best Open-Source AI Project — Official MLH Challenge • Hacktoberfest Hack Day (Hyderabad)**  
> *MLH × DEV × React Hyderabad*

RepoLens AI is an open-source contributor intelligence engine and agent harness powered by open-weight models (`Llama-3.1-8B` and `Qwen-2.5-Coder`). It transforms the daunting friction of contributing to unfamiliar open-source codebases into an intuitive, guided workflow — translating complex issue descriptions and repository file hierarchies into actionable Pull Request blueprints, unified diff patches, and verified test specifications.

---

## 🌟 Why Open-Source AI is Central to the Architecture

Unlike superficial coding assistants or decorative wrappers, GitCompass builds open-source AI directly into the operational pipeline:

1. **Agent Skill Open Standard Compliance**:
   Exposes discovery and execution metadata at `/skill` strictly adhering to the [Agent Skill Open Standard (v1.0.0)](https://agentskills.org/v1/skill.json). Any external orchestrator or autonomous agent can discover, invoke, and inspect GitCompass capabilities.

2. **Open-Weight Model Reasoning Harness**:
   Interfaces directly with open-weight foundation models:
   - **Qwen-2.5-Coder (7B/32B)** for deep AST-level syntax reasoning and unified diff generation.
   - **Llama-3.1 (8B-Instruct)** for architectural component mapping, root cause deduction, and conventional commit drafting.
   - Runs locally on Ollama/vLLM (100% offline & private) or via high-throughput open-weight API endpoints (Groq / Hugging Face TGI).

3. **Deterministic AST & Topology Ingestion**:
   Parses repository file trees, identifies target subsystem boundaries, and generates structured execution plans with verifiable test cases before any pull request is opened.

---

## 🏗️ System Architecture

```
                          +------------------------------------------+
                          |   React + Tailwind Contributor Dashboard  |
                          +------------------------------------------+
                                               |
                                               v  REST / JSON
                          +------------------------------------------+
                          |        GitCompass FastAPI Harness        |
                          +------------------------------------------+
                                /              |              \
                               v               v               v
                +---------------------+ +-------------+ +--------------------+
                |  Agent Skill Spec   | | File Tree   | | Unified Diff       |
                |  (agentskills.org)  | | AST Ingest  | | Patch Synthesizer  |
                +---------------------+ +-------------+ +--------------------+
                                               |
                                               v
                          +------------------------------------------+
                          |     Open-Weight Inference Engine         |
                          | (Ollama / Groq: Llama 3.1 & Qwen 2.5)    |
                          +------------------------------------------+
```

---

## 🚀 Quickstart (Under 2 Minutes)

### Prerequisites
- Python 3.10+
- (Optional) [Ollama](https://ollama.ai) for local execution, OR a free [Groq API Key](https://console.groq.com)

### 1. Start the Backend Agent Harness
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Choose your open-weight provider:
# Option A: Groq (Instant cloud open-weight Llama 3.1)
export MODEL_PROVIDER="groq"
export GROQ_API_KEY="your-groq-api-key"

# Option B: Ollama (100% local, private, offline)
# export MODEL_PROVIDER="ollama"
# export DEFAULT_MODEL="qwen2.5-coder:7b"

uvicorn main:app --reload --port 8000
```

### 2. Launch the Contributor Interface
In a new terminal:
```bash
cd frontend
# Serve frontend via Python HTTP server:
python3 -m http.server 3000
```
Open **http://localhost:3000** in your browser.

---

## 🔬 Agent Skill Manifest & Open Endpoints

- `GET /skill` — Returns Agent Skill Open Standard manifest describing inputs, outputs, and capabilities.
- `POST /api/triage` — Ingests `{ repo_name, file_tree, issue_title, issue_body }` and produces structured triage blueprints.
- `GET /api/health` — Sanity check verifying open-weight model provider and readiness.

---

## 🎬 2-Minute Hackathon Demo Script for Judges

1. **Dashboard Overview**: Launch dashboard showing pre-configured open-source issue presets (Express router crash, React DevTools hook warning, Flask request context).
2. **Execute Live Triage**: Click **"Analyze & Generate PR Blueprint"** to trigger the open-weight model harness.
3. **Inspect Output**:
   - High-level architecture context and root cause analysis.
   - Identified target files to touch.
   - Step-by-step PR implementation gameplan.
   - Required automated test assertions.
   - Formatted conventional commit string.
4. **Agent Skill Compliance**: Open `http://localhost:8000/skill` in a browser tab to demonstrate Agent Skill Open Standard discovery metadata.

---

## 📄 License
Released under the [MIT License](LICENSE). Built for the MLH Hack Day Hacktoberfest Challenge.