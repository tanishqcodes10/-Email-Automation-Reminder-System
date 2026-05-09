# 📧 Email Automation & Reminder System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SMTP](https://img.shields.io/badge/Gmail-SMTP%20Enabled-EA4335?style=for-the-badge&logo=gmail&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A complete, industry-oriented Python automation project that sends personalized email reminders to contacts — with scheduling, live Streamlit dashboard, logging, dry-run simulation, and CSV report generation.**

[🚀 Run Dashboard](#-how-to-run) · [📂 Folder Structure](#-folder-structure) · [🎯 Features](#-features) · [📸 Screenshots](#-screenshots)

</div>

---

## 📌 Problem Statement

Companies manually send hundreds of reminder emails every day — meeting alerts, payment reminders, follow-ups, webinar nudges, and task notifications. This wastes hours of productive time and introduces human errors such as missed sends, wrong recipient names, and inconsistent messaging.

This project **fully automates the email workflow** — from reading a contact list and personalizing messages to scheduling sends, logging results, and generating reports — all controllable via a visual Streamlit dashboard or CLI.

---

## 🏢 Industry Relevance

| Team | Real-World Use Case |
|------|---------------------|
| 🧑‍💼 HR | Interview reminders, onboarding emails, offer letter follow-ups |
| 💰 Sales | Payment reminders, product demo follow-ups, lead nurturing |
| ⚙️ Operations | Meeting alerts, task deadline notifications, shift reminders |
| 🎓 Training | Webinar reminders, assignment nudges, course deadline alerts |
| 🗂️ Admin | Event reminders, document submission deadlines, policy notices |

---

## 🎯 Features

- 📋 **CSV Contact Management** — Read contacts (name, email, company, role) from CSV
- 📅 **Reminder Scheduling** — Load reminders with type, subject, date, and time from CSV
- ✉️ **Personalized Email Templates** — Auto-fill `{name}`, `{company}`, `{role}` placeholders
- 🔒 **Secure Credentials** — Gmail App Password stored in `.env` (never hardcoded)
- 🧪 **Dry-Run Mode** — Simulate the full pipeline without sending real emails
- ⏰ **Daily Scheduler** — Schedule sends at any time using the `schedule` library
- 📝 **Full Activity Logging** — Timestamped log file for every send attempt
- 📊 **Streamlit Dashboard** — 5-tab visual interface with charts, email preview, and run controls
- 📈 **Auto-Generated CSV Reports** — Status report after every run (Sent / Failed / Simulated)
- ❌ **Error Handling** — SMTP failures caught and logged without crashing the pipeline

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core language |
| smtplib | Built-in | SMTP email sending via Gmail |
| email.mime | Built-in | Email message formatting |
| pandas | ≥ 2.2.3 | CSV data loading, merging, report generation |
| schedule | ≥ 1.2.0 | Daily job scheduling |
| python-dotenv | ≥ 1.0.0 | Secure environment variable management |
| logging | Built-in | Activity and error logging |
| streamlit | ≥ 1.35.0 | Interactive visual dashboard |
| plotly | ≥ 5.22.0 | Charts inside Streamlit dashboard |

---

## 📁 Folder Structure

```
Email-Automation-Reminder-System/
│
├── data/                          # Input CSV files
│   ├── contacts.csv               # Name, email, company, role
│   └── reminders.csv              # Reminder ID, subject, date, type
│
├── templates/                     # Email message templates
│   ├── reminder_template.txt      # Generic reminder (webinar, task, follow-up)
│   ├── meeting_template.txt       # Meeting alert template
│   └── payment_template.txt       # Payment reminder template
│
├── src/                           # All Python source modules
│   ├── data_loader.py             # Reads and merges CSV files using pandas
│   ├── personalizer.py            # Fills {placeholders} from templates
│   ├── email_sender.py            # SMTP send logic + dry-run mode
│   ├── scheduler.py               # schedule library integration
│   ├── logger.py                  # Logging configuration
│   └── reporter.py                # Generates CSV report
│
├── outputs/                       # Generated report files
│   └── email_report_*.csv         # Auto-named report after each run
│
├── logs/                          # Runtime log files
│   └── email_log_YYYYMMDD.log     # Timestamped activity log
│
├── images/                        # Screenshots for README
│   ├── dashboard_overview.png
│   ├── dashboard_run.png
│   ├── dashboard_report.png
│   ├── dry_run_terminal.png
│   └── folder_structure.png
│
├── docs/                          # Optional extended documentation
│   └── project_notes.md
│
├── dashboard.py                   # Streamlit dashboard (5-tab UI)
├── main.py                        # CLI entry point
├── requirements.txt               # All pip dependencies
├── .env.example                   # Credential template (safe to commit)
├── .gitignore                     # Excludes .env, __pycache__, venv/
└── README.md                      # This file
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Email-Automation-Reminder-System.git
cd Email-Automation-Reminder-System
```

### 2️⃣ Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Python 3.14 users:** If you get build errors, run:
> ```bash
> pip install --only-binary=:all: pandas schedule python-dotenv streamlit plotly
> ```

### 4️⃣ Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Open .env and fill in your real values
```

---

## 🔐 Environment Variable Setup

Create a `.env` file in the project root with the following:

```env
EMAIL_ADDRESS=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
SENDER_COMPANY=YourCompany Pvt Ltd
DRY_RUN=True
```

### How to Get a Gmail App Password

1. Go to **myaccount.google.com → Security**
2. Enable **2-Step Verification** (required first)
3. Search for **"App Passwords"** and open it
4. Enter an app name (e.g., `EmailAutomationProject`) → Click **Create**
5. Copy the **16-character password** Google shows you
6. Paste it as `EMAIL_PASSWORD` in your `.env` file (remove spaces)

> 🔒 **Never commit your `.env` file to GitHub.** It is already listed in `.gitignore`.

---

## ▶️ How to Run

### Option 1 — Streamlit Dashboard (Recommended)

```bash
streamlit run dashboard.py
```

Opens at `http://localhost:8501` in your browser with a full 5-tab visual interface.

### Option 2 — CLI Dry-Run (Simulate — No Real Emails)

```bash
python main.py --mode dry-run
```

### Option 3 — CLI Live Send (Real Emails via Gmail)

```bash
# First set DRY_RUN=False in your .env file
python main.py --mode send
```

### Option 4 — CLI Scheduled Daily Send

```bash
python main.py --mode schedule --time 09:00
```

Runs the email pipeline every day at 9:00 AM automatically.

---

## 🖥️ Dashboard — 5 Tabs

| Tab | What It Shows |
|-----|---------------|
| 🏠 **Overview** | Metric cards, reminder type pie chart, company bar chart, workflow diagram |
| 👥 **Contacts** | Searchable + filterable contact table, CSV download button |
| 📅 **Reminders** | Full reminder schedule, live email body preview per contact |
| ▶️ **Run & Send** | One-click dry-run or live send, progress bar, activity log, results table |
| 📊 **Reports** | Load past reports, status pie chart, per-recipient bar chart, CSV download |

---

## 📊 Sample Output

### Terminal — Dry-Run Mode

```
2026-05-09 09:00:01 | INFO | ============================================================
2026-05-09 09:00:01 | INFO | Email Automation & Reminder System Started
2026-05-09 09:00:01 | INFO | Mode selected: DRY-RUN
2026-05-09 09:00:01 | INFO | Contacts loaded: 5 records from 'data/contacts.csv'
2026-05-09 09:00:01 | INFO | Reminders loaded: 5 records from 'data/reminders.csv'
2026-05-09 09:00:01 | INFO | Data merged successfully: 5 email tasks ready
2026-05-09 09:00:01 | INFO | [DRY-RUN] SIMULATED → To: priya.sharma@example.com | Subject: Team Standup Meeting Reminder
2026-05-09 09:00:01 | INFO | [DRY-RUN] SIMULATED → To: rahul.mehta@example.com  | Subject: Invoice Payment Due Reminder
2026-05-09 09:00:01 | INFO | [DRY-RUN] SIMULATED → To: ananya.singh@example.com | Subject: Python Automation Webinar Reminder
2026-05-09 09:00:01 | INFO | [DRY-RUN] SIMULATED → To: vikas.gupta@example.com  | Subject: Quarterly Report Submission Reminder
2026-05-09 09:00:01 | INFO | [DRY-RUN] SIMULATED → To: sneha.patel@example.com  | Subject: Follow-Up: Product Demo Scheduled
2026-05-09 09:00:01 | INFO | ============================================================
2026-05-09 09:00:01 | INFO | REPORT SUMMARY
2026-05-09 09:00:01 | INFO |   Total Emails Processed : 5
2026-05-09 09:00:01 | INFO |   Sent / Simulated       : 5
2026-05-09 09:00:01 | INFO |   Failed                 : 0
2026-05-09 09:00:01 | INFO |   Report saved to        : outputs/email_report_20260509_090001.csv
2026-05-09 09:00:01 | INFO | ============================================================
```

### Generated Report CSV

| timestamp | recipient_name | recipient_email | subject | status | error |
|-----------|---------------|-----------------|---------|--------|-------|
| 2026-05-09 09:00:01 | Priya Sharma | priya.sharma@example.com | Team Standup Meeting Reminder | DRY-RUN (Simulated) | |
| 2026-05-09 09:00:01 | Rahul Mehta | rahul.mehta@example.com | Invoice Payment Due Reminder | DRY-RUN (Simulated) | |
| 2026-05-09 09:00:01 | Ananya Singh | ananya.singh@example.com | Python Automation Webinar Reminder | DRY-RUN (Simulated) | |
| 2026-05-09 09:00:01 | Vikas Gupta | vikas.gupta@example.com | Quarterly Report Submission Reminder | DRY-RUN (Simulated) | |
| 2026-05-09 09:00:01 | Sneha Patel | sneha.patel@example.com | Follow-Up: Product Demo Scheduled | DRY-RUN (Simulated) | |

---

## 📸 Screenshots

> *(Add screenshots to the `images/` folder and they will appear here)*

| Screenshot | Description |
|------------|-------------|
| `images/dashboard_overview.png` | Streamlit Overview tab with metrics and charts |
| `images/dashboard_run.png` | Run & Send tab showing live progress and activity log |
| `images/dashboard_report.png` | Reports tab with status pie chart |
| `images/dry_run_terminal.png` | Terminal output in dry-run mode |
| `images/folder_structure.png` | Project folder in VS Code Explorer |

---

## 🔄 Automation Workflow

```
📋 contacts.csv ──┐
                  ├──► 🔀 Merge Data ──► ✉️ Personalize ──► 📤 Send / Simulate
📅 reminders.csv ─┘                                               │
                                                                  ▼
                                                    📝 Log (logs/email_log.log)
                                                                  │
                                                                  ▼
                                                    📊 Report (outputs/email_report.csv)
```

---

## 🧪 Running Without Real Emails (Safe Simulation)

This project is fully testable without any Gmail account or real recipients:

1. Keep `DRY_RUN=True` in your `.env` file
2. Use dummy contacts with `@example.com` email addresses in `data/contacts.csv`
3. Run `python main.py --mode dry-run` or use the Streamlit dashboard
4. The full pipeline runs — loading, merging, personalizing, logging, reporting — with `[DRY-RUN] SIMULATED` in place of real sends
5. All logs and reports are generated exactly as they would be in production

---

## 🎓 Learning Outcomes

After building this project, you will know:

- ✅ How to send emails in Python using `smtplib` and Gmail SMTP
- ✅ How to process CSV data using `pandas` (load, merge, iterate, export)
- ✅ How to securely manage credentials with `python-dotenv`
- ✅ How to schedule automated jobs using the `schedule` library
- ✅ How to implement Python `logging` for production-grade audit trails
- ✅ How to build interactive dashboards with `Streamlit` and `Plotly`
- ✅ How to structure a modular Python project for GitHub
- ✅ How to use Git and GitHub for version control with meaningful commits
- ✅ How to implement error handling and dry-run modes

---

## 📅 Day-Wise Build Plan

| Day | Task | Commit Message |
|-----|------|----------------|
| Day 1 | Setup venv, install libraries, create folder structure | `Phase 1-2: Environment setup and folder structure` |
| Day 2 | Create contacts.csv, reminders.csv, all templates | `Phase 3-4: Add dummy contacts CSV and email templates` |
| Day 3 | Write data_loader.py and personalizer.py | `Phase 6: Implement data loading and email personalization` |
| Day 4 | Write email_sender.py + main.py with dry-run | `Phase 7-8: Email sender with dry-run mode and scheduler` |
| Day 5 | Write logger.py and reporter.py, verify outputs | `Phase 9: Add logging module and CSV report generation` |
| Day 6 | Add Streamlit dashboard (dashboard.py) | `Phase 11: Add Streamlit dashboard with 5 tabs and charts` |
| Day 7 | Write README, add screenshots, push to GitHub | `Phase 10: Complete README, documentation, and final cleanup` |

---

## 🔐 Security Notes

| ✅ Do This | ❌ Never Do This |
|-----------|-----------------|
| Store credentials in `.env` | Hardcode email/password in code |
| Add `.env` to `.gitignore` | Commit `.env` to GitHub |
| Upload `.env.example` with placeholders | Upload real credentials |
| Use Gmail App Password | Use your regular Gmail password |
| Use dummy `@example.com` contacts | Upload real people's email addresses |

---

## 📦 requirements.txt

```
pandas>=2.2.3
schedule>=1.2.0
python-dotenv>=1.0.0
streamlit>=1.35.0
plotly>=5.22.0
```

---

## 👤 Author

**Tanishq Jakate**
🔗 [LinkedIn](linkedin.com/in/tanishq-jakate-93617a402) | 🐙 [GitHub](https://github.com/tanishqcodes10)

> 💡 *Built as a Python automation portfolio project demonstrating real-world email workflow automation skills relevant to Python Developer, Automation Engineer, HR Tech, Operations, and Business Productivity roles.*

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute for personal and commercial purposes.

---

<div align="center">
⭐ If you found this project useful, please give it a star on GitHub!
</div>
