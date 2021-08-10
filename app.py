import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from options import element_names, reaction_names

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            # id='demo-dropdown',
            options=element_names,
            placeholder='Enter an element...',
            style={'width': 200, "display": "inline-block"},
            # labelStyle={"display": "inline-block"}
            id='element_name',
        ),
        dcc.Input(
            id='fraction_value',
            value='',
            type='number',
            style={'padding': 10},
            min=0,
            max=1,
            step=0.01,
        ),
        # does not allow step size
        # daq.NumericInput(
        #     id='fraction_value',
        #     label='Enter a fraction value...',
        #     value=0,
        #     min=0,
        #     max=1,
        #     # step=0.01,
        #     size=50,
        #     style={'width': 200, "display": "inline-block"},
        #     # style={'padding': 10}
        # ),
        html.Button('Add Element', id='editing-rows-button', n_clicks=0),
    ], style={'height': 50}),
    html.Br(),
    dash_table.DataTable(
        id='adding-rows-table',
        columns=[{
            'name': 'Elements',
            'id': 'Elements',
        }, {
            'name': 'Fractions',
            'id': 'Fractions',

        }],
        data=[],
        editable=True,
        row_deletable=True
    ),
    dcc.Input(
        id='density_value',
        value='',
        type='number',
        style={'padding': 10},
        min=0,
        step=0.01,
    ),
    dcc.Dropdown(
        # id='demo-dropdown',
        options=reaction_names,
        placeholder='Select reactions to plot',
        style={'width': 700, "display": "inline-block"},
        # labelStyle={"display": "inline-block"}
        id='reaction_names',
        multi=True
    ),
    html.Button('Plot material', id='update_plot', title='Click to create or refresh the plot'),
    # dcc.Graph(id='graph-container')
    html.Div(id="graph_container"),
])

@app.callback(
    dash.dependencies.Output('graph_container', "children"),
    [
        Input("update_plot", "n_clicks"),
        Input("reaction_names", "value"),
        # Input("density_value", "value"),
        # Input("adding-rows-table", "rows"),
    ],
    # [dash.dependencies.Input('update_plot', 'n_clicks')],
    # [dash.dependencies.State('input-on-submit', 'value')]
    )
def update_output(n_clicks, value):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    if n_clicks > 0:
        print('got here')

@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('element_name', 'value'),
    State('fraction_value', 'value'),
    )
def add_row(n_clicks, rows, element_name, fraction_value):
    if n_clicks > 0:
        if element_name==None:
            print('no elements selected')
            return rows
        if fraction_value=='':
            print('no fraction_value provided')
            return rows
        rows.append({'Elements':element_name, 'Fractions':fraction_value})
    return rows


# @app.callback(
#     Output('adding-rows-table', 'columns'),
#     Input('adding-rows-button', 'n_clicks'),
#     State('adding-rows-name', 'value'),
#     State('adding-rows-table', 'columns'))
# def update_rows(n_clicks, value, existing_rows):
#     if n_clicks > 0:
#         existing_rows.append({
#             'id': value, 'name': value,
#             'renamable': True, 'deletable': True
#         })
#     return existing_rows


#adapt to plot cross sections on table update
# @app.callback(
#     Output('adding-rows-graph', 'figure'),
#     Input('adding-rows-table', 'data'),
#     Input('adding-rows-table', 'columns'))
# def display_output(rows, columns):
#     return {
#         'data': [{
#             'type': 'heatmap',
#             'z': [[row.get(c['id'], None) for c in columns] for row in rows],
#             'x': [c['name'] for c in columns]
#         }]
#     }


if __name__ == '__main__':
    app.run_server(debug=True)