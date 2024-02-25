import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
url = 'https://github.com/ddannyyl/Dashboard-Alberta-Grad/raw/main/alberta_post_grad_dataset.csv'
df = pd.read_csv(url)

# Create a Dash web application
app = dash.Dash("Alberta Post-Secondary Graduate Earnings Analysis", external_stylesheets=['assets/style.css'])

# Define layout
app.layout = html.Div([
    html.H1("Alberta Post-Secondary Graduate Earnings Analysis", className='header'),

       # Dropdown for selecting fields of study
    dcc.Dropdown(
        id='field-dropdown',
        options=[{'label': field, 'value': field} for field in df['Field of Study (2-digit CIP code)'].unique()],
        value=df['Field of Study (2-digit CIP code)'].unique()[0],
        multi=False,
        className='dropdown'
    ),


    # Line chart for median earnings over the years
    dcc.Graph(
        id='earnings-line-chart',
        figure=px.line(df, x='Years After Graduation', y='Median Income',
                       title=f'Median Income Over the Years - {df["Field of Study (2-digit CIP code)"].unique()[0]}',
                       labels={'Years After Graduation': 'Years After Graduation', 'Median Income': 'Median Income'}),
        className='graph'
    ),
    # Bar chart for average earnings by degree level
    dcc.Graph(
        id='earnings-bar-chart',
        figure=px.bar(df, x='Credential', y='Median Income',
                      title=f'Average Earnings by Degree Level - {df["Field of Study (2-digit CIP code)"].unique()[0]}',
                      labels={'Credential': 'Degree Level', 'Median Income': 'Average Earnings'}),
        className='graph'
    ),

    # Scatter plot for earnings vs. employment rate
    dcc.Graph(
        id='earnings-scatter-plot',
        figure=px.scatter(df, x='Years After Graduation', y='Median Income',
                          title=f'Earnings vs. Employment Rate - {df["Field of Study (2-digit CIP code)"].unique()[0]}',
                          labels={'Years After Graduation': 'Years After Graduation', 'Median Income': 'Median Income'}),
        className='graph'
    ),

    # Bar chart for cohort size
    dcc.Graph(
        id='cohort-size-bar-chart',
        className='graph'
    )
])

# Callback to update the graphs based on the selected field of study
@app.callback(
    [Output('earnings-line-chart', 'figure'),
     Output('earnings-bar-chart', 'figure'),
     Output('earnings-scatter-plot', 'figure'),
     Output('cohort-size-bar-chart', 'figure')],
    [Input('field-dropdown', 'value')]
)
def update_graphs(selected_field):
    # Filter the DataFrame based on the selected field of study
    filtered_df = df[df['Field of Study (2-digit CIP code)'] == selected_field]

    # Line chart for median earnings over the years
    line_chart = px.line(filtered_df, x='Years After Graduation', y='Median Income',
                         title=f'Median Income Over the Years - {selected_field}',
                         labels={'Years After Graduation': 'Years After Graduation', 'Median Income': 'Median Income'})

    # Bar chart for average earnings by degree level
    bar_chart = px.bar(filtered_df, x='Credential', y='Median Income',
                       title=f'Average Earnings by Degree Level - {selected_field}',
                       labels={'Credential': 'Degree Level', 'Median Income': 'Average Earnings'})

    # Scatter plot for earnings vs. employment rate
    scatter_plot = px.scatter(filtered_df, x='Years After Graduation', y='Median Income',
                              title=f'Earnings vs. Employment Rate - {selected_field}',
                              labels={'Years After Graduation': 'Years After Graduation', 'Median Income': 'Median Income'})

    # Bar chart for cohort size
    cohort_size_chart = px.bar(filtered_df, x='Credential', y='Cohort Size',
                               title=f'Cohort Size - {selected_field}',
                               labels={'Credential': 'Degree Level', 'Cohort Size': 'Cohort Size'})




# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)