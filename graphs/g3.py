import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)
categories = ['A', 'B', 'C']
values = [10, 15, 7]
df = px.data.iris()

# Create specific charts
scatter_chart = px.scatter(df, x='sepal_width', y='sepal_length', color='species', title="Scatter Chart (1,3)")
bar_chart = px.bar(x=categories, y=values, title="Bar Chart (2,2)")
line_chart = px.line(x=x, y=y, title="Line Chart (3,3)")

# Filler charts
filler_chart = lambda title: px.line(x=np.random.rand(10), y=np.random.rand(10), title=title)

# Layout
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("3x3 Chart Layout Dashboard", style={'textAlign': 'center'}),
    html.Div([
        # Row 1
        html.Div(dcc.Graph(figure=filler_chart("Chart (1,1)")), className="chart"),
        html.Div(dcc.Graph(figure=filler_chart("Chart (1,2)")), className="chart"),
        html.Div(dcc.Graph(figure=scatter_chart), className="chart"),

        # Row 2
        html.Div(dcc.Graph(figure=filler_chart("Chart (2,1)")), className="chart"),
        html.Div(dcc.Graph(figure=bar_chart), className="chart"),
        html.Div(dcc.Graph(figure=filler_chart("Chart (2,3)")), className="chart"),

        # Row 3
        html.Div(dcc.Graph(figure=filler_chart("Chart (3,1)")), className="chart"),
        html.Div(dcc.Graph(figure=filler_chart("Chart (3,2)")), className="chart"),
        html.Div(dcc.Graph(figure=line_chart), className="chart"),
    ], style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr 1fr',
        'gap': '10px',
        'padding': '20px'
    })
])

if __name__ == '__main__':
    app.run_server(debug=True)
