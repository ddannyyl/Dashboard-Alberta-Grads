import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Set default plotly template
px.defaults.template = "ggplot2"

# Load the dataset
url = 'https://raw.githubusercontent.com/ddannyyl/Dashboard-Alberta-Grads/master/alberta_post_grad_dataset.csv'
df = pd.read_csv(url)

app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])

app.layout = html.Div([
    html.H1("Alberta Post-Secondary Graduate Earnings Analysis",
            className='header'),

    # Dropdown for selecting fields of study
    dcc.Dropdown(
        id='field-dropdown',
        options=[{'label': field, 'value': field}
                 for field in df['Field of Study (2-digit CIP code)'].unique()],
        value=df['Field of Study (2-digit CIP code)'].unique()[0],
        multi=False,
        className='dropdown'
    ),
    # Container for displaying graphs
    html.Div([
        dcc.Loading(
            id='loading-indicator',
            type='circle',
            children=[
                dcc.Graph(
                    id=f'earnings-{graph_type.lower()}-chart', className='graph')
                for graph_type in ['Line', 'Bar', 'Scatter', 'CohortSize']
            ]
        )
    ], className='graph-container'),
    # Footer
    html.Footer([
        html.P('© 2024 Alberta Grads Dashboard. All rights reserved.'),
        html.A('Terms of Service', href='#'),
    ], className='footer')
])

# Update graph when the user changes the program


@app.callback(
    [Output(f'earnings-{graph_type.lower()}-chart', 'figure')
     for graph_type in ['Line', 'Bar', 'Scatter', 'CohortSize']],
    [Input('field-dropdown', 'value')]
)
# Graph made for each statistic
def update_graphs(selected_field):
    # Filter dataset based on selected field of study
    filtered_df = df[df['Field of Study (2-digit CIP code)'] == selected_field]

    # Create line chart for median income over years
    line_chart = px.line(filtered_df, x='Years After Graduation', y='Median Income',
                         title=f'Median Income Over the Years - {
                             selected_field}',
                         labels={'Years After Graduation': 'Years After Graduation', 'Median Income': 'Median Income'})

    # Create bar chart for average earnings by degree level
    bar_chart = px.bar(filtered_df, x='Credential', y='Median Income',
                       title=f'Average Earnings by Degree Level - {
                           selected_field}',
                       labels={'Credential': 'Degree Level', 'Median Income': 'Average Earnings'})

    # Create scatter plot for earnings vs. employment rate
    scatter_plot = px.scatter(filtered_df, x='Years After Graduation', y='Median Income',
                              title=f'Earnings vs. Employment Rate - {
                                  selected_field}',
                              labels={'Years After Graduation': 'Years After Graduation', 'Median Income': 'Median Income'})

    # Create bar chart for cohort size
    cohort_size_chart = px.bar(filtered_df, x='Credential', y='Cohort Size',
                               title=f'Cohort Size - {selected_field}',
                               labels={'Credential': 'Degree Level', 'Cohort Size': 'Cohort Size'})

    return line_chart, bar_chart, scatter_plot, cohort_size_chart


if __name__ == '__main__':
    app.run_server(debug=True)
