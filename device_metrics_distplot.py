import plotly_express as px 
import dash 
from datetime import datetime as dt 
from plotly import tools 
import plotly.graph_objs as go
import plotly.figure_factory as ff

import dash_html_components as html 
import dash_core_components as dcc 
from dash.dependencies import Input, Output 
import os 
import pandas as pd
import numpy as np
# tips = px.data.tips()


# col_options = [dict(label=x, value=x) for x in tips.columns]
# DATA_DIR=r"/home/user/windstream_dtnx/WS_Accuracy/experiments/data//"
DATA_DIR="D:\experiments\data"

PM_NETCOOL_DIR=os.path.join(DATA_DIR,"pm_netcool")
nodenames=['ASBNVACYO3Y.csv', 'ATLNGAMAO4Y.csv', 'CHCGILDTO6Y.csv',
        'CHCGILWUO7Y.csv', 'MIAUFLWSO0Y.csv', 'MIAUFLWSO3P-NE70191.csv',
        'NYCMNYZRO1Y.csv', 'WASHDC12O1Y.csv']
columns=['performance_metrics.ts','BerPostFecAve', 'BerPostFecMax', 'BerPostFecMin', 'BerPreFecAve', 'BerPreFecMax', 'BerPreFecMin', 
 'CWProc', 'CardType', 'ChanOchChromaticDispersionAve', 'ChanOchChromaticDispersionMax', 
 'ChanOchChromaticDispersionMin', 'ChanOchLBCAve', 'ChanOchLBCMax', 'ChanOchLBCMin', 
 'ChanOchOprAve', 'ChanOchOprMax', 'ChanOchOprMin', 'ChanOchOptAve', 'ChanOchOptMax',
  'ChanOchOptMin', 'CrctdBits', 'PhaseCorrectionAve', 'PhaseCorrectionMax', 'PhaseCorrectionMin',
   'PmdAve', 'PmdMax', 'PmdMin', 'Qave', 'Qmax', 'Qmin', 'SoPmdAve', 'SoPmdMax','SoPmdMin']

node_options=[dict(label=x.split('.')[0],value=x)for x in nodenames]
dimensions = ['columns']
collist=['ChanOchOprAve','ChanOchLBCAve','ChanOchChromaticDispersionAve','BerPreFecAve','BerPostFecAve',
         'PhaseCorrectionAve','Qave','PmdAve','SoPmdAve','ChanOchOptAve']#,'performance_metrics.ts']

global df
previousbtn=0
# df=pd.DataFrame()
df=pd.read_pickle(os.path.join(DATA_DIR,"dm.pkl"))
######################  TRansform ####################################################
# print(df.head())
    


####################################################################################

col_options = [dict(label=x, value=x) for x in columns]
devnames=df.columns.tolist()
dev_options=[dict(label=x,value=x)for x in devnames]
app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

initial_devices="7-A-1-L1-1,7-A-1-L1-10,7-B-1-L1-1,7-B-1-L1-10,8-A-1-L1-1,8-A-1-L1-10,8-B-1-L1-1,8-B-1-L1-10,9-A-1-L1-1,9-A-1-L1-10,9-B-3-L1-1,\
9-B-3-L1-10,10-L1-1,10-L1-2,10-L1-10,11-L1-1,11-L1-2,11-L1-10,13-L1-1,13-L1-10".split(',')

print(initial_devices)
print(dimensions)
app.config['suppress_callback_exceptions']=True
app.layout = html.Div(
    [
        html.H1("DTNX-Data Analysis"),
        html.Div(
            [html.Div([html.P(['nodename :',dcc.Dropdown(id='nodename', options=dev_options,value=initial_devices, multi=True)]),
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
            html.Button('Show', id='show-btn', n_clicks_timestamp=0),
            ],style={"width": "25%", "float": "left"},
        ),
        
        html.Div(id='nodename-output'),
        html.Div(id="graph_output"),
        html.Div(dcc.Graph(id="graph", style={"width": "75%", "height":"120%","display": "inline-block"}),
        style={"height":"120%"}),
    ]
)


# # @app.callback(Output('nodename-output', "children"), [Input("nodename", "value")])
# def get_data(devicename):
#     if not devicename:
#         return pd.DataFrame()
#     if isinstance(devicename,list):
#         device_metric_dict[devicename]
#     # global df
#     dev=df[df['performance_metrics.module'].isin(devicename)]
#     # dev['performance_metrics.module']=dev['performance_metrics.module'].sort_values()
#     dev=dev.sort_values(by='performance_metrics.ts')
#     print(dev.shape)
#     # global df
#     return dev #html.H1(nodename.split('.')[0]+" with rows "+str(df.shape[0]))

@app.callback(Output("graph", "figure"), [Input("nodename", "value"),
                                            Input('my-date-picker-range', 'start_date'),
                                            Input('my-date-picker-range', 'end_date'),
                                            Input('show-btn', "n_clicks_timestamp")]+
                                            [Input(d, "value") for d in dimensions])
def make_figure(nodename,start_date,end_date,showbtn,col):

    # df=get_data(nodename)
    # df=df[(df['performance_metrics.ts']>start_date) & (df['performance_metrics.ts']<end_date)]
    #fig=px.line(df, x=x, y=y, color=color)# marginal_y="violin",
    
    #df.columns=df.columns.str.lower()
    # collist=df.columns[df.columns.str.lower().str.contains(signal_type)]

    print(nodename)
    global previousbtn
        
    print("btn",previousbtn,showbtn)
    if int(previousbtn)<int(showbtn):
        # print(df.loc['performance_metrics.ts'])
        # collist=collist[:5]
        # fig = tools.make_subplots(rows=len(nodename), cols=1, subplot_titles=tuple(col for col in nodename),
        # )
        
        hist_data=[np.nan_to_num(np.array(df.loc[col][node])[-2880:]) for node in nodename]
        print(hist_data)
    
        fig = ff.create_distplot(hist_data, nodename,show_hist=False)
    previousbtn=showbtn
    return fig

app.run_server(debug=True,host="0.0.0.0",port=8051)

# host="10.168.126.39"
# fig.append_trace(trace2, 1, 2)
# fig.append_trace(trace3, 2, 1)
# fig.append_trace(trace4, 2, 2)


# 1-A-1-L1-1,
# 1-A-1-L1-10,
# 1-A-1-L1-2,
# 1-A-1-L1-3,
# 1-A-1-L1-4,
# 1-A-1-L1-5,
# 1-A-1-L1-6,
# 1-A-1-L1-7,
# 1-A-1-L1-8,
# 1-A-1-L1-9,

