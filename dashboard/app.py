import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="CloudLeak | FinOps & Waste Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
USD_TO_INR = 94.10

# Initialize Session State for Remediation Workflow
if "remediated_ids" not in st.session_state:
    st.session_state.remediated_ids = []

# Comprehensive CSS: SaaS Dark Theme Polish + High-Contrast Metrics & Buttons
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Force Deep Dark Theme Across Entire App & Sidebar */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0d1117 !important;
        color: #f0f6fc !important;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] * {
        color: #f0f6fc !important;
    }

    /* Metric Cards Styling & High-Contrast Text (No Truncation) */
    div[data-testid="stMetric"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        padding: 16px 18px !important;
        border-radius: 10px !important;
    }
    div[data-testid="stMetricLabel"] p {
        color: #8b949e !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
    }

    /* Force Button Text & Background Crisp White / High Contrast */
    div.stButton > button {
        color: #ffffff !important;
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
    }
    div.stButton > button:hover {
        background-color: #30363d !important;
        border-color: #8b949e !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.title("⚡ CloudLeak: Multi-Cloud FinOps & Waste Analytics")
st.markdown("Enterprise-grade cloud cost optimization, idle resource detection, and automated rightsizing.")

# Sidebar Controls & Filters
st.sidebar.header("🎛️ Dashboard Controls")

currency = st.sidebar.radio("Display Currency", ["INR (₹)", "USD ($)"], horizontal=True)
is_inr = currency == "INR (₹)"
curr_symbol = "₹" if is_inr else "$"
multiplier = USD_TO_INR if is_inr else 1.0

selected_mode = st.sidebar.selectbox("Data Source Mode", ["Demo Mock Data", "Live FastAPI Telemetry (Pending)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Telemetry Filters")
providers = st.sidebar.multiselect("Cloud Provider", ["AWS", "GCP", "Azure"], default=["AWS", "GCP", "Azure"])
severity_filter = st.sidebar.selectbox("Waste Severity", ["All", "Critical (<5% Util)", "Moderate (<15% Util)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎚️ What-If Policy Simulator")
cpu_threshold = st.sidebar.slider("Idle CPU Threshold (%)", min_value=2, max_value=20, value=10, step=1)

# Mock Data Generation
@st.cache_data
def load_mock_data():
    data = {
        "Resource ID": [
            "i-0a8b7c6d5e4f3a2b1", "i-0123456789abcdef0", "vol-0987654321fedcba0",
            "db-prod-sql-01", "aks-cluster-node-89", "gcp-instance-alpha",
            "s3-orphan-bucket-xyz", "azure-vm-legacy-02", "lambda-zombie-fn", "rds-idle-replica-04"
        ],
        "Provider": ["AWS", "AWS", "AWS", "Azure", "Azure", "GCP", "AWS", "Azure", "AWS", "Azure"],
        "Type": ["EC2 Compute", "EC2 Compute", "EBS Volume", "PostgreSQL RDS", "AKS Node", "Compute Engine", "S3 Storage", "Virtual Machine", "Lambda", "SQL Replica"],
        "Region": ["ap-south-1", "eu-west-1", "ap-south-1", "centralindia", "eastus", "asia-south1", "ap-south-1", "westus", "ap-south-1", "centralindia"],
        "Base Cost USD": [1250.0, 3400.0, 450.0, 4800.0, 2100.0, 1850.0, 320.0, 950.0, 600.0, 2700.0],
        "CPU Utilization (%)": [2.4, 4.1, 0.0, 12.5, 6.2, 3.8, 0.0, 5.1, 1.2, 4.9],
        "Recommendation": [
            "Terminate or Downsize to t3.medium", "Rightsize to t3.large", "Delete Unattached Volume",
            "Optimize Connection Pools", "Scale down node pool", "Migrate to e2-medium",
            "Apply Lifecycle Rule / Delete", "Decommission Legacy VM", "Delete Inactive Function", "Terminate Unused Replica"
        ]
    }
    return pd.DataFrame(data)

df_raw = load_mock_data().copy()

# Dynamic Policy & Currency Calculations
df_raw["Status"] = df_raw["CPU Utilization (%)"].apply(
    lambda x: "Critical" if x < 5.0 else ("Moderate" if x <= cpu_threshold else "Healthy")
)
df_raw["Monthly Cost"] = df_raw["Base Cost USD"] * multiplier
df_raw["Estimated Waste"] = df_raw.apply(
    lambda r: r["Monthly Cost"] * 0.9 if r["CPU Utilization (%)"] < 5.0 else (
        r["Monthly Cost"] * 0.5 if r["CPU Utilization (%)"] <= cpu_threshold else 0.0
    ),
    axis=1
)
df_raw["Remediated"] = df_raw["Resource ID"].isin(st.session_state.remediated_ids)

# Calculate Session Savings from Remediated Items
session_savings = df_raw[df_raw["Remediated"]]["Estimated Waste"].sum()

# Apply Sidebar Filters
df_filtered = df_raw[df_raw["Provider"].isin(providers)].copy()
if severity_filter != "All":
    target_status = "Critical" if "Critical" in severity_filter else "Moderate"
    df_filtered = df_filtered[df_filtered["Status"] == target_status]

# Tabs Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Overview",
    "🗑️ Waste Audit & Remediation",
    "⚙️ Rules & Policy Engine",
    "📚 Architecture & Docs"
])

with tab1:
    st.subheader(f"High-Level Cost & Waste Metrics ({currency})")

    total_spend = df_filtered["Monthly Cost"].sum()
    active_waste = df_filtered[~df_filtered["Remediated"]]["Estimated Waste"].sum()
    avg_cpu = df_filtered["CPU Utilization (%)"].mean() if not df_filtered.empty else 0.0
    flagged_count = len(df_filtered[df_filtered["Status"] != "Healthy"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Monthly Spend", f"{curr_symbol}{total_spend:,.0f}", delta="+4.2% vs last month", delta_color="inverse")
    col2.metric("Remaining Actionable Waste", f"{curr_symbol}{active_waste:,.0f}", delta=f"Threshold: <{cpu_threshold}% CPU", delta_color="off")
    col3.metric("Session Savings Realized", f"{curr_symbol}{session_savings:,.0f}", delta=f"{len(st.session_state.remediated_ids)} fixed", delta_color="normal")
    col4.metric("Flagged Resources", f"{flagged_count} / {len(df_filtered)}", delta=f"Avg CPU: {avg_cpu:.1f}%", delta_color="off")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Spend Distribution by Provider")
        if not df_filtered.empty:
            fig_prov = px.pie(
                df_filtered,
                names="Provider",
                values="Monthly Cost",
                hole=0.45,
                color_discrete_sequence=["#58a6ff", "#3fb950", "#d29922"]
            )
            fig_prov.update_traces(hovertemplate=f"<b>%{{label}}</b><br>Spend: {curr_symbol}%{{value:,.0f}}<extra></extra>")
            fig_prov.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22", font_color="#f0f6fc")
            st.plotly_chart(fig_prov, use_container_width=True)
        else:
            st.info("No data available for selected filters.")

    with col_b:
        st.markdown("### Waste Impact by Resource Type")
        if not df_filtered.empty:
            fig_waste = px.bar(
                df_filtered,
                x="Type",
                y="Estimated Waste",
                color="Provider",
                barmode="group",
                color_discrete_sequence=["#58a6ff", "#3fb950", "#d29922"]
            )
            fig_waste.update_traces(hovertemplate=f"<b>%{{x}}</b><br>Waste: {curr_symbol}%{{y:,.0f}}<extra></extra>")
            fig_waste.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="#f0f6fc",
                yaxis_title=f"Wasted Spend ({curr_symbol})",
                xaxis_title=""
            )
            st.plotly_chart(fig_waste, use_container_width=True)
        else:
            st.info("No data available for selected filters.")

with tab2:
    st.subheader("Interactive Waste Audit & One-Click Remediation")
    st.markdown("Select flagged resources below to simulate automated rightsizing and calculate immediate savings.")

    if not df_filtered.empty:
        audit_df = df_filtered[[
            "Remediated", "Resource ID", "Provider", "Type", "Region",
            "Monthly Cost", "Estimated Waste", "CPU Utilization (%)", "Status", "Recommendation"
        ]].copy()

        edited_df = st.data_editor(
            audit_df,
            use_container_width=True,
            hide_index=True,
            disabled=["Resource ID", "Provider", "Type", "Region", "Monthly Cost", "Estimated Waste", "CPU Utilization (%)", "Status", "Recommendation"],
            column_config={
                "Remediated": st.column_config.CheckboxColumn("Apply Fix", help="Check to simulate rightsizing this resource"),
                "Monthly Cost": st.column_config.NumberColumn(f"Monthly Cost ({curr_symbol})", format=f"{curr_symbol}%.0f"),
                "Estimated Waste": st.column_config.NumberColumn(f"Est. Waste ({curr_symbol})", format=f"{curr_symbol}%.0f"),
                "CPU Utilization (%)": st.column_config.ProgressColumn(
                    "CPU Utilization",
                    help="Average 7-day CPU utilization",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            }
        )

        btn_col1, btn_col2, _ = st.columns([2, 2, 4])
        with btn_col1:
            if st.button("🚀 Apply Selected Rightsizing", type="primary"):
                newly_fixed = edited_df[edited_df["Remediated"]]["Resource ID"].tolist()
                unfixed_visible = edited_df[~edited_df["Remediated"]]["Resource ID"].tolist()
                updated_set = (set(st.session_state.remediated_ids) - set(unfixed_visible)) | set(newly_fixed)
                st.session_state.remediated_ids = list(updated_set)
                st.toast("Rightsizing policies applied! Savings updated.", icon="✅")
                st.rerun()

        with btn_col2:
            if st.button("🔄 Reset Simulation"):
                st.session_state.remediated_ids = []
                st.toast("Remediation state reset.", icon="🔄")
                st.rerun()

        st.markdown("---")
        export_cols = ["Resource ID", "Provider", "Type", "Region", "Monthly Cost", "Estimated Waste", "CPU Utilization (%)", "Status", "Recommendation"]
        csv_data = df_filtered[export_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 Export Filtered Audit Report ({currency} CSV)",
            data=csv_data,
            file_name=f"cloudleak_audit_{'inr' if is_inr else 'usd'}.csv",
            mime="text/csv",
        )
    else:
        st.info("No resources match your active sidebar filters.")

with tab3:
    st.subheader("CloudLeak Rules & Threshold Engine")
    st.info(f"**Active Dynamic Policy:** Resources below **{cpu_threshold}% CPU utilization** are automatically flagged for rightsizing.")
    st.markdown("""
    CloudLeak evaluates telemetry against predefined FinOps guardrails:
    * **Critical Idle Compute:** Instances with sustained CPU utilization $< 5\%$ over a 7-day rolling window (90% waste recovery).
    * **Moderate Underutilization:** Instances below the user-defined threshold slider (50% waste recovery via instance downsize).
    * **Orphaned Storage:** EBS disks or persistent volumes unattached to any running instance for $> 48$ hours.
    * **Zombie Serverless Functions:** Lambda / Cloud Functions invoked $0$ times in 14 days.
    """)

with tab4:
    st.subheader("System Architecture & Documentation")
    st.markdown("""
    ### Architecture Overview
    * **Frontend Layer:** Streamlit with Plotly data visualization engines, custom CSS dark mode, and session-state remediation simulation.
    * **Data Pipeline:** Currently operating in **Demo Mode** via structured multi-cloud telemetry simulators (`ap-south-1`, `centralindia`, `asia-south1`, and global regions).
    * **Backend Integration:** Decoupled design ready to connect to FastAPI telemetry collectors and cloud SDKs (Boto3, Azure SDK, Google Cloud Client).

    ### Repository & Deployment
    * Version controlled via Git & GitHub.
    * Container-ready for multi-host Docker orchestration.
    """)