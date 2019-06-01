import plotly_express as px
import dash
from datetime import datetime as dt

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import os
import pandas as pd
tips = px.data.tips()
# col_options = [dict(label=x, value=x) for x in tips.columns]
DATA_DIR=r"D:\experiments\data\\"

NETCOOL_DIR=os.path.join(DATA_DIR,"Netcool")
nodenames=['ASBNVACYO3Y.csv', 'ATLNGAMAO4Y.csv', 'CHCGILDTO6Y.csv',
        'CHCGILWUO7Y.csv', 'MIAUFLWSO0Y.csv', 'MIAUFLWSO3P-NE70191.csv',
        'NYCMNYZRO1Y.csv', 'WASHDC12O1Y.csv']
node_options=[dict(label=x.split('.')[0],value=x)for x in nodenames]
dimensions = ["x", "y", "color", "facet_col", "facet_row"]
collist=['ChanOchOprAve','ChanOchLBCAve','ChanOchChromaticDispersionAve','BerPreFecAve','BerPostFecAve',
         'PhaseCorrectionAve','Qave','PmdAve','SoPmdAve','ChanOchOptAve','device','ts','SHORT_SUMMARY']

collist=['MANAGER',
 'AGENT',   
 'ALERTGROUP',
 'ALERTKEY',
 'SEVERITY',
 'SUMMARY',
 'STATECHANGE',
 'FIRSTOCCURRENCE',
 'LASTOCCURRENCE',
 'LASTMODIFIED',
 'POLL',
 'TYPE',
 'TALLY',
 'CLASS',
 'GRADE',
 'LOCATION',
 'OWNERUID',
 'OWNERGID',
 'ACKNOWLEDGED',
 'FLASH',
 'EVENTID',
 'PROCESSREQ',
 'SUPPRESSESCL',
 'CUSTOMER',
 'SERVICE',
 'PHYSICALSLOT',
 'PHYSICALPORT',
 'PHYSICALCARD',
 'TASKLIST',
 'NMOSSERIAL',
 'NMOSOBJINST',
 'NMOSCAUSETYPE',
 'LOCALNODEALIAS',
 'LOCALPRIOBJ',
 'LOCALSECOBJ',
 'LOCALROOTOBJ',
 'REMOTENODEALIAS',
 'REMOTEPRIOBJ',
 'REMOTESECOBJ',
 'REMOTEROOTOBJ',
 'X733EVENTTYPE',
 'X733PROBABLECAUSE',
 'X733SPECIFICPROB',
 'X733CORRNOTIF',
 'SERVERNAME',
 'SERVERSERIAL',
 'ORIGINALSEVERITY',
 'DELETEDAT',
 'ACKBY',
 'ACKTIME',
 'ADDITIONALINFO',
 'ADMINDOMAIN',
 'AIS_OAM_STATUS',
 'BITMAPFIELD',
 'CIRCUITDATA',
 'CLARIFYDATA1',
 'CLARIFYDATA10',
 'CLARIFYDATA2',
 'CLARIFYDATA3',
 'CLARIFYDATA4',
 'CLARIFYDATA5',
 'CLARIFYDATA6',
 'CLARIFYDATA7',
 'CLARIFYDATA8',
 'CLARIFYDATA9',
 'CLARIFYTICKET',
 'CLARIFYTICKET2',
 'CLEAREDBY',
 'CONTACT',
 'CONVERT',
 'CUSTOMERNUMBER',
 'DACSASSIGNMENT',
 'DACSCLLI',
 'DACSMFG',
 'DACSMFGPART',
 'DNOC_CLASS',
 'DSAP',
 'EQUIPMENT',
 'EXITTIME',
 'FIRSTNAME',
 'FRASM_MISC',
 'LASTNAME',
 'LECCIRCUITID',
 'LNNI',
 'LSAP',
 'MISCDATA1',
 'MISCDATA10',
 'MISCDATA2',
 'MISCDATA3',
 'MISCDATA4',
 'MISCDATA5',
 'MISCDATA6',
 'MISCDATA7',
 'MISCDATA8',
 'MISCDATA9',
 'NCACTION',
 'NEADDRESS',
 'NEFWVERSION',
 'NEMODELID',
 'NEN',
 'NENAME',
 'NENCLLI',
 'NENMFG',
 'NETWORKNAME',
 'NETYPE',
 'NSCCIRCUITID',
 'NXACTION',
 'NXALERTKEY',
 'NXCOUNT',
 'NXGATE',
 'NXOPER',
 'NXSYSTEM',
 'OBJECTSTATUS',
 'OBJECTTYPE',
 'OLDCLASS',
 'OLDOBJECTSTATUS',
 'OVO_EVENTFLAG',
 'PSAP',
 'RECEIVED',
 'RECEIVEDCHECK',
 'REFERENCE',
 'REGION',
 'REMEDY_TICKET',
 'REMOTEDSAP',
 'REMOTELSAP',
 'REMOTENENAME',
 'REMOTEPSAP',
 'REMOTESLOT',
 'RNNI',
 'SERVICE_TYPE',
 'SERVICE_TYPE_ORIGINAL',
 'SERVICEIDENTIFIER',
 'SERVICETYPE',
 'SITE',
 'SLOT',
 'SUBOBJECTTYPE',
 'SVVERSION',
 'TICKETNUMBER',
 'TIER_LEVEL',
 'TRAPREASON',
 'ACKBYFULLNAME',
 'ADVCORRCAUSETYPE',
 'ADVCORRSERVERNAME',
 'ADVCORRSERVERSERIAL',
 'AGGREGATIONFIRST',
 'APLASTUPDATED',
 'APRESPONDER',
 'APSTATE',
 'APTARGET',
 'BSM_IDENTITY',
 'CAUSETYPE',
 'CLARIFYFLAG',
 'CLEARED',
 'COLLECTIONFIRST',
 'CORRSCORE',
 'DISCARDTAG',
 'DNOC_DISCARDS',
 'EMAILALM',
 'EMAILED',
 'EMPID',
 'ENVIROMENTAL',
 'EXTENDEDATTR',
 'FULLDATA',
 'IMPACT_DISPLAY',
 'IMPACT_PROCESSED',
 'IMPACT_SERVER',
 'INTERFACEDESCRIPTION',
 'INTERFACENAME',
 'INTERNALLAST',
 'ITK_GROUP',
 'LOCALOBJRELATE',
 'LOCALTERTOBJ',
 'MANUAL_CLEAR_REQUIRED',
 'MPLSTYPE',
 'NMOSDOMAINNAME',
 'NMOSENTITYID',
 'NMOSEVENTMAP',
 'NMOSMANAGEDSTATUS',
 'OLDROW',
 'ORIGACKBY',
 'ORIGACKBYFULLNAME',
 'ORIGACKTIME',
 'OVO_OBJECT',
 'PROBESUBSECONDID',
 'REMOTEOBJRELATE',
 'REMOTETERTOBJ',
 'STATE',
 'SUPPRESS',
 'SUPPRESSESC',
 'TDAX_TEST',
 'TIER_LEVEL_ORIGINAL',
 'TIERLOCK',
 'URL',
 'VENDOR',
 'WINDSTREAMCODE',
 'WS_NODE',
 'WS_NODE_CONF',
 'PHONENUMBER',
 'EXPIRETIME',
 'PROBE_TAG',
 'SERVICE_TAG',
 'PROCESS_TAG',
 'MANAGEMENT_TAG',
 'RESOLVE_TAG',
 'ROLE_TAG',
 'IDENTIFIER',
 'RECEIVED_MONTH',
 'SERVICE_LEVEL',
 'RESOLVELOG']
col_options = [dict(label=x, value=x) for x in collist]
global df
df=pd.DataFrame()
app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)
print(dimensions)
app.config['suppress_callback_exceptions']=True
app.layout = html.Div(
    [
        html.H1("Netcool Board"),
        html.Div(
            [html.Div([html.P(['nodename :',dcc.Dropdown(id='nodename', options=node_options)]),
            dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt(2019, 1, 1),
            max_date_allowed=dt(2019, 5, 1),
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
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),

    ]
)

# @app.callback(Output('nodename-output', "children"), [Input("nodename", "value")])
def get_data(nodename):
    if not nodename:
        return pd.DataFrame()
    # global df
    df=pd.read_csv(os.path.join(NETCOOL_DIR,nodename))
    print(df.shape)
    # global df
    return df #html.H1(nodename.split('.')[0]+" with rows "+str(df.shape[0]))

@app.callback(Output("graph", "figure"), [Input("nodename", "value"),
                                            Input('my-date-picker-range', 'start_date'),
                                            Input('my-date-picker-range', 'end_date')]+
                                            [Input(d, "value") for d in dimensions])
def make_figure(nodename,start_date,end_date,x, y, color, facet_col, facet_row):
    df=get_data(nodename)
    df=df[(df['FIRSTOCCURRENCE']>start_date) & (df['FIRSTOCCURRENCE']<end_date)]
    fig= px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
    )
    fig.layout.template='ggplot2'

    return fig

app.run_server(debug=True)












