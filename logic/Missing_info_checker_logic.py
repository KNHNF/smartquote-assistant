def check_missing_info(data):
    issues = []

    # -------------------------
    # CUSTOMER CHECKS
    # -------------------------
    if data["customer"]["name"] == "":
        issues.append("Customer name missing")

    if len(data["customer"]["name_variants"]) > 1:
        issues.append("Multiple customer name variants detected")

    if data["customer"]["annual_form_received"] == "no":
        issues.append("Annual customer form missing")

    if data["customer"]["billing_rate_exists"] == "no":
        issues.append("Billing rate missing for this customer")

    if (
        data["customer"]["contact_name"] == "" or
        data["customer"]["contact_email"] == "" or
        data["customer"]["contact_phone"] == ""
    ):
        issues.append("Customer contact details incomplete")

    # -------------------------
    # PROJECT CHECKS
    # -------------------------
    if data["project"]["name"] == "":
        issues.append("Project name missing")

    if data["project"]["number"] == "":
        issues.append("Project number missing")

    if data["project"]["category"] == "":
        issues.append("Project category missing")

    if data["project"]["system_type"] == "unknown":
        issues.append("System type missing or unclear")

    # -------------------------
    # TASK CHECKS
    # -------------------------
    if data["task"]["title_caps"] == "":
        issues.append("Task title missing")

    if data["task"]["description"] == "":
        issues.append("Task description missing")

    if data["task"]["task_type"] == "unknown":
        issues.append("Task type unclear")

    if data["task"]["estimated_design_time_minutes"] in ["", None]:
        issues.append("Estimated design time missing")

    if data["task"]["staff_time_minutes"] in ["", None]:
        issues.append("Staff time missing")

    # -------------------------
    # FINANCIAL CHECKS
    # -------------------------
    if data["financial"]["quoted_amount"] in ["", None]:
        issues.append("Quoted amount missing")

    if (
        data["task"]["task_type"] == "hourly" and
        data["financial"]["hourly_rate"] in ["", None]
    ):
        issues.append("Hourly rate missing for hourly task")

    if (
        data["task"]["task_type"] == "lump_sum" and
        data["financial"]["lump_sum_value"] in ["", None]
    ):
        issues.append("Lump sum value missing")

    if data["financial"]["vat_required"] == "unknown":
        issues.append("VAT requirement unclear")

    # -------------------------
    # PO & CREDIT CHECKS
    # -------------------------
    if data["po"]["po_required"] == "yes" and data["po"]["po_number"] == "":
        issues.append("PO required but missing")

    if (
        data["po"]["po_number"] != "" and
        not data["po"]["po_number"].replace("-", "").isalnum()
    ):
        issues.append("PO number invalid format")

    if data["credit"]["credit_check_needed"] == "yes" and data["credit"]["credit_outcome"] == "unknown":
        issues.append("Credit check required but missing")

    if data["credit"]["credit_outcome"] == "unclear":
        issues.append("Credit check unclear – finance review needed")

    # -------------------------
    # DOCUMENT CHECKS
    # -------------------------
    if len(data["documents"]["attachments"]) == 0:
        issues.append("Attachments missing")

    if len(data["documents"]["drawing_numbers"]) == 0:
        issues.append("Drawing numbers missing")

    if len(data["documents"]["reference_numbers"]) == 0:
        issues.append("Reference numbers missing")

    if len(data["documents"]["required_recipients"]) == 0:
        issues.append("Email recipients missing")

    # -------------------------
    # TRACKER CHECKS
    # -------------------------
    if data["tracker"]["quote_id"] == "":
        issues.append("Quote ID missing")

    if data["tracker"]["status"] == "unknown":
        issues.append("Tracker status missing")

    if data["tracker"]["next_action_date"] == "":
        issues.append("Next action date missing")

    if (
        data["tracker"]["chase_required"] == "yes" and
        data["tracker"]["next_action_date"] == ""
    ):
        issues.append("Chase required but no next action date scheduled")

    return issues
