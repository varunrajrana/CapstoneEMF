from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

from paramiko import SSHClient, AutoAddPolicy
import os

dataPath=r'C:\Users\varun\Documents\Capstone\Data'
data = pd.read_csv(dataPath+"\\testdata.csv",delimiter = ',',names=["Time","EMF"],skiprows=1)

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=[external_stylesheets])

def show_in_native_window(app: Dash) -> None:
    """
    Modify the application to launch a minimal browser window, and shut down when this window is closed,
    to give the look & feel of a native application.
    """
    from threading import Timer
    import flask
    import native_web_app

    # Add URL that can be used to shut down the Dash application
    @app.server.route('/shutdown', methods=['GET', 'POST'])
    def shutdown():
        func = flask.request.environ.get('werkzeug.server.shutdown')
        if func is not None:
            func()
        return ''

    # Add Javascript that POSTs to the shutdown URL when the window is closed
    shutdown_js = "window.addEventListener('pagehide', () => {navigator.sendBeacon('/shutdown');});"
    app.config.external_scripts.append('data:,' + shutdown_js)

    def open_native_window():
        native_web_app.open('http://127.0.0.1:8050')

    # Open the application in a local window once the Dash server has had some time to start
    Timer(1, open_native_window).start()
    
    # Start the Dash application
    app.run_server()

def ftp():
    wdir=r'C:\Users\varun\Documents\Capstone\Data'
    rdir=r'/home/pi/Data/'

    client = SSHClient()
    #LOAD HOST KEYS
    #client.load_host_keys('~/.ssh/known_hosts')
    client.load_host_keys('C:/Users/varun/.ssh/known_hosts')
    client.load_system_host_keys()

    #Known_host policy
    client.set_missing_host_key_policy(AutoAddPolicy())

    #client.connect('10.1.1.92', username='root', password='password1')
    client.connect('raspberrypi.local', username='pi',password='3953')

    sftp=client.open_sftp()
    remote_dir=sftp.listdir(rdir)

    for index, file in enumerate(remote_dir):
        if not os.path.exists(file):
            file_name=remote_dir[index]
            if not os.path.exists(file):
                print(wdir)
                sftp.get(rdir+file_name,wdir+"\\"+file_name)

    # Close the client itself
    sftp.close()
    client.close()
    return

def demo():
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    app.title = "EMF Analytics"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data["Time"], y = data["EMF"], name="EMF",
                        line_shape="spline"))
    fig.update_layout(hovermode="x",title="EMF (mG)")
    app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="EMF Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the EMF exposure recorded",
                    className="header-description",
                ),
                dbc.Button(
                    "Sync Files", color="primary", id="sync-req", className="me-2 center", n_clicks=0
                ),
                dbc.Toast(
                    "Files have been synced with the EMF meter",
                    id="sync-output",
                    header="Sync Complete",
                    is_open=False,
                    dismissable=True,
                    icon="success",
                    duration=4000,
                    # top: 66 positions the toast below the navbar
                    style={"position": "fixed", "top": 30, "right": 20, "width": 350},
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(figure=fig),
                    className="card",
                )
            ],
            className="wrapper",
        ),
    ]
)
    @app.callback(
        Output("sync-output", "is_open"), [Input("sync-req", "n_clicks")]
    )
    def sync_files(n):
        if n:
            ftp()
            return True
        return False
        

    
    show_in_native_window(app)
    
if __name__ == '__main__':
    demo()