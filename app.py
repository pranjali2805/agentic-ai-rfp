import streamlit as st
import pandas as pd
from sales_agent import SalesAgent
from technical_agent import TechnicalAgent
from pricing_agent import PricingAgent
from report_generator import ReportGenerator

# --- Page Config ---
st.set_page_config(page_title="Agentic AI – RFP Automation", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    /* General App Background */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
        font-family: 'Inter', sans-serif;
    }

    /* Headings */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        padding: 1.5rem 1rem;
        border-right: 1px solid #30363d;
    }

    /* Buttons */
    .stButton>button {
        background-color: #238636;
        color: #ffffff;
        border: none;
        padding: 0.5rem 1.2rem;
        border-radius: 6px;
        font-weight: 500;
        transition: background-color 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        color: #ffffff;
    }

    /* File uploader */
    [data-testid="stFileUploader"] section {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
    }

    /* Info box */
    .stAlert {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
    }

    /* Divider */
    hr {
        border: 0;
        border-top: 1px solid #30363d;
        margin: 1.5rem 0;
    }

    /* Footer text */
    .footer-text {
        color: #8b949e;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Title Section ---
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1> Agentic AI System for Automating B2B RFP Responses</h1>
    <p style="color:#8b949e; font-size:1.05rem;">
         An intelligent multi-agent workflow for automating enterprise tender responses.
    </p>
    <hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, #238636, transparent);">
</div>
""", unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header(" System Controls")
uploaded_file = st.sidebar.file_uploader(
    "Upload RFP File (JSON, PDF, or DOCX)", 
    type=["json", "pdf", "docx"]
)
run_process = st.sidebar.button(" Run Automation")

st.sidebar.markdown("---")
st.sidebar.download_button(
    label=" Download Sample RFP (PDF)",
    data=open("data/Sample_RFP_Report.pdf", "rb"),
    file_name="Sample_RFP_Report.pdf"
)

# --- Default Paths ---
rfp_path = "data/sample_rfp.json"
sku_path = "data/mock_skus.csv"

# --- Main App Logic ---
if run_process:
    with st.spinner("Running AI Agents... please wait "):
        if uploaded_file is not None:
            rfp_path = f"data/{uploaded_file.name}"
            with open(rfp_path, "wb") as f:
                f.write(uploaded_file.read())

        # Load agents
        sales = SalesAgent(rfp_path)
        sales.load_rfp()
        items = sales.get_rfp_items()

        tabs = st.tabs([" RFP Summary", " SKU Matches", " Pricing", " Report"])

        with tabs[0]:
            st.subheader("RFP Summary")
            st.json(sales.rfp_data)

        if not items:
            st.error(" No items detected in this RFP. Ensure it contains a clear item table or try OCR version.")
            st.stop()

        # Technical Agent
        tech = TechnicalAgent(sku_path)
        tech.load_sku_data()
        matches_df = tech.match_rfp_items(items)
        matches_csv = "data/technical_matches.csv"
        matches_df.to_csv(matches_csv, index=False)

        with tabs[1]:
            st.subheader("Top SKU Matches per Item")
            st.dataframe(matches_df, use_container_width=True)

        # Pricing Agent
        pricing = PricingAgent(matches_csv)
        pricing.load_matches()
        top_df = pricing.select_top_matches()
        final_df = pricing.calculate_costs(top_df)
        pricing_csv = "data/final_pricing_summary.csv"
        final_df.to_csv(pricing_csv, index=False)

        with tabs[2]:
            st.subheader("Final Pricing Summary")
            st.dataframe(final_df, use_container_width=True)

        # Report Generator
        ppt_path = "data/Generated_RFP_Report.pptx"
        ppt = ReportGenerator("Industrial Cable Supply (Demo)", final_df)
        ppt.add_title_slide()
        ppt.add_process_flow()
        ppt.add_match_summary()
        ppt.add_pricing_summary()
        ppt.add_conclusion_slide()
        ppt.save_ppt(ppt_path)

        with tabs[3]:
            st.success("Workflow Completed Successfully!")
            st.download_button(
                label="Download PPT Report",
                data=open(ppt_path, "rb"),
                file_name="Generated_RFP_Report.pptx"
            )
else:
    st.info("Upload an RFP file (PDF/JSON) and click **Run Automation** to start.")

