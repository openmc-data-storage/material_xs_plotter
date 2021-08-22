
from json import dumps, load
from dash_table import DataTable
import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from openmc import Material, calculate_cexs
from header_and_footer import header, footer
from reactions import reaction_names, ATOMIC_SYMBOL, convert_strings_to_numbers, zaid_to_isotope


downloaded_data = []
mcnp_downloaded_data = []

with open('options.json') as json_file:
    element_names = load(json_file)

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
            "name": "keywords",
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
        {
            "name": "charset",
            "content": "UTF-8"
        }
    ],
)
app.title = "XSPlot \U0001f4c9 neutron cross section plotter \U0001f4c8"
app.description = "Plot neutron cross sections. Nuclear data from the TENDL library."
app.config['suppress_callback_exceptions'] = True

server = app.server

app.layout = html.Div(header + [
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='One element/isotope at a time', children= [
            html.Div(
                [
                html.Div([
                    html.H3(
                        [
                            "First select an element or isotope \U0001f449 then specficy a fraction \U0001f449 then add the element / isotope to the material table" 
                        ],
                        style={'text-align': 'center'}
                    ),
                    html.H3(
                        [
                            "Continue adding elements / isotopes to the table to build up a material  \U0000267b"
                        ],
                        style={'text-align': 'center'}
                    ),
                    html.H3(
                        [
                            'Specify the material density \U0001f449 then selection reactions of interest ',  html.A("[reaction descriptions \U0001f517]", href="https://t2.lanl.gov/nis/endf/mts.html")
                        ],
                        style={'text-align': 'center'}
                    ),
                    html.H3(
                        [
                            '\U0001f4c8 The plot should update automatically \U0001f389'
                        ],
                        style={'text-align': 'center'}
                    ),
                    ],
                ),
                html.Br(),
                html.Table(
                    [
                        html.Tr(
                            [
                                html.Th(
                                    dcc.Dropdown(
                                        options=element_names,
                                        placeholder="Select an element / isotope ...",
                                        style={"width": 250, "display": "inline-block"},
                                        id="element_name",
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
                                        # max=1,  # users might want to user percents or ratios
                                        step=0.01,
                                    ),
                                ),
                                html.Th(
                                    html.Button(
                                        "Add Element / Isotope",
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

                html.Br(),
                dash_table.DataTable(
                    id="adding-rows-table",
                    columns=[
                        {
                            "name": "Elements / Isotopes",
                            "id": "Elements",
                        },
                        {
                            "name": "Fractions",
                            "id": "Fractions",
                        },
                    ],
                    data=[],
                    editable=False,
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
                                        options=reaction_names,
                                        placeholder="Select reaction(s) to plot",
                                        style={"width": 400, "display": "inline-block"},
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
                                html.Button(
                                    "Download Plotted Data",
                                    title="Download a text file of the data in JSON format",
                                    id="download_button",
                                )
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
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div(id="graph_container")
            ),
            dcc.Download(id="download-text"),
        ]+footer),
        dcc.Tab(label='From MCNP material card', value='tab-2'),
    ]),
    html.Div(id='tab-2-content'),
    dcc.Download(id="download-text-mcnp"),
])


@app.callback(Output('tab-2-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-2':
        return html.Div([
            html.Div([
                html.H3(
                    [
                        " \U00002702 Copy a material card in MCNP format" 
                    ],
                    style={'text-align': 'center'}
                ),
                html.H3(
                    [
                        "\U0001f4cb Paste the text into the input box bellow"
                    ],
                    style={'text-align': 'center'}
                ),
                html.H3(
                    [
                        'Finally specify the material density \U0001f449 then selection reactions of interest ',  html.A("[reaction descriptions \U0001f517]", href="https://t2.lanl.gov/nis/endf/mts.html")
                    ],
                    style={'text-align': 'center'}
                ),
                html.H3(
                    [
                        '\U0001f4c8 The plot should update automatically \U0001f389'
                    ],
                    style={'text-align': 'center'}
                ),
                html.H3(
                    [
                    html.Label("\U0000269b If you make MCNP materials then you might be interested in the "),
                    html.A("neutronics material maker", href="https://docs.openmc.org/en/stable/"),
                    html.Label(" Python \U0001f40d package"),
                    ],
                    style={'text-align': 'center'}
                ),
                ],
            ),
            html.Br(),
            html.Div(
                [
                html.Table(
                    [
                        html.Tr(
                            [
                                html.Th(
                                    dcc.Textarea(
                                        title='Enter the material card in MCNP format here',
                                        id="mcnp_input_text",
                                        placeholder=(
                                            "Copy and paste your MCNP card here \n"
                                            "\n"
                                            "For exmple ...\n"
                                            "\n"
                                            "M24 001001  6.66562840e-01\n"
                                            "     001002  1.03826667e-04\n"
                                            "     008016  3.32540200e-01\n"
                                            "     008017  1.26333333e-04\n"
                                            "     008018  6.66800000e-04\n"
                                            "\n"
                                        ),
                                        value="",
                                        style={'width': '50%', 'height': 300},
                                    ),
                                ),
                                html.Th(id='processed_input_mcnp',children=[],
                                        style={'width': '50%', 'height': 300}
                                ),
                            ]
                        ),
                    ],
                    style={"width": "100%"},
                ),

                html.Br(),
                html.Br(),
                html.Table(
                    [
                        html.Tr(
                            [
                                html.Th(
                                    dcc.Input(
                                        id="mcnp_density_value",
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
                                        options=reaction_names,
                                        placeholder="Select reaction(s) to plot",
                                        style={"width": 400, "display": "inline-block"},
                                        id="mcnp_reaction_names",
                                        multi=True,
                                    ),
                                ),
                            ]
                        )
                    ],
                    style={"width": "100%"},
                ),
                html.Br(),
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
                                    id="mcnp_xaxis_scale",
                                    labelStyle={"display": "inline-block"},
                                ),
                            ),
                            html.Th(
                                html.Button(
                                    "Download Plotted Data",
                                    title="Download a text file of the data in JSON format",
                                    id="mcnp_download_button",
                                )
                            ),
                            html.Th(
                                dcc.RadioItems(
                                    options=[
                                        {"label": "log Y axis", "value": "log"},
                                        {"label": "linear y axis", "value": "linear"},
                                    ],
                                    value="log",
                                    id="mcnp_yaxis_scale",
                                    labelStyle={"display": "inline-block"},
                                ),
                            )
                        ]
                    )
                ],
                style={"width": "100%"},
            ),
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div(id="mcnp_graph_container")
            ),
        ])



@app.callback([
    dash.dependencies.Output("mcnp_graph_container", "children"),
    dash.dependencies.Output("processed_input_mcnp", "children"),
    ],
    [
        Input("mcnp_reaction_names", "value"),
        Input("mcnp_input_text", "value"),
        Input("mcnp_xaxis_scale", "value"),
        Input("mcnp_yaxis_scale", "value"),
        Input("mcnp_density_value", "value"),
    ],
)

def update_graph_from_mcnp(reaction_names, mcnp_input_text,  xaxis_scale, yaxis_scale, density_value):

    """mcnp_input_text is and mcnp material card like the example below
M24  001001  6.66562840e-01
     001002  1.03826667e-04
     008016  3.32540200e-01
     008017  1.26333333e-04
     008018  6.66800000e-04
    """
    no_density = html.H4(
        'Specify a density in g/cm3',
        style={"text-align": "center", "color": "red"},
    )
    no_mcnp_material_text = html.H4(
        'Specify a material card in MCNP format',
        style={"text-align": "center", "color": "red"},
    )
    no_mcnp_reaction = html.H4(
            'Select a reaction',
            style={"text-align": "center", "color": "red"},
        )


    if mcnp_input_text == None:
        return [], no_mcnp_material_text
    elif  mcnp_input_text == '':
        return [], no_mcnp_material_text
    elif  density_value == None:
        return [], no_density
    elif  density_value == 0:
        return [], no_density
    elif  density_value == '':
        return [], no_density
    elif reaction_names == None:
        return [], no_mcnp_reaction
    elif reaction_names == []:
        return [], no_mcnp_reaction
    
    else:
        try:
            # inputs look ok, but if the processing fails then return error

            file_lines = mcnp_input_text.split('\n')
            tokens = file_lines[0].split()
            # makes the first string without the material number
            material_string = f'{" ".join(tokens[1:])} '

            # removes inline comments
            if "$" in material_string:
                position = material_string.find("$")
                material_string = material_string[0:position]
            current_line_number = 1

            while True:
                # end of the file check
                if current_line_number == len(file_lines):
                    break

                while True:
                    # end of the file check
                    if (current_line_number == len(file_lines)):
                        break
                    line = file_lines[current_line_number]
                    # handels mcnp continue line (which is 5 spaces)
                    if line[:5] == "     ":
                        # removes inline comments
                        if "$" in line:
                            line = line[0:line.find("$")]
                        material_string = material_string + line
                    else: # new cell card
                        break
                    # increment the line number
                    current_line_number = current_line_number + 1
                break

            # removes end of line chars and splits up
            tokens = material_string.replace("\n","").split()
            if len(tokens)%2 != 0:
                html.H4(
                    'The material string contains an odd number of zaids and fractions',
                    style={"text-align": "center", "color": "red"},
                )
            zaid_fraction_dict = []
            while len(tokens) != 0:
                nuclide = tokens[0].split(".")
                isotope_name = zaid_to_isotope(nuclide[0])

                fraction = convert_strings_to_numbers(tokens[1])
                # removes two tokens from list
                tokens.pop(0)
                tokens.pop(0)
                zaid_fraction_dict.append({
                    'element' : isotope_name,
                    'fraction' : fraction
                })

            my_mat = Material(name="my_mat")

            table_contents = []

            for entry in zaid_fraction_dict:
                if entry['fraction'] < 0:
                    fraction_type = 'wo'
                else:
                    fraction_type = 'ao'

                if entry['element'][-1].isdigit():
                    my_mat.add_nuclide(
                        entry['element'], entry['fraction'], percent_type=fraction_type
                    )
                else:
                    my_mat.add_element(
                        entry['element'], entry['fraction'], percent_type=fraction_type
                    )
                table_contents.append(
                    html.Tr(
                            [
                                html.Td(
                                    html.Label(f"{entry['element']}"),
                                    style={"width":"25%","text-align": "left"}
                                ),
                                html.Td(
                                    html.Label(f"{entry['fraction']}"),
                                    style={"width":"25%","text-align": "left"}
                                )
                            ]
                        )
                    )

            my_mat.set_density("g/cm3", density_value)

            if len(my_mat.nuclides) == 0:
                no_elements = html.H4(
                    'No elements or isotopes added',
                    style={"text-align": "center", "color": "red"},
                )
                return [], no_elements
            else:
                energy, xs_data_set = calculate_cexs(
                    my_mat, "material", reaction_names
                )

            global mcnp_downloaded_data

            mcnp_downloaded_data = []

            table_of_processed = [
                html.Table(
                    [
                        html.Tr([
                            html.Th(
                                'Elements / isotopes',
                                style={"width":"25%","text-align": "left"}
                            ),
                            html.Th(
                                'Fraction',
                                style={"width":"25%","text-align": "left"}
                            ),
                            ]
                        ),
                    ]+table_contents,
                    style={"width": "50%"},
                )
            ]


            for xs_data, reaction_name in zip(xs_data_set, reaction_names):
                mcnp_downloaded_data.append(
                    {
                        "y": xs_data,
                        "x": energy,
                        "type": "scatter",
                        "name": f"MT {reaction_name}"
                    }
                )


            energy_units = "eV"
            xs_units = "Macroscopic cross section [1/cm]"
            return [
                dcc.Graph(
                    config=dict(showSendToCloud=True),
                    figure={
                        "data": mcnp_downloaded_data,
                        "layout": {
                            "height": 800,
                            # "width":1600,
                            "margin": {"l": 3, "r": 2, "t": 15, "b": 60},
                            "xaxis": {
                                "title": {"text": f"Energy {energy_units}"},
                                "type": xaxis_scale,
                                "tickformat": ".1e",
                                "tickangle": 45,
                            },
                            "yaxis": {
                                "automargin": True,
                                "title": {"text": xs_units},
                                "type": yaxis_scale,
                                "tickformat": ".1e",
                            },
                            "showlegend": True,
                        },
                    },
                )
            ], table_of_processed

        except:
            return  [], html.H4(
                'There was an error processing the MCNP material format',
                style={"text-align": "center", "color": "red"},
            )


def make_download_dict(data):
    plotting_data = []
    for entry in data:
        plotting_data.append(
            {
                'energy (eV)':list(entry['x']),
                'macroscopic cross section (1/cm)':list(entry['y']),
                'reaction':entry['name'],
            }
        )
    return dict(
        content=dumps(plotting_data, indent=2),
        filename="xsplot_download.json",
    )

# uses a trigger to identify the callback and if the button is used then jsonifys the selected data
@app.callback(
    Output("download-text", "data"),
    [
        Input("download_button", "n_clicks"),
    ],
)
def clicked_download(n_clicks):
    trigger_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "download_button":
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate
        else:
            global downloaded_data
            if len(downloaded_data) > 0:
                download_dict = make_download_dict(downloaded_data)
                return download_dict

# uses a trigger to identify the callback and if the button is used then jsonifys the selected data
@app.callback(
    Output("download-text-mcnp", "data"),
    [
        Input("mcnp_download_button", "n_clicks"),
    ],
)
def clicked_mcnp_download(n_clicks):
    trigger_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "mcnp_download_button":
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate
        else:
            global mcnp_downloaded_data
            if len(mcnp_downloaded_data) > 0:
                download_dict = make_download_dict(mcnp_downloaded_data)
                return download_dict


@app.callback(
    dash.dependencies.Output("graph_container", "children"),
    [
        Input("reaction_names", "value"),
        Input("adding-rows-table", "data"),
        Input("density_value", "value"),
        Input("fraction_type", "value"),
        Input("xaxis_scale", "value"),
        Input("yaxis_scale", "value"),
    ],
)
def update_output(reaction_names, rows, density_value, fraction_type,  xaxis_scale, yaxis_scale):

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

            my_mat = Material(name="my_mat")

            for entry in rows:
                if entry["Elements"][-1].isdigit():
                    my_mat.add_nuclide(
                        entry["Elements"], entry["Fractions"], percent_type=fraction_type
                    )
                else:
                    my_mat.add_element(
                        entry["Elements"], entry["Fractions"], percent_type=fraction_type
                    )

            my_mat.set_density("g/cm3", density_value)
            if len(my_mat.nuclides) == 0:
                no_elements = html.H4(
                    'No elements or isotopes added',
                    style={"text-align": "center", "color": "red"},
                )
                return no_elements
            else:
                energy, xs_data_set = calculate_cexs(
                    my_mat, "material", reaction_names
                )

                global downloaded_data

                downloaded_data = []

                for xs_data, reaction_name in zip(xs_data_set, reaction_names):
                    downloaded_data.append(
                        {
                            "y": xs_data,
                            "x": energy,
                            "type": "scatter",
                            "name": f"MT {reaction_name}"
                        }
                    )
                energy_units = "eV"
                xs_units = "Macroscopic cross section [1/cm]"
                return [
                    dcc.Graph(
                        config=dict(showSendToCloud=True),
                        figure={
                            "data": downloaded_data,
                            "layout": {
                                "height": 800,
                                # "width":1600,
                                "margin": {"l": 3, "r": 2, "t": 15, "b": 60},
                                "xaxis": {
                                    "title": {"text": f"Energy {energy_units}"},
                                    "type": xaxis_scale,
                                    "tickformat": ".1e",
                                    "tickangle": 45,
                                },
                                "yaxis": {
                                    "automargin": True,
                                    "title": {"text": xs_units},
                                    "type": yaxis_scale,
                                    "tickformat": ".1e",
                                },
                                "showlegend": True,
                            },
                        },
                    )
                ]
    else:
        raise dash.exceptions.PreventUpdate


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
            # no element selected
            return rows
        if fraction_value == "" or fraction_value == 0:
            return rows
        rows.append({"Elements": element_name, "Fractions": fraction_value})
    return rows


if __name__ == "__main__":
    app.run_server(debug=True)
