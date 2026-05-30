import json
import subprocess
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_raw_facts_with_gpt(email_text):
    prompt = f"""
You are SmartQuote, an extraction engine. Extract ALL structured fields from the email below.

Return ONLY valid JSON matching EXACTLY this schema:

{{
  "customer": {{
    "name": "",
    "name_variants": [],
    "status": "existing | new | unknown",
    "contact_name": "",
    "contact_email": "",
    "contact_phone": "",
    "annual_form_received": "yes | no | unknown",
    "billing_rate_exists": "yes | no | unknown"
  }},
  "project": {{
    "name": "",
    "number": "",
    "status": "existing | new | unknown",
    "office_of_origin": "",
    "category": "",
    "system_type": "standard_quote | hourly_rate | lump_sum | pro_forma | unknown"
  }},
  "task": {{
    "title_caps": "",
    "description": "",
    "task_type": "standard | hourly | lump_sum | pro_forma | unknown",
    "revision": "",
    "estimated_design_time_minutes": "",
    "staff_time_minutes": "",
    "billing_rate_category": ""
  }},
  "financial": {{
    "quoted_amount": "",
    "hourly_rate": "",
    "lump_sum_value": "",
    "currency": "GBP",
    "vat_required": "yes | no | unknown"
  }},
  "po": {{
    "po_required": "yes | no | unknown",
    "po_number": "",
    "po_status": "provided | missing | tbc | needs_chasing | unknown",
    "pro_forma_required": "yes | no | unknown"
  }},
  "credit": {{
    "credit_check_needed": "yes | no | unknown",
    "suggested_credit_limit": "",
    "trading_experience_summary": "",
    "credit_risk_score": "",
    "credit_outcome": "satisfactory | unsatisfactory | unclear | unknown"
  }},
  "designer": {{
    "designer_name": "",
    "prepared_by": "",
    "checked_by": "",
    "designer_notes": ""
  }},
  "documents": {{
    "attachments": [],
    "drawing_numbers": [],
    "reference_numbers": [],
    "quote_template_type": "",
    "required_recipients": []
  }},
  "tracker": {{
    "quote_date": "",
    "quote_id": "",
    "project_task_revision": "",
    "status": "sent | waiting_for_po | waiting_for_form | accepted | lost | revised | unknown",
    "next_action_date": "",
    "chase_required": "yes | no | unknown"
  }}
}}

Email:
{email_text}
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content
    usage = response.usage

    start = output.find("{")
    end = output.rfind("}") + 1
    data = json.loads(output[start:end])

    return data, usage

def normalize_usage(usage):
    if isinstance(usage, dict):
        return usage
    return {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens
    }


def map_facts_to_schema(facts):
    return facts

def extract_fields_with_gpt(email_text):
    facts, usage = extract_raw_facts_with_gpt(email_text)
    schema = map_facts_to_schema(facts)
    return schema, normalize_usage(usage)



def extract_fields_with_local_llm(email_text, local_model="phi3:mini"):
    prompt = f"""
Extract the following fields from the email:

- customer_name
- project_name
- estimated_hours
- category
- po_status
- designer_name

Return ONLY valid JSON.

Email:
{email_text}
"""

    result = subprocess.run(
        ["ollama", "run", local_model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )

    output = result.stdout.decode("utf-8")
    start = output.find("{")
    end = output.rfind("}") + 1
    json_str = output[start:end].strip()

    if not json_str.startswith("{") or not json_str.endswith("}"):
        raise ValueError("Local model did not return valid JSON.")

    facts = json.loads(json_str)


    hours = facts.get("estimated_hours", "0")
    try:
        minutes = str(int(hours) * 60)
    except:
        minutes = ""

    schema = {
        "customer": {
            "name": facts.get("customer_name", ""),
            "name_variants": [],
            "status": "unknown",
            "contact_name": facts.get("designer_name", ""),
            "contact_email": "",
            "contact_phone": "",
            "annual_form_received": "unknown",
            "billing_rate_exists": "unknown"
        },
        "project": {
            "name": facts.get("project_name", ""),
            "number": "",
            "status": "unknown",
            "office_of_origin": "",
            "category": facts.get("category", ""),
            "system_type": "standard_quote"
        },
        "task": {
            "title_caps": facts.get("project_name", "").upper(),
            "description": "",
            "task_type": "standard",
            "revision": "",
            "estimated_design_time_minutes": minutes,
            "staff_time_minutes": "",
            "billing_rate_category": ""
        },
        "financial": {
            "quoted_amount": "",
            "hourly_rate": "",
            "lump_sum_value": "",
            "currency": "GBP",
            "vat_required": "unknown"
        },
        "po": {
            "po_required": "unknown",
            "po_number": "",
            "po_status": facts.get("po_status", ""),
            "pro_forma_required": "unknown"
        },
        "credit": {
            "credit_check_needed": "unknown",
            "suggested_credit_limit": "",
            "trading_experience_summary": "",
            "credit_risk_score": "",
            "credit_outcome": "unknown"
        },
        "designer": {
            "designer_name": facts.get("designer_name", ""),
            "prepared_by": "",
            "checked_by": "",
            "designer_notes": ""
        },
        "documents": {
            "attachments": [],
            "drawing_numbers": [],
            "reference_numbers": [],
            "quote_template_type": "",
            "required_recipients": []
        },
        "tracker": {
            "quote_date": "",
            "quote_id": "",
            "project_task_revision": "",
            "status": "unknown",
            "next_action_date": "",
            "chase_required": "unknown"
        }
    }

    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    return schema, normalize_usage(usage)



def extract_fields(email_text, model="local", local_model="phi3:mini"):
    if model == "gpt":
        return extract_fields_with_gpt(email_text)
    else:
        return extract_fields_with_local_llm(email_text, local_model=local_model)
