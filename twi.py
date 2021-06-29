import requests as r
import pandas as pd
import re
from datetime import datetime
import pytz
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import time
import sys, signal


import plotly
from dash.dependencies import Input, Output

import plotly.io as pio
pio.renderers.default = "browser"

def get_payload(name_of_the_channel, get_counts = False, get_general_info = False, get_preview_image = False, get_stream_info = False):
    x = {"operationName":"UseViewCount","variables":{"channelLogin":name_of_the_channel},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"00b11c9c428f79ae228f30080a06ffd8226a1f068d6f52fbc057cbde66e994c2"}}}
    y = {"operationName":"PlayerTrackingContextQuery","variables":{"channel":name_of_the_channel,"isLive":True,"hasCollection":False,"collectionID":"","videoID":"","hasVideo":False,"slug":"","hasClip":False},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"3fbf508886ff5e008cb94047acc752aad7428c07b6055995604de16c4b01160a"}}}
    z = {"operationName":"VideoPreviewOverlay","variables":{"login":name_of_the_channel},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"3006e77e51b128d838fa4e835723ca4dc9a05c5efd4466c1085215c6e437e65c"}}}
    t = {"operationName":"StreamMetadata","variables":{"channelLogin":name_of_the_channel},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"1c719a40e481453e5c48d9bb585d971b8b372f8ebb105b17076722264dfa5b3e"}}}
    pre = """[{},{},{},{}]""".format(str(x)*get_counts,str(y)*get_general_info,str(z)*get_preview_image,str(t)*get_stream_info).replace("'",'"').replace('True','true').replace('False','false')
    pre = re.sub(',+',',',pre)
    pre = re.sub(',+]$',']',pre)
    return re.sub('^\[,+','[',pre)


def clean_a_bit(data: r.models.Response) -> pd.Series:
    data = data.json()
    namedData = dict()
    cleanedData = dict()
    for i in data:
        name = i['extensions']['operationName']
        namedData[name] = i['data']
    now = datetime.now(tz =pytz.timezone('Europe/Paris'))
    
    if 'PlayerTrackingContextQuery' in namedData.keys():
        cleanedData['streamer_id'] = namedData['PlayerTrackingContextQuery']['user']['id']
        cleanedData['streamer_login'] = namedData['PlayerTrackingContextQuery']['user']['login']
        cleanedData['game_id'] = namedData['PlayerTrackingContextQuery']['user']['broadcastSettings']['game']['id']
        cleanedData['name'] = namedData['PlayerTrackingContextQuery']['user']['broadcastSettings']['game']['name']
        cleanedData['type'] = namedData['PlayerTrackingContextQuery']['user']['broadcastSettings']['game']['__typename']
    if 'VideoPreviewOverlay' in namedData.keys():
        cleanedData['PreviewImage'] = namedData['VideoPreviewOverlay']['user']['stream']['previewImageURL']
    if 'StreamMetadata' in namedData.keys():
        cleanedData['lastBroadcast_title'] = namedData['StreamMetadata']['user']['lastBroadcast']['title']
        cleanedData['current_created_at'] = namedData['StreamMetadata']['user']['stream']['createdAt']
    if 'UseViewCount' in namedData.keys():
        cleanedData['current_viewers'] = namedData['UseViewCount']['user']['stream']['viewersCount']
    series = pd.Series(cleanedData)
    series['time']=now
    return series.to_frame().T.set_index('time')

def get_data(username, get_counts, get_general_info=False, get_preview_image=False, get_stream_info=False, **kwargs):
    url = 'https://gql.twitch.tv/gql'
    headers = """Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US
Cache-Control: no-cache
Client-Id: kimne78kx3ncx6brgo4mv6wki5h1ko
Connection: keep-alive
Content-Length: 6576
Content-Type: text/plain;charset=UTF-8
DNT: 1
Host: gql.twitch.tv
Origin: https://www.twitch.tv
Pragma: no-cache
Referer: https://www.twitch.tv/{}
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36
X-Device-Id: c170bf824a20e5aa""".format(username)
    headers = dict(i.split(': ') for i in headers.split('\n'))
    resp=r.post(url, headers=headers, data=get_payload(username,get_counts,get_general_info,get_preview_image,get_stream_info))
    return clean_a_bit(resp)


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

def create_plot(data):
    fig=go.FigureWidget([go.Scatter(x=data.index, y=data.current_viewers,
                    mode='lines',
                    name='Number of views of a certain channel')])
    return fig

def upd(data, fig):
    dat = create_plot(data).data
    fig.data[0]['y'] = dat[0].y
    fig.data[0]['x'] = dat[0].x
    

if __name__ == '__main__':

    print('Assessing the data for ', str(sys.argv[1]),'.')
    name = sys.argv[1]

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div(
        html.Div([
            html.H4(f'Live updates on number of viewers for Twitch channel {name}'),
            html.Div(id='live-update-text'),
            dcc.Graph(id='live-update-graph'),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            )
        ])
    )

    data = get_data(name, get_counts = True)
    @app.callback(Output('live-update-text', 'children'),
                  Input('interval-component', 'n_intervals'))
    def update_metrics(n):
        global data
        number = data.iloc[-1,0]
        style = {'padding': '5px', 'fontSize': '16px'}
        return [
            html.Span('Current: {}'.format(number), style=style)
        ]

    #data = get_data(name, get_counts = True)
    #fig =create_plot(data)

    @app.callback(Output('live-update-graph', 'figure'),
                  Input('interval-component', 'n_intervals'))
    def update_graph_live(n):
        global data
        data = data.append(get_data(name, get_counts = True))
        fig =create_plot(data)
        upd(data, fig)
        return fig

   
    app.run_server(debug=True, use_reloader=True)

