import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
server = app.server

def generate_plot(X, h1, h2, h3, K, T, P, W):
    years = np.arange(0, T + 1)

    # Inflation curves
    inflation_1 = X * (1 - h1 / 100) ** years
    inflation_2 = X * (1 - h2 / 100) ** years
    inflation_3 = X * (1 - h3 / 100) ** years

    # Investment growth with withdrawals
    investment = []
    value = K
    r = P / 100
    for t in years:
        if t > 0:
            value = value * (1 + r) - (W * 12)
        investment.append(value)

    fig = go.Figure()

    for infl, rate in zip([inflation_1, inflation_2, inflation_3], [h1, h2, h3]):
        fig.add_trace(go.Scatter(
            x=years, y=infl,
            mode='lines+text',
            name=f"Inflation @ {rate}%",
            text=[f"{v:,.0f}" for v in infl],
            textposition="top right"
        ))

    fig.add_trace(go.Scatter(
        x=years, y=investment,
        mode='lines+text',
        name=f"Investment @ {P}% | ₹{W}/mo withdrawal",
        text=[f"{v:,.0f}" for v in investment],
        textposition="bottom right",
        line=dict(width=4, dash='dot')
    ))

    fig.update_layout(
        title="📈 Inflation vs Investment Projection",
        xaxis_title="Years",
        yaxis_title="Value (₹)",
        hovermode="x unified",
        legend=dict(x=0.01, y=0.99),
        template="plotly_dark",
        margin=dict(t=50, l=30, r=30, b=30)
    )

    return fig

def generate_plot_2(X, h1, h2, h3, K, T, P, W):
    years = np.arange(0, T + 1)

    # Inflation curves (purchasing power of X)
    inflation_1 = X * (1 - h1 / 100) ** years
    inflation_2 = X * (1 - h2 / 100) ** years
    inflation_3 = X * (1 - h3 / 100) ** years

    # Investment growth with monthly withdrawals
    investment = []
    value = K
    r = P / 100
    for t in years:
        if t > 0:
            value = value * (1 + r) - (W * 12)
        investment.append(value)
    investment = np.array(investment)

    # Inflation-adjusted investment values for each inflation rate
    invest_real_1 = investment / ((1 + h1 / 100) ** years)
    invest_real_2 = investment / ((1 + h2 / 100) ** years)
    invest_real_3 = investment / ((1 + h3 / 100) ** years)

    fig = go.Figure()

    # Plot inflation curves (value of X eroding)
    for infl, rate in zip([inflation_1, inflation_2, inflation_3], [h1, h2, h3]):
        fig.add_trace(go.Scatter(
            x=years, y=infl,
            mode='lines+text',
            name=f"Inflation @ {rate}% (Purchasing power of ₹X)",
            text=[f"{v:,.0f}" for v in infl],
            textposition="top right"
        ))

    # Plot nominal investment value
    fig.add_trace(go.Scatter(
        x=years, y=investment,
        mode='lines+text',
        name=f"Nominal Investment @ {P}% with ₹{W}/mo withdrawal",
        text=[f"{v:,.0f}" for v in investment],
        textposition="bottom right",
        line=dict(width=4, dash='dot', color='green')
    ))

    # Plot inflation-adjusted investment values for each inflation
    colors = ['red', 'orange', 'purple']
    for invest_real, rate, color in zip([invest_real_1, invest_real_2, invest_real_3], [h1, h2, h3], colors):
        fig.add_trace(go.Scatter(
            x=years, y=invest_real,
            mode='lines+text',
            name=f"Investment real @ {P}% adjusted for {rate}% inflation",
            text=[f"{v:,.0f}" for v in invest_real],
            textposition="bottom left",
            line=dict(width=3, dash='dash', color=color)
        ))

    fig.update_layout(
        title="Inflation Impact & Investment Growth (Nominal + Inflation-Adjusted)",
        xaxis_title="Years",
        yaxis_title="Value (₹)",
        hovermode="x unified",
        legend=dict(x=0.01, y=0.99),
        template="plotly_dark",
        margin=dict(t=50, l=30, r=30, b=30)
    )

    return fig


app.layout = html.Div([
    html.H2("📊 Inflation vs Investment Plotter", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Label("Base Amount (X)"),
            dcc.Input(id="X", type="number", value=1000000, step=10000)
        ]),
        html.Div([
            html.Label("Inflation Rates (%)"),
            dcc.Slider(id="h1", min=1, max=15, step=0.5, value=4, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Slider(id="h2", min=1, max=15, step=0.5, value=6, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Slider(id="h3", min=1, max=15, step=0.5, value=8, marks=None, tooltip={"placement": "bottom", "always_visible": True})
        ]),
        html.Div([
            html.Label("Investment Amount (K)"),
            dcc.Input(id="K", type="number", value=1000000, step=10000)
        ]),
        html.Div([
            html.Label("Duration (Years)"),
            dcc.Input(id="T", type="number", value=20, step=1)
        ]),
        html.Div([
            html.Label("Return Rate (%)"),
            dcc.Input(id="P", type="number", value=10, step=0.5)
        ]),
        html.Div([
            html.Label("Monthly Withdrawal (W)"),
            dcc.Input(id="W", type="number", value=10000, step=500)
        ])
    ], style={'columnCount': 2, 'gap': '20px'}),

    html.Br(),

    dcc.Graph(id="plot", config={'toImageButtonOptions': {
        'format': 'png', 'filename': 'inflation_vs_investment', 'scale': 2
    }}),

    html.Div("Use the 📷 camera icon on the top right of the chart to save as PNG.", style={'textAlign': 'center', 'marginTop': '10px'})
])

@app.callback(
    Output("plot", "figure"),
    Input("X", "value"),
    Input("h1", "value"),
    Input("h2", "value"),
    Input("h3", "value"),
    Input("K", "value"),
    Input("T", "value"),
    Input("P", "value"),
    Input("W", "value")
)
def update_plot(X, h1, h2, h3, K, T, P, W):
    return generate_plot_2(X, h1, h2, h3, K, T, P, W)

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run(debug=True)
