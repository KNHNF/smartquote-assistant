def generate_customer_email(extracted_data, missing_info):
    customer_name = extracted_data["customer"]["name"] or "Customer"
    project_name = extracted_data["project"]["name"] or "your project"
    quote_id = extracted_data["tracker"]["quote_id"] or "TBC"

    missing_count = len(missing_info)

    if missing_count == 0:
        missing_text = (
            "We have all the information we need and will now prepare and issue your formal quotation."
        )
    else:
        missing_text = (
            f"We are almost ready to finalise your quotation. "
            f"There are {missing_count} small points we need to confirm with you. "
            "A member of our team will be in touch shortly to clarify these."
        )

    email_body = f"""
Dear {customer_name},

Thank you for your enquiry regarding {project_name}.

We have prepared your quote (Reference: {quote_id}).

{missing_text}

If you have any questions in the meantime, please feel free to contact us.

Kind regards,
SmartQuote Engineering Team
"""

    return email_body
