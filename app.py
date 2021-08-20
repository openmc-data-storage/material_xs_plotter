
from json import dumps, load

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from openmc import Material, calculate_cexs
from header_and_footer import header, footer
from reactions import reaction_names

ATOMIC_SYMBOL = {
    0: 'n', 1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C',
    7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al',
    14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K',
    20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn',
    26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga',
    32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb',
    38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc',
    44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In',
    50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs',
    56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm',
    62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho',
    68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta',
    74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au',
    80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At',
    86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa',
    92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk',
    98: 'Cf', 99: 'Es', 100: 'Fm', 101: 'Md', 102: 'No',
    103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh',
    108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg', 112: 'Cn',
    113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts',
    118: 'Og'
}

def zaid_to_isotope(zaid: str) -> str:
    """converts an isotope into a zaid e.g. 003006 -> Li6"""
    a = str(zaid)[-3:]
    z = str(zaid)[:-3]
    symbol = ATOMIC_SYMBOL[int(z)]
    return symbol + str(int(a))

def convert_strings_to_numbers(input_string: str) -> float:
    """Converts a number represented as a string into a float. Handels special
    case formatting that is used in fotran inputs"""

    processed_string = input_string.split(".")
    if len(processed_string) == 1 : # in case there is no decimal point
        return float(input_string)

    # the string is a normal number
    if any(item in processed_string[1].lower() for item in ["e+","e", "e-"]):
        return float(input_string)

    # the string is a fortran formatted number
    processed_string[1] = processed_string[1].replace("+","e+")
    processed_string[1] = processed_string[1].replace("-","e-")
    combined_string = f"{processed_string[0]}.{processed_string[1]}"

    return float(combined_string)


downloaded_data = []

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


# app.layout = html.Div(components)

app.layout = html.Div(header + [
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='One element/isotope at a time', children= [
            html.Div(
                [
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
                                    id="btn_download2",
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
            html.Div(id="graph_container"),
        ]),
        dcc.Tab(label='From MCNP material card', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content'),
    dcc.Download(id="download-text-index"),
])



@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-2':
        return html.Div([
            html.Div(
                [
                html.Table(
                    [
                        html.Tr(
                            [
                                html.Th(
                                    dcc.Textarea(
                                        id="mcnp_input_text",
                                        placeholder="Copy and paste your MCNP card here",
                                        value="",
                                        # type="number",
                                        style={'width': '100%', 'height': 300},
                                    ),
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
                                    id="mcnp_btn_download2",
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
            html.Div(id="mcnp_graph_container"),
        ])



@app.callback(
    dash.dependencies.Output("mcnp_graph_container", "children"),
    [
        Input("mcnp_reaction_names", "value"),
        Input("mcnp_input_text", "value"),
        Input("mcnp_xaxis_scale", "value"),
        Input("mcnp_yaxis_scale", "value"),
    ],
)

def update_output(reaction_names, mcnp_input_text,  xaxis_scale, yaxis_scale):

    """mcnp_input_text is and mcnp material card like the example below
    M24   001001  6.66562840e-01
            001002  1.03826667e-04
            008016  3.32540200e-01
            008017  1.26333333e-04
            008018  6.66800000e-04
    """

    if (reaction_names != None):
        no_mcnp_material_text = html.H4(
            'Specify a material card in MCNP format',
            style={"text-align": "center", "color": "red"},
        )
        if mcnp_input_text == None:
            return no_mcnp_material_text
        elif  mcnp_input_text == '':
            return no_mcnp_material_text
        else:

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
                print ("The material string contains an odd number of zaids "
                       "and fractions")

            zaid_fraction_dict = {}
            while len(tokens) != 0:
                nuclide = tokens[0].split(".")
                isotope_name = zaid_to_isotope(nuclide[0])

                fraction = convert_strings_to_numbers(tokens[1])
                # removes two tokens from list
                tokens.pop(0)
                tokens.pop(0)
                if isotope_name not in zaid_fraction_dict.keys():
                    zaid_fraction_dict[isotope_name] = fraction
                else:
                    zaid_fraction_dict[isotope_name] = zaid_fraction_dict[isotope_name] + fraction

            print(zaid_fraction_dict)
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








# uses a trigger to identify the callback and if the button is used then jsonifys the selected data
@app.callback(
    Output("download-text-index", "data"),
    [
        Input("btn_download2", "n_clicks"),
        # Input("datatable-interactivity", "selected_rows"),
    ],
)
def func2(n_clicks):
    trigger_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    global downloaded_data

    if trigger_id == "btn_download2":
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate
        else:
            if len(downloaded_data) > 0:

                plotting_data = []
                for entry in downloaded_data:
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
