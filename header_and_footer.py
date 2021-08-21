import dash_html_components as html

header = [
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
]

footer = [
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
            html.A(" IAEA Libraries", href="https://nds.iaea.org/dataexplorer"),
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