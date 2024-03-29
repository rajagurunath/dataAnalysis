import plotly_express as px
import dash
from datetime import datetime as dt
from plotly import tools
import plotly.graph_objs as go
import json
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import os
import pandas as pd
from datetime import datetime,timedelta
# tips = px.data.tips()


"""

['Unnamed: 0', 'performance_metrics.nodename', 'performance_metrics.module', 'performance_metrics.ts',
 'BerPostFecAve', 'BerPostFecMax', 'BerPostFecMin', 'BerPreFecAve', 'BerPreFecMax', 'BerPreFecMin', 
 'CWProc', 'CardType', 'ChanOchChromaticDispersionAve', 'ChanOchChromaticDispersionMax', 
 'ChanOchChromaticDispersionMin', 'ChanOchLBCAve', 'ChanOchLBCMax', 'ChanOchLBCMin', 
 'ChanOchOprAve', 'ChanOchOprMax', 'ChanOchOprMin', 'ChanOchOptAve', 'ChanOchOptMax',
  'ChanOchOptMin', 'CrctdBits', 'PhaseCorrectionAve', 'PhaseCorrectionMax', 'PhaseCorrectionMin',
   'PmdAve', 'PmdMax', 'PmdMin', 'Qave', 'Qmax', 'Qmin', 'SoPmdAve', 'SoPmdMax',
    'SoPmdMin', 'UnCrctblCW']
"""
# col_options = [dict(label=x, value=x) for x in tips.columns]
DATA_DIR=r"D:\experiments\data\Research_data\ochctp\\"
PM_NETCOOL_DIR=os.path.join(DATA_DIR,"pm_netcool")
nodenames=['ASBNVACYO3Y.csv', 'ATLNGAMAO4Y.csv', 'CHCGILDTO6Y.csv',
        'CHCGILWUO7Y.csv', 'MIAUFLWSO0Y.csv', 'MIAUFLWSO3P-NE70191.csv',
        'NYCMNYZRO1Y.csv', 'WASHDC12O1Y.csv']

node_options=[dict(label=x.split('.')[0],value=x)for x in nodenames]
dimensions = ["signal_type"]
collist=['ChanOchOprAve','ChanOchLBCAve','ChanOchChromaticDispersionAve','BerPreFecAve','BerPostFecAve',
         'PhaseCorrectionAve','Qave','PmdAve','SoPmdAve','ChanOchOptAve']#,'performance_metrics.ts']

global df
df=pd.DataFrame()
df=pd.read_feather(os.path.join(DATA_DIR,"pivoted_ochctp.feather"))
print(df.shape)
netcoolDF=pd.read_feather(r"D:\experiments\data\netcool_with_devices.feather")
# print(netcoolDF['device'].value_counts())
col_options = [dict(label=x, value=x.lower()) for x in ["Ave","Min","Max"]]
devnames=set(df['performance_metrics.module'].tolist())
# devnames=set(netcoolDF['device'].tolist())
dev_options=[dict(label=x.split('.')[0],value=x)for x in devnames]
app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)


print(dimensions)
app.config['suppress_callback_exceptions']=False
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
            # html.Div([
            #     html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
            #     for d in dimensions
            # ]),
            ],style={"width": "25%", "float": "left"},
        ),
        html.Div(id='nodename-output'),
        html.Div(id="netcool_output"),
        # html.Pre(id='click-data'),#, style=styles['pre']),

        html.Div(id="graph_output"),
        html.Div(dcc.Graph(id='netcool_fig', style={"width": "75%", "height":"120%","display": "inline-block"}),
        style={"height":"120%"}),
    ]
)

def get_netcool(devicename):
    if not devicename:
        return pd.DataFrame()
    
    # global df
    print(devicename)
    net=netcoolDF[netcoolDF['device'].str.contains(devicename)]
    if net.empty:
        return 
    # dev['performance_metrics.module']=dev['performance_metrics.module'].sort_values()
    net=net.sort_values(by='FIRSTOCCURRENCE')
    print("net filtered:",net.shape)
    print("after duplicate removal :",net.drop_duplicates().shape)
    # global df
    return net #html.H1(nodename.split('.')[0]+" with rows "+str(df.shape[0]))


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

@app.callback(Output("netcool_output", "children"), [Input("nodename", "value"),
                                            Input('my-date-picker-range', 'start_date'),
                                            Input('my-date-picker-range', 'end_date')])

def make_netcool_figure(nodename,start_date,end_date):
    netcooldF=get_netcool(nodename)
    print("netcool: ",netcooldF.shape)
    netcooldF=netcooldF[(netcooldF['FIRSTOCCURRENCE']>start_date) &(netcooldF['FIRSTOCCURRENCE']<end_date)]
    
    figure=dcc.Graph(id='netcool_fig',figure={
            'data': [
                {'x': netcooldF['FIRSTOCCURRENCE'], 'y': netcooldF["SEVERITY"], 
                'mode': 'markers', 'name': "netcool","text":netcooldF['SUMMARY'],
                'marker':{'color':netcooldF['SUMMARY']},}
                
                
            ],
            'layout': {
                'title': "Netcool Alarms for {}".format(nodename),
                 'template':'ggplot2',
            }
        },style={"width": "75%", "height":"100%","display": "inline-block"})
    return [figure]

# @app.callback(
#     Output('click-data', 'children'),
#     [Input('netcool_fig', 'clickData')])
# def display_click_data(clickData):
#     """
#     {
#   "points": [
#     {
#       "curveNumber": 0,
#       "pointNumber": 0,
#       "pointIndex": 0,
#       "x": "2019-01-30 12:32:38",
#       "y": 0,
#       "text": "Loss Of Signal  ( Optical Channel Connection Termination Point: 13-L1-10 ): WINTERSTATE DEVICE"
#     }
#   ]
# }

#     """

#     return json.dumps(clickData, indent=2)


@app.callback(Output("graph_output", "children"), [Input("nodename", "value"),
                                            Input('my-date-picker-range', 'start_date'),
                                            Input('my-date-picker-range', 'end_date'),
                                            Input('netcool_fig', 'clickData')])
def make_figure(nodename,start_date,end_date,clickedData=None):
    df=get_data(nodename)
        
    df=df[(df['performance_metrics.ts']>start_date) & (df['performance_metrics.ts']<end_date)]
    #fig=px.line(df, x=x, y=y, color=color)# marginal_y="violin",
    
    df.columns=df.columns.str.lower()
    # collist=df.columns[df.columns.str.lower().str.contains(signal_type)]
    # fig = tools.make_subplots(rows=len(collist), cols=1, subplot_titles=tuple(col for col in collist),
    # )
    print("test")
    print(clickedData)
    if not clickedData:
        print(clickedData)
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
            },style={"width": "100%", "height":"120%","display": "inline-block"})

            fig.append(figure)
        # trace1 = go.Scatter(x=df['performance_metrics.ts'], y=df[col])
    # trace2 = go.Scatter(x=[20, 30, 40], y=[50, 60, 70])
    # trace3 = go.Scatter(x=[300, 400, 500], y=[600, 700, 800])
    # trace4 = go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000])
            # data=[go.Scatter(x=df['performance_metrics.ts'], y=df[col],name=col),
            #     go.Scatter(x=df['performance_metrics.ts'], y=df[col]+1,name=col)]
            # fig.append_trace(go.Figure(data,layout=go.Layout(title=col)),col_no+1,1)
        #     fig.append_trace(go.Scatter(x=df['performance_metrics.ts'], y=df[col],name=col), col_no+1,1 )
        #     fig['layout']['yaxis{}'.format(col_no+1)].update(dict(title='{}'.format(col)))
        # fig['layout'].update(height=3000, width=1000,showlegend=False,
        #             title='Device-{} visualization'.format(nodename))
        # fig['layout'].update( title='Subplots with Shared X-Axes')

        
            #marginal_x="box")

        # fig=px.histogram(
        #     df,
        #     x=x,
        #     y=y,
        #     color=color,
        #     facet_col=facet_col,
        #     facet_row=facet_row,
        #     height=700,
            
        # )
        # fig.layout.template='ggplot2'
    else:
        alarmts=clickedData["points"][0]["x"]

        starttime=str(datetime.strptime(alarmts,"%Y-%m-%d %H:%M:%S")-timedelta(hours=5))
        endtime=str(datetime.strptime(alarmts,"%Y-%m-%d %H:%M:%S")+timedelta(hours=5))
        fig=[]
        print(alarmts,starttime,endtime)
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
                    'shapes':[
                        {
                            'type':'rect',
                            'x0':starttime,
                            'x1':endtime,
                            'y0':min(df[col.lower().replace("ave","min")].min(),df[col.lower().replace("ave","max")].min(),df[col.lower()].min()),
                            'y1':max(df[col.lower().replace("ave","max")].max(),df[col.lower().replace("ave","min")].max(),df[col.lower()].max()),
                            'fillcolor':'red',
                            'opacity':0.5,
                            'line': {
                            'color': 'rgba(128, 0, 128, 1)',
                                    }
                        }
                    ]
                }
            },style={"width": "100%", "height":"120%","display": "inline-block"})

            fig.append(figure)

    return fig

app.run_server(debug=True,port=8051)


# fig.append_trace(trace2, 1, 2)
# fig.append_trace(trace3, 2, 1)
# fig.append_trace(trace4, 2, 2)
