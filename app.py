import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load data (make sure the file is in the data/ folder)
df = pd.read_csv("data/owid-covid-data.csv")

# Preprocess data: Remove global aggregates and null countries
df = df[df["iso_code"].str.len() == 3]
df = df[df["location"].notna()]
df["date"] = pd.to_datetime(df["date"])

# Extract dropdown options
countries = df["location"].sort_values().unique()
metrics = [
    "total_cases", "new_cases", "total_deaths", "new_deaths",
    "people_vaccinated", "people_fully_vaccinated"
]

# Create app
app = dash.Dash(__name__)
app.title = "COVID-19 Time Series Dashboard"

# Layout
app.layout = html.Div([
    html.H1("COVID-19 Time Series Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Country:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": c, "value": c} for c in countries],
            value="Portugal",
            style={"width": "60%"}
        )
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Select Metric:"),
        dcc.Dropdown(
            id="metric-dropdown",
            options=[{"label": m.replace("_", " ").title(), "value": m} for m in metrics],
            value="new_cases",
            style={"width": "60%"}
        )
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Select Date Range:"),
        dcc.DatePickerRange(
            id="date-range",
            min_date_allowed=df["date"].min(),
            max_date_allowed=df["date"].max(),
            start_date=df["date"].min(),
            end_date=df["date"].max()
        )
    ], style={"padding": "10px"}),

    dcc.Graph(id="timeseries-plot")
])

# Callback
@app.callback(
    Output("timeseries-plot", "figure"),
    [
        Input("country-dropdown", "value"),
        Input("metric-dropdown", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date")
    ]
)
def update_graph(country, metric, start_date, end_date):
    dff = df[(df["location"] == country) & (df["date"] >= start_date) & (df["date"] <= end_date)]
    fig = px.line(
        dff,
        x="date",
        y=metric,
        title=f"{metric.replace('_', ' ').title()} in {country}",
        labels={"date": "Date", metric: metric.replace('_', ' ').title()}
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
