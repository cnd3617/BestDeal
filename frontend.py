# coding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import timedelta, date
import plotly
import bestdeal
import itertools


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def build_graph_by_product_type(bd, product_type, colors):
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

    no_data = True
    data = []
    start_date = date(year=2018, month=1, day=1)
    end_date = date(year=2018, month=12, day=31)
    for source in bd.db.get_source_identifiers():
        x = []
        y = []
        for single_date in daterange(start_date, end_date):
            current_date = single_date.strftime('%Y%m%d')
            minimum_record = bd.db.get_minimum_price(source['source_id'], product_type, current_date)
            if minimum_record['histo_price']:
                x.append(current_date)
                y.append(minimum_record['histo_price'])
        if x and y:
            no_data = False
            data.append(plotly.graph_objs.Scatter(name=source['source_name'], x=x, y=y, connectgaps=True))

    if no_data:
        return []

    graph = dcc.Graph(
        id='{}_graph'.format(product_type),
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
    return [title, description, graph]


def build_website():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }

    bd = bestdeal.BestDeal()
    children = []
    product_items = [['GTX'], bd.product_types, ['', 'Ti']]
    for product_type in itertools.product(*product_items):
        children += build_graph_by_product_type(bd, ' '.join(product_type).strip(), colors)

    app.layout = html.Div(style={'backgroundColor': colors['background']}, children=children)
    return app


if __name__ == '__main__':
    app = build_website()
    app.run_server(debug=True)
