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
dimensions = ['columns','signal_type']
collist=['ChanOchOprAve','ChanOchLBCAve','ChanOchChromaticDispersionAve','BerPreFecAve','BerPostFecAve',
         'PhaseCorrectionAve','Qave','PmdAve','SoPmdAve','ChanOchOptAve']#,'performance_metrics.ts']

global df
previousbtn=0
# df=pd.DataFrame()
df=pd.read_pickle(os.path.join(DATA_DIR,"dm.pkl"))
######################  TRansform ####################################################
# print(df.head())
    


####################################################################################

col_options = [dict(label=x, value=x[:-3]) for x in columns]
signal_options=[dict(label=x,value=x) for x in ['Min','Max',"Ave","All3"]]
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
                html.P([d + ":", dcc.Dropdown(id=d, options=options)])
                for d,options in zip(dimensions,[col_options,signal_options])
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

@app.callback(Output("graph_output", "children"), [Input("nodename", "value"),
                                            Input('my-date-picker-range', 'start_date'),
                                            Input('my-date-picker-range', 'end_date'),
                                            Input('show-btn', "n_clicks_timestamp")]+
                                            [Input(d, "value") for d in dimensions])
def make_figure(nodename,start_date,end_date,showbtn,col,signal_type):

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
        # fig = tools.make_subplots(rows=len(nodename),30), cols=1, subplot_titles=tuple(col for col in nodename),
        # )
        

            
        data=[]
        for node_no,node in enumerate(nodename):
            ts=sorted(df.loc['performance_metrics.ts'][node])
            # data.append({'x':ts,'y':df.loc[col+signal_type][node],'type': 'line', 'name': col+signal_type})
            trace1 = go.Histogram(
                x=df.loc[col+signal_type][node],
                opacity=0.75
            )            
            data.append(trace1)
        figure=dcc.Graph(figure={
        'data':data,
        'layout':dict(
        title=col+signal_type,
    )
    },style={"width": "75%", "height":"120%","display": "inline-block"})

    

        #     figure=dcc.Graph(figure={
        #         'data': [
        #             {'x': df['performance_metrics.ts'], 'y': df[col.lower()], 'type': 'line', 'name': col},
        #             {'x': df['performance_metrics.ts'], 'y': df[col.lower().replace("ave","min")], 
        #             'type': 'line', 'name': col.replace("Ave","Min")},
        #             {'x': df['performance_metrics.ts'], 'y': df[col.lower().replace("ave","max")], 
        #             'type': 'line', 'name': col.replace("Ave","Max")},
                    
        #         ],
        #         'layout': {
        #             'title': col,
        #              'template':'ggplot2',
        #         }
        #     },style={"width": "75%", "height":"120%","display": "inline-block"})

        #     fig.append(figure)
        # # trace1 = go.Scatter(x=df['performance_metrics.ts'], y=df[col])
    # trace2 = go.Scatter(x=[20, 30, 40], y=[50, 60, 70])
    # trace3 = go.Scatter(x=[300, 400, 500], y=[600, 700, 800])
    # trace4 = go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000])
            # data=[go.Scatter(x=df['performance_metrics.ts'], y=df[col],name=col),
            #     go.Scatter(x=df['performance_metrics.ts'], y=df[col]+1,name=col)]
            # fig.append_trace(go.Figure(data,layout=go.Layout(title=col)),col_no+1,1)
        #     fig.append_trace(go.Scatter(x=sorted(df.loc['performance_metrics.ts'][node]),
        #             y=df.loc[col][node],name=col), node_no+1,1 )
        #     # fig['layout']['yaxis{}'.format(col_no+1)].update(dict(title='{}'.format(col)))
        
        # fig['layout']['xaxis1'].update(title='xaxis 1 title')
        # fig['layout'].update(height=300*max(len(nodename),1), width=1000,showlegend=False,
        #             title='Device-{} visualization'.format(col))
        # # fig['layout'].update( title='Subplots with Shared X-Axes')

        
            #marginal_x="box")

        # fig=px.histogram(s
        #     df,
        #     x=x,
        #     y=y,
        #     color=color,
        #     facet_col=facet_col,
        #     facet_row=facet_row,
        #     height=700,
            
        # )
        # fig.layout.template='ggplot2'
    previousbtn=showbtn
    return figure

app.run_server(debug=True,host="0.0.0.0",port=8051)

# host="10.168.126.39"
# fig.append_trace(trace2, 1, 2)
# fig.append_trace(trace3, 2, 1)
# fig.append_trace(trace4, 2, 2)

device_groups={"1-A-1":"1-A-1-L1-1,\
1-A-1-L1-10,\
1-A-1-L1-2,\
1-A-1-L1-3,\
1-A-1-L1-4,\
1-A-1-L1-5,\
1-A-1-L1-6,\
1-A-1-L1-7,\
1-A-1-L1-8,\
1-A-1-L1-9".split(','),
"1-A-3":"1-A-3-L1-1,\
1-A-3-L1-10,\
1-A-3-L1-2,\
1-A-3-L1-3,\
1-A-3-L1-4,\
1-A-3-L1-5,\
1-A-3-L1-6,\
1-A-3-L1-7,\
1-A-3-L1-8,\
1-A-3-L1-9".split(","),
"1-A-5":"1-A-5-L1-1,\
1-A-5-L1-10,\
1-A-5-L1-2,\
1-A-5-L1-3,\
1-A-5-L1-4,\
1-A-5-L1-5,\
1-A-5-L1-6,\
1-A-5-L1-7,\
1-A-5-L1-8,\
1-A-5-L1-9".split(","),
"1-B-1":"1-B-1-L1-1,\
1-B-1-L1-10,\
1-B-1-L1-2,\
1-B-1-L1-3,\
1-B-1-L1-4,\
1-B-1-L1-5,\
1-B-1-L1-6,\
1-B-1-L1-7,\
1-B-1-L1-8,\
1-B-1-L1-9".split(","),
"1-B-5":"1-B-5-L1-1,\
1-B-5-L1-10,\
1-B-5-L1-2,\
1-B-5-L1-3,\
1-B-5-L1-4,\
1-B-5-L1-5,\
1-B-5-L1-6,\
1-B-5-L1-7,\
1-B-5-L1-8,\
1-B-5-L1-9".split(","),
"10-L1":"10-L1-1,\
10-L1-10,\
10-L1-2,\
10-L1-3,\
10-L1-4,\
10-L1-5,\
10-L1-6,\
10-L1-7,\
10-L1-8,\
10-L1-9".split(","),
"11-L1":"11-L1-1,\
11-L1-10,\
11-L1-2,\
11-L1-3,\
11-L1-4,\
11-L1-5,\
11-L1-6,\
11-L1-7,\
11-L1-8,\
11-L1-9".split(","),
"13-L1":"13-L1-1,\
13-L1-10,\
13-L1-2,\
13-L1-3,\
13-L1-4,\
13-L1-5,\
13-L1-6,\
13-L1-7,\
13-L1-8,\
13-L1-9".split(","),
"7-A-1":"7-A-1-L1-1,\
7-A-1-L1-10,\
7-A-1-L1-2,\
7-A-1-L1-3,\
7-A-1-L1-4,\
7-A-1-L1-5,\
7-A-1-L1-6,\
7-A-1-L1-7,\
7-A-1-L1-8,\
7-A-1-L1-9".split(","),
"7-A-3":"7-A-3-L1-1,\
7-A-3-L1-10,\
7-A-3-L1-2,\
7-A-3-L1-3,\
7-A-3-L1-4,\
7-A-3-L1-5,\
7-A-3-L1-6,\
7-A-3-L1-7,\
7-A-3-L1-8,\
7-A-3-L1-9".split(","),
"7-B-1":"7-B-1-L1-1,\
7-B-1-L1-10,\
7-B-1-L1-2,\
7-B-1-L1-3,\
7-B-1-L1-4,\
7-B-1-L1-5,\
7-B-1-L1-6,\
7-B-1-L1-7,\
7-B-1-L1-8,\
7-B-1-L1-9".split(","),
"7-B-3":"7-B-3-L1-1,\
7-B-3-L1-10,\
7-B-3-L1-2,\
7-B-3-L1-3,\
7-B-3-L1-4,\
7-B-3-L1-5,\
7-B-3-L1-6,\
7-B-3-L1-7,\
7-B-3-L1-8,\
7-B-3-L1-9".split(","),
"7-B-4":"7-B-4-L1-1,\
7-B-4-L1-10,\
7-B-4-L1-2,\
7-B-4-L1-3,\
7-B-4-L1-4,\
7-B-4-L1-5,\
7-B-4-L1-6,\
7-B-4-L1-7,\
7-B-4-L1-8,\
7-B-4-L1-9".split(","),
"8-A-1":"8-A-1-L1-1,\
8-A-1-L1-10,\
8-A-1-L1-2,\
8-A-1-L1-3,\
8-A-1-L1-4,\
8-A-1-L1-5,\
8-A-1-L1-6,\
8-A-1-L1-7,\
8-A-1-L1-8,\
8-A-1-L1-9".split(","),
"8-A-3":"8-A-3-L1-1,\
8-A-3-L1-10,\
8-A-3-L1-2,\
8-A-3-L1-3,\
8-A-3-L1-4,\
8-A-3-L1-5,\
8-A-3-L1-6,\
8-A-3-L1-7,\
8-A-3-L1-8,\
8-A-3-L1-9".split(","),
"8-A-5":"8-A-5-L1-1,\
8-A-5-L1-10,\
8-A-5-L1-2,\
8-A-5-L1-3,\
8-A-5-L1-4,\
8-A-5-L1-5,\
8-A-5-L1-6,\
8-A-5-L1-7,\
8-A-5-L1-8,\
8-A-5-L1-9".split(","),
"8-B-1":"8-B-1-L1-1,\
8-B-1-L1-10,\
8-B-1-L1-2,\
8-B-1-L1-3,\
8-B-1-L1-4,\
8-B-1-L1-5,\
8-B-1-L1-6,\
8-B-1-L1-7,\
8-B-1-L1-8,\
8-B-1-L1-9".split(","),
"8-B-3":"8-B-3-L1-1,\
8-B-3-L1-10,\
8-B-3-L1-2,\
8-B-3-L1-3,\
8-B-3-L1-4,\
8-B-3-L1-5,\
8-B-3-L1-6,\
8-B-3-L1-7,\
8-B-3-L1-8,\
8-B-3-L1-9".split(","),
"8-B-5":"8-B-5-L1-1,\
8-B-5-L1-10,\
8-B-5-L1-2,\
8-B-5-L1-3,\
8-B-5-L1-4,\
8-B-5-L1-5,\
8-B-5-L1-6,\
8-B-5-L1-7,\
8-B-5-L1-8,\
8-B-5-L1-9".split(","),
"9-A-1":"9-A-1-L1-1,\
9-A-1-L1-10,\
9-A-1-L1-2,\
9-A-1-L1-3,\
9-A-1-L1-4,\
9-A-1-L1-5,\
9-A-1-L1-6,\
9-A-1-L1-7,\
9-A-1-L1-8,\
9-A-1-L1-9".split(","),
"9-A-3":"9-A-3-L1-1,\
9-A-3-L1-10,\
9-A-3-L1-2,\
9-A-3-L1-3,\
9-A-3-L1-4,\
9-A-3-L1-5,\
9-A-3-L1-6,\
9-A-3-L1-7,\
9-A-3-L1-8,\
9-A-3-L1-9".split(","),
"9-A-5":"9-A-5-L1-1,\
9-A-5-L1-10,\
9-A-5-L1-2,\
9-A-5-L1-3,\
9-A-5-L1-4,\
9-A-5-L1-5,\
9-A-5-L1-6,\
9-A-5-L1-7,\
9-A-5-L1-8,\
9-A-5-L1-9".split(","),
"9-B-1":"9-B-1-L1-1,\
9-B-1-L1-10,\
9-B-1-L1-2,\
9-B-1-L1-3,\
9-B-1-L1-4,\
9-B-1-L1-5,\
9-B-1-L1-6,\
9-B-1-L1-7,\
9-B-1-L1-8,\
9-B-1-L1-9".split(","),
"9-B-3":"9-B-3-L1-1,\
9-B-3-L1-10,\
9-B-3-L1-2,\
9-B-3-L1-3,\
9-B-3-L1-4,\
9-B-3-L1-5,\
9-B-3-L1-6,\
9-B-3-L1-7,\
9-B-3-L1-8,\
9-B-3-L1-9".split(","),
"9-B-5":"9-B-5-L1-1,\
9-B-5-L1-10,\
9-B-5-L1-2,\
9-B-5-L1-3,\
9-B-5-L1-4,\
9-B-5-L1-5,\
9-B-5-L1-6,\
9-B-5-L1-7,\
9-B-5-L1-8,\
9-B-5-L1-9​".split(",")
}