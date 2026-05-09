# data_loader.py — Reads contacts and reminders from CSV files

import pandas as pd
import logging

logger = logging.getLogger("EmailAutomation")

def load_contacts(filepath="data/contacts.csv"):
    """Load contact list from CSV file."""
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Contacts loaded: {len(df)} records from '{filepath}'")
        return df
    except FileNotFoundError:
        logger.error(f"Contact file not found: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading contacts: {e}")
        return pd.DataFrame()

def load_reminders(filepath="data/reminders.csv"):
    """Load reminder schedule from CSV file."""
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Reminders loaded: {len(df)} records from '{filepath}'")
        return df
    except FileNotFoundError:
        logger.error(f"Reminder file not found: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading reminders: {e}")
        return pd.DataFrame()

def merge_data(contacts_df, reminders_df):
    """Merge contacts with their reminders using contact_id."""
    try:
        # Merge on contact_id (reminders) and id (contacts)
        merged = pd.merge(
            reminders_df,
            contacts_df,
            left_on="contact_id",
            right_on="id",
            how="inner"
        )
        logger.info(f"Data merged successfully: {len(merged)} email tasks ready")
        return merged
    except Exception as e:
        logger.error(f"Error merging data: {e}")
        return pd.DataFrame()