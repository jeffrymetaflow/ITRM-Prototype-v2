import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
import uuid
import numpy as np
from utils.bootstrap import page_bootstrap
from utils.session_state import initialize_session
initialize_session()
from utils.auth import enforce_login
enforce_login()
from datetime import date
import io

st.title("📝 ITRM Session Input Form")

page_bootstrap(current_page="ITRM Session Input Form")  # Or "Risk Model", etc.

st.header("Required Inputs")
client_name = st.text_input("Client Name", "")
assessment_date = st.date_input("Assessment Date", value=date.today())
analyst_name = st.text_input("Analyst Name", "")
assessment_scope = st.text_input("Assessment Scope", "")
baseline_revenue = st.number_input("Baseline Revenue ($)", min_value=0.0, step=100000.0, format="%.2f")
it_expense = st.number_input("Total IT Expense ($)", min_value=0.0, step=100000.0, format="%.2f")
architecture_components = st.text_area("Architecture Components (comma-separated)", "")

st.header("Optional Inputs")
hardware_expense = st.number_input("Hardware Expense ($)", min_value=0.0, step=10000.0, format="%.2f")
software_expense = st.number_input("Software Expense ($)", min_value=0.0, step=10000.0, format="%.2f")
cybersecurity_expense = st.number_input("Cybersecurity Expense ($)", min_value=0.0, step=10000.0, format="%.2f")
maintenance_expense = st.number_input("Maintenance Expense ($)", min_value=0.0, step=10000.0, format="%.2f")
telecom_expense = st.number_input("Telecom Expense ($)", min_value=0.0, step=10000.0, format="%.2f")
personnel_expense = st.number_input("Personnel Expense ($)", min_value=0.0, step=10000.0, format="%.2f")
bcdr_expense = st.number_input("BC/DR Expense ($)", min_value=0.0, step=10000.0, format="%.2f")

component_maturity_scores = st.text_area("Component Maturity Scores (e.g., NetApp:4, AWS:3)", "")
component_risk_flags = st.text_area("Component Risk Flags (e.g., NetApp:False, AWS:True)", "")
criticality_score = st.text_area("Criticality Scores (e.g., NetApp:High, AWS:Medium)", "")

# Create a blank input template DataFrame
input_template = {
    "Input Name": [
        "client_name", "assessment_date", "analyst_name", "assessment_scope",
        "baseline_revenue", "it_expense", "architecture_components",
        "hardware_expense", "software_expense", "cybersecurity_expense",
        "maintenance_expense", "telecom_expense", "personnel_expense", "bcdr_expense",
        "component_maturity_scores", "component_risk_flags", "criticality_score"
    ],
    "Example Value": [
        "ACME Corp", "2025-05-04", "Jane Doe", "Full IT Environment",
        "150000000", "12000000", "AWS EC2, NetApp, VMware",
        "2500000", "1800000", "1400000",
        "900000", "700000", "4000000", "800000",
        "NetApp:4, AWS:3", "NetApp:False, AWS:True", "NetApp:High, AWS:Medium"
    ]
}
df_template = pd.DataFrame(input_template)

csv_buffer = io.StringIO()
df_template.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

# Download button for CSV
st.download_button(
    label="📥 Download ITRM Input Template (CSV)",
    data=csv_data,
    file_name="ITRM_Input_Template.csv",
    mime="text/csv"
)

if st.button("✅ Submit ITRM Inputs"):
    st.session_state.update({
        "client_name": client_name,
        "assessment_date": assessment_date,
        "analyst_name": analyst_name,
        "assessment_scope": assessment_scope,
        "baseline_revenue": baseline_revenue,
        "it_expense": it_expense,
        "architecture_components": architecture_components.split(","),
        "hardware_expense": hardware_expense,
        "software_expense": software_expense,
        "cybersecurity_expense": cybersecurity_expense,
        "maintenance_expense": maintenance_expense,
        "telecom_expense": telecom_expense,
        "personnel_expense": personnel_expense,
        "bcdr_expense": bcdr_expense,
        "component_maturity_scores": component_maturity_scores,
        "component_risk_flags": component_risk_flags,
        "criticality_score": criticality_score
    })
    st.success("Inputs saved to session state and ready for simulation.")
