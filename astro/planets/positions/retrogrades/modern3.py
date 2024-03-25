# coding=utf-8
"""
Created on 2020, April 16th
@author: orion
"""
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Output, Input

import mydcc

app = dash.Dash()
app.layout = html.Div([
    mydcc.Listener( id = "uuu", aim = 'graph' ),
    dcc.Graph( id = 'graph',
               figure = { 'data': [  {'x': [1, 2, 3], 'y': [4, 1, 2]}  ]  }
              ),
    html.Div( id = 'text' )
])

@app.callback(
    Output('text', 'children'),
    [Input('uuu', 'data')])
def myfun(ddd):
    print(ddd)
    # return str(ddd['y']) + ' and ' + str(ddd['y'])
    return 'ttttttt'


if __name__ == '__main__':
    app.run_server()

