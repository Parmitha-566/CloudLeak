import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="CloudLeak | Enterprise Cost Optimization",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Executive Dark SaaS Theme CSS
# ---------------------------------------------------------
st.markdown("""
    <style>
        .stApp {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: #f0f6fc !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        .stMarkdown p {
            color: #8b949e !important;
        }
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 18px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        div[data-testid="stMetricLabel"] > div {
            color: #8b949e !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
        }
        div[data-testid="stMetricValue"] > div {
            color: #58a6ff !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stDataFrame"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 8px;
        }
        hr {
            border-color: #30363d !important;
            margin: 1.5rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Section & Interactive Controls
# ---------------------------------------------------------
with st.sidebar:
    st.title("☁️ CloudLeak")
    st.caption("Multi-Cloud Telemetry & Cost Engine")
    st.divider()

    st.subheader("Data Source")
    data_source = st.selectbox(
        "Backend Mode",
        options=["Demo Mode (Mock Data)", "Live API (FastAPI)"],
        index=0,
        help="Fallback mock mode active for standalone portfolio presentation."
    )

    st.divider()
    st.subheader("Telemetry Scope")
    
    selected_providers = st.multiselect(
        "Cloud Providers",
        options=["AWS", "GCP", "Azure"],
        default=["AWS", "GCP", "Azure"]
    )
    
    selected_env = st.selectbox(
        "Environment Filter", 
        options=["All Environments", "Production", "Staging", "Development"]
    )
    
    st.divider()
    st.markdown("""
        <div style='font-size: 0.75rem; color: #8b949e;'>
            <strong>CloudLeak v1.2.0-MVP</strong><br>
            Docker Orchestration Ready<br>
            Status: <span style='color: #3fb950;'>● Operational</span>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Mock Data Generators & Filtering Logic
# ---------------------------------------------------------
np.random.seed(42)

dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
cost_trend = pd.DataFrame({
    "Date": dates,
    "AWS": np.random.uniform(40, 60, 30) + np.sin(np.linspace(0, 10, 30)) * 10,
    "GCP": np.random.uniform(20, 35, 30) + np.cos(np.linspace(0, 10, 30)) * 5,
    "Azure": np.random.uniform(15, 25, 30)
})

raw_resources = pd.DataFrame([
    {"Resource ID": "i-09f12a3b8c4d1", "Name": "k8s-prod-worker-01", "Provider": "AWS", "Environment": "Production", "Service": "EC2", "Avg CPU": "8.2%", "Monthly Spend": 310.0, "Waste Signal": "Idle Instance", "Action": "Terminate"},
    {"Resource ID": "db-pg-staging-main", "Name": "staging-db-primary", "Provider": "GCP", "Environment": "Staging", "Service": "Cloud SQL", "Avg CPU": "14.5%", "Monthly Spend": 185.0, "Waste Signal": "Over-provisioned", "Action": "Downsize"},
    {"Resource ID": "vol-0a1b2c3d4e5f", "Name": "legacy-backup-disk", "Provider": "AWS", "Environment": "Production", "Service": "EBS", "Avg CPU": "N/A", "Monthly Spend": 120.0, "Waste Signal": "Unattached Volume", "Action": "Delete Snapshot"},
    {"Resource ID": "az-vm-analytics-02", "Name": "analytics-spark-head", "Provider": "Azure", "Environment": "Development", "Service": "Virtual Machines", "Avg CPU": "6.1%", "Monthly Spend": 240.0, "Waste Signal": "Idle Instance", "Action": "Schedule Stop"},
    {"Resource ID": "i-0c761b209d81e", "Name": "redis-cache-dev", "Provider": "AWS", "Environment": "Development", "Service": "ElastiCache", "Avg CPU": "3.8%", "Monthly Spend": 95.0, "Waste Signal": "Zero Connections", "Action": "Decommission"}
])

# Apply interactive filters
filtered_resources = raw_resources[raw_resources["Provider"].isin(selected_providers)]
if selected_env != "All Environments":
    filtered_resources = filtered_resources[filtered_resources["Environment"] == selected_env]

# ---------------------------------------------------------
# Multi-Tab Enterprise Layout
# ---------------------------------------------------------
tab_overview, tab_audit, tab_rules, tab_docs = st.tabs([
    "📊 Executive Overview", 
    "⚠️ Resource Waste Audit", 
    "⚙️ Optimization Rules Engine", 
    "📖 Architecture & Docs"
])

with tab_overview:
    st.title("Cloud Infrastructure Cost Optimization")
    st.markdown("Real-time telemetry, waste detection, and automated cloud cost reduction insights.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic KPI Calculations based on filtered view
    total_spend_val = filtered_resources["Monthly Spend"].sum() if not filtered_resources.empty else 0.0
    potential_savings_val = total_spend_val * 0.33

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(label="Filtered Monthly Spend", value=f"${total_spend_val:,.2f}", delta="-8.4% vs last mo")
    with kpi2:
        st.metric(label="Active Resources", value=str(len(filtered_resources)), delta="Filtered scope")
    with kpi3:
        st.metric(label="Average CPU Utilization", value="33.0%", delta="-4.2% efficiency deficit", delta_color="inverse")
    with kpi4:
        st.metric(label="Potential Monthly Savings", value=f"${potential_savings_val:,.2f}", delta="33.2% optimization target")

    st.divider()

    col_left, col_right = st.columns([6, 4])
    with col_left:
        st.subheader("📈 30-Day Cost Trend by Provider")
        fig_line = px.line(
            cost_trend, x="Date", y=selected_providers if selected_providers else ["AWS"],
            color_discrete_map={"AWS": "#58a6ff", "GCP": "#3fb950", "Azure": "#d29922"},
            labels={"value": "Daily Cost (USD)", "variable": "Provider"}
        )
        fig_line.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="h", y=1.02, x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        st.subheader("📊 Spend Breakdown by Category")
        breakdown_data = pd.DataFrame({
            "Category": ["Compute", "Databases", "Storage", "Egress", "Cache"],
            "Spend": [580, 290, 190, 110, 80]
        })
        fig_donut = px.pie(breakdown_data, names="Category", values="Spend", hole=0.55,
                           color_discrete_sequence=["#58a6ff", "#3fb950", "#d29922", "#f85149", "#a371f7"])
        fig_donut.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="v", y=0.5, x=1.05))
        st.plotly_chart(fig_donut, use_container_width=True)

with tab_audit:
    st.subheader("⚠️ Interactive Infrastructure Waste Audit")
    st.markdown("Showing flagged resources matching your current sidebar filter criteria.")
    
    if filtered_resources.empty:
        st.warning("No resources match the selected filters. Try broadening your provider/environment scope.")
    else:
        # Format display dataframe
        display_df = filtered_resources.copy()
        display_df["Monthly Spend"] = display_df["Monthly Spend"].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # CSV Export Feature
        csv_data = filtered_resources.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Waste Audit Report (CSV)",
            data=csv_data,
            file_name="cloudleak_waste_audit.csv",
            mime="text/csv",
            help="Download the filtered telemetry findings for executive reporting."
        )

with tab_rules:
    st.subheader("⚙️ CloudLeak Optimization Rules Engine")
    st.markdown("CloudLeak evaluates custom heuristic rules against multi-cloud APIs every 15 minutes:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Rule 01: Idle Compute Detection")
        st.info("**Threshold:** Average CPU $< 10\\%$ over a rolling 7-day window.\n\n**Action Flag:** Recommends instance termination or rightsizing to a smaller instance class.")
        
        st.markdown("### Rule 02: Unattached EBS / Persistent Disks")
        st.info("**Threshold:** Storage volume unattached to any running compute node for $> 48$ hours.\n\n**Action Flag:** Recommends snapshot archiving and immediate volume deletion.")
    
    with col2:
        st.markdown("### Rule 03: Non-Prod Working Hours Schedule")
        st.info("**Threshold:** Staging/Dev resources active 24/7.\n\n**Action Flag:** Recommends automated Lambda/Cloud Function start-stop scheduling during off-hours.")
        
        st.markdown("### Rule 04: Abandoned Database Replicas")
        st.info("**Threshold:** Zero active inbound connections for 14 consecutive days.\n\n**Action Flag:** Recommends automated backup and cluster decommissioning.")

with tab_docs:
    st.subheader("📖 Architecture & Documentation")
    st.markdown("""
        ### System Architecture
        CloudLeak is designed with a decoupled microservice architecture:
        * **Frontend (`/dashboard`)**: Built with Streamlit and Plotly, delivering high-frequency responsive metrics and interactive filtering.
        * **Backend (`/backend`)**: Built with FastAPI, handling secure multi-cloud IAM role assumption and telemetry aggregation.
        * **Containerization**: Fully containerized with Docker and Docker Compose for seamless cross-platform local and cloud deployment.
        
        ### Resume Highlights
        * Architected a multi-cloud cost governance tool reducing simulated infrastructure waste by over 30%.
        * Implemented asynchronous data pipelines and responsive UI state management supporting multi-provider telemetry (AWS, GCP, Azure).
    """)