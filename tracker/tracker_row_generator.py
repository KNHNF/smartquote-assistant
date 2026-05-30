def generate_tracker_row(data, missing_info):
    """
    Creates a clean tracker row dictionary from extracted JSON + missing info list.
    """

    # Determine credit status summary
    if data["credit"]["credit_outcome"] in ["unsatisfactory", "unclear"]:
        credit_status = f"{data['credit']['credit_outcome']} (review needed)"
    else:
        credit_status = data["credit"]["credit_outcome"]

    # Determine PO status summary
    if data["po"]["po_required"] == "yes" and data["po"]["po_number"] == "":
        po_status = "missing"
    else:
        po_status = data["po"]["po_status"]

    # Determine overall status
    if "PO required but missing" in missing_info:
        overall_status = "waiting_for_po"
    elif "Annual customer form missing" in missing_info:
        overall_status = "waiting_for_form"
    elif "Credit check required but missing" in missing_info:
        overall_status = "waiting_for_credit"
    else:
        overall_status = data["tracker"]["status"]

    # Build tracker row
    row = {
        "quote_id": data["tracker"]["quote_id"],
        "quote_date": data["tracker"]["quote_date"],
        "customer": data["customer"]["name"],
        "project": data["project"]["name"],
        "task_title": data["task"]["title_caps"],
        "quoted_amount": data["financial"]["quoted_amount"],
        "po_status": po_status,
        "credit_status": credit_status,
        "status": overall_status,
        "next_action_date": data["tracker"]["next_action_date"],
        "chase_required": data["tracker"]["chase_required"]
    }

    return row
