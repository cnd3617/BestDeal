# coding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import bestdeal

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

product_type = 'GTX 1080'
title = html.H1(
        children='{} price history'.format(product_type),
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )

description = html.Div(children='Grab the best deals among all vendors easily', style={
        'textAlign': 'center',
        'color': colors['text']
    })

bd = bestdeal.BestDeal()
data = []
for source in bd.db.get_source_identifiers():
    ts = bd.db.get_time_series(source_id=source['source_id'], product_type=product_type)
    x = []
    y = []
    for record in ts:
        x.append(record['histo_date'])
        y.append(record['histo_price'])
    data.append(plotly.graph_objs.Scatter(name=source['source_name'], x=x, y=y))
    #data.append(plotly.graph_objs.Scatter(name=source['source_name'], x=x, y=y, connectgaps=True))

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

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[title, description, graph])

if __name__ == '__main__':
    app.run_server(debug=True)
