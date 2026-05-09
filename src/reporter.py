# reporter.py — Generates a CSV report of all email send activity

import pandas as pd
import os
import logging
from datetime import datetime

logger = logging.getLogger("EmailAutomation")

def generate_report(results_list, output_dir="outputs"):
    """
    Takes a list of send result dicts and writes a CSV report.
    
    Args:
        results_list: List of dicts returned by email_sender.send_email()
        output_dir:   Folder to save report in
    Returns:
        Path to the generated report file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not results_list:
        logger.warning("No results to report. Report not generated.")
        return None
    
    # Convert results list to DataFrame
    report_df = pd.DataFrame(results_list)
    
    # Add timestamp column
    report_df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Reorder columns for readability
    columns = ["timestamp", "recipient_name", "recipient_email", 
               "subject", "status", "error"]
    report_df = report_df[[c for c in columns if c in report_df.columns]]
    
    # Generate filename with date
    filename = f"email_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(output_dir, filename)
    
    report_df.to_csv(filepath, index=False)
    
    # Print summary
    total   = len(report_df)
    sent    = len(report_df[report_df["status"].str.contains("SENT|DRY-RUN", na=False)])
    failed  = len(report_df[report_df["status"] == "FAILED"])
    
    logger.info("=" * 60)
    logger.info(f"REPORT SUMMARY")
    logger.info(f"  Total Emails Processed : {total}")
    logger.info(f"  Sent / Simulated       : {sent}")
    logger.info(f"  Failed                 : {failed}")
    logger.info(f"  Report saved to        : {filepath}")
    logger.info("=" * 60)
    
    return filepath