import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from options import element_names, reaction_names
import openmc
from openmc.data import REACTION_MT
from openmc.data.reaction import REACTION_NAME

app = dash.Dash(
    __name__,
    prevent_initial_callbacks=True,
    meta_tags=[
        {
            "name": "title",
            "content": "XSPlot material cross section plotter"
        },
        {
            "name": "description",
            "content": "Online graph plotting tool for neutron macroscopic cross sections of materials",
        },
        {
            "name": "keywrds",
            "keywords": "plot neutron nuclear cross section energy barns database plotter",
        },
        {
            "name": "author",
            "content": "Jonathan Shimwell"
        },
        {
            "http-equiv": "X-UA-Compatible",
            "content": "IE=edge"
        },
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        },
    ],
)
app.title = "XSPlot neutron cross section plotter"
app.description = "Plot neutron cross sections. Nuclear data from the TENDL library."



server = app.server


app.layout = html.Div(
    [
    html.Table(
        [
            html.Tr(
                [
                    html.Th(
                        dcc.Dropdown(
                            # id='demo-dropdown',
                            options=element_names,
                            placeholder="Select an element...",
                            style={"width": 200, "display": "inline-block"},
                            # labelStyle={"display": "inline-block"}
                            id="element_name",
                            # style={"height": 50}
                        ),
                    ),
                    html.Th(
                        dcc.Input(
                            id="fraction_value",
                            placeholder="Mass fraction",
                            value="",
                            type="number",
                            style={"padding": 10},
                            min=0,
                            max=1,
                            step=0.01,
                            # style={"height": 50}
                        ),
                    ),
                    html.Th(
                        html.Button(
                            "Add Element",
                            id="editing-rows-button",
                            n_clicks=0,
                            style={"height": 40, "width":200}
                        ),
                    ),
                ]
            ),
        ],
        style={"width": "100%"},
    ),
        # style={},
        # style={"height": 50, "text-align": "center"},

    html.Br(),
    dash_table.DataTable(
        id="adding-rows-table",
        style_cell={'textAlign': 'center'},
        columns=[
            {
                "name": "Elements",
                "id": "Elements",
            },
            {
                "name": "Fractions",
                "id": "Fractions",
            },
        ],
        data=[],
        editable=True,
        row_deletable=True,
    ),
    html.Br(),
    html.Table(
        [
            html.Tr(
                [
                    html.Th(
                        dcc.Input(
                            id="density_value",
                            placeholder="density in g/cm3",
                            value="",
                            type="number",
                            style={"padding": 10},
                            min=0,
                            step=0.01,
                        ),
                    ),
                    html.Th(
                        dcc.Dropdown(
                            # id='demo-dropdown',
                            options=reaction_names,
                            placeholder="Select reaction(s) to plot",
                            style={"width": 400, "display": "inline-block"},
                            # labelStyle={"display": "inline-block"}
                            id="reaction_names",
                            multi=True,
                        ),
                    ),
                ]
            )
        ],
        style={"width": "100%"},
    ),
    html.Br(),
    html.Div(
        [
            html.Button(
                "Plot material",
                id="update_plot",
                title="Click to create or refresh the plot",
                style={"height": 40, "width":200}
            ),
        ],
        style={"height": 50, "text-align": "center"},
    ),
    # dcc.Graph(id='graph-container')
    html.Div(id="graph_container"),
]
)


@app.callback(
    dash.dependencies.Output("graph_container", "children"),
    [
        Input("update_plot", "n_clicks"),
        Input("reaction_names", "value"),
        Input("adding-rows-table", "data"),
        Input("density_value", "value"),
        # Input("adding-rows-table", "rows"),
    ],
    # [dash.dependencies.Input('update_plot', 'n_clicks')],
    # [dash.dependencies.State('input-on-submit', 'value')]
)
def update_output(n_clicks, reaction_names, rows, density_value):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    if n_clicks > 0:
        trigger_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "update_plot":

            print("reaction_names", reaction_names)
            print("rows", rows)
            print("density_value", density_value)

            my_mat = openmc.Material(name="my_mat")

            for entry in rows:
                # for key, values in entry.items():
                print(entry)
                # print('key',key, 'values',values)

                my_mat.add_element(
                    entry["Elements"], entry["Fractions"], percent_type="ao"
                )

            my_mat.set_density("g/cm3", density_value)

            energy, xs_data_set = openmc.calculate_cexs(
                my_mat, "material", reaction_names
            )

            all_x_y_data = []

            for xs_data, reaction_name in zip(xs_data_set, reaction_names):
                all_x_y_data.append(
                    {
                        "y": xs_data,
                        "x": energy,
                        "type": "scatter",
                        "name": f"MT {reaction_name}"
                        # "marker": {"color": colors},
                    }
                )
            energy_units = "eV"
            xs_units = "Macroscopic cross section $m^-1$"
            return [
                dcc.Graph(
                    config=dict(showSendToCloud=True),
                    figure={
                        "data": all_x_y_data,
                        "layout": {
                            "height": 800,
                            # "width":1600,
                            "margin": {"l": 3, "r": 2, "t": 15, "b": 60},
                            "xaxis": {
                                "title": {"text": f"Energy {energy_units}"},
                                # "type": xaxis_scale,
                                "type": "log",
                                "tickformat": ".1e",
                                "tickangle": 45,
                            },
                            "yaxis": {
                                "automargin": True,
                                # "title": {"text": f"Cross Section {xs_units}"},
                                "title": {"text": xs_units},
                                "type": "log",
                                # "type": yaxis_scale,
                                "tickformat": ".1e",
                            },
                            "showlegend": True,
                            # "height": 250,
                            # "margin": {"t": 10, "l": 10, "r": 10},
                        },
                    },
                )
            ]

        # print('energy',energy)
        # print('xs_data',xs_data)


@app.callback(
    Output("adding-rows-table", "data"),
    Input("editing-rows-button", "n_clicks"),
    State("adding-rows-table", "data"),
    State("element_name", "value"),
    State("fraction_value", "value"),
)
def add_row(n_clicks, rows, element_name, fraction_value):
    if n_clicks > 0:
        if element_name == None:
            print("no elements selected")
            return rows
        if fraction_value == "":
            print("no fraction_value provided")
            return rows
        rows.append({"Elements": element_name, "Fractions": fraction_value})
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


# adapt to plot cross sections on table update
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


# def create_material_plot(materials, reaction):

#     if reaction not in REACTION_MT.keys():
#         print('Reaction not found, only these reactions are accepted', REACTION_MT.keys())
#         return None

#     # fig = create_plotly_figure(y_axis_label='Macroscopic Cross Section (1/cm)')

#     # if isinstance(reaction, str):
#     #     REACTION_NUMBER = dict(zip(REACTION_NAME.values(), REACTION_NAME.keys()))
#     #     MT_number = REACTION_NUMBER[reaction]
#     # else:
#     #     MT_number = reaction
#     #     reaction = REACTION_NAME[MT_number]

#     # if not isinstance(materials, list):
#     #     materials = [materials]

#     # for material in materials:
#         # extracts energy and cross section for the material for the provided MT reaction mumber
#         energy, xs_data = openmc.calculate_cexs(
#             material,
#             'material',
#             [MT_number])

#         # adds the energy dependnat cross sction to the plot
#         fig.add_trace(go.Scatter(
#             x=energy,
#             y=xs_data[0],
#             mode='lines',
#             name=material.name + ' ' + reaction)
#         )

#     return fig


if __name__ == "__main__":
    app.run_server(debug=True)
