# LOOP Agent - Self-Correcting Multi-Agent System

A sophisticated multi-agent system that implements **Loop Engineering** pattern using LangGraph, Groq LLM, and FastAPI. The system automatically iterates between Writer, Reviewer, and Reviser agents until quality standards are met.

---

## 🎯 Overview

LOOP Agent is a self-correcting system where:
1. **Writer Agent** generates beginner-friendly answers (120-160 words)
2. **Reviewer Agent** evaluates quality against 4 criteria
3. **Reviser Agent** improves answers based on feedback
4. **Loop Control** repeats until PASS or max revisions

The result: High-quality, well-structured answers that meet strict quality standards.

---

## ✨ Key Features

- **Multi-Agent Loop Engineering**: Writer → Reviewer → Reviser cycle
- **Automated Quality Evaluation**: 4-point quality checklist
  - Beginner-friendly language
  - Includes everyday analogy
  - Contains concrete example
  - Stays on topic
- **Modern Web UI**: Beautiful gradient interface with real-time workflow visualization
- **REST API**: Easy integration with other applications
- **Fast LLM Inference**: Groq API for 70B+ models in seconds
- **Production-Ready**: Error handling, UTF-8 support, extensible architecture
- **Responsive Design**: Works on desktop, tablet, and mobile

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser                          │
│         (HTML UI + JavaScript + CSS3)                   │
└────────────────────┬────────────────────────────────────┘
                     │ Fetch API
┌────────────────────▼────────────────────────────────────┐
│              FastAPI Server (app.py)                    │
│  - GET /  → Serve HTML UI                              │
│  - POST /api/run → Execute workflow                     │
└────────────────────┬────────────────────────────────────┘
                     │ Jinja2 Templates
┌────────────────────▼────────────────────────────────────┐
│          LangGraph Workflow (backend.py)                │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Writer    │→ │  Reviewer    │→ │   Reviser    │  │
│  │   Agent     │  │   Agent      │  │   Agent      │  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
│       ▲                  ▲                              │
│       └──────────────────┘ (Feedback Loop)             │
└────────────────────┬────────────────────────────────────┘
                     │ LangChain
┌────────────────────▼────────────────────────────────────┐
│            Groq LLM API (OpenAI-compatible)             │
│  - openai/gpt-oss-120b (Recommended)                   │
│  - openai/gpt-oss-20b (Faster)                         │
│  - qwen/qwen3.8-27b (Alternative)                      │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
LOOP AGENT/
├── app.py                      # FastAPI application
├── backend.py                  # LangGraph workflow + agents
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project configuration
├── .gitignore                  # Git ignore rules
├── .env                        # Environment variables (create this)
├── README.md                   # This file
├── templates/
│   └── index.html              # Jinja2 HTML template
└── static/
    ├── app.js                  # Frontend JavaScript
    └── style.css               # CSS3 styling
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Groq API Key (free at https://console.groq.com)
- Internet connection

### Installation

#### 1. Clone/Setup Project
```bash
mkdir LOOP-AGENT
cd LOOP-AGENT
# (copy all files here)
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure API
Create `.env` file in project root:
```env
GROQ_API_KEY=your_actual_api_key_from_console.groq.com
GROQ_MODEL=openai/gpt-oss-120b
MAX_REVISIONS=2
```

#### 5. Run Application
```bash
python app.py
```

Open browser: **http://127.0.0.1:8000**

---

## 📖 Usage

### Web UI

1. **Input**: Type a topic or question
   - Examples: "What is an API?", "Explain machine learning"
   
2. **Execute**: Click "Run workflow" button

3. **Monitor**: Watch the pipeline:
   - ✏️ Writer stage (blue)
   - 🔍 Reviewer stage (purple)
   - 🔄 Reviser stage (pink)
   - ✅ Final stage (green)

4. **Review**: View:
   - Agent activity timeline with drafts and feedback
   - Final answer with PASS/REVISE badge
   - Revision count and model used

### Command Line

```bash
python backend.py "Your topic here"
```

Output: Formatted answer with revision count

### API Endpoint

```bash
curl -X POST http://127.0.0.1:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"topic":"Explain APIs in simple terms"}'
```

**Response:**
```json
{
  "topic": "Explain APIs in simple terms",
  "events": [
    {
      "agent": "writer",
      "draft": "...",
      "feedback": "",
      "decision": "",
      "revision_count": 0
    },
    {
      "agent": "reviewer",
      "draft": "",
      "feedback": "",
      "decision": "PASS",
      "revision_count": 0
    }
  ],
  "final_answer": "...",
  "final_decision": "PASS",
  "final_revision_count": 0,
  "provider": "Groq",
  "model": "openai/gpt-oss-120b"
}
```

---

## 🔧 API Reference

### GET /
Returns the HTML user interface.

**Response:** HTML page (200 OK)

### POST /api/run
Execute the workflow for a given topic.

**Request:**
```json
{
  "topic": "string (1-300 characters, required)"
}
```

**Response:** (200 OK)
```json
{
  "topic": "string",
  "events": [
    {
      "agent": "writer|reviewer|reviser",
      "draft": "string",
      "feedback": "string",
      "decision": "PASS|REVISE",
      "revision_count": "number"
    }
  ],
  "final_answer": "string",
  "final_decision": "PASS|REVISE",
  "final_revision_count": "number",
  "provider": "Groq",
  "model": "string"
}
```

**Error Response:** (500 Internal Server Error)
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | (required) | Your Groq API key from https://console.groq.com |
| `GROQ_MODEL` | llama-3.3-70b-versatile | LLM model to use (see Available Models) |
| `MAX_REVISIONS` | 2 | Maximum number of revision cycles |

### Available Models

**Note:** Your API key must have access to the selected model.

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `openai/gpt-oss-120b` | Medium | High | Recommended for best quality |
| `openai/gpt-oss-20b` | Fast | Good | Faster responses, lower cost |
| `qwen/qwen3.8-27b` | Medium | Good | Alternative option |
| `meta-llama/llama-*` | Varies | Good | Various Llama versions |

### Model Selection

```python
# In .env file, change GROQ_MODEL to:
GROQ_MODEL=openai/gpt-oss-120b  # Recommended
GROQ_MODEL=openai/gpt-oss-20b   # Fast alternative
GROQ_MODEL=qwen/qwen3.8-27b     # Another option
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Cold Start** | 10-15 seconds |
| **Warm Start** | 8-10 seconds |
| **Max Response Time** | 15 seconds |
| **Typical Revisions** | 0-2 |
| **Virtual Env Setup** | 1-2 minutes |
| **Dependency Install** | 2-5 minutes |

---

## 🛠️ Customization

### Modify Agent Behavior

Edit `backend.py` to customize agents:

**Writer Agent** (lines 48-62):
```python
"You are a beginner-friendly teacher. Explain the topic in 120-160 words..."
```

**Reviewer Criteria** (lines 65-80):
```python
"Check answer using ONLY these rules:
1. Is it easy for beginner.
2. It contains an everyday analogy.
3. It contains a tiny concrete example.
4. It stays focused on the requested topic."
```

**Reviser Instructions** (lines 100-108):
```python
"You are a careful reviser. Use the reviewer's feedback to improve..."
```

### Customize UI

**Colors & Styling**: Edit `static/style.css`
```css
:root {
  --writer: #2f80ed;      /* Blue */
  --reviewer: #7c3aed;    /* Purple */
  --reviser: #ec4899;     /* Pink */
  --pass: #10b981;        /* Green */
}
```

**UI Layout**: Edit `templates/index.html`
- Form structure
- Pipeline visualization
- Timeline display
- Result formatting

**Frontend Logic**: Edit `static/app.js`
- Form submission
- API calls
- Event rendering
- Error handling

---

## 🐛 Troubleshooting

### "No module named 'fastapi'"
```bash
# Ensure venv is activated
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### "GROQ_API_KEY not found"
```bash
# Check .env file exists in project root
# Should contain: GROQ_API_KEY=your_key_here
# Get key from: https://console.groq.com
```

### "Model does not exist or access denied"
```bash
# Check GROQ_MODEL in .env
# Your API key may not have access to the model
# Try: GROQ_MODEL=openai/gpt-oss-120b
# Or: GROQ_MODEL=openai/gpt-oss-20b

# Verify on: https://console.groq.com
```

### "Port 8000 already in use"
Edit `app.py` last line:
```python
uvicorn.run("app:app", host="127.0.0.1", port=8001)  # Change 8000 to 8001
```

### Unicode/Encoding Errors
```bash
# Ensure Python 3.10+
python --version

# Already handled in backend.py with UTF-8 reconfiguration
# If issues persist, set environment variable:
set PYTHONIOENCODING=utf-8  # Windows
export PYTHONIOENCODING=utf-8  # Linux/macOS
```

### Connection Timeout
```bash
# Check internet connection (Groq API requires connection)
# Groq status: https://status.groq.com
# Try again in a few moments
```

---

## 📚 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | Web server & API |
| **Task Queue** | LangGraph | Agent workflow orchestration |
| **LLM** | Groq API | Fast language model inference |
| **LLM Wrapper** | LangChain | Groq API integration |
| **Server** | Uvicorn | ASGI application server |
| **Data Validation** | Pydantic | Type checking & validation |
| **Templates** | Jinja2 | Server-side HTML rendering |
| **Frontend** | Vanilla JavaScript | Client-side logic |
| **Styling** | CSS3 | Modern responsive design |
| **Config** | python-dotenv | Environment variable management |

---

## 🔐 Security Notes

### .env File
- **Never commit** `.env` file to version control
- **Already in .gitignore** (safe by default)
- Regenerate API keys if accidentally exposed
- Keep API key confidential

### API Key Management
- Get keys from: https://console.groq.com
- Rotate keys periodically
- Use separate keys for dev/prod
- Monitor usage on Groq dashboard

### Data Privacy
- No data stored locally (stateless)
- Groq processes requests on their servers
- Review Groq privacy policy: https://groq.com/privacy

---

## 📈 Performance Optimization

### Reduce Response Time
1. **Use faster model**: `openai/gpt-oss-20b` instead of 120b
2. **Reduce MAX_REVISIONS**: Set to 1 or 0 if sufficient
3. **Cache results**: Implement response caching for identical topics

### Scaling Considerations
- Current: Single-threaded, one workflow at a time
- For production: Consider message queues (Celery, RQ)
- Database: Add storage for workflow history
- Load balancing: Multiple FastAPI instances behind nginx

---

## 🧪 Testing

### Manual Testing

**Test 1: Simple Topic**
```
Topic: "What is a variable?"
Expected: PASS on first try
Time: ~10 seconds
```

**Test 2: Complex Topic**
```
Topic: "Explain quantum entanglement"
Expected: May need 1-2 revisions
Time: ~15 seconds
```

**Test 3: Edge Case**
```
Topic: "xyz123!@#$"
Expected: Graceful error handling
Time: <5 seconds
```

### API Testing

```bash
# Using curl
curl -X POST http://127.0.0.1:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"topic":"Test topic"}'

# Using Python requests
python -c "
import requests
resp = requests.post('http://127.0.0.1:8000/api/run', 
  json={'topic':'Test topic'})
print(resp.json())
"
```

---

## 📝 Project Statistics

- **Lines of Code**: ~650
- **Files**: 8 source files
- **Python**: ~240 lines
- **Frontend**: ~380 lines (HTML, JS, CSS)
- **Config**: ~30 lines
- **Dependencies**: 40+ packages
- **Archive Size**: 38 KB (base64)
- **Install Size**: ~200 MB (with venv)

---

## 🤝 Contributing

This project is open for modifications and improvements:

1. **Bug fixes**: Submit issues with reproduction steps
2. **Features**: Add new agents or evaluation criteria
3. **Optimization**: Improve performance or reduce latency
4. **Documentation**: Clarify or expand guides

---

## 📄 License

Open source. Use freely for personal, educational, and commercial projects.

---

## 🔗 Resources

- **Groq Console**: https://console.groq.com
- **Groq Docs**: https://console.groq.com/docs
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **FastAPI**: https://fastapi.tiangolo.com/
- **LangChain**: https://docs.langchain.com/

---

## 📞 Support & FAQ

**Q: Where do I get a Groq API key?**
A: Visit https://console.groq.com, sign up, and create an API key in the dashboard.

**Q: Can I use this offline?**
A: No, Groq API requires internet connection. For offline use, deploy a local LLM (Ollama, LLaMA.cpp).

**Q: How do I change the model?**
A: Edit `GROQ_MODEL` in `.env` file. Must have access to the model on your Groq account.

**Q: Can I modify the agent behavior?**
A: Yes! Edit the prompts in `backend.py` (Writer, Reviewer, Reviser classes).

**Q: Is there a database for history?**
A: Currently no. Results are shown in-memory. Add SQLite/PostgreSQL for persistence.

**Q: How do I deploy to production?**
A: Use Gunicorn/uWSGI, add reverse proxy (nginx), configure domain/SSL, monitor with logging.

---

## 🎉 Getting Started

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
# Create .env with GROQ_API_KEY

# 3. Run
python app.py

# 4. Access
# Open http://127.0.0.1:8000
```

**That's it!** Start using the Loop Agent immediately. 🚀

---

**Last Updated**: November 24, 2024  
**Status**: ✅ Production Ready  
**Python**: 3.10+  
**Version**: 1.0


cd /Users/vikaskumar/LOOP_AGENT
.venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8000

*** vercel setup ***

create a vercel account via web signup and then open the terminal and run the following commands

npm install -g vercel

vercel login

Navigate to your project directory and type the following command to deploy your application.

vercel --prod

Give the project name
Customize seting as No

Go to the browser verrcel and navigate to your application and click on Domain link.

