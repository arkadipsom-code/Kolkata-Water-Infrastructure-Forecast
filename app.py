import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# PAGE CONFIG
st.set_page_config(
    page_title="Kolkata's Population Forecast",
    layout="wide"
)

# TITLE
st.title("Kolkata's Population Forecasting Dashboard")

st.markdown(
"""
This interactive dashboard predicts **future population of Kolkata**
using both **Civil Engineering forecasting methods** and **Machine Learning models**.
"""
)

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