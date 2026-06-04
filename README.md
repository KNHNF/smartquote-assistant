# SmartQuote Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-3572A5?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-local%20LLM-black?style=flat-square)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-a78bfa?style=flat-square)](LICENSE)

LLM-powered automation tool that reads inbound engineering quote emails, extracts structured data, drafts customer and admin replies, and generates internal tracker rows — reducing manual data entry in quote workflows.

Supports free local models via Ollama (Mistral 7B, Phi-3 Mini) and OpenAI GPT.

---

## Model Performance

| Model | Field Extraction | Notes |
|---|---|---|
| GPT-4 | 96% | Near-perfect extraction and formatting |
| Phi-3 Mini | 61% | Extracts core fields, misses complex ones |
| Mistral 7B | 59% | Similar to Phi-3 on structured emails |

GPT-4 is the only model that reliably handles all field types in a single pass. Local models are free and useful for prototyping or lower-stakes workflows.

---

## How It Works

1. Paste or load an inbound quote email
2. Choose a model (local via Ollama, or GPT)
3. LLM extracts all structured fields into JSON
4. App flags missing or ambiguous fields
5. Generates a customer-facing email and internal admin email
6. Supervisor approves or rejects before anything is sent
7. Exports a CSV-ready tracker row for internal systems

---

## Quick Start

Requires Python 3.10+, and either Ollama (local mode) or an OpenAI API key (GPT mode).

```bash
git clone https://github.com/KNHNF/smartquote-assistant.git
cd smartquote-assistant

python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

pip install -r requirements.txt
streamlit run streamlit_app.py
```

Add your OpenAI API key in the Streamlit UI to enable GPT mode. Local mode requires no API key.

---

## Local Models via Ollama

Install Ollama from [ollama.com](https://ollama.com/download), then pull models:

```bash
ollama pull mistral:7b
ollama pull phi3:mini
```

No internet connection or API key required once models are downloaded.

---

## Repository Structure

```
smartquote-assistant/
├── streamlit_app.py       main Streamlit UI
├── FINAL_run_agent.py     agent runner (non-UI)
├── extraction/            LLM field extraction logic
├── logic/                 validation and missing field detection
├── tracker/               CSV tracker row generation
├── emails/                email draft generation
├── sample_emails/         example input emails
├── schema/                expected field schema
├── demo_database/         demo data
├── results/               output files
├── requirements.txt
└── README.md
```

---

## Known Issues (UI only)

These do not affect extraction accuracy or JSON output:

- Streamlit Arrow serialization errors when lists appear in DataFrames
- Duplicate button keys on unexpected component rerenders
- Hermes 7B frequently returns invalid JSON
- GPT token usage object requires normalization before display

---

## Future Work

- Event-driven mode: process emails automatically on arrival
- Database integration: auto-populate internal systems on approval
- Improved local model prompting to close the accuracy gap with GPT
- Multi-email batch processing
- Supervisor dashboard with audit trail

---

## Background

Originally prototyped at a university hackathon, then expanded into a standalone tool with improved extraction logic, supervisor approval flow, and local model support.

---

## Author

**Karan Homayounfar** · MSc Data Science, UWE Bristol
[Portfolio](https://karan-portfolio-al7.pages.dev) · [LinkedIn](https://linkedin.com/in/karan-homayounfar) · [GitHub](https://github.com/KNHNF)

## License

MIT
