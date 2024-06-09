import numpy as np
import pandas as pd
import yfinance as yf
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go

start = '2021-01-01'
end = '2024-01-24'
tickers = ['META', 'TSLA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'NVDA']
selected_tickers = ['META', 'TSLA']

df = yf.download(tickers, start=start, end=end)['Adj Close'][tickers]
daily_log_returns = np.log(df) - np.log(df.shift(1))
daily_log_returns = daily_log_returns.round(3)
daily_log_returns.reset_index(drop=True, inplace=True)

# Calculate correlation matrix
corr = daily_log_returns.corr()

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    html.H1(children='Portfolio Optimizer', style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        multi=True,
        value=selected_tickers,
        style={'width': '60%', 'margin': 'auto'}
    ),
    html.Div([
        dcc.Graph(id='log-returns-graph', style={'width': '60%', 'display': 'inline-block'}),
        dcc.Graph(id='correlation-heatmap', style={'width': '40%', 'display': 'inline-block'}),
    ])
    # ]),
    # dash_table.DataTable(
    #     id='returns-table',
    #     columns=[{'name': col, 'id': col} for col in daily_log_returns.columns],
    #     data=daily_log_returns.to_dict('records'),
    #     style_table={'width': '80%', 'margin': 'auto'},
    #     style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
    #     style_cell={'textAlign': 'center'},
    # )
])

@app.callback(
    [Output('log-returns-graph', 'figure'), Output('correlation-heatmap', 'figure')], #, Output('returns-table', 'data')],
    [Input('ticker-dropdown', 'value')]
)
def update_graph(selected_tickers):
    filtered_df = daily_log_returns[selected_tickers]
    
    fig = px.line(filtered_df, title='Daily Log Returns')
    
    # Generate the correlation heatmap
    corr = filtered_df.corr()
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='viridis',
        colorbar=dict(title='Correlation Coefficient')
    ))
    heatmap_fig.update_layout(title='Log Returns Correlation Heatmap')

    # table_data = filtered_df.to_dict('records')
    return fig, heatmap_fig #, table_data

if __name__ == '__main__':
    app.run_server(debug=True)
