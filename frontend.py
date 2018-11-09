# coding: utf-8

import bestdeal
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

title = html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )

description = html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    })

bd = bestdeal.BestDeal()

data = []
ts = bd.db.get_time_series(source_id=1, product_type='GTX 1080')

for source_id in [1, 2, 3]:
    ts = bd.db.get_time_series(source_id=source_id, product_type='GTX 1080')
    x = []
    y = []
    for record in ts:
        x.append(record['histo_date'])
        y.append(record['histo_price'])
    data.append(plotly.graph_objs.Scatter(x=x, y=y, connectgaps=True))

graph = dcc.Graph(
        id='example-graph-2',
        figure={
            'data': data,
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )

#trace = plotly.graph_objs.Scatter(x = [10, 20, 30], y = [500, 1000, 1500])
#data = [trace]
#plotly.plotly.iplot(data, filename='basic-line')

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[title, description, graph])

if __name__ == '__main__':
    app.run_server(debug=True)