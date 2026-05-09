# dashboard.py — Streamlit Dashboard for Email Automation & Reminder System
# Run: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import logging
from datetime import datetime

# ── Credential loading: supports both local .env and Streamlit Cloud secrets ──
try:
    # Streamlit Cloud — reads from Secrets dashboard
    EMAIL_ADDRESS  = st.secrets["EMAIL_ADDRESS"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
    SENDER_COMPANY = st.secrets.get("SENDER_COMPANY", "Email Automation System")
    DRY_RUN        = st.secrets.get("DRY_RUN", "True")
    os.environ["EMAIL_ADDRESS"]  = EMAIL_ADDRESS
    os.environ["EMAIL_PASSWORD"] = EMAIL_PASSWORD
    os.environ["SENDER_COMPANY"] = SENDER_COMPANY
    os.environ["DRY_RUN"]        = DRY_RUN
except Exception:
    # Local development — reads from .env file
    from dotenv import load_dotenv
    load_dotenv()

# Add src/ to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from data_loader   import load_contacts, load_reminders, merge_data
from personalizer  import load_template, personalize_message
from email_sender  import send_email
from reporter      import generate_report
from logger        import setup_logger
# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Email Automation System",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS STYLING
# ─────────────────────────────────────────────
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f0f4ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
    .log-box {
        background-color: #1e1e1e;
        color: #00ff41;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        padding: 1rem;
        border-radius: 8px;
        height: 300px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="main-header">📧 Email Automation & Reminder System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated personalized email reminders </div>', unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────────
# SIDEBAR — CONFIGURATION PANEL
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/email-open.png", width=80)
    st.title("⚙️ Configuration")
    st.divider()

    # Run mode selector
    st.subheader("🔧 Run Mode")
    run_mode = st.radio(
        "Select Mode:",
        options=["🧪 Dry-Run (Simulate)", "📤 Send Real Emails"],
        index=0,
        help="Dry-Run simulates emails without sending. Real mode sends via Gmail SMTP."
    )
    is_dry_run = "Dry-Run" in run_mode

    # Show current .env status
    st.divider()
    st.subheader("🔐 Credentials Status")
    email_addr = os.getenv("EMAIL_ADDRESS", "")
    email_pass = os.getenv("EMAIL_PASSWORD", "")

    if email_addr and email_pass:
        st.success(f"✅ Email: {email_addr}")
        st.success("✅ App Password: Loaded")
    else:
        st.error("❌ .env credentials not found")
        st.caption("Create a .env file with EMAIL_ADDRESS and EMAIL_PASSWORD")

    # Company name
    st.divider()
    st.subheader("🏢 Sender Info")
    company_name = st.text_input(
        "Sender Company Name",
        value=os.getenv("SENDER_COMPANY", "Email Automation System")
    )

    # File paths
    st.divider()
    st.subheader("📁 Data Files")
    contacts_path  = st.text_input("Contacts CSV Path",  value="data/contacts.csv")
    reminders_path = st.text_input("Reminders CSV Path", value="data/reminders.csv")

    st.divider()
    st.caption("📌 Built with Python + Streamlit")
    st.caption(f"🕐 {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_all_data(c_path, r_path):
    contacts_df  = load_contacts(c_path)
    reminders_df = load_reminders(r_path)
    merged_df    = merge_data(contacts_df, reminders_df)
    return contacts_df, reminders_df, merged_df

try:
    contacts_df, reminders_df, merged_df = load_all_data(contacts_path, reminders_path)
    data_loaded = not contacts_df.empty and not reminders_df.empty
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# ─────────────────────────────────────────────
# TABS LAYOUT
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview",
    "👥 Contacts",
    "📅 Reminders",
    "▶️ Run & Send",
    "📊 Reports"
])

# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW / SUMMARY METRICS
# ══════════════════════════════════════════════
with tab1:
    st.subheader("📌 System Overview")

    if data_loaded:
        # Summary metric cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="👥 Total Contacts",
                value=len(contacts_df),
                delta="Loaded from CSV"
            )
        with col2:
            st.metric(
                label="📅 Total Reminders",
                value=len(reminders_df),
                delta="Scheduled"
            )
        with col3:
            reminder_types = reminders_df["reminder_type"].nunique() if not reminders_df.empty else 0
            st.metric(
                label="📂 Reminder Types",
                value=reminder_types,
                delta="Categories"
            )
        with col4:
            st.metric(
                label="🔧 Current Mode",
                value="DRY-RUN" if is_dry_run else "LIVE SEND",
                delta="Safe" if is_dry_run else "⚠️ Real Emails"
            )

        st.divider()

        # Reminder type breakdown chart
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📊 Reminder Types Breakdown")
            if not reminders_df.empty and "reminder_type" in reminders_df.columns:
                type_counts = reminders_df["reminder_type"].value_counts().reset_index()
                type_counts.columns = ["Reminder Type", "Count"]

                fig_pie = px.pie(
                    type_counts,
                    names="Reminder Type",
                    values="Count",
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=0.4
                )
                fig_pie.update_layout(
                    margin=dict(t=20, b=20, l=0, r=0),
                    showlegend=True,
                    height=300
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        with col_right:
            st.subheader("🏢 Contacts by Company")
            if not contacts_df.empty and "company" in contacts_df.columns:
                company_counts = contacts_df["company"].value_counts().reset_index()
                company_counts.columns = ["Company", "Count"]

                fig_bar = px.bar(
                    company_counts,
                    x="Count",
                    y="Company",
                    orientation="h",
                    color="Count",
                    color_continuous_scale="Blues",
                    text="Count"
                )
                fig_bar.update_layout(
                    margin=dict(t=20, b=20, l=0, r=0),
                    height=300,
                    showlegend=False,
                    coloraxis_showscale=False
                )
                fig_bar.update_traces(textposition="outside")
                st.plotly_chart(fig_bar, use_container_width=True)

        # Workflow diagram
        st.divider()
        st.subheader("🔄 Automation Workflow")
        st.markdown("""
        ```
        📋 contacts.csv  ──┐
                           ├──► 🔀 Merge Data ──► ✉️ Personalize ──► 📤 Send/Simulate ──► 📝 Log ──► 📊 Report
        📅 reminders.csv ──┘
        ```
        """)

    else:
        st.warning("⚠️ No data loaded. Check your CSV file paths in the sidebar.")

# ══════════════════════════════════════════════
# TAB 2 — CONTACTS
# ══════════════════════════════════════════════
with tab2:
    st.subheader("👥 Contact List")

    if data_loaded and not contacts_df.empty:
        # Filter options
        col_search, col_filter = st.columns([2, 1])
        with col_search:
            search_name = st.text_input("🔍 Search by Name or Company", placeholder="Type to filter...")
        with col_filter:
            if "role" in contacts_df.columns:
                roles = ["All"] + sorted(contacts_df["role"].dropna().unique().tolist())
                selected_role = st.selectbox("Filter by Role", roles)

        # Apply filters
        filtered_contacts = contacts_df.copy()
        if search_name:
            mask = (
                filtered_contacts["name"].str.contains(search_name, case=False, na=False) |
                filtered_contacts["company"].str.contains(search_name, case=False, na=False)
            )
            filtered_contacts = filtered_contacts[mask]

        if "role" in contacts_df.columns and selected_role != "All":
            filtered_contacts = filtered_contacts[filtered_contacts["role"] == selected_role]

        st.info(f"Showing **{len(filtered_contacts)}** of **{len(contacts_df)}** contacts")

        # Display table
        st.dataframe(
            filtered_contacts,
            use_container_width=True,
            hide_index=True,
            column_config={
                "email": st.column_config.TextColumn("📧 Email"),
                "name":  st.column_config.TextColumn("👤 Name"),
                "company": st.column_config.TextColumn("🏢 Company"),
                "role":  st.column_config.TextColumn("💼 Role"),
            }
        )

        # Download button
        csv_contacts = filtered_contacts.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Filtered Contacts CSV",
            data=csv_contacts,
            file_name="filtered_contacts.csv",
            mime="text/csv"
        )
    else:
        st.error("❌ contacts.csv not found or empty. Check path in sidebar.")

# ══════════════════════════════════════════════
# TAB 3 — REMINDERS
# ══════════════════════════════════════════════
with tab3:
    st.subheader("📅 Reminder Schedule")

    if data_loaded and not reminders_df.empty:

        # Filter by type
        if "reminder_type" in reminders_df.columns:
            reminder_types_list = ["All"] + sorted(reminders_df["reminder_type"].dropna().unique().tolist())
            selected_type = st.selectbox("Filter by Reminder Type", reminder_types_list)

            if selected_type != "All":
                filtered_reminders = reminders_df[reminders_df["reminder_type"] == selected_type]
            else:
                filtered_reminders = reminders_df.copy()
        else:
            filtered_reminders = reminders_df.copy()

        st.info(f"Showing **{len(filtered_reminders)}** reminders")

        # Show merged preview (with contact names)
        if not merged_df.empty:
            display_cols = ["reminder_id", "name", "email", "reminder_type", "subject", "send_date", "send_time"]
            available_cols = [c for c in display_cols if c in merged_df.columns]

            st.dataframe(
                merged_df[available_cols],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "reminder_id":   st.column_config.TextColumn("🆔 ID"),
                    "name":          st.column_config.TextColumn("👤 Recipient"),
                    "email":         st.column_config.TextColumn("📧 Email"),
                    "reminder_type": st.column_config.TextColumn("📂 Type"),
                    "subject":       st.column_config.TextColumn("📌 Subject"),
                    "send_date":     st.column_config.TextColumn("📅 Date"),
                    "send_time":     st.column_config.TextColumn("⏰ Time"),
                }
            )
        else:
            st.warning("Could not merge contacts and reminders. Check that contact_id matches.")

        # Email preview section
        st.divider()
        st.subheader("👁️ Email Preview")
        st.caption("Select a reminder to preview the personalized email that will be sent.")

        if not merged_df.empty:
            preview_options = merged_df.apply(
                lambda r: f"{r['name']} — {r['subject']}", axis=1
            ).tolist()
            selected_preview = st.selectbox("Select Reminder to Preview", preview_options)

            selected_idx = preview_options.index(selected_preview)
            selected_row = merged_df.iloc[selected_idx]

            template = load_template(selected_row["reminder_type"])
            if template:
                preview_body = personalize_message(template, selected_row, company_name)
                with st.expander("📄 Click to View Full Email Body", expanded=True):
                    st.text(preview_body)
    else:
        st.error("❌ reminders.csv not found or empty. Check path in sidebar.")

# ══════════════════════════════════════════════
# TAB 4 — RUN & SEND
# ══════════════════════════════════════════════
with tab4:
    st.subheader("▶️ Run Email Automation")

    # Mode banner
    if is_dry_run:
        st.markdown('<div class="warning-box">🧪 <strong>DRY-RUN MODE</strong> — Emails will be simulated only. No real emails will be sent.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">📤 <strong>LIVE SEND MODE</strong> — Real emails will be sent via Gmail SMTP.</div>', unsafe_allow_html=True)

    st.write("")

    if not data_loaded:
        st.error("Cannot run — data files not loaded. Fix CSV paths in sidebar.")
    else:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

        with col_btn1:
            run_button = st.button(
                "▶️ Run Now",
                type="primary",
                use_container_width=True,
                help="Process all reminders and send (or simulate) emails"
            )
        with col_btn2:
            clear_button = st.button(
                "🗑️ Clear Results",
                use_container_width=True,
                help="Clear the results and log below"
            )

        if clear_button:
            if "run_results" in st.session_state:
                del st.session_state["run_results"]
            if "run_logs" in st.session_state:
                del st.session_state["run_logs"]
            st.rerun()

        # ── RUN THE PIPELINE ─────────────────────────────────
        if run_button:
            # Override dry run mode
            os.environ["DRY_RUN"] = str(is_dry_run)

            results = []
            log_lines = []

            progress_bar = st.progress(0, text="Starting email automation...")
            total = len(merged_df)

            for i, (_, row) in enumerate(merged_df.iterrows()):
                progress_pct = int((i / total) * 100)
                progress_bar.progress(
                    progress_pct,
                    text=f"Processing {i+1}/{total}: {row['name']}..."
                )

                # Load and personalize template
                template = load_template(row["reminder_type"])
                if template is None:
                    log_lines.append(f"❌ SKIP | {row['name']} | Template not found")
                    continue

                body = personalize_message(template, row, company_name)
                if body is None:
                    log_lines.append(f"❌ SKIP | {row['name']} | Personalization failed")
                    continue

                # Send or simulate
                result = send_email(
                    recipient_email=row["email"],
                    recipient_name=row["name"],
                    subject=row["subject"],
                    body=body
                )
                results.append(result)

                # Build log line
                status_icon = "✅" if "SENT" in result["status"] or "DRY" in result["status"] else "❌"
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_lines.append(
                    f"{status_icon} [{timestamp}] | {result['status']} | To: {result['recipient_email']} | Subject: {result['subject']}"
                )

            progress_bar.progress(100, text="✅ All emails processed!")

            # Save to session state
            st.session_state["run_results"] = results
            st.session_state["run_logs"]    = log_lines

            # Generate CSV report
            if results:
                report_path = generate_report(results)
                st.session_state["report_path"] = report_path

        # ── DISPLAY RESULTS ────────────────────────────────────
        if "run_results" in st.session_state and st.session_state["run_results"]:
            results   = st.session_state["run_results"]
            log_lines = st.session_state.get("run_logs", [])

            st.divider()
            results_df = pd.DataFrame(results)

            # Summary metrics
            total   = len(results_df)
            success = len(results_df[results_df["status"].str.contains("SENT|DRY", na=False)])
            failed  = len(results_df[results_df["status"] == "FAILED"])

            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("📬 Total Processed", total)
            col_m2.metric("✅ Success / Simulated", success, delta=f"{round(success/total*100)}%")
            col_m3.metric("❌ Failed", failed, delta=f"-{failed}" if failed > 0 else "0")

            # Live log display
            st.subheader("📋 Activity Log")
            log_text = "\n".join(log_lines)
            st.code(log_text, language=None)

            # Results table
            st.subheader("📊 Results Table")
            st.dataframe(
                results_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "status": st.column_config.TextColumn("📌 Status"),
                    "recipient_name":  st.column_config.TextColumn("👤 Name"),
                    "recipient_email": st.column_config.TextColumn("📧 Email"),
                    "subject": st.column_config.TextColumn("📌 Subject"),
                    "error":   st.column_config.TextColumn("⚠️ Error"),
                }
            )

            # Download report
            if "report_path" in st.session_state:
                with open(st.session_state["report_path"], "r") as f:
                    st.download_button(
                        label="⬇️ Download Full Report CSV",
                        data=f.read(),
                        file_name="email_report.csv",
                        mime="text/csv"
                    )

# ══════════════════════════════════════════════
# TAB 5 — REPORTS & ANALYTICS
# ══════════════════════════════════════════════
with tab5:
    st.subheader("📊 Reports & Analytics")

    # Load existing reports from outputs folder
    output_dir = "outputs"
    report_files = []

    if os.path.exists(output_dir):
        report_files = sorted(
            [f for f in os.listdir(output_dir) if f.endswith(".csv")],
            reverse=True
        )

    if report_files:
        selected_report = st.selectbox(
            "📁 Select Report File",
            report_files,
            help="Reports are generated each time you run the automation"
        )

        report_df = pd.read_csv(os.path.join(output_dir, selected_report))

        # Metrics
        total   = len(report_df)
        success = len(report_df[report_df["status"].str.contains("SENT|DRY", na=False)])
        failed  = len(report_df[report_df["status"] == "FAILED"])

        col1, col2, col3 = st.columns(3)
        col1.metric("📬 Total", total)
        col2.metric("✅ Success", success)
        col3.metric("❌ Failed", failed)

        st.divider()

        col_chart1, col_chart2 = st.columns(2)

        # Status pie chart
        with col_chart1:
            st.subheader("📈 Email Status Distribution")
            status_counts = report_df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]

            color_map = {
                "SENT":               "#28a745",
                "DRY-RUN (Simulated)":"#17a2b8",
                "FAILED":             "#dc3545"
            }

            fig_status = px.pie(
                status_counts,
                names="Status",
                values="Count",
                color="Status",
                color_discrete_map=color_map,
                hole=0.4
            )
            fig_status.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig_status, use_container_width=True)

        # Bar chart by recipient
        with col_chart2:
            st.subheader("👥 Emails Per Recipient")
            if "recipient_name" in report_df.columns:
                name_counts = report_df["recipient_name"].value_counts().reset_index()
                name_counts.columns = ["Name", "Count"]

                fig_names = px.bar(
                    name_counts,
                    x="Name",
                    y="Count",
                    color="Count",
                    color_continuous_scale="Teal",
                    text="Count"
                )
                fig_names.update_layout(
                    height=300,
                    margin=dict(t=10, b=10),
                    coloraxis_showscale=False
                )
                fig_names.update_traces(textposition="outside")
                st.plotly_chart(fig_names, use_container_width=True)

        # Full report table
        st.subheader("📋 Full Report Table")
        st.dataframe(report_df, use_container_width=True, hide_index=True)

        # Download
        csv_data = report_df.to_csv(index=False)
        st.download_button(
            "⬇️ Download This Report",
            data=csv_data,
            file_name=selected_report,
            mime="text/csv"
        )

    elif "run_results" in st.session_state:
        st.info("✅ Run the automation in the '▶️ Run & Send' tab first to generate a report.")
    else:
        st.info("📭 No reports found yet. Run the automation to generate your first report.")
        st.caption("Reports are saved to: outputs/email_report_YYYYMMDD_HHMMSS.csv")