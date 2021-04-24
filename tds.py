import pandas as pd
from helper import *
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from collections import deque

channel_name = 'kyle'
app = dash.Dash(__name__)

data = get_data(channel_name, get_counts = True, get_general_info=True, get_preview_image=True, get_stream_info=True)
print(data)

X = deque(maxlen=50)
X.append(data.index[-1])
Y = deque(maxlen=50)
Y.append(data.current_viewers.values[-1])

app.layout = html.Div([
    html.Div([html.H1(f'Current Number of Viewers for the Channel {data.streamer_id.values[0]}'),
              html.H2(f'{data.lastBroadcast_title.values[0]}, started on {data.current_created_at.values[0]}')]),
    html.Div([html.Img(src=data['PreviewImage'][0], width=300)]),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=120000), ##update every 2 minutes
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('graph-update', 'n_intervals')]
    )
def update_graph(n):
    graphs = []

    upd = get_data(channel_name, get_counts = True)
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