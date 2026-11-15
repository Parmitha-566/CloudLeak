
import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.api_client import load_dashboard_data, APIError


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CloudLeak | FinOps & Waste Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

USD_TO_INR = 94.10


# =========================================================
# 2. SESSION STATE
# =========================================================

if "remediated_ids" not in st.session_state:
    st.session_state.remediated_ids = []


# =========================================================
# 3. DARK THEME CSS
# =========================================================

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

.stApp, [data-testid="stAppViewContainer"] {
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

div[data-testid="stMetric"] {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    padding: 16px 18px !important;
    border-radius: 10px !important;
}

div[data-testid="stMetricLabel"] p {
    color: #8b949e !important;
    font-size: 0.9rem !important;
}

div[data-testid="stMetricValue"] div {
    color: #ffffff !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

div.stButton > button {
    color: #ffffff !important;
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
}

div.stButton > button:hover {
    background-color: #30363d !important;
    border-color: #8b949e !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. LOAD LIVE BACKEND DATA
# =========================================================

@st.cache_data(ttl=30)
def fetch_live_data():
    return load_dashboard_data("api")


try:
    (
        summary,
        resources,
        recommendations,
        anomalies,
        forecast,
        source_label,
    ) = fetch_live_data()

except APIError as exc:
    st.error("Unable to connect to the CLOUDLEAK backend.")
    st.code(str(exc))

    st.info(
        "Check that the backend is running at "
        "http://localhost:8006."
    )

    if st.button("Retry Connection"):
        st.cache_data.clear()
        st.rerun()

    st.stop()


# =========================================================
# 5. PREPARE DATA
# =========================================================

resource_df = pd.DataFrame(resources)
recommendation_df = pd.DataFrame(recommendations)
anomaly_df = pd.DataFrame(anomalies)
forecast_df = pd.DataFrame(forecast)

if resource_df.empty:
    st.error("The backend returned no resource records.")
    st.stop()

required_columns = {
    "resource_id",
    "resource_type",
    "region",
    "usage",
    "cost",
    "utilization",
}

if not required_columns.issubset(resource_df.columns):
    st.error("Unexpected resource API response.")
    st.stop()

resource_df["cost"] = pd.to_numeric(
    resource_df["cost"], errors="coerce"
).fillna(0)

resource_df["utilization"] = pd.to_numeric(
    resource_df["utilization"], errors="coerce"
)


# =========================================================
# 6. HEADER
# =========================================================

st.title("⚡ CloudLeak: Intelligent Cloud Cost Optimization")

st.markdown(
    "Enterprise-style cloud cost monitoring, resource utilization "
    "analysis, anomaly detection, forecasting, and remediation planning."
)

st.caption(
    f"Data Source: {source_label} | Backend: FastAPI"
)


# =========================================================
# 7. SIDEBAR CONTROLS
# =========================================================

st.sidebar.header("🎛️ Dashboard Controls")

currency = st.sidebar.radio(
    "Display Currency",
    ["USD ($)", "INR (₹)"],
    horizontal=True,
)

is_inr = currency == "INR (₹)"
symbol = "₹" if is_inr else "$"
multiplier = USD_TO_INR if is_inr else 1.0

st.sidebar.markdown("---")
st.sidebar.subheader("Resource Filters")

resource_types = sorted(
    resource_df["resource_type"].dropna().unique().tolist()
)

selected_types = st.sidebar.multiselect(
    "Resource Type",
    resource_types,
    default=resource_types,
)

regions = sorted(
    resource_df["region"].dropna().unique().tolist()
)

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions,
)

st.sidebar.markdown("---")
st.sidebar.subheader("What-If Policy Simulator")

cpu_threshold = st.sidebar.slider(
    "Idle Utilization Threshold (%)",
    min_value=2,
    max_value=20,
    value=10,
    step=1,
)

st.sidebar.caption(
    "This threshold changes dashboard classifications and "
    "estimated waste. It does not modify cloud infrastructure."
)


# =========================================================
# 8. FILTER AND TRANSFORM DATA
# =========================================================

df = resource_df[
    resource_df["resource_type"].isin(selected_types)
    & resource_df["region"].isin(selected_regions)
].copy()

df["display_cost"] = df["cost"] * multiplier

df["status"] = df["utilization"].apply(
    lambda value:
        "Critical" if pd.notna(value) and value < 5
        else "Moderate" if pd.notna(value) and value <= cpu_threshold
        else "Healthy" if pd.notna(value)
        else "Unknown"
)

# Dashboard-only estimated waste simulation.
df["estimated_waste"] = df.apply(
    lambda row:
        row["display_cost"] * 0.90
        if pd.notna(row["utilization"]) and row["utilization"] < 5
        else row["display_cost"] * 0.50
        if pd.notna(row["utilization"])
        and row["utilization"] <= cpu_threshold
        else 0.0,
    axis=1,
)

df["remediated"] = df["resource_id"].isin(
    st.session_state.remediated_ids
)


# =========================================================
# 9. CALCULATE METRICS
# =========================================================

total_spend = df["display_cost"].sum()

active_waste = df.loc[
    ~df["remediated"], "estimated_waste"
].sum()

session_savings = df.loc[
    df["remediated"], "estimated_waste"
].sum()

avg_utilization = (
    df["utilization"].mean()
    if not df.empty and df["utilization"].notna().any()
    else 0.0
)

flagged_count = df["status"].isin(
    ["Critical", "Moderate"]
).sum()

total_resources = len(df)

total_recommendation_savings = sum(
    float(item.get("estimated_monthly_savings", 0) or 0)
    for item in recommendations
) * multiplier


# =========================================================
# 10. DASHBOARD TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Overview",
    "🗑️ Waste Audit & Remediation",
    "⚙️ Rules & Policy Engine",
    "📚 Architecture & Documentation",
])


# =========================================================
# TAB 1: EXECUTIVE OVERVIEW
# =========================================================

with tab1:

    st.subheader(f"Cloud Cost & Utilization Overview ({currency})")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Monthly Spend",
        f"{symbol}{total_spend:,.2f}",
    )

    col2.metric(
        "Total Resources",
        f"{total_resources}",
    )

    col3.metric(
        "Average Utilization",
        f"{avg_utilization:.2f}%",
    )

    col4.metric(
        "Flagged Resources",
        f"{flagged_count}/{total_resources}",
    )

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:

        st.markdown("### Spend by Resource Type")

        if not df.empty:

            service_data = (
                df.groupby("resource_type", as_index=False)["display_cost"]
                .sum()
            )

            fig = px.pie(
                service_data,
                names="resource_type",
                values="display_cost",
                hole=0.45,
                title="Monthly Cost Distribution",
            )

            fig.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="#f0f6fc",
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No resources match the selected filters.")

    with col_b:

        st.markdown("### Utilization by Resource")

        if not df.empty:

            fig = px.bar(
                df,
                x="resource_id",
                y="utilization",
                color="status",
                title="Resource Utilization",
                hover_data=["resource_type", "region"],
            )

            fig.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="#f0f6fc",
                xaxis_title="Resource",
                yaxis_title="Utilization (%)",
                xaxis_tickangle=-45,
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No resources match the selected filters.")

    st.markdown("---")

    col_c, col_d = st.columns(2)

    with col_c:

        st.markdown("### Regional Expenditure")

        if not df.empty:

            region_data = (
                df.groupby("region", as_index=False)["display_cost"]
                .sum()
            )

            fig = px.bar(
                region_data,
                x="region",
                y="display_cost",
                title="Cost by Region",
            )

            fig.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="#f0f6fc",
                xaxis_title="Region",
                yaxis_title=f"Cost ({symbol})",
            )

            st.plotly_chart(fig, use_container_width=True)

    with col_d:

        st.markdown("### Seven-Day Cost Forecast")

        if not forecast_df.empty:

            forecast_df["display_prediction"] = (
                pd.to_numeric(
                    forecast_df["predicted_cost"],
                    errors="coerce",
                ) * multiplier
            )

            fig = px.line(
                forecast_df,
                x="date",
                y="display_prediction",
                markers=True,
                title="Predicted Daily Expenditure",
            )

            fig.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="#f0f6fc",
                xaxis_title="Date",
                yaxis_title=f"Predicted Cost ({symbol})",
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No forecast records are available.")


# =========================================================
# TAB 2: WASTE AUDIT AND REMEDIATION
# =========================================================

with tab2:

    st.subheader("Interactive Resource Audit")

    st.markdown(
        "Review actual resource records and simulate remediation "
        "for underutilized resources."
    )

    st.caption(
        "Estimated waste is a what-if estimate, not an actual "
        "measured cloud saving."
    )

    if not df.empty:

        audit_df = df[
            [
                "remediated",
                "resource_id",
                "resource_type",
                "region",
                "display_cost",
                "estimated_waste",
                "utilization",
                "status",
            ]
        ].copy()

        audit_df = audit_df.rename(
            columns={
                "remediated": "Apply Fix",
                "resource_id": "Resource ID",
                "resource_type": "Resource Type",
                "region": "Region",
                "display_cost": f"Monthly Cost ({symbol})",
                "estimated_waste": f"Estimated Waste ({symbol})",
                "utilization": "Utilization (%)",
                "status": "Status",
            }
        )

        edited_df = st.data_editor(
            audit_df,
            use_container_width=True,
            hide_index=True,
            disabled=[
                "Resource ID",
                "Resource Type",
                "Region",
                f"Monthly Cost ({symbol})",
                f"Estimated Waste ({symbol})",
                "Utilization (%)",
                "Status",
            ],
            column_config={
                "Apply Fix": st.column_config.CheckboxColumn(
                    "Apply Fix",
                    help="Select resources for simulated remediation.",
                ),
                "Utilization (%)": st.column_config.ProgressColumn(
                    "Utilization",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%",
                ),
            },
            key="resource_editor",
        )

        btn_col1, btn_col2, _ = st.columns([2, 2, 4])

        with btn_col1:

            if st.button(
                "🚀 Apply Selected Remediation",
                type="primary",
            ):

                newly_fixed = edited_df.loc[
                    edited_df["Apply Fix"], "Resource ID"
                ].tolist()

                visible_ids = edited_df["Resource ID"].tolist()

                existing = set(st.session_state.remediated_ids)
                existing.difference_update(visible_ids)
                existing.update(newly_fixed)

                st.session_state.remediated_ids = list(existing)

                st.toast(
                    "Simulation updated successfully.",
                    icon="✅",
                )

                st.rerun()

        with btn_col2:

            if st.button("🔄 Reset Simulation"):

                st.session_state.remediated_ids = []

                st.toast("Simulation reset.", icon="🔄")
                st.rerun()

        st.markdown("---")

        st.markdown("### Backend Recommendations")

        if recommendation_df.empty:

            st.info("The backend returned no recommendations.")

        else:

            display_recommendations = recommendation_df.copy()

            if "estimated_monthly_savings" in display_recommendations:

                display_recommendations[
                    "estimated_monthly_savings"
                ] = (
                    pd.to_numeric(
                        display_recommendations[
                            "estimated_monthly_savings"
                        ],
                        errors="coerce",
                    ).fillna(0) * multiplier
                )

                display_recommendations = display_recommendations.rename(
                    columns={
                        "estimated_monthly_savings":
                            f"Estimated Monthly Savings ({symbol})"
                    }
                )

            st.dataframe(
                display_recommendations,
                use_container_width=True,
                hide_index=True,
            )

        st.markdown("---")

        export_df = df[
            [
                "resource_id",
                "resource_type",
                "region",
                "cost",
                "utilization",
                "status",
                "estimated_waste",
            ]
        ].copy()

        export_df = export_df.rename(
            columns={
                "resource_id": "Resource ID",
                "resource_type": "Resource Type",
                "region": "Region",
                "cost": "Monthly Cost (USD)",
                "utilization": "Utilization (%)",
                "status": "Status",
                "estimated_waste": f"Estimated Waste ({symbol})",
            }
        )

        st.download_button(
            label="📥 Export Resource Audit CSV",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="cloudleak_resource_audit.csv",
            mime="text/csv",
        )

    else:

        st.info("No resources match the active filters.")


# =========================================================
# TAB 3: RULES AND POLICY ENGINE
# =========================================================

with tab3:

    st.subheader("CloudLeak Rules & Threshold Engine")

    st.info(
        f"Current dashboard classification threshold: "
        f"{cpu_threshold}% utilization."
    )

    st.markdown("""
    **Resource Classification Rules**

    - **Critical:** Utilization below 5%.
    - **Moderate:** Utilization from 5% up to the selected threshold.
    - **Healthy:** Utilization above the selected threshold.
    - **Unknown:** Utilization was not supplied by the API.

    **Estimated Waste Simulation**

    - Critical resources: 90% of cost is treated as potentially wasteful.
    - Moderate resources: 50% of cost is treated as potentially wasteful.
    - Healthy resources: No estimated waste is assigned.

    These percentages are dashboard assumptions, not verified savings.
    """)

    st.markdown("---")

    st.markdown("### Actual Backend Recommendation Savings")

    st.metric(
        "Estimated Monthly Savings",
        f"{symbol}{total_recommendation_savings:,.2f}",
    )

    st.caption(
        "Calculated from the backend's estimated_monthly_savings fields."
    )

    st.markdown("---")

    st.markdown("### Anomaly Detection")

    if anomaly_df.empty:

        st.success(
            "The backend currently reports zero detected cost anomalies."
        )

    else:

        st.dataframe(
            anomaly_df,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# TAB 4: ARCHITECTURE AND DOCUMENTATION
# =========================================================

with tab4:

    st.subheader("System Architecture & Documentation")

    st.markdown("""
    ### Architecture Overview

    **Frontend**
    - Streamlit dashboard.
    - Plotly charts and visualizations.
    - Interactive resource audit.
    - Currency conversion and what-if simulation.

    **Backend**
    - FastAPI REST API.
    - Resource summary and utilization information.
    - Cost optimization recommendations.
    - Anomaly detection.
    - Seven-day expenditure forecasting.

    **Data and Analytics**
    - Member 1: Cloud resource and billing data.
    - Member 2: Cost analysis, recommendations,
      anomaly detection, and forecasting.
    - Member 3: Backend APIs and integration.
    - Member 4: Dashboard and visualization.

    **Deployment**
    - Docker containerization.
    - Docker Compose for local services.
    - Kubernetes deployment for the backend.
    """)

    st.markdown("---")

    st.markdown("### Live Backend Summary")

    summary_display = {
        "Total Cost (USD)": summary.get("total_cost"),
        "Resource Count": summary.get("resource_count"),
        "Average Cost (USD)": summary.get("average_cost"),
        "Average Utilization (%)": summary.get("average_utilization"),
        "High Utilization Resources": summary.get(
            "high_utilization_resources"
        ),
    }

    st.json(summary_display)

    st.markdown("---")

    st.markdown("### Data Integrity Notes")

    st.write(
        "The dashboard displays resource, recommendation, anomaly, "
        "and forecast information retrieved from the connected API. "
        "The remediation feature is a local simulation and does not "
        "execute changes in AWS, Azure, or Google Cloud."
    )


# =========================================================
# 11. FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "CLOUDLEAK | Intelligent Cloud Cost Optimization Platform "
    "| Live API Integration"
)
