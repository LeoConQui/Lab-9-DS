import plotly
import pandas as pd
df = pd.read_csv("risk_factors_cervical_cancer.csv")
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample DataFrame (replace this with your own DataFrame)
data = {
    "Age": [25, 30, 35, 40, 45, 50, 55, 60],
    "Smokes (years)": [10, 15, 20, 5, 25, 15, 30, 10],
    "Smokes (packs/year)": [2, 5, 10, 1, 15, 8, 12, 3],
    "Number of sexual partners": [2, 3, 5, 2, 6, 4, 7, 3],
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Interactive Dashboard"),
    
    # Dropdown component for filtering by Age
    dcc.Dropdown(
        id='age-dropdown',
        options=[{'label': age, 'value': age} for age in df['Age'].unique()],
        value=df['Age'].unique()[0]
    ),
    
    # Dropdowns for selecting x and y axes for the scatter plot
    dcc.Dropdown(
        id='x-axis-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='Smokes (years)'
    ),
    dcc.Dropdown(
        id='y-axis-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='Smokes (packs/year)'
    ),
    
    # Scatter plot
    html.Div([
        dcc.Graph(id='scatter-plot'),
    ]),
    
    # Dropdown for selecting the bar graph column
    dcc.Dropdown(
        id='bar-graph-column-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='Number of sexual partners'
    ),
    
    # Bar graph for Number of sexual partners
    html.Div([
        dcc.Graph(id='bar-graph')
    ])
])

# Define a callback to update the scatter plot and bar graph based on user input
@app.callback(
    [Output('scatter-plot', 'figure'), Output('bar-graph', 'figure')],
    [Input('age-dropdown', 'value'), Input('x-axis-dropdown', 'value'), Input('y-axis-dropdown', 'value'), Input('bar-graph-column-dropdown', 'value')]
)
def update_plots(selected_age, x_column, y_column, bar_column):
    filtered_df = df[df['Age'] == selected_age]
    
    # Update scatter plot based on the selected x and y axes
    scatter_fig = px.scatter(
        filtered_df,
        x=x_column,
        y=y_column,
        color=x_column,
        title=f"Scatter Plot for Age {selected_age}"
    )
    
    # Update bar graph based on the selected column
    bar_fig = px.bar(
        filtered_df,
        x=bar_column,
        title=f"Bar Graph for {bar_column} for Age {selected_age}"
    )
    
    return scatter_fig, bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)

