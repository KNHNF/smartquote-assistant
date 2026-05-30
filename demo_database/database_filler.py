import csv
import os

def fill_demo_database(tracker_row, missing_info, csv_path="demo_database/demo_db.csv"):
    """
    Appends a new row to the demo database CSV.
    Creates the CSV with headers if it does not exist.
    """

    # Ensure folder exists
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    # Define CSV headers
    headers = [
        "quote_id",
        "quote_date",
        "customer",
        "project",
        "task_title",
        "quoted_amount",
        "po_status",
        "credit_status",
        "status",
        "next_action_date",
        "chase_required",
        "missing_info"
    ]

    # Convert missing info list → single string
    missing_info_str = "; ".join(missing_info) if missing_info else ""

    # Add missing info to tracker row
    tracker_row_with_issues = tracker_row.copy()
    tracker_row_with_issues["missing_info"] = missing_info_str

    # Check if CSV exists
    file_exists = os.path.isfile(csv_path)

    # Write to CSV
    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write header only if file is new
        if not file_exists:
            writer.writeheader()

        # Write the row
        writer.writerow(tracker_row_with_issues)

    return f"Row added to demo database: {csv_path}"
