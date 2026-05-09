# main.py — Main entry point for Email Automation & Reminder System
# Run: python main.py --mode dry-run   (simulate without sending)
# Run: python main.py --mode send      (send real emails)
# Run: python main.py --mode schedule  (schedule daily at 09:00)

import argparse
import logging
import os
from dotenv import load_dotenv

# Load .env before importing src modules
load_dotenv()

from src.logger        import setup_logger
from src.data_loader   import load_contacts, load_reminders, merge_data
from src.personalizer  import load_template, personalize_message
from src.email_sender  import send_email
from src.reporter      import generate_report
from src.scheduler     import schedule_daily, run_once_now


def process_all_reminders(merged_df, company_sender):
    """
    Core pipeline: for each merged row, personalize and send (or simulate) email.
    Returns list of result dicts.
    """
    results = []
    
    if merged_df.empty:
        logger.warning("No reminder data found. Exiting.")
        return results
    
    for _, row in merged_df.iterrows():
        # 1. Load correct template based on reminder type
        template = load_template(row["reminder_type"])
        if template is None:
            logger.error(f"Skipping {row['name']} — template not found")
            continue
        
        # 2. Personalize the message
        body = personalize_message(template, row, company_sender)
        if body is None:
            logger.error(f"Skipping {row['name']} — personalization failed")
            continue
        
        # 3. Send or simulate email
        result = send_email(
            recipient_email = row["email"],
            recipient_name  = row["name"],
            subject         = row["subject"],
            body            = body
        )
        results.append(result)
    
    return results


def main():
    global logger
    
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Email Automation & Reminder System"
    )
    parser.add_argument(
        "--mode",
        choices=["dry-run", "send", "schedule"],
        default="dry-run",
        help="Run mode: dry-run (simulate), send (real), schedule (daily)"
    )
    parser.add_argument(
        "--time",
        default="09:00",
        help="Time to schedule daily sends in HH:MM format (default: 09:00)"
    )
    args = parser.parse_args()
    
    # Initialize logger
    logger = setup_logger()
    logger.info(f"Mode selected: {args.mode.upper()}")
    
    # Override DRY_RUN setting based on --mode flag
    if args.mode in ["dry-run"]:
        os.environ["DRY_RUN"] = "True"
        logger.info("DRY-RUN mode: No real emails will be sent.")
    elif args.mode == "send":
        os.environ["DRY_RUN"] = "False"
        logger.info("SEND mode: Real emails will be sent via Gmail SMTP.")
    
    # Load and merge data
    contacts_df  = load_contacts("data/contacts.csv")
    reminders_df = load_reminders("data/reminders.csv")
    merged_df    = merge_data(contacts_df, reminders_df)
    
    # Get company name from env
    company_sender = os.getenv("SENDER_COMPANY", "Email Automation System")
    
    # Run based on mode
    if args.mode in ["dry-run", "send"]:
        results = process_all_reminders(merged_df, company_sender)
        generate_report(results)
        
    elif args.mode == "schedule":
        # Schedule to run every day at specified time
        def job():
            results = process_all_reminders(merged_df, company_sender)
            generate_report(results)
        
        schedule_daily(args.time, job)


if __name__ == "__main__":
    main()