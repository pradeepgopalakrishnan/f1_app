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
from plotly.subplots import make_subplots
from datetime import datetime

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

# # Define callback to update the displayed scatter plot based on the selected table and columns
# @app.callback(
#     Output('scatter-plot', 'figure'),
#     [Input('driver1-input', 'value'),
#      Input('lap1-input', 'value'),
#     Input('driver2-input', 'value'),
#      Input('lap2-input', 'value')]
# )
# def update_scatter_plot(driver1, lap1_number, driver2, lap2_number):
    
#     driver1_number = driver_config[driver1.upper()]
#     driver2_number = driver_config[driver2.upper()]
    
#     query = f"SELECT * FROM laps WHERE driver_number = '{driver1_number}' and lap_number = '{lap1_number}';"
#     df = pd.read_sql_query(query, engine)
#     lap_start_time, lap_end_time, lap1_duration = df.date_start.iloc[0], df.date_end.iloc[0], df.lap_duration.iloc[0]
#     query = f"SELECT * FROM cardata WHERE driver_number = '{driver1_number}' and date >= '{lap_start_time}' and date < '{lap_end_time}'"
#     df1 = pd.read_sql_query(query, engine)
#     df1['date'] = pd.to_datetime(df1.date)
#     df1[['rpm', 'speed','n_gear', 'throttle', 'drs', 'brake']] = df1[['rpm', 'speed', 'n_gear', 'throttle', 'drs', 'brake']].astype(int)

#     query = f"SELECT * FROM laps WHERE driver_number = '{driver2_number}' and lap_number = '{lap2_number}';"
#     df = pd.read_sql_query(query, engine)
#     lap_start_time, lap_end_time, lap2_duration = df.date_start.iloc[0], df.date_end.iloc[0], df.lap_duration.iloc[0]
#     query = f"SELECT * FROM cardata WHERE driver_number = '{driver2_number}' and date >= '{lap_start_time}' and date < '{lap_end_time}'"
#     df2 = pd.read_sql_query(query, engine)
#     df2['date'] = pd.to_datetime(df2.date)
#     df2[['rpm', 'speed','n_gear', 'throttle', 'drs', 'brake']] = df2[['rpm', 'speed', 'n_gear', 'throttle', 'drs', 'brake']].astype(int)

#     time1 = df1['date'] - df1['date'].iloc[0]
#     time2 = df2['date'] - df2['date'].iloc[0]
    
#     speeds = [go.Scatter(x=time1, y=df1['speed'], mode='lines', name=f'{driver1.upper()}'),
#               go.Scatter(x=time2, y=df2['speed'], mode='lines', name=f'{driver2.upper()}')]

#     pedals = [go.Scatter(x=time1, y=df1['throttle'], mode='lines', name=f'{driver1.upper()} Thr'),
#               go.Scatter(x=time2, y=df2['throttle'], mode='lines', name=f'{driver2.upper()} Thr'),
#               go.Scatter(x=time1, y=df1['brake'], mode='lines', name=f'{driver1.upper()} Br'),
#               go.Scatter(x=time2, y=df2['brake'], mode='lines', name=f'{driver2.upper()} Br')]

#     rpms = [go.Scatter(x=time1, y=df1['rpm'], mode='lines', name=f'{driver1.upper()}'),
#               go.Scatter(x=time2, y=df2['rpm'], mode='lines', name=f'{driver2.upper()}')]

#     gears = [go.Scatter(x=time1, y=df1['n_gear'], mode='lines', name=f'{driver1.upper()}'),
#               go.Scatter(x=time2, y=df2['n_gear'], mode='lines', name=f'{driver2.upper()}')]

#     drss = [go.Scatter(x=time1, y=df1['drs'], mode='lines', name=f'{driver1.upper()}'),
#               go.Scatter(x=time2, y=df2['drs'], mode='lines', name=f'{driver2.upper()}')]

#     # rpms = [go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['rpm'], mode='lines', name=f'{driver1.upper()}'),
#     #       go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['rpm'], mode='lines', name=f'{driver2.upper()}')]
    
#     # gears = [go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['n_gear'], mode='lines', name=f'{driver1.upper()}'),
#     #           go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['n_gear'], mode='lines', name=f'{driver2.upper()}')]

#     # drs = [go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['drs'], mode='lines', name=f'{driver1.upper()}'),
#     #           go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['drs'], mode='lines', name=f'{driver2.upper()}')]

#     # Create subplots with two rows and one column
#     fig = make_subplots(rows=5, cols=1, subplot_titles=['Speed', 'Pedals', 'RPM', 'Gear', 'DRS'])
#     # fig = make_subplots(rows=2, cols=1, subplot_titles=['Speed', 'Pedals'])

#     # Add traces to subplots
#     for trace in speeds:
#         fig.add_trace(trace, row=1, col=1)
#     for trace in pedals:
#         fig.add_trace(trace, row=2, col=1)
#     for trace in rpms:
#         fig.add_trace(trace, row=3, col=1)
#     for trace in gears:
#         fig.add_trace(trace, row=4, col=1)
#     for trace in drss:
#         fig.add_trace(trace, row=5, col=1)
#     # fig.add_trace(rpms, row=3, col=1)
#     # fig.add_trace(gears, row=4, col=1)
#     # fig.add_trace(drs, row=5, col=1)

#     # Update layout
#     fig.update_layout(height=600, width=800, title_text=f'''{driver1.upper()} : {lap1_duration}s, {driver2.upper()}: {lap2_duration}s''')

#     return fig
    
#     # trace1 = go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['speed'], mode='lines', name=f'{driver1.upper()}')
#     # trace2 = go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['speed'], mode='lines', name=f'{driver2.upper()}')
#     # layout = go.Layout(title = f'''{driver1.upper()} : {lap1_duration}s, {driver2.upper()}: {lap2_duration}s''', width = 800, height = 400, xaxis=dict(title='Time'), yaxis=dict(title='Speed'))
#     # figure = go.Figure(data=[trace1, trace2], layout=layout)

#     # return figure
def compute_distance(df):
    dt = (df['date'] - datetime.now()).dt.total_seconds().diff()
    # dt.iloc[0] = (df['date'].iloc[0] - pd.to_datetime(lap_start_time)).total_seconds()
    dt.iloc[0] = 1
    ds = df['speed'] / 3.6 * dt
    ds.iloc[0] = 0 # on average the first point is 0.1 s after the start line, avg spd of 250kmh(70m/s) => 7m
    df['distance'] = ds.cumsum()

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('driver1-input', 'value'),
     Input('lap1-input', 'value'),
    Input('driver2-input', 'value'),
     Input('lap2-input', 'value')]
)
def update_scatter_plot_2(driver1, lap1_number, driver2, lap2_number):
    
    driver1_number = driver_config[driver1.upper()]
    driver2_number = driver_config[driver2.upper()]
    
    query = f"SELECT * FROM laps WHERE driver_number = '{driver1_number}' and lap_number = '{lap1_number}';"
    df = pd.read_sql_query(query, engine)
    lap_start_time_1, lap_end_time_1, lap_duration_1 = df.date_start.iloc[0], df.date_end.iloc[0], df.lap_duration.iloc[0]
    query = f"SELECT * FROM merged_data WHERE driver_number = '{driver1_number}' and date >= '{lap_start_time_1}' and date < '{lap_end_time_1}'"
    df1 = pd.read_sql_query(query, engine)
    df1['date'] = pd.to_datetime(df1.date)
    df1[['rpm', 'speed','n_gear', 'throttle', 'drs', 'brake', 'x', 'y', 'z']] = df1[['rpm', 'speed', 'n_gear', 'throttle', 'drs', 'brake', 'x', 'y', 'z']].astype(int)

    query = f"SELECT * FROM laps WHERE driver_number = '{driver2_number}' and lap_number = '{lap2_number}';"
    df = pd.read_sql_query(query, engine)
    lap_start_time_2, lap_end_time_2, lap_duration_2 = df.date_start.iloc[0], df.date_end.iloc[0], df.lap_duration.iloc[0]
    query = f"SELECT * FROM merged_data WHERE driver_number = '{driver2_number}' and date >= '{lap_start_time_2}' and date < '{lap_end_time_2}'"
    df2 = pd.read_sql_query(query, engine)
    df2['date'] = pd.to_datetime(df2.date)
    df2[['rpm', 'speed','n_gear', 'throttle', 'drs', 'brake', 'x', 'y', 'z']] = df2[['rpm', 'speed', 'n_gear', 'throttle', 'drs', 'brake', 'x', 'y', 'z']].astype(int)

    compute_distance(df1)
    compute_distance(df2)

    dist1 = df1.distance
    dist2 = df2.distance

    time1 = df1['date'] - df1['date'].iloc[0]
    time2 = df2['date'] - df2['date'].iloc[0]
    
    speeds = [go.Scatter(x=dist1, y=df1['speed'], mode='lines', name=f'{driver1.upper()}'),
              go.Scatter(x=dist2, y=df2['speed'], mode='lines', name=f'{driver2.upper()}')]

    throttles = [go.Scatter(x=dist1, y=df1['throttle'], mode='lines', name=f'{driver1.upper()} Thr'),
              go.Scatter(x=dist2, y=df2['throttle'], mode='lines', name=f'{driver2.upper()} Thr'),]
    brakes = [go.Scatter(x=dist1, y=df1['brake'], mode='lines', name=f'{driver1.upper()} Br'),
              go.Scatter(x=dist2, y=df2['brake'], mode='lines', name=f'{driver2.upper()} Br')]

    rpms = [go.Scatter(x=dist1, y=df1['rpm'], mode='lines', name=f'{driver1.upper()}'),
              go.Scatter(x=dist2, y=df2['rpm'], mode='lines', name=f'{driver2.upper()}')]

    gears = [go.Scatter(x=dist1, y=df1['n_gear'], mode='lines', name=f'{driver1.upper()}'),
              go.Scatter(x=dist2, y=df2['n_gear'], mode='lines', name=f'{driver2.upper()}')]

    drss = [go.Scatter(x=dist1, y=df1['drs'], mode='lines', name=f'{driver1.upper()}'),
              go.Scatter(x=dist2, y=df2['drs'], mode='lines', name=f'{driver2.upper()}')]

    # rpms = [go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['rpm'], mode='lines', name=f'{driver1.upper()}'),
    #       go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['rpm'], mode='lines', name=f'{driver2.upper()}')]
    
    # gears = [go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['n_gear'], mode='lines', name=f'{driver1.upper()}'),
    #           go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['n_gear'], mode='lines', name=f'{driver2.upper()}')]

    # drs = [go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['drs'], mode='lines', name=f'{driver1.upper()}'),
    #           go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['drs'], mode='lines', name=f'{driver2.upper()}')]

    # Create subplots with two rows and one column
    # fig = make_subplots(rows=5, cols=1, subplot_titles=['Speed', 'Pedals', 'RPM', 'Gear', 'DRS'])
    fig = make_subplots(rows=6, cols=1, vertical_spacing = 0.01)
    # fig = make_subplots(rows=2, cols=1, subplot_titles=['Speed', 'Pedals'])

    # Add traces to subplots
    for trace in speeds:
        fig.add_trace(trace, row=1, col=1)
    for trace in throttles:
        fig.add_trace(trace, row=2, col=1)
    for trace in brakes:
        fig.add_trace(trace, row=3, col=1)
    for trace in rpms:
        fig.add_trace(trace, row=4, col=1)
    for trace in gears:
        fig.add_trace(trace, row=5, col=1)
    for trace in drss:
        fig.add_trace(trace, row=6, col=1)
    # fig.add_trace(rpms, row=3, col=1)
    # fig.add_trace(gears, row=4, col=1)
    # fig.add_trace(drs, row=5, col=1)

    # Update layout
    fig.update_layout(height=1000, width=1175, title_text=f'''{driver1.upper()} : {lap_duration_1}s, {driver2.upper()}: {lap_duration_2}s''')
    # fig.update_layout(autosize = True, title_text=f'''{driver1.upper()} : {lap1_duration}s, {driver2.upper()}: {lap2_duration}s''')

    return fig
    
    # trace1 = go.Scatter(x=df1['date'] - df1['date'].iloc[0], y=df1['speed'], mode='lines', name=f'{driver1.upper()}')
    # trace2 = go.Scatter(x=df2['date'] - df2['date'].iloc[0], y=df2['speed'], mode='lines', name=f'{driver2.upper()}')
    # layout = go.Layout(title = f'''{driver1.upper()} : {lap1_duration}s, {driver2.upper()}: {lap2_duration}s''', width = 800, height = 400, xaxis=dict(title='Time'), yaxis=dict(title='Speed'))
    # figure = go.Figure(data=[trace1, trace2], layout=layout)

    # return figure

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
        traces.append(go.Scatter(x=df['date'], y=df[col], mode='lines', name=f'{col}'))
    layout = go.Layout(title = f'''Weather Data''', xaxis=dict(title='Time'), yaxis=dict(title='Value'))
    figure = go.Figure(data=traces, layout=layout)

    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port = 8024)