import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Driver Behaviour Dashboard", page_icon="🚛", layout="wide")

st.title("🚛 Driver Behaviour & Maintenance Analytics Dashboard")
st.markdown("Analyze ECU data to understand driver performance and maintenance cost patterns.")

# --- Load Data ---
df = pd.read_csv("driver_data.csv")

st.subheader("🔍 Trip Data Preview")
st.dataframe(df.head())

# --- KPIs ---
avg_score = round(df["driver_score"].mean(), 2)
total_cost = df["maintenance_cost_inr"].sum()
high_risk_pct = round((df["high_risk"].mean()) * 100, 2)

col1, col2, col3 = st.columns(3)
col1.metric("📊 Average Driver Score", avg_score)
col2.metric("💰 Total Maintenance Cost", f"₹{total_cost:,}")
col3.metric("⚠️ High-Risk Trips (%)", f"{high_risk_pct}%")

# --- Visuals ---
st.subheader("📈 Analytics Visuals")

tab1, tab2, tab3 = st.tabs(["Driver Scores", "Maintenance Cost", "Score Distribution"])

with tab1:
    fig = px.bar(df, x="driver_id", y="driver_score", color="driver_id", title="Average Driver Scores")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.bar(df, x="driver_id", y="maintenance_cost_inr", color="driver_id", title="Maintenance Cost per Driver")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.histogram(df, x="driver_score", nbins=15, title="Distribution of Driver Behaviour Scores")
    st.plotly_chart(fig3, use_container_width=True)

st.success("✅ Dashboard Loaded Successfully!")

# --- SMART INSIGHTS SECTION ---
st.subheader("🧠 Smart Insights & Recommendations")

# Aggregate by driver to get summary
summary = df.groupby("driver_id").agg(
    avg_score=("driver_score", "mean"),
    avg_temp=("engine_temp_peak", "mean"),
    avg_tyre_wear=("tyre_wear_mm", "mean"),
    trips=("trip_id", "count"),
    total_cost=("maintenance_cost_inr", "sum")
).reset_index()

insights = []
for _, row in summary.iterrows():
    if row.avg_score < 60:
        msg = f"⚠️ Driver {row.driver_id} shows risky driving patterns — frequent harsh braking and high engine temperature. Estimated maintenance ₹{row.total_cost:,}."
    elif row.avg_score < 80:
        msg = f"🔸 Driver {row.driver_id} has moderate driving quality. Monitoring required to reduce maintenance cost ₹{row.total_cost:,}."
    else:
        msg = f"✅ Driver {row.driver_id} maintains excellent driving habits — efficient fuel use and low wear. Keep it up!"
    insights.append(msg)

for i in insights:
    st.markdown(i)

# --- DATA VIEW TOGGLE ---
st.subheader("📋 Detailed Data View")
view_option = st.radio("Choose View:", ["Trip View", "Driver Summary"])

if view_option == "Trip View":
    st.dataframe(df)
else:
    st.dataframe(summary)

# --- EXPORT SECTION ---
st.subheader("📤 Export Analysis Results")

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Trip Data (CSV)",
    data=csv,
    file_name="driver_analysis.csv",
    mime="text/csv",
)

csv_summary = summary.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Driver Summary (CSV)",
    data=csv_summary,
    file_name="driver_summary.csv",
    mime="text/csv",
)

