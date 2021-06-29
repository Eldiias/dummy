import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque


X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)
initial_trace = plotly.graph_objs.Scatter(
    x=list(X),
    y=list(Y),
    name='Scatter',
    mode='lines+markers'
)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph',
                  animate=True,
                  figure={'data': [initial_trace],
                          'layout': go.Layout(
                              xaxis=dict(range=[min(X), max(X)]),
                              yaxis=dict(range=[min(Y), max(Y)]))
                          }),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    X.append(X[-1]+1)
    Y.append(Y[-1]+2)

    trace = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [trace],
            'layout': go.Layout(
                xaxis=dict(range=[min(X), max(X)]),
                yaxis=dict(range=[min(Y), max(Y)]))
            }


if __name__ == '__main__':
    app.run_server(port=8051, debug=True)