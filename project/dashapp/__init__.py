from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import os

def create_dash_application(flask_app):
    # Create a Dash application integrated with Flask
    dash_app = Dash(
        server=flask_app,
        name="Dashboard",
        url_base_pathname="/dash/",
        external_stylesheets=[
            {
                "href": (
                    "https://fonts.googleapis.com/css2?"
                    "family=Lato:wght@400;700&display=swap"
                ),
                "rel": "stylesheet",
            },
        ],
    )

    # Get the path of the current Python file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute file path
    file_path = os.path.join(current_dir, "custData.csv")

    try:
        data = (
            pd.read_csv(file_path)
            .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
            .sort_values(by="Date")
        )
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        data = pd.DataFrame()  # Set an empty DataFrame in case of error

    if not data.empty:  # Proceed only if data is available
        regions = data["region"].sort_values().unique()
        customer_types = data["type"].sort_values().unique()

        

        dash_app.layout = html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(children="Customer  Analytics", className="header-title"),
                        html.P(
                            children=(
                                "Analyze the behavior of Customers"
                                " and the transactions made  between 2015 and 2018"
                            ),
                            className="header-description",
                        ),
                    ],
                    className="header",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(children="Region", className="menu-title"),
                                dcc.Dropdown(
                                    id="region-filter",
                                    options=[
                                        {"label": region, "value": region}
                                        for region in regions
                                    ],
                                    value="Albany",
                                    clearable=False,
                                    className="dropdown",
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(children="Type", className="menu-title"),
                                dcc.Dropdown(
                                    id="type-filter",
                                    options=[
                                        {
                                            "label": customer_type.title(),
                                            "value": customer_type,
                                        }
                                        for customer_type in customer_types
                                    ],
                                    value="organic",
                                    clearable=False,
                                    searchable=False,
                                    className="dropdown",
                                ),
                            ],
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    children="Date Range", className="menu-title"
                                ),
                                dcc.DatePickerRange(
                                    id="date-range",
                                    min_date_allowed=data["Date"].min().date(),
                                    max_date_allowed=data["Date"].max().date(),
                                    start_date=data["Date"].min().date(),
                                    end_date=data["Date"].max().date(),
                                ),
                            ]
                        ),
                    ],
                    className="menu",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id="price-chart",
                                config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                        html.Div(
                            children=dcc.Graph(
                                id="volume-chart",
                                config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    ],
                    className="wrapper",
                ),
            ]
        )

        @dash_app.callback(
            Output("price-chart", "figure"),
            Output("volume-chart", "figure"),
            Input("region-filter", "value"),
            Input("type-filter", "value"),
            Input("date-range", "start_date"),
            Input("date-range", "end_date"),
        )
        def update_charts(region, customer_type, start_date, end_date):
            filtered_data = data.query(
                "region == @region and type == @customer_type"
                " and Date >= @start_date and Date <= @end_date"
            )
            price_chart_figure = {
                "data": [
                    {
                        "x": filtered_data["Date"],
                        "y": filtered_data["AveragePrice"],
                        "type": "lines",
                        "hovertemplate": "$%{y:.2f}<extra></extra>",
                    },
                ],
                "layout": {
                    "title": {
                        "text": "Average Transaction Amount",
                        "x": 0.05,
                        "xanchor": "left",
                    },
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"tickprefix": "$", "fixedrange": True},
                    "colorway": ["#17B897"],
                },
            }

            volume_chart_figure = {
                "data": [
                    {
                        "x": filtered_data["Date"],
                        "y": filtered_data["Total Volume"],
                        "type": "lines",
                    },
                ],
                "layout": {
                    "title": {"text": "Transaction Amounts", "x": 0.05, "xanchor": "left"},
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"fixedrange": True},
                    "colorway": ["#E12D39"],
                },
            }
            return price_chart_figure, volume_chart_figure

    return dash_app
