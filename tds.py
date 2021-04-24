import pandas as pd
from helper import *
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from collections import deque


app = dash.Dash(__name__)


X = deque(maxlen=50)
Y = deque(maxlen=50)

channel_name = ''
headers = ''
def build_plot(channel_name, headers):
    global X,Y
    data = get_data(channel_name, get_counts = True, get_general_info=True, get_preview_image=True, get_stream_info=True, headers=headers)
    print(data)
    X.append(data.index[-1])
    Y.append(data.current_viewers.values[-1])
    return None


app.layout = html.Div([html.Div([
    html.Div(children='''\nName of the channel to track:\t'''),
    dcc.Input(id='channel', value='', type='text'),
    html.Div(children='''\nPaste the headers\n'''),
    dcc.Input(id='headers', value='', type='text'),
    html.Button('Submit', id='submit-val', n_clicks=0),
    ]),


    html.Div([html.H1(id='container-button-basic',children = f'waiting for input'),
              html.H2(id='add_info',children = '')]),
    html.Div([html.Img(id='image',src='', width=300)]),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=120000), ##update every 2 minutes
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})

@app.callback(
    Output('container-button-basic', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('channel', 'value')])
def update_output(n_clicks, value):
    return f'Current Number of Viewers for the Channel {value}'

@app.callback(
    Output('add_info', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('channel', 'value'),
     State('headers', 'value')])
def update_output(n_clicks, value, head):
    global channel_name, headers, data 
    headers = head
    channel_name = value
    build_plot(channel_name, headers)
    return f'{data.lastBroadcast_title.values[0]}, started on {data.current_created_at.values[0]}'
@app.callback(
    Output('image', 'src'),
    [Input('submit-val', 'n_clicks')],
    [State('channel', 'value')])
def update_output(n_clicks, value):
    global data 
    return data['PreviewImage'][0]

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('graph-update', 'n_intervals')]
    )
def update_graph(n):
    graphs = []

    upd = get_data(channel_name, headers=headers, get_counts = True)
    X.append(upd.index[-1])
    Y.append(upd.current_viewers.values[-1])
    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers',
        )

    graphs.append(html.Div(dcc.Graph(
        animate=True,
        figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]))}
        ), className='col s12'))

    return graphs

app.run_server(debug=True)