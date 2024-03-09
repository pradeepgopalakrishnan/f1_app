# Import necessary libraries
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Connect to your SQL database
engine = create_engine("sqlite:///f1_9472.db")

driver_config = {'VER': 1,
  'SAR': 2,
  'RIC': 3,
  'NOR': 4,
  'GAS': 10,
  'PER': 11,
  'ALO': 14,
  'LEC': 16,
  'STR': 18,
  'MAG': 20,
  'TSU': 22,
  'ALB': 23,
  'ZHO': 24,
  'HUL': 27,
  'OCO': 31,
  'BEA': 38,
  'HAM': 44,
  'RUS': 63,
  'BOT': 77,
  'PIA': 81}

# Define your Dash app
app = dash.Dash(__name__)

# Define the layout of your app
app.layout = html.Div([
    html.H1("Laptime Comparison for session 9472"),
    
    # Dropdown to select table
   
    html.Label("Driver 1"),
    dcc.Dropdown(
        id='driver1-input',
        options=[
            {'label': col, 'value': col} for col in driver_config.keys()
        ],
        style = {'width':'100px'},
        value='VER'  # Default selected column
    ),

    html.Label("Lap 1"),
    dcc.Input(id='lap1-input', type='number', value=5),

    html.Label("Driver 2"),
        dcc.Dropdown(
        id='driver2-input',
        options=[
            {'label': col, 'value': col} for col in driver_config.keys()
        ],
        style = {'width':'100px'},
        value='HAM'  # Default selected column
    ),

    html.Label("Lap 2"),
    dcc.Input(id='lap2-input', type='number', value=5),
    
    # Display scatter plot based on the selected table and columns
    dcc.Graph(id='scatter-plot'),

    dcc.Graph(id='weather-plot'),
])

# Define callback to update the displayed scatter plot based on the selected table and columns
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('driver1-input', 'value'),
     Input('lap1-input', 'value'),
    Input('driver2-input', 'value'),
     Input('lap2-input', 'value')]
)
def update_scatter_plot(driver1, lap1_number, driver2, lap2_number):
    driver1_number = driver_config[driver1.upper()]
    driver2_number = driver_config[driver2.upper()]
    query = f"SELECT * FROM laps WHERE driver_number = '{driver1_number}' and lap_number = '{lap1_number}';"
    df = pd.read_sql_query(query, engine)
    lap_start_time, lap_end_time, lap1_duration = df.date_start.iloc[0], df.date_end.iloc[0], df.lap_duration.iloc[0]
    query = f"SELECT * FROM cardata WHERE driver_number = '{driver1_number}' and date >= '{lap_start_time}' and date < '{lap_end_time}'"
    df1 = pd.read_sql_query(query, engine)
    df1['date'] = pd.to_datetime(df1.date)
    df1[['rpm', 'speed','n_gear', 'throttle', 'drs', 'brake']] = df1[['rpm', 'speed', 'n_gear', 'throttle', 'drs', 'brake']].astype(int)

    query = f"SELECT * FROM laps WHERE driver_number = '{driver2_number}' and lap_number = '{lap2_number}';"
    df = pd.read_sql_query(query, engine)
    lap_start_time, lap_end_time, lap2_duration = df.date_start.iloc[0], df.date_end.iloc[0], df.lap_duration.iloc[0]
    query = f"SELECT * FROM cardata WHERE driver_number = '{driver2_number}' and date >= '{lap_start_time}' and date < '{lap_end_time}'"
    df2 = pd.read_sql_query(query, engine)
    df2['date'] = pd.to_datetime(df2.date)
    df2[['rpm', 'speed','n_gear', 'throttle', 'drs', 'brake']] = df2[['rpm', 'speed', 'n_gear', 'throttle', 'drs', 'brake']].astype(int)

    trace1 = go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['speed'], mode='lines', name=f'{driver1.upper()}')
    trace2 = go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['speed'], mode='lines', name=f'{driver2.upper()}')
    layout = go.Layout(title = f'''{driver1.upper()} : {lap1_duration}s, {driver2.upper()}: {lap2_duration}s''', width = 800, height = 400, xaxis=dict(title='Time'), yaxis=dict(title='Speed'))
    figure = go.Figure(data=[trace1, trace2], layout=layout)

    return figure

@app.callback(
    Output('weather-plot', 'figure'),
    [Input('driver1-input', 'value'),]
)
def update_weather_plot(_):

    query = f"SELECT * FROM weather"
    df = pd.read_sql_query(query, engine)

    cols = ['air_temperature', 'humidity',
       'pressure', 'rainfall', 'track_temperature', 'wind_direction',
       'wind_speed']
    df['date'] = pd.to_datetime(df.date)
    df[cols] = df[cols].astype(float)
    
    traces = []
    for col in cols:
        # df[col] = df[col].astype(float)
        traces.append(go.Scatter(x=df['date'] - df['date'].iloc[0], y=df[col], mode='lines', name=f'{col}'))
    layout = go.Layout(title = f'''Weather Data''', xaxis=dict(title='Time'), yaxis=dict(title='Value'))
    figure = go.Figure(data=traces, layout=layout)

    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port = 8050)