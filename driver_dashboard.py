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
