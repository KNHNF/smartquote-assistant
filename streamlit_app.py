import streamlit as st
import json
import os
import glob
import pandas as pd

from extraction.extraction import extract_fields
from logic.Missing_info_checker_logic import check_missing_info
from tracker.tracker_row_generator import generate_tracker_row
from emails.customer_email_generator import generate_customer_email
from emails.admin_email_generator import generate_admin_email

def safe_filename(name: str) -> str:
    return name.replace(":", "_").replace("/", "_").replace("\\", "_").replace(" ", "_")


st.set_page_config(page_title="SmartQuote Assistant", layout="wide")
st.title("SmartQuote Assistant")

# session state
keys = ["extracted", "missing", "tracker", "customer_email", "admin_email", "usage"]
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = None

if "confirm_customer" not in st.session_state:
    st.session_state.confirm_customer = False
if "confirm_admin" not in st.session_state:
    st.session_state.confirm_admin = False
if "model_results" not in st.session_state:
    st.session_state.model_results = {}
if "reset_confirm" not in st.session_state:
    st.session_state.reset_confirm = False


# GLOBAL RELOAD BUTTON
if st.button("Reload App"):
    st.experimental_rerun()


tab_input, tab_record, tab_emails, tab_tokens, tab_approval, tab_compare, tab_help = st.tabs([
    "Email Input",
    "Quote Record",
    "Emails",
    "Token Usage",
    "Supervisor Approval",
    "Model Comparison",
    "Help"
])


# TAB 1: EMAIL INPUT
with tab_input:
    st.subheader("Designer Email")

    # Unified model selection
    st.subheader("Model Selection")

    model_type = st.radio("Choose extraction mode", ["Local (free)", "GPT (requires API key)"], key="model_type")
    
    st.warning("Hermes 7B is not recommended. It often fails to return valid JSON for long emails.")

    if model_type == "Local (free)":
        local_model = st.selectbox(
            "Choose local model",
            ["mistral:7b", "hermes:7b", "phi3:mini"],
            key="local_model"
        )
        model = "local"
        user_key = None

    else:
        user_key = st.text_input("Enter your OpenAI API key", type="password", key="api_key")
        model = "gpt"
        local_model = None

        if not user_key:
            st.warning("Enter your API key to use GPT mode.")
        else:
            os.environ["OPENAI_API_KEY"] = user_key

    sample_files = glob.glob("sample_emails/*.txt")
    sample_names = ["None"] + [os.path.basename(f) for f in sample_files]
    sample_choice = st.selectbox("Choose a sample email", sample_names)

    email_text = ""
    if sample_choice != "None":
        with open(f"sample_emails/{sample_choice}", "r", encoding="utf-8") as f:
            email_text = f.read()

    email_text = st.text_area("Paste or edit the email", value=email_text, height=350)

    if st.button("Run Agent", key="run_agent"):
        if not email_text.strip():
            st.error("Please paste an email first.")
        elif model == "gpt" and not user_key:
            st.error("GPT mode requires an API key.")
        else:
            with st.spinner("Extracting fields..."):
                extracted, usage = extract_fields(
                    email_text,
                    model=model,
                    local_model=local_model
                )
                missing = check_missing_info(extracted)
                tracker = generate_tracker_row(extracted, missing)
                customer_email = generate_customer_email(extracted, missing)
                admin_email = generate_admin_email(extracted, missing)

            st.session_state.extracted = extracted
            st.session_state.missing = missing
            st.session_state.tracker = tracker
            st.session_state.customer_email = customer_email
            st.session_state.admin_email = admin_email
            st.session_state.usage = usage

            completion_score = max(0, 100 - int(100 * len(missing) / max(len(missing) + 20, 1)))

            model_name = model if model == "gpt" else local_model

            st.session_state.model_results[model_name] = {
                "model_name": model_name,
                "extracted": extracted,
                "missing": missing,
                "tracker": tracker,
                "completion": completion_score,
                "usage": usage
            }

            os.makedirs("results", exist_ok=True)

            safe_name = safe_filename(model_name)
            with open(f"results/{safe_name}.json", "w") as f:
                json.dump(st.session_state.model_results[model_name], f, indent=2)

            st.success("Extraction complete. Continue to the 'Quote Record' tab.")


    # RESET BUTTON (2-click flow)
    st.markdown("---")
    st.subheader("App Controls")

    if st.session_state.reset_confirm:
        st.warning("Are you sure you want to reset the entire app? This will clear all extracted data and results.")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("Yes, reset everything", key="reset_yes"):
                for k in ["extracted", "missing", "tracker", "customer_email", "admin_email", "usage"]:
                    st.session_state[k] = None

                st.session_state.confirm_customer = False
                st.session_state.confirm_admin = False
                st.session_state.model_results = {}
                st.session_state.reset_confirm = False

                st.success("App has been reset.")
        with col_r2:
            if st.button("Cancel", key="reset_cancel"):
                st.session_state.reset_confirm = False

    else:
        if st.button("Reset App", key="reset_app"):
            st.session_state.reset_confirm = True



# TAB 2: QUOTE RECORD
with tab_record:
    st.subheader("Quote Record")

    if st.session_state.extracted is None:
        st.info("Run the agent in the 'Email Input' tab first.")
    else:
        extracted = st.session_state.extracted
        missing = st.session_state.missing
        tracker = st.session_state.tracker

        total_checks = len(missing) + 20
        completion = max(0, 100 - int(100 * len(missing) / max(total_checks, 1)))
        st.metric("Completion Score", f"{completion}%")

        rows = []
        def add(section, label, value):
            rows.append({"Section": section, "Field": label, "Value": value})

        for section, fields in extracted.items():
            if isinstance(fields, dict):
                for k, v in fields.items():
                    add(section.capitalize(), k, v)

        df_view = pd.DataFrame(rows)
        st.dataframe(df_view, use_container_width=True)

        st.subheader("Missing Information")
        st.write(missing)

        st.subheader("Tracker Row")
        st.json(tracker)

        csv_data = pd.DataFrame([tracker]).to_csv(index=False).encode("utf-8")
        st.download_button("Download Tracker Row CSV", csv_data, "tracker_row.csv", key="download_tracker")



# TAB 3: EMAILS
with tab_emails:
    st.subheader("Generated Emails")

    if st.session_state.customer_email is None:
        st.info("Run the agent in the 'Email Input' tab first.")
    else:
        customer_email = st.session_state.customer_email
        admin_email = st.session_state.admin_email

        st.markdown("Customer Email (external, friendly)")
        st.code(customer_email)

        st.markdown("Admin Email (internal, detailed)")
        st.code(admin_email)

        st.subheader("Send Emails (Simulation)")

        col_cust, col_admin = st.columns(2)

        with col_cust:
            st.write("Customer Email")
            if not st.session_state.confirm_customer:
                if st.button("Send Customer Email (simulate)", key="send_customer"):
                    st.session_state.confirm_customer = True
            else:
                st.warning("Are you sure you want to send the customer email?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Yes, send customer email", key="send_customer_yes"):
                        st.success("Customer email 'sent'.")
                        st.session_state.confirm_customer = False
                with c2:
                    if st.button("Cancel", key="send_customer_cancel"):
                        st.session_state.confirm_customer = False

        with col_admin:
            st.write("Admin Email")
            if not st.session_state.confirm_admin:
                if st.button("Send Admin Email (simulate)", key="send_admin"):
                    st.session_state.confirm_admin = True
            else:
                st.warning("Are you sure you want to send the admin email?")
                a1, a2 = st.columns(2)
                with a1:
                    if st.button("Yes, send admin email", key="send_admin_yes"):
                        st.success("Admin email 'sent'.")
                        st.session_state.confirm_admin = False
                with a2:
                    if st.button("Cancel", key="send_admin_cancel"):
                        st.session_state.confirm_admin = False



# TAB 4: TOKEN USAGE
with tab_tokens:
    st.subheader("Token Usage")
    st.info("Token usage is only available for GPT mode. Local models do not return token usage.")

    if st.session_state.usage is None:
        st.info("Run the agent in the 'Email Input' tab first.")
    else:
        usage = st.session_state.usage
        st.write(f"Prompt tokens: {usage.get('prompt_tokens')}")
        st.write(f"Completion tokens: {usage.get('completion_tokens')}")
        st.write(f"Total tokens: {usage.get('total_tokens')}")


# TAB 5: SUPERVISOR APPROVAL
with tab_approval:
    st.subheader("Supervisor Approval")

    if st.session_state.extracted is None:
        st.info("Run the agent in the 'Email Input' tab first.")
    else:
        approve = st.radio("Approve this quote?", ["Pending", "Approved", "Rejected"], key="approval_radio")

        if approve == "Approved":
            st.success("Supervisor approved the quote.")
        elif approve == "Rejected":
            st.error("Supervisor rejected the quote.")
        else:
            st.warning("Awaiting supervisor decision.")



# TAB 6: MODEL COMPARISON
with tab_compare:
    st.subheader("Model Comparison")

    results = st.session_state.model_results

    if not results:
        st.info("Run at least one model to compare results.")
    else:
        model_names = list(results.keys())
        st.write("Models run so far:", model_names)

        st.subheader("Completion Scores")
        for m in model_names:
            st.write(f"{m}: {results[m]['completion']}%")

        st.subheader("Extracted Fields Comparison")
        selected_models = st.multiselect("Select models to compare", model_names, default=model_names)

        cols = st.columns(len(selected_models))
        for i, m in enumerate(selected_models):
            with cols[i]:
                st.markdown(f"### {m}")
                st.json(results[m]["extracted"])

        st.subheader("Missing Information Comparison")
        for m in selected_models:
            st.write(f"### {m}")
            st.write(results[m]["missing"])

        st.subheader("Token Usage (GPT only)")
        for m in selected_models:
            if m == "gpt":
                st.json(results[m]["usage"])
            else:
                st.write(f"{m}: Local model (no token usage)")

    if st.button("Clear Comparison Results"):
        st.session_state.model_results = {}
        st.success("Comparison results cleared.")



# TAB 7: HELP
with tab_help:
    st.subheader("Guide")

    st.markdown("""
### How to use SmartQuote

**Email Input**
- Paste a designer email or choose a sample.
- Choose Local mode (free) or GPT mode (requires your own API key).
- Run the agent.

**Quote Record**
- Review extracted fields.
- Check completion score.
- Review missing information.
- Download tracker row.

**Emails**
- Review customer and admin emails.
- Simulate sending with confirmation.

**Token Usage**
- View GPT token usage if GPT mode was used.

**Supervisor Approval**
- Approve or reject the quote before issuing.

**Model Comparison**
- Compare extraction quality across models.
- View missing fields, extracted JSON, and token usage.

**Local vs GPT mode**
- Local models run 100% free but may produce lower accuracy.
- GPT mode provides higher accuracy and token usage analytics.
""")
