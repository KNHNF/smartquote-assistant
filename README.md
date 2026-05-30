# SmartQuote Assistant

SmartQuote Assistant is a small automation tool designed to reduce human error and manual data entry in engineering quote workflows.  
It reads incoming emails from engineers or designers, extracts structured information using LLMs, prepares customer/admin emails, and generates a tracker row for internal systems.  
The goal is to move toward an event‑driven workflow where incoming emails automatically trigger extraction, validation, and supervisor‑approved output.

---

## Features

- **LLM‑powered field extraction**  
  Supports both free local models (Mistral 7B, Phi3 Mini) and GPT mode for higher accuracy.

- **Structured JSON output**  
  Extracts customer, project, task, financial, PO, credit, designer, documents, and tracker fields.

- **Missing information detection**  
  Highlights incomplete or unclear fields before approval.

- **Automatic email generation**  
  Creates a customer‑friendly email and an internal admin email based on extracted data.

- **Tracker row generation**  
  Produces a CSV‑ready row for internal quote tracking systems.

- **Supervisor approval flow**  
  Allows a human to approve or reject the quote before sending.

- **Model comparison**  
  Compare extraction quality across local LLMs and GPT.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/smartquote-assistant.git
cd smartquote-assistant
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run streamlit_app.py
```

(Optional) Add your OpenAI API key in the UI to enable GPT mode.

---

## How It Works

### 1. Paste or load an email  
The engineer/designer sends a structured or semi‑structured email.  
You paste it into the app or load a sample.

### 2. Choose a model  
- **Local mode (free):** Mistral 7B, Phi3 Mini  
- **GPT mode:** Higher accuracy, token usage shown

### 3. Run extraction  
The model returns structured JSON + missing fields + tracker row.

### 4. Review generated emails  
- Customer email (external)  
- Admin email (internal)

### 5. Supervisor approval  
Approve or reject before sending.

### 6. Compare models  
See how different LLMs perform on the same email.

---

## Architecture Overview

When a new email arrives, SmartQuote Assistant follows a simple flow:

1. Read the incoming email
2. Use an LLM (local or GPT) to pull out all the structured fields
3. Check what information is missing or unclear
4. Build the internal tracker row
5. Draft the customer email and the admin email
6. Wait for supervisor approval before anything is sent
7. (Planned) Push the approved data straight into the database and send the emails automatically

---

## Repository Structure

```
smartquote-assistant/
│
├── streamlit_app.py
├── requirements.txt
├── sample_emails/
│   └── sample_email_complete.txt
│
├── extraction/
│   └── extraction.py
│
├── logic/
│   └── Missing_info_checker_logic.py
│
├── tracker/
│   └── tracker_row_generator.py
│
├── emails/
│   ├── customer_email_generator.py
│   └── admin_email_generator.py
│
└── results/
    ├── phi3_mini.json
    ├── mistral_7b.json
    └── gpt.json
```

---

## Model Performance (Based on Real Results)

| Model       | Completion | Notes |
|-------------|------------|-------|
| **Phi3 Mini** | 61% | Extracts some fields, misses many |
| **Mistral 7B** | 59% | Slightly worse on this email |
| **GPT** | 96% | Near‑perfect extraction, correct formatting |

GPT is the only model that fully understood the structured email and returned almost all fields correctly.

---

## Known Issues

These do **not** affect extraction or JSON results — only the UI:

- Streamlit Arrow serialization errors when lists appear in DataFrames  
- Duplicate button IDs if keys are missing  
- Hermes 7B often fails to return valid JSON  
- Token usage object from GPT needs normalization  
- Some UI elements rerun unexpectedly due to Streamlit’s reactive model  

These are planned to be addressed in future updates.

---

## Future Work

- Event‑driven automation (process emails automatically on arrival)
- Database integration (auto‑populate internal systems)
- Improved local model prompting
- Better error handling for malformed emails
- Multi‑email batch processing
- Supervisor dashboard
- Cleaner Streamlit UI and layout
- Optional screenshot or GIF demo once UI stabilizes

---

## Why This Project Exists

Engineering teams often receive structured emails from designers, but manually copying this information into internal systems is slow and error‑prone.  
SmartQuote Assistant reduces this friction by:

- extracting structured data  
- generating emails  
- preparing tracker rows  
- reducing human mistakes  
- keeping supervisors in control  

It’s a step toward a fully automated quote‑to‑task pipeline.