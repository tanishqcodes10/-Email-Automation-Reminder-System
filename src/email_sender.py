# email_sender.py — Handles SMTP connection and email sending

import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger("EmailAutomation")

# SMTP Configuration
SMTP_SERVER   = "smtp.gmail.com"
SMTP_PORT     = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DRY_RUN       = os.getenv("DRY_RUN", "True").lower() == "true"


def send_email(recipient_email, recipient_name, subject, body):
    """
    Send a personalized email to one recipient.
    
    If DRY_RUN=True in .env, simulates sending without real SMTP call.
    Returns: dict with status, recipient, and message info.
    """
    
    result = {
        "recipient_name":  recipient_name,
        "recipient_email": recipient_email,
        "subject":         subject,
        "status":          None,
        "error":           None
    }
    
    # ── DRY-RUN MODE ─────────────────────────────────────────────
    if DRY_RUN:
        logger.info(f"[DRY-RUN] SIMULATED → To: {recipient_email} | Subject: {subject}")
        result["status"] = "DRY-RUN (Simulated)"
        return result
    
    # ── REAL SEND MODE ───────────────────────────────────────────
    try:
        # Validate credentials are loaded
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            raise ValueError("EMAIL_ADDRESS or EMAIL_PASSWORD not set in .env file")
        
        # Build email message
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        # Connect and send
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()           # Encrypt connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        
        logger.info(f"[SENT] ✅ To: {recipient_email} | Subject: {subject}")
        result["status"] = "SENT"
        
    except smtplib.SMTPAuthenticationError:
        error_msg = "Authentication failed — check your App Password"
        logger.error(f"[FAILED] ❌ To: {recipient_email} | Error: {error_msg}")
        result["status"] = "FAILED"
        result["error"]  = error_msg
        
    except smtplib.SMTPException as e:
        logger.error(f"[FAILED] ❌ To: {recipient_email} | SMTP Error: {e}")
        result["status"] = "FAILED"
        result["error"]  = str(e)
        
    except Exception as e:
        logger.error(f"[FAILED] ❌ To: {recipient_email} | Unexpected Error: {e}")
        result["status"] = "FAILED"
        result["error"]  = str(e)
    
    return result