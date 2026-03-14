# Kolkata Water Infrastructure Forecast Dashboard

An interactive **urban water infrastructure forecasting dashboard** built using **Streamlit, Machine Learning, and Civil Engineering design methods**.

The application forecasts **future population growth in Kolkata** and evaluates its impact on **water demand, wastewater generation, sewer flow, and treatment plant capacity**.

🌐 **Live App:**  
https://kolkata-water-infrastructure-forecast-dashboard.streamlit.app/

---

## Project Overview

Urban infrastructure planning requires accurate **population forecasting** to estimate future water demand and wastewater loads.

This dashboard integrates:

- Traditional **civil engineering population forecasting methods**
- **Machine learning regression models**
- **urban water demand modelling**
- **sewage generation estimation**
- **treatment plant capacity analysis**

The tool helps visualize how **future population growth will impact Kolkata's wastewater infrastructure**.

---

## Features

### Population Forecasting

Population is predicted using four methods:

- Arithmetic Increase Method
- Geometric Increase Method
- Linear Regression (Machine Learning)
- Polynomial Regression (Machine Learning)

Interactive visualizations compare predictions across decades.

---

### Water Demand Estimation

Water demand is calculated using standard engineering assumptions:

```
Water Demand = Population × Per Capita Demand
```

Where:

```
Per Capita Demand = 135 litres/person/day
```

The results are displayed in **Million Litres per Day (MLD)**.

---

### Wastewater Generation

Approximately **80% of supplied water becomes wastewater**.

```
Wastewater = Water Demand × 0.8
```

---

### Wastewater Quality Analysis

Typical domestic wastewater parameters used:

```
BOD = 250 mg/L
COD = 500 mg/L
```

The dashboard calculates:

- **BOD Load (kg/day)**
- **COD Load (kg/day)**

---

### Sewer Flow Analysis

Sewer design considers multiple flow conditions:

| Flow Type    | Description                 |
| ------------ | --------------------------- |
| Minimum Flow | Low usage conditions        |
| Average Flow | Normal wastewater discharge |
| Peak Flow    | Maximum expected sewer load |

Peak flow is estimated using a **peaking factor**.

---

### Treatment Plant Network Load

The dashboard evaluates the load on **Kolkata's sewage treatment plants (STPs)**.

Existing infrastructure includes plants such as:

- Garden Reach
- Keorapukur
- Bangur
- Dhapa
- Jorabagan
- Watgunge
- New Town STPs
- South Suburban East
- Bagjola

Future infrastructure additions include:

- Garden Reach Extension
- Palta Extension
- Hossainpur STP
- Joka STP
- Rania STP

The system compares **current capacity vs future expanded capacity**.

---

### Infrastructure Capacity Assessment

Infrastructure stress is evaluated using:

```
Load (%) = Wastewater / Treatment Capacity × 100
```

Results are categorized as:

- Safe capacity
- Near capacity
- Overloaded infrastructure

---

## Technology Stack

This project combines **data science and civil engineering modelling**.

Libraries used:

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-Learn

Machine Learning models:

- Linear Regression
- Polynomial Regression

---

## Project Structure

```
project-folder
│
├── app.py
├── kolkata_population.csv
├── requirements.txt
└── README.md
```

---

## Engineering Assumptions

The model uses common urban planning assumptions:

```
Per Capita Water Demand = 135 L/person/day
Wastewater Generation = 80% of water demand
BOD concentration = 250 mg/L
COD concentration = 500 mg/L
```

These values are used for **demonstration and planning analysis**.

---

## Urban Water System Model

The dashboard simulates the following infrastructure pipeline:

```
Population Forecast
        ↓
Water Demand Estimation
        ↓
Wastewater Generation
        ↓
Sewer Flow Analysis
        ↓
Treatment Plant Load Distribution
        ↓
Infrastructure Capacity Assessment
```

---

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/arkadipsom-code/Kolkata-Water-Infrastructure-Forecast.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

---

## Author

**Arkadip Som**  
Civil Engineering Undergrad at Indian Institute of Engineering Science and Technology (IIEST), Shibpur

---

## License

© 2026 All Rights Reserved
