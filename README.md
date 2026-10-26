# Student Management API with AI Agent (v2)

FastAPI + SQLAlchemy + Pydantic + local LLM (Ollama) or Gemini + n8n.
Built from the EWB "AI/ML vs Future AI Agents" notes, Days 1 to 10.

## What it does

- Full CRUD for students (create, read, update, delete)
- `/query-ai`: ask questions about the student records; an AI answers (with chat memory)
- `/chat`: a simple chat web page (works on phone and laptop)
- n8n workflow: webhook -> FastAPI -> AI -> reply
- Every API call is logged to `logs/app.log`

## Architecture

```
Phone / Laptop  ->  n8n webhook  ->  FastAPI /query-ai  ->  Ollama (local)  or  Gemini (cloud)
                                          |
                                      SQLite students.db
```

## Folder structure (Day 7)

```
main.py                    app entry point (also request logging)
.env.example               copy to .env
requirements.txt           packages for the local setup
requirements-gemini.txt    adds the Gemini package (used on Render)
n8n_workflow.json          import into n8n
render.yaml                public deploy config (Render)
seed.py                    adds 5 sample students
scripts/call_n8n.py        call n8n from Python (Day 5)
deploy/Caddyfile           reverse proxy (Day 6)
deploy/student-ai.service  systemd service (Day 6)
app/
  config.py                reads .env with pydantic-settings (Day 7)
  database.py  model.py  schema.py  logger.py  seed.py
  services/llm_service.py  AI logic + chat memory (Day 3, 4)
  routes/
    base.py                registers all routers
    create_student.py  get_student.py  update_student.py  delete_student.py
    ai_query.py  chat_page.py
  static/chat.html
```

## Run locally (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
ollama pull llama3.2
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000/chat or http://127.0.0.1:8000/docs
On your phone (same Wi-Fi): `http://<laptop-IP>:8000/chat` (find the IP with `ipconfig`).

### n8n

```powershell
npx n8n
```
Open http://localhost:5678, import `n8n_workflow.json`, **Save**, **Publish**. Then:

```powershell
python scripts/call_n8n.py --question "Which students are in class 10?"
```

## Use Gemini instead of Ollama

1. Get a key at https://aistudio.google.com (Get API key).
2. In `.env` set `LLM_PROVIDER=gemini` and `GOOGLE_API_KEY=your-key`.
3. `pip install -r requirements-gemini.txt`
4. If you get a 404 model error, change `GEMINI_MODEL` (for example to another flash or pro model).

## Public live link (for submission)

**Option A: Render (stays online, laptop can be off).** Uses Gemini.
1. Push this folder to GitHub (without `.env`).
2. On render.com: New > Blueprint (or Web Service) > connect the repo. `render.yaml` sets everything.
3. In Render's Environment tab add `GOOGLE_API_KEY`.
4. Your link is `https://<name>.onrender.com/chat`. The free plan sleeps when idle, so the first open can take about a minute. Its database resets when it restarts; `SEED_DEMO_DATA=true` re-adds the sample students.

**Option B: temporary link from your laptop (uses local Ollama).** Works only while your laptop and the terminals are running.
```powershell
cloudflared tunnel --url http://localhost:8000
```
It prints a `https://....trycloudflare.com` link. Use `/chat` on that link. Do not expose n8n this way.

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named ...` | Activate the venv, then `pip install -r requirements.txt` |
| 503 on `/query-ai` | Ollama: run `ollama serve`. Gemini: check `GOOGLE_API_KEY` and `GEMINI_MODEL` |
| 422 | A field is missing or has the wrong type |
| n8n "connection refused" | FastAPI is not running, or the HTTP node URL is not `http://127.0.0.1:8000/query-ai` |
| n8n webhook 404 | Workflow is not Published |
