import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Food Waste Management Dashboard",
    page_icon="🍲",
    layout="wide"
)

st.title("🍲 Food Waste Management Dashboard")

st.markdown("---")

st.markdown(
    "### Real-Time Food Waste Management Analytics Dashboard"
)


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rohit123",
    database="food_waste_management"
)

providers = pd.read_sql(
    "SELECT * FROM providers_data",
    conn
)

receivers = pd.read_sql(
    "SELECT * FROM receivers_data",
    conn
)

food = pd.read_sql(
    "SELECT * FROM food_listings_data",
    conn
)

claims = pd.read_sql(
    "SELECT * FROM claims_data_cleaned",
    conn
)

st.sidebar.header("Filters")

food_type_filter = st.sidebar.selectbox(
    "Select Food Type",
    ["All"] + sorted(food["Food_Type"].unique().tolist())
)

if food_type_filter != "All":
    food = food[food["Food_Type"] == food_type_filter]

total_providers = len(providers)
total_receivers = len(receivers)
total_food = len(food)
total_claims = len(claims)
total_quantity = food["Quantity"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Providers", total_providers)
col2.metric("Receivers", total_receivers)
col3.metric("Food Listings", total_food)
col4.metric("Claims", total_claims)
col5.metric("Quantity", total_quantity)


provider_chart = providers["Type"].value_counts().reset_index()

provider_chart.columns = [
    "Provider Type",
    "Count"
]

fig = px.bar(
    provider_chart,
    x="Provider Type",
    y="Count",
    title="Provider Type Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

col1, col2 = st.columns(2)

# Food Type Distribution
food_chart = food["Food_Type"].value_counts().reset_index()
food_chart.columns = ["Food Type", "Count"]

fig2 = px.pie(
    food_chart,
    names="Food Type",
    values="Count",
    title="Food Type Distribution"
)

with col1:
    st.plotly_chart(fig2, use_container_width=True)


# Receiver Type Distribution
receiver_chart = receivers["Type"].value_counts().reset_index()
receiver_chart.columns = ["Receiver Type", "Count"]

fig3 = px.bar(
    receiver_chart,
    x="Receiver Type",
    y="Count",
    title="Receiver Type Distribution"
)

with col2:
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

# Quantity by Food Type
qty_chart = food.groupby("Food_Type")["Quantity"].sum().reset_index()

fig4 = px.bar(
    qty_chart,
    x="Food_Type",
    y="Quantity",
    title="Quantity by Food Type"
)

with col3:
    st.plotly_chart(fig4, use_container_width=True)


# Top 10 Cities
city_chart = providers["City"].value_counts().head(10).reset_index()
city_chart.columns = ["City", "Count"]

fig5 = px.bar(
    city_chart,
    x="City",
    y="Count",
    title="Top 10 Provider Cities"
)

with col4:
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

st.subheader("📊 Claims Overview")

claim_chart = claims["Status"].value_counts().reset_index()
claim_chart.columns = ["Status", "Count"]

fig6 = px.pie(
    claim_chart,
    names="Status",
    values="Count",
    title="Claims Status Distribution"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

st.subheader("🏆 Top 10 Foods by Quantity")

top_foods = food.groupby("Food_Name")["Quantity"].sum().reset_index()

top_foods = top_foods.sort_values(
    by="Quantity",
    ascending=False
).head(10)

fig7 = px.bar(
    top_foods,
    x="Food_Name",
    y="Quantity",
    title="Top 10 Foods by Quantity"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.markdown("---")

st.subheader("📋 Food Listings Preview")

st.dataframe(
    food.head(20),
    use_container_width=True
)
