import pandas as pd

# Load and prepare data
def load_covid_data():
    df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    df = df[df["continent"].notna()]
    df['date'] = pd.to_datetime(df['date'])
    return df

# Extract unique country names
def get_country_list(df):
    return sorted(df["location"].unique())

# Extract numeric metrics to display
def get_metric_list(df):
    metrics = df.select_dtypes(include='number').columns
    exclude = ["new_tests", "icu_patients", "hosp_patients"]  # noisy/irregular metrics
    return sorted([m for m in metrics if m not in exclude and df[m].nunique() > 50])

# Filter data for selected country and metric
def filter_data(df, country, metric):
    return df[df["location"] == country][["date", metric]].dropna()