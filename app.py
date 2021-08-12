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


components = [
    html.Title("xsplot.com material cross section plotting"),
    html.Iframe(
        src="https://ghbtns.com/github-btn.html?user=openmc-data-storage&repo=material_xs_plotter&type=star&count=true&size=large",
        width="170",
        height="30",
        title="GitHub",
        style={"border": 0, "scrolling": "0"},
    ),
    html.H1(
        "XSPlot - Neutron cross section plotter for materials",
        # TODO find a nicer font
        # style={'font-family': 'Times New Roman, Times, serif'},
        # style={'font-family': 'Georgia, serif'},
        style={"text-align": "center"},
    ),
    html.Div(
        html.Iframe(
            src="https://www.youtube.com/embed/Rhb0Oqm29B8",
            width="560",
            height="315",
            title="Tutorial video",
            # style={},
            style={"text-align": "center", "border": 0, "scrolling": "0"},
        ),
        style={"text-align": "center"},
    ),
    html.Div(
        html.H3(
            [
                "Build up a collection of elements and fractions into a material. ",
                'Then specify the material density and reactions of interest and click "Update plot" to produce the plot. '
                "MT reaction numbers can be found ", html.A("here", href="https://t2.lanl.gov/nis/endf/mts.html"),
            ]
        ),
        id="heading2",
    ),
    html.Div(
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
                                # max=1,
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
            style_cell={'textAlign': 'center', 'fontSize':16, 'font-family':'sans-serif'},
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
                            dcc.RadioItems(
                                options=[
                                    {"label": "atom percent", "value": "ao"},
                                    {"label": "weight percent", "value": "wo"},
                                ],
                                value="ao",
                                id="fraction_type",
                                labelStyle={"display": "inline-block"},
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
        # html.Div(
        #     [
        #         html.Button(
        #             "Plot material",
        #             id="update_plot",
        #             title="Click to create or refresh the plot",
        #             style={"height": 40, "width":200}
        #         ),
        #     ],
        #     style={"height": 50, "text-align": "center"},
        # ),
        # dcc.Graph(id='graph-container')
        html.Div(id="graph_container"),
    ]
    ),
    html.Br(),
    html.Table(
        [
            html.Tr(
                [
                    html.Th(
                        dcc.RadioItems(
                            options=[
                                {"label": "log X axis", "value": "log"},
                                {"label": "linear X axis", "value": "linear"},
                            ],
                            value="log",
                            id="xaxis_scale",
                            labelStyle={"display": "inline-block"},
                        ),
                    ),
                    html.Th(
                        # html.Button(
                        #     "Download Plotted Data",
                        #     title="Download a text file of the data in JSON format",
                        #     id="btn_download2",
                        # )
                    ),
                    html.Th(
                        dcc.RadioItems(
                            options=[
                                {"label": "log Y axis", "value": "log"},
                                {"label": "linear y axis", "value": "linear"},
                            ],
                            value="log",
                            id="yaxis_scale",
                            labelStyle={"display": "inline-block"},
                        ),
                    )
                ]
            )
        ],
        style={"width": "100%"},
    ),

    html.Br(),
    html.Br(),
    html.Div(
        [
            html.Label("XSPlot is an open-source project powered by "),
            html.A("OpenMC", href="https://docs.openmc.org/en/stable/"),
            html.Label(", "),
            html.A(" Plotly", href="https://plotly.com/"),
            html.Label(", "),
            html.A(" Dash", href="https://dash.plotly.com/"),
            html.Label(", "),
            html.A(" Dash datatable", href="https://dash.plotly.com/datatable"),
            html.Label(", "),
            html.A(" Flask", href="https://flask.palletsprojects.com/en/2.0.x/"),
            html.Label(", "),
            html.A(" Gunicorn", href="https://gunicorn.org/"),
            html.Label(", "),
            html.A(" Docker", href="https://www.docker.com"),
            html.Label(", "),
            html.A(" GCloud", href="https://cloud.google.com"),
            html.Label(", "),
            html.A(" Python", href="https://www.python.org/"),
            html.Label(" with the source code available on "),
            html.A(" GitHub", href="https://github.com/openmc-data-storage"),
        ],
        style={"text-align": "center"},
    ),
    html.Br(),
    html.Div(
        [
            html.Label("Links to alternative cross section plotting websites: "),
            html.A("NEA JANIS", href="https://www.oecd-nea.org/jcms/pl_39910/janis"),
            html.Label(", "),
            html.A(" IAEA ENDF", href="https://www-nds.iaea.org/exfor/endf.htm"),
            html.Label(", "),
            html.A(" NNDC Sigma", href="https://www.nndc.bnl.gov/sigma/"),
            html.Label(", "),
            html.A(
                " Nuclear Data Center JAEA",
                href="https://wwwndc.jaea.go.jp/ENDF_Graph/",
            ),
            html.Label(", "),
            html.A("T2 LANL", href="https://t2.lanl.gov/nis/data/endf/index.html"),
            html.Label(", "),
            html.A("Nuclear Data Center KAERI", href="https://atom.kaeri.re.kr"),
        ],
        style={"text-align": "center"},
    ),
]

app.layout = html.Div(components)

@app.callback(
    dash.dependencies.Output("graph_container", "children"),
    [
        # Input("update_plot", "n_clicks"),
        Input("reaction_names", "value"),
        Input("adding-rows-table", "data"),
        Input("density_value", "value"),
        Input("fraction_type", "value"),
        Input("xaxis_scale", "value"),
        Input("yaxis_scale", "value"),
        
        # Input("adding-rows-table", "rows"),
    ],
    # [dash.dependencies.Input('update_plot', 'n_clicks')],
    # [dash.dependencies.State('input-on-submit', 'value')]
)
# def update_output(n_clicks, reaction_names, rows, density_value, fraction_type,  xaxis_scale, yaxis_scale):
def update_output(reaction_names, rows, density_value, fraction_type,  xaxis_scale, yaxis_scale):
    # if n_clicks is None:
    #     raise dash.exceptions.PreventUpdate
    # if n_clicks > 0:
        # trigger_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

        # if trigger_id == "update_plot":

    if (reaction_names != None) and (rows != None) and (density_value != None):
        
        no_density = html.H4(
            'Specify a density in g/cm3',
            style={"text-align": "center", "color": "red"},
        )
        if  density_value == None:
            return no_density
        elif  density_value == 0:
            return no_density
        elif  density_value == '':
            return no_density
        else:

            print("reaction_names", reaction_names)
            print("rows", rows)
            print("density_value", density_value)

            my_mat = openmc.Material(name="my_mat")

            for entry in rows:
                # for key, values in entry.items():
                print(entry)
                # print('key',key, 'values',values)

                my_mat.add_element(
                    entry["Elements"], entry["Fractions"], percent_type=fraction_type
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
            xs_units = "Macroscopic cross section [1/cm]"
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
                                "type": xaxis_scale,
                                # "type": "log",
                                "tickformat": ".1e",
                                "tickangle": 45,
                            },
                            "yaxis": {
                                "automargin": True,
                                # "title": {"text": f"Cross Section {xs_units}"},
                                "title": {"text": xs_units},
                                # "type": "log",
                                "type": yaxis_scale,
                                "tickformat": ".1e",
                            },
                            "showlegend": True,
                            # "height": 250,
                            # "margin": {"t": 10, "l": 10, "r": 10},
                        },
                    },
                )
            ]
        # else:
        #     raise dash.exceptions.PreventUpdate
    else:
        raise dash.exceptions.PreventUpdate

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
        if fraction_value == "" or fraction_value == 0:
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
