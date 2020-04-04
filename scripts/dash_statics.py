
import dash
import dash_html_components as html
import dash_core_components as dcc



def header(latestDate,confirmedCases):
    return html.Div(style={'marginRight': '1.5%',},
        id="header",
        children=[
            html.H4(
                children="Coronavirus Monitor"),
            html.P(
                id="description",
                children=dcc.Markdown(
                    children=(
                    '''
                    On Dec 31, 2019, the World Health Organization (WHO) was informed 
                    an outbreak of “pneumonia of unknown cause” detected in Wuhan, Hubei Province, China. 
                    
                    The virus that caused the outbreak of COVID-19 was lately known as _severe acute respiratory syndrome coronavirus 2_ (SARS-CoV-2). 
                    
                    The WHO declared the outbreak to be a Public Health Emergency of International Concern on 
                    Jan 30, 2020 and recognized it as a pandemic on Mar 11, 2020. As of {}, there are {:,d} cases of COVID-19 confirmed globally.
                    
                    This dash board is developed to visualise and track the recent reported 
                    cases on a hourly timescale.'''.format(latestDate, confirmedCases),
                    )
                )
            ),
            html.Hr(style={'marginTop': '.5%'},),
                ]
            ),
    
def cards(daysOutbreak):
    
    card1 = html.Div(
        id="number-plate",
        style={'marginLeft': '1.5%','marginRight': '1.5%', 'marginBottom': '.8%'},
        children=[
            html.Div(
                style={'width': '24.4%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                        'marginRight': '.8%', 'verticalAlign': 'top', 
                        'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'},
                children=[
                    html.H3(style={'textAlign': 'center','fontWeight': 'bold', 'color': '#2674f6'},
                            children=[
                                html.P(
                                    style={'color': '#ffffff', 'padding': '.5rem'},
                                    children='xxxx xx xxx xxxx xxx xxxxx'
                                ),
                                '{}'.format(daysOutbreak),
                            ]
                    ),
                    html.H5(
                        style={'textAlign': 'center', 'color': '#2674f6', 'padding': '.1rem'},
                        children="days since outbreak"
                    )
                ]
            ), 
    ]),
    
    card2 = html.Div(
        id="number-plate",
        style={'marginLeft': '1.5%','marginRight': '1.5%', 'marginBottom': '.8%'},
        children=[
            html.Div(
                style={'width': '24.4%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                        'marginRight': '.8%', 'verticalAlign': 'top', 
                        'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'},
                children=[
                    html.H3(style={'textAlign': 'center','fontWeight': 'bold', 'color': '#2674f6'},
                            children=[
                                html.P(
                                    style={'color': '#ffffff', 'padding': '.5rem'},
                                    children='xxxx xx xxx xxxx xxx xxxxx'
                                ),
                                '{}'.format(daysOutbreak),
                            ]
                    ),
                    html.H5(
                        style={'textAlign': 'center', 'color': '#2674f6', 'padding': '.1rem'},
                        children="days since outbreak"
                    )
                ]
            ), 
    ]),
    
    
    
    return card1