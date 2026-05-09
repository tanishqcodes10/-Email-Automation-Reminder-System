# personalizer.py — Loads templates and personalizes email messages

import os
import logging

logger = logging.getLogger("EmailAutomation")

def load_template(reminder_type):
    """Load the correct email template based on reminder type."""
    
    # Map reminder types to template files
    template_map = {
        "meeting":  "templates/meeting_template.txt",
        "payment":  "templates/payment_template.txt",
        "webinar":  "templates/reminder_template.txt",
        "task":     "templates/reminder_template.txt",
        "followup": "templates/reminder_template.txt",
    }
    
    # Get template path (default to reminder_template)
    template_path = template_map.get(reminder_type, "templates/reminder_template.txt")
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info(f"Template loaded: '{template_path}' for type '{reminder_type}'")
        return content
    except FileNotFoundError:
        logger.error(f"Template file not found: {template_path}")
        return None

def personalize_message(template_content, row, company_sender):
    """Replace placeholders in the template with actual contact data."""
    try:
        # Build the replacement dictionary from the merged row
        replacements = {
            "{name}":           str(row.get("name", "Valued Contact")),
            "{company}":        str(row.get("company", "Your Organization")),
            "{role}":           str(row.get("role", "Team Member")),
            "{subject}":        str(row.get("subject", "Important Reminder")),
            "{reminder_type}":  str(row.get("reminder_type", "General")),
            "{send_date}":      str(row.get("send_date", "N/A")),
            "{send_time}":      str(row.get("send_time", "N/A")),
            "{company_sender}": company_sender,
        }
        
        # Replace each placeholder in the template
        message = template_content
        for placeholder, value in replacements.items():
            message = message.replace(placeholder, value)
        
        return message
    except Exception as e:
        logger.error(f"Error personalizing message for {row.get('name', 'Unknown')}: {e}")
        return None