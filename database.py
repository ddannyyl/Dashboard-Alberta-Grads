import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
url = 'https://github.com/ddannyyl/Dashboard-Alberta-Grads/raw/main/alberta_post_grad_dataset.csv'
df = pd.read_csv(url)

# Create a Dash web application
app = dash.Dash("Alberta Post-Secondary Graduate Earnings Analysis", external_stylesheets=['assets/style.css'])