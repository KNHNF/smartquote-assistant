def generate_admin_email(extracted_data, missing_info):
    quote_id = extracted_data["tracker"]["quote_id"]
    project_name = extracted_data["project"]["name"] or "Unknown Project"
    customer_name = extracted_data["customer"]["name"] or "Unknown Customer"

    missing_list = "\n".join([f"- {item}" for item in missing_info]) if missing_info else "None"

    email_body = f"""
Admin Team,

A new quote has been processed by the SmartQuote Assistant.

Quote ID: {quote_id}
Customer: {customer_name}
Project: {project_name}

Missing or unclear information:
{missing_list}

Please review and follow up as required.

Regards,
SmartQuote Assistant
"""

    return email_body
