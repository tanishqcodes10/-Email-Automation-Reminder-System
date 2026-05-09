# scheduler.py — Schedules email sends using the schedule library

import schedule
import time
import logging

logger = logging.getLogger("EmailAutomation")

def run_email_job(job_function, *args):
    """Wrapper to run an email job with logging."""
    logger.info("Scheduler triggered — running email job now...")
    job_function(*args)

def schedule_daily(send_time, job_function, *args):
    """
    Schedule a job to run every day at a specific time.
    
    Args:
        send_time:    Time string in "HH:MM" format e.g. "09:00"
        job_function: The function to call (e.g. process_all_reminders)
    """
    schedule.every().day.at(send_time).do(run_email_job, job_function, *args)
    logger.info(f"Scheduled: Email job will run daily at {send_time}")
    
    logger.info("Scheduler running... Press Ctrl+C to stop.")
    
    while True:
        schedule.run_pending()
        time.sleep(30)   # Check every 30 seconds

def run_once_now(job_function, *args):
    """Run the email job immediately (used for testing or on-demand sends)."""
    logger.info("Running email job immediately (on-demand mode)...")
    job_function(*args)