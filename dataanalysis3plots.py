import plotly_express as px
import dash
from datetime import datetime as dt
from plotly import tools
import plotly.graph_objs as go

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import os
import pandas as pd
# col_options = [dict(label=x, value=x) for x in tips.columns]
DATA_DIR=r"D:\experiments\data\Research_data\ochctp\\"
PM_NETCOOL_DIR=os.path.join(DATA_DIR,"pm_netcool")
nodenames=['ASBNVACYO3Y.csv', 'ATLNGAMAO4Y.csv', 'CHCGILDTO6Y.csv',
        'CHCGILWUO7Y.csv', 'MIAUFLWSO0Y.csv', 'MIAUFLWSO3P-NE70191.csv',
        'NYCMNYZRO1Y.csv', 'WASHDC12O1Y.csv']

node_options=[dict(label=x.split('.')[0],value=x)for x in nodenames]
dimensions = ["x", "color", "signal_type", "facet_row"]
collist=['ChanOchOprAve','ChanOchLBCAve','ChanOchChromaticDispersionAve','BerPreFecAve','BerPostFecAve',
         'PhaseCorrectionAve','Qave','PmdAve','SoPmdAve','ChanOchOptAve']#,'performance_metrics.ts']

df=pd.read_feather(os.path.join(DATA_DIR,"pivoted_ochctp.feather"))
col_options = [dict(label=x, value=x.lower()) for x in ["Ave","Min","Max"]]
devnames=set(df['performance_metrics.module'].tolist())
dev_options=[dict(label=x.split('.')[0],value=x)for x in devnames]
app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)


app.config['suppress_callback_exceptions']=True
app.layout = html.Div(
    [
        html.H1("DTNX-Data Analysis"),
        html.Div(
            [html.Div([html.P(['nodename :',dcc.Dropdown(id='nodename', options=dev_options)]),
            dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt(2018, 5, 1),
            max_date_allowed=dt(2019, 2, 28),
            initial_visible_month=dt(2019, 1, 1),
            end_date=dt(2019, 1, 5)
            )]),
            html.Div([
                html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                for d in dimensions
            ]),
            ],style={"width": "25%", "float": "left"},
        ),
        html.Div(id='nodename-output'),
        html.Div(id="graph_output"),
        html.Div(dcc.Graph(id="graph", style={"width": "75%", "height":"120%","display": "inline-block"}),
        style={"height":"120%"}),
    ]
)


# @app.callback(Output('nodename-output', "children"), [Input("nodename", "value")])
def get_data(devicename):
    if not devicename:
        return pd.DataFrame()
    # global df
    dev=df[df['performance_metrics.module']==devicename]
    # dev['performance_metrics.module']=dev['performance_metrics.module'].sort_values()
    dev=dev.sort_values(by='performance_metrics.ts')
    print(dev.shape)
    # global df
    return dev #html.H1(nodename.split('.')[0]+" with rows "+str(df.shape[0]))

@app.callback(Output("graph_output", "children"), [Input("nodename", "value"),
                                            Input('my-date-picker-range', 'start_date'),
                                            Input('my-date-picker-range', 'end_date')]+
                                            [Input(d, "value") for d in dimensions])
def make_figure(nodename,start_date,end_date,x, color, signal_type, facet_row):
    df=get_data(nodename)
    df=df[(df['performance_metrics.ts']>start_date) & (df['performance_metrics.ts']<end_date)]
    #fig=px.line(df, x=x, y=y, color=color)# marginal_y="violin",
    
    df.columns=df.columns.str.lower()
    # collist=df.columns[df.columns.str.lower().str.contains(signal_type)]
    # fig = tools.make_subplots(rows=len(collist), cols=1, subplot_titles=tuple(col for col in collist),
    # )
    
    fig=[]
    for col_no,col in enumerate(collist):

        figure=dcc.Graph(figure={
            'data': [
                {'x': df['performance_metrics.ts'], 'y': df[col.lower()], 'type': 'line', 'name': col},
                {'x': df['performance_metrics.ts'], 'y': df[col.lower().replace("ave","min")], 
                'type': 'line', 'name': col.replace("Ave","Min")},
                {'x': df['performance_metrics.ts'], 'y': df[col.lower().replace("ave","max")], 
                'type': 'line', 'name': col.replace("Ave","Max")},
                
            ],
            'layout': {
                'title': nodename+": "+col,
                 'template':'ggplot2',
            }
        },style={"width": "75%", "height":"120%","display": "inline-block"})

        fig.append(figure)
    return fig

app.run_server(debug=True,host="10.168.126.47",port=8052)


# fig.append_trace(trace2, 1, 2)
# fig.append_trace(trace3, 2, 1)
# fig.append_trace(trace4, 2, 2)
