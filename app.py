import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# PAGE CONFIG
st.set_page_config(
    page_title="Kolkata's Water Infrastructure",
    layout="wide"
)

# TITLE
st.title("Kolkata's Decadal Population and Water Demand Forecast Dashboard")

st.info(
"This dashboard estimates future water demand and sewer infrastructure load for Kolkata using population forecasting and standard engineering design assumptions."
)

st.divider()

# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_csv("kolkata_population.csv")

data = load_data()

data.columns = data.columns.str.strip()

years = data["Year"].values
population = data["Population"].values

last_year = years[-1]
base_population = population[-1]

# CIVIL ENGINEERING METHODS

avg_increase = np.mean(np.diff(population))

percent_growth = np.diff(population) / population[:-1]
avg_percent = np.mean(percent_growth)

# MACHINE LEARNING MODELS

X = years.reshape(-1,1)
y = population

@st.cache_resource
def train_models(X, y):

    linear_model = LinearRegression()
    linear_model.fit(X,y)

    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    poly_model = LinearRegression()
    poly_model.fit(X_poly,y)

    return linear_model, poly_model, poly

linear_model, poly_model, poly = train_models(X,y)

# SIDEBAR

st.sidebar.header("Prediction Controls")

target_year = st.sidebar.number_input(
    "Enter Future Year",
    min_value=2021,
    max_value=10000,
    value=2031,
    step=10
)

# FORECAST

n = (target_year - last_year)/10

arith_pred = base_population + n*avg_increase
geo_pred = base_population*(1+avg_percent)**n

linear_pred = linear_model.predict([[target_year]])[0]

poly_pred = poly_model.predict(
    poly.transform([[target_year]])
)[0]

st.header("Population Forecast Models")
# TABS
tab1, tab2, tab3 = st.tabs(["Forecast", "Visualization", "Dataset"])

# FORECAST TAB

with tab1:
    st.subheader("Population Prediction")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Arithmetic Method", f"{round(arith_pred):,}")
    col2.metric("Geometric Method", f"{round(geo_pred):,}")
    col3.metric("Linear Regression", f"{round(linear_pred):,}")
    col4.metric("Polynomial Regression", f"{round(poly_pred):,}")

    st.write(f"Forecast Year: **{target_year}**")

# VISUALIZATION TAB

with tab2:

    st.subheader("Population Trend Analysis")

    future_years = list(range(2021, target_year+1, 10))

    arith_values = [
        base_population + ((y-last_year)/10)*avg_increase
        for y in future_years
    ]

    geo_values = [
        base_population*(1+avg_percent)**((y-last_year)/10)
        for y in future_years
    ]

    linear_values = linear_model.predict(
        np.array(future_years).reshape(-1,1)
    )

    poly_values = poly_model.predict(
        poly.transform(np.array(future_years).reshape(-1,1))
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years,
        y=population,
        mode="lines+markers",
        name="Historical Population"
    ))

    fig.add_trace(go.Scatter(
        x=future_years,
        y=arith_values,
        mode="lines+markers",
        name="Arithmetic Method"
    ))

    fig.add_trace(go.Scatter(
        x=future_years,
        y=geo_values,
        mode="lines+markers",
        name="Geometric Method"
    ))

    fig.add_trace(go.Scatter(
        x=future_years,
        y=linear_values,
        mode="lines+markers",
        name="Linear Regression"
    ))

    fig.add_trace(go.Scatter(
        x=future_years,
        y=poly_values,
        mode="lines+markers",
        name="Polynomial Regression"
    ))

    fig.update_layout(
        title="Population Forecast Comparison",
        xaxis_title="Year",
        yaxis_title="Population",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# DATASET TAB

with tab3:

    st.subheader("Historical Census Data")

    st.dataframe(data)

    st.markdown(
    """
    Dataset Source: Indian Census Data.
    Used for forecasting future population trends.
    """
    )

st.divider()

st.header("Kolkata's Water Infrastructure Analysis")

st.divider()

# Water Demand Model


st.subheader("Water Demand and Wastewater Generation Estiamation")

st.caption("***Note: Population estimated by LinearRegression ML model is considered in the calculations of Water Demand & Wastewater Generation!***")

population_wd = linear_pred

# st.subheader("Water Demand Estimation for Kolkata")
per_capita = 135 # litres per person per day (lpcd)

water_demand = population_wd * per_capita


# Wastewater Generation

# st.subheader("Estimated Wastewater Generation")

ww = water_demand * 0.8

col1, col2 = st.columns(2)

with col1:
    st.metric(
    "Estimated Water Demand (MLD)",
    round(water_demand / 1e6, 2)
)
with col2:
    st.metric(
    "Estimated Wastewater Generation (MLD)",
    round(ww / 1e6, 2)
)
    
st.divider()

st.subheader("Wastewater Quality Analysis")

bod_concentration = 250  # mg/L
cod_concentration = 500  # mg/L


wastewater_L_day = ww 

bod_load = wastewater_L_day * bod_concentration / 1e6
cod_load = wastewater_L_day * cod_concentration / 1e6

col1, col2 = st.columns(2)

with col1:
    st.metric("BOD Load (kg/day)", round(bod_load,2))

with col2:
    st.metric("COD Load (kg/day)", round(cod_load,2))

# Pollution Chart

import plotly.express as px

pollution_data = {
    "Parameter": ["BOD Load", "COD Load"],
    "Load (kg/day)": [bod_load, cod_load]
}

df_pollution = pd.DataFrame(pollution_data)
fig = px.bar(
    df_pollution,
    x="Parameter",
    y="Load (kg/day)",
    color="Parameter",
    text_auto=True,
    title="Wastewater Pollution Load"
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Sewer Flow Model

st.subheader("Sewer Flow Model")

avg_flow = ww
min_flow = ww * 0.5
peak_flow = ww * 2.5


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Flow (MLD)", round(avg_flow,2))

with col2:
    st.metric("Minimum Flow (MLD)", round(min_flow,2))

with col3:
    st.metric("Peak Flow (MLD)", round(peak_flow,2))

# water flow chart

flow_data = {
    "Stage": [
        "Water Demand",
        "Wastewater Generated",
        "Average Sewer Flow",
        "Peak Sewer Flow"
    ],
    "Flow (MLD)": [
        water_demand,
        ww,
        avg_flow,
        peak_flow
    ]
}

flow_df = pd.DataFrame(flow_data)

fig = px.bar(
    flow_df,
    x="Stage",
    y="Flow (MLD)",
    title="Urban Water Flow Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Treatment Plant Load

st.subheader("Treatment Plant Network Load")

st.write("""**Important Note:** \nKolkata’s wastewater management is a combination of natural treatment via the East Kolkata Wetlands (EKW) and a growing network of mechanized Sewage Treatment Plants (STPs). 
         \n***Here all the load calculations are done by considering STPs only!***""")

plants_existing = {
    "Garden Reach": 57,
    "Keorapukur": 45,
    "Bangur": 45,
    "Dhapa": 80,
    "Jorabagan": 45,
    "Watgunge": 35,
    "New Town (AA-IIC)": 31,
    "New Town (AA-IIB)": 14,
    "South Suburban East": 30,
    "Bagjola": 18
}

plants_future = {
    "Garden Reach Extension": 113.6,
    "Palta Extension": 90.9,
    "Hossainpur STP": 41.0,
    "Joka (Bank Plot)": 40.0,
    "Joka (WBSETCL Campus)": 45.0,
    "Rania STP": 23.0
}

existing_capacity = sum(plants_existing.values())

all_plants = {**plants_existing, **plants_future}
future_capacity = sum(all_plants.values())

# Load distribution (existing plants)

ww_mld = ww / 1e6
plant_load_existing = {
    plant: ww_mld * (capacity / existing_capacity)
    for plant, capacity in plants_existing.items()
}

# Load distribution (future plants added)
plant_load_future = {
    plant: ww_mld * (capacity / future_capacity)
    for plant, capacity in all_plants.items()
}

st.caption("Wastewater Distribution (Existing Plants)")

df_existing = pd.DataFrame(
    plant_load_existing.items(),
    columns=["Plant", "Load (MLD)"]
)

st.dataframe(df_existing)

fig = px.bar(
    df_existing,
    x="Plant",
    y="Load (MLD)",
    title="Wastewater Load Distribution - Current Infrastructure"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("Wastewater Distribution (After New Plants)")

df_future = pd.DataFrame(
    plant_load_future.items(),
    columns=["Plant", "Load (MLD)"]
)

st.dataframe(df_future)

fig = px.bar(
    df_future,
    x="Plant",
    y="Load (MLD)",
    title="Wastewater Load Distribution - Future Infrastructure"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()


# Infra capacity comparison
st.subheader(f"Infrastructure Capacity Comparison — Forecast Year: {target_year}")

load_existing = (ww_mld / existing_capacity) * 100
load_future = (ww_mld / future_capacity) * 100

gap_existing = ww_mld - existing_capacity   # MLD over/under
gap_future = ww_mld - future_capacity       # MLD over/under

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Forecast Year", target_year)

with col2:
    st.metric(
        "Current System Load (%)",
        round(load_existing, 2),
        delta=f"{round(gap_existing, 2)} MLD {'surplus' if gap_existing < 0 else 'deficit'}",
        delta_color="inverse"
    )

with col3:
    st.metric(
        "Future System Load (%)",
        round(load_future, 2),
        delta=f"{round(gap_future, 2)} MLD {'surplus' if gap_future < 0 else 'deficit'}",
        delta_color="inverse"
    )

# Extra capacity gap row
col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Current Capacity Gap (MLD)",
        round(gap_existing, 2),
        help="Positive = deficit (overloaded). Negative = surplus."
    )

with col5:
    st.metric(
        "Future Capacity Gap (MLD)",
        round(gap_future, 2),
        help="Positive = deficit (overloaded). Negative = surplus."
    )

# Infrastructure status
st.subheader(f"Wastewater Infrastructure Status in {target_year}")

if load_existing > 100:
    st.error(f"⚠ Current infrastructure overloaded — {round(gap_existing, 2)} MLD deficit")
elif load_existing > 80:
    st.warning(f"⚠ Current infrastructure nearing capacity — {round(gap_existing, 2)} MLD headroom remaining")
else:
    st.success(f"✓ Current infrastructure sufficient — {round(abs(gap_existing), 2)} MLD surplus")

if load_future > 100:
    st.error(f"⚠ Even with new plants, capacity will be insufficient — {round(gap_future, 2)} MLD deficit")
elif load_future > 80:
    st.warning(f"⚠ Future infrastructure may face pressure — {round(gap_future, 2)} MLD headroom remaining")
else:
    st.success(f"✓ New treatment plants will reduce system load — {round(abs(gap_future), 2)} MLD surplus")

st.divider()

with st.expander("Engineering Assumptions"):
    st.write("Per capita rate of sewage contributed per day = 135 L per capita per day")
    st.write("Wastewater generation = 80% of water demand")
    st.write("BOD concentration = 250 mg/L")
    st.write("COD concentration = 500 mg/L")

with st.expander("List of Capacity of the Plants (in MLD)"):
    st.caption("Existing Plants:")
    st.write("Garden Reach: 57")
    st.write("Keorapukur: 45")
    st.write("Bangur: 45")
    st.write("Dhapa: 80")
    st.write("Jorabagan: 45")
    st.write("Watgunge: 35")
    st.write("New Town (AA-IIC): 31")
    st.write("New Town (AA-IIB): 14")
    st.write("South Suburban East: 30")
    st.write("Bagjola: 18")

    st.caption("Future Plants:")
    st.write("Garden Reach Extension: 113.6")
    st.write("Palta Extension: 90.9")
    st.write("Hossainpur STP: 41.0")
    st.write("Joka (Bank Plot): 40.0")
    st.write("Joka (WBSETCL Campus): 45.0")
    st.write("Rania STP: 23.0")


st.divider()

st.subheader("Urban Water System Model")

st.info(
"""
Population Forecast → Water Demand → Wastewater Generation → 
Sewer Flow → Treatment Plant Load → Infrastructure Capacity
"""
)

st.divider()

st.markdown(
"""
<div style='text-align: center; font-size: 14px;'>

© 2026 All Rights Reserved  

Developed with ❤️ by **Arkadip Som**

</div>
""",
unsafe_allow_html=True
)