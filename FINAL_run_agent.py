import json
import os

from extraction.extraction import extract_fields
from logic.Missing_info_checker_logic import check_missing_info
from tracker.tracker_row_generator import generate_tracker_row
from emails.customer_email_generator import generate_customer_email
from emails.admin_email_generator import generate_admin_email


def save_output(filename, content):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", filename)

    if isinstance(content, (dict, list)):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Saved: outputs/{filename}")


def choose_model():
    print("Select extraction mode:")
    print("1. Local LLM")
    print("2. GPT")
    choice = input("Enter 1 or 2: ")
    return "local" if choice == "1" else "gpt"


def load_email(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    print("\n=== SmartQuote Assistant ===\n")

    model_choice = choose_model()
    email_text = load_email("sample_email.txt")

    extracted, usage = extract_fields(email_text, model=model_choice)
    missing = check_missing_info(extracted)
    tracker = generate_tracker_row(extracted, missing)
    customer_email = generate_customer_email(extracted, missing)
    admin_email = generate_admin_email(extracted, missing)

    save_output("extracted.json", extracted)
    save_output("missing_info.json", missing)
    save_output("tracker_row.json", tracker)
    save_output("customer_email.txt", customer_email)
    save_output("admin_email.txt", admin_email)

    print("\nToken usage:", usage)
    print("\n=== Process Complete ===\n")


if __name__ == "__main__":
    main()
