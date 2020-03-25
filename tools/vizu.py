import numpy as np
import pandas as pd

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline


from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')
date_time = datetime.today().strftime('%Y-%m-%d-%H-%M')

def normalize_cols(df):
    return df.str.normalize('NFKD').str.replace("$","").str.replace("(","").str.replace(")","").str.replace('-','').str.replace(' ','_').str.lower().str.replace('.','')


import unicodedata
def remove_acentos(s):
    ss =  ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    
    return ss.lower().replace(' ','_')


def total_casos(df,mask_countrys, escala='lin',var='cases',date=today, save=False):
    mask = df['new_{}'.format(var)]!=0
    df = df[mask]
    df['count'] = 1
    
    since_first_day = df[['count','countrycode']].groupby(by = ['countrycode',]).cumsum()['count'].tolist()
    df['since_first_day'] = since_first_day
    
    dd = df[mask_countrys]
    
    dd = dd.sort_values(by=['countryname'], ascending=False)
    dd = dd.sort_values(by=['date'])
    
    data = []
    wid = 10
    marker_size = 15
    
        
    if escala == 'lin':
        tick = 'n'
        tipo = None
    elif escala=='log':
        tick = None
        tipo = 'log'
    
    
    if var == 'deaths':
        title = '<b>Total de Mortes Confirmadas em {}</b>'.format(date)
        var_col = 'deaths'
        var_save= 'mortes'
        y_name = "<b>MORTES CONFIRMADAS<b>"
        x_name = "<b>DIAS DESDE A PRIMEIRA MORTE<b>"
        
    if var== 'cases':
        title = '<b>Total de Casos Confirmadas em {}</b>'.format(date)
        var_col = 'confirmed'
        var_save= 'total'
        y_name = "<b>CASOS CONFIRMADOS<b>"
        x_name = "<b>DIAS DESDE O PRIMEIRO CASO<b>"
        
    if var== 'recovered':       
        title = '<b>Total de Recuperados Confirmados em {}</b>'.format(date)
        var_col = 'recovered'
        var_save= 'recuperados'
        y_name = "<b>RECUPERADOS CONFIRMADOS<b>"
        x_name = "<b>DIAS DESDE O PRIMEIRO CASO<b>"        
        
    if save ==True:
        largura = None
    else:
        largura = 1600
        

    
    
    countrys = list(dd['countrycode'].unique())
    countrys.sort(reverse=True)
    
    for geoid in countrys:

        mask = (dd['countrycode']==geoid)

        trace = go.Scatter(
        name=dd[mask]['countryname'].str.replace('_',' ').tolist()[0],
        x=dd[mask]['since_first_day'], 
        y=dd[mask][var_col],
    #     line=dict(color='#a14900', width=wid),
        line=dict(width=wid),
        mode='lines+markers',
        marker=dict(size=marker_size),
        hoverlabel=dict(namelength=-1, font=dict(size=18))   
        )
        data.append(trace)
        
    layout = go.Layout(
        barmode='stack',

        yaxis_title=y_name,
        yaxis = dict(

            tickfont=dict(
                size=22,
                color='black',
            ),
            tickformat=tick,
            type=tipo,
        ),
        xaxis_title=x_name,
        xaxis = dict(
            tickfont=dict(
                size=22,
                color='black',
            ),
    #         font = dict(size=20)

        ),

        title=dict(
            text=title,
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top',
            font = dict(
                size=22,
            )
        ),

        legend=go.layout.Legend(
            x=0.05,
            y=0.99,
    #         traceorder="normal",
            orientation='v',
            font=dict(
                family="sans-serif",
                size=20,
                color="black"
            ),
            bgcolor= 'rgba(0,0,0,0)' ,
    #         bordercolor="Black",
        #     borderwidth=2
        ),

        height = 800,

        width = largura,

        font=dict(
            size=18,
        )
    )

    fig = go.Figure(data=data, layout=layout)

    
    if save==True:
        if escala == 'lin':
            plot(fig, filename="../images/{}_lin.html".format(var_save), auto_open=False)
            plot(fig, filename="../../sample_pages/images/covid19/{}_lin.html".format(var_save), auto_open=False)
        elif escala=='log':
            plot(fig, filename="../images/{}_log.html".format(var_save), auto_open=False)
            plot(fig, filename="../../sample_pages/images/covid19/{}_log.html".format(var_save),auto_open=False)
    else:
        if escala == 'lin':
            fig.write_image("../images/pdf/{}_lin.pdf".format(var_save))
        elif escala=='log':
            fig.write_image("../images/pdf/{}_log.pdf".format(var_save))

    return(fig, dd)









def total_by_country(df,geoid, escala='lin',var='cases', data=today, save=False):
    
    if geoid=='IT':
        mask = (df['countrycode']=='IT')
        dd = df[mask]


        mask = (dd['confirmed']>0)
        dd = dd[mask]

        mask = dd['date']>='2020-03-09'
        dd['lockdown'] = np.where(mask,1,0)

        mask = dd['date']>='2020-02-21'
        dd = dd[mask]
        
        pais = 'Itália'
        pais_save = 'italia'
        
    
    elif geoid=='CN':
        
        mask = (df['confirmed']>0)
        dd = df[mask]
        
        mask = (df['countrycode']=='CN')
        dd = df[mask]

        mask = dd['date']>='2020-01-24'
        dd['lockdown'] = np.where(mask,1,0)
        
        pais='China'
        pais_save = 'china'

    
    else:
        
        mask = (df['countrycode']==geoid)
        dd = df[mask]
        
        mask = (dd['confirmed']>0)
        dd = dd[mask]
        
        dd['lockdown']=0
        pais = dd['countryname'].tolist()[0]
        pais_save = pais
    
    
    
    if escala == 'lin':
        tick = 'n'
        tipo = None
    elif escala=='log':
        tick = None
        tipo = 'log'
    
    
    if var == 'deaths':
        title = '<b>{} - Total de Mortes Confirmadas em {}</b>'.format(pais,data)
        var_col = 'deaths'
        var_save= 'mortes'
        barra1 = "Mortes Diarias na Quarentena"
        barra2 = "Mortes Diarias no LockDown"
        y_name = "<b>Mortes Confirmadas<b>"
        nome_final = "Total de Mortes"
        
    if var== 'cases':
        title = '<b>{} - Total de Casos Confirmados em {}</b>'.format(pais,data)
        var_col = 'confirmed'
        var_save= 'total'
        barra1 = "Casos Diarios na Quarentena"
        barra2 = "Casos Diarios no LockDown"
        y_name = "<b>Casos Confirmados<b>"
        nome_final = "Total de Casos"
        
        
    if var== 'recovered':
        title = '<b>{} - Total de Recuperados Confirmados em {}</b>'.format(pais,data)
        var_col = 'recovered'
        var_save= 'recuperados'
        barra1 = "Recuperados Diarios na Quarentena"
        barra2 = "Recuperados Diarios no LockDown"
        y_name = "<b>Recuperados Confirmados<b>"
        nome_final = "Total de Recuperados"
        
    if save ==True:
        largura = None
    else:
        largura = 1600
        
    wid = 10
    marker_size = 15



    trace1 = go.Scatter(
    name=nome_final,
    x=dd['date'], 
    y=dd[var_col],
    line=dict(width=wid, color='#3b5bff'),
    mode='lines+markers',
    marker=dict(size=marker_size),
    hoverlabel=dict(namelength=-1, font=dict(size=18))   
    )


    mask = dd['lockdown']==0


    trace2 = go.Bar(
    name=barra1,
    x=dd[mask]['date'], 
    y=dd[mask]['new_{}'.format(var)],

    marker=dict(color='#1d8179',),
    hoverlabel=dict(namelength=-1, font=dict(size=18))   
    )

    mask = dd['lockdown']==1

    trace3 = go.Bar(
    name=barra2,
    x=dd[mask]['date'], 
    y=dd[mask]['new_{}'.format(var)],

    marker=dict(color='#fa7609',),
    hoverlabel=dict(namelength=-1, font=dict(size=18))   
    )




    data = [trace3, trace2, trace1]
#     data = [trace1]

    layout = go.Layout(
        barmode='stack',

        yaxis_title=y_name,
        yaxis = dict(

            tickfont=dict(
                size=22,
                color='black',
            ),
            
            
            tickformat=tick,
            type=tipo,

        ),
        xaxis_title="<b>Data<b>",
        xaxis = dict(
            tickfont=dict(
                size=22,
                color='black',
            ),
    #         font = dict(size=20)

        ),

        title=dict(
            text=title,
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top',
            font = dict(
                size=22,
            )
        ),

        legend=go.layout.Legend(
            x=0.01,
            y=0.99,
    #         traceorder="normal",
            orientation='v',
            font=dict(
                family="sans-serif",
                size=20,
                color="black"
            ),
            bgcolor= 'rgba(0,0,0,0)' ,
    #         bordercolor="Black",
        #     borderwidth=2
        ),

        height = 800,

        width = largura,

        font=dict(
            size=18,
        )
    )

    fig = go.Figure(data=data, layout=layout)
    
    
    
    if save==True:
        if escala == 'lin':
            plot(fig, filename="../images/{}_lin_{}.html".format(pais_save,var_save), auto_open=False)
            plot(fig, filename="../../sample_pages/images/covid19/{}_{}_lin.html".format(pais_save,var_save), auto_open=False)
        elif escala=='log':
            plot(fig, filename="../images/{}_log_{}.html".format(pais_save,var_save), auto_open=False)
            plot(fig, filename="../../sample_pages/images/covid19/{}_{}_log.html".format(pais_save,var_save),auto_open=False)
    else:
        if escala == 'lin':
            fig.write_image("../images/pdf/{}_{}_lin.pdf".format(pais_save,var_save))
        elif escala=='log':
            fig.write_image("../images/pdf/{}_{}_log.pdf".format(pais_save,var_save))
    
    return(fig,dd)




def bar_compare(br_it,pais='BR',pais_name='Brasil',pais_comp='IT',pais_comp_name='Itália', save=False, color='#007482',color_comp='#F29120', col='confirmed'):
    
    
    
    mask = (br_it['countrycode'] == pais)

    trace2 = go.Bar(
    name=pais_name,
    x=br_it[mask]['since_first_day'], 
    y=br_it[mask][col],

    marker=dict(color=color,),
    hoverlabel=dict(namelength=-1, font=dict(size=18))   
    )


    mask = (br_it['countrycode'] == pais_comp)

    trace3 = go.Bar(
    name=pais_comp_name,
    x=br_it[mask]['since_first_day'], 
    y=br_it[mask][col],

    marker=dict(color=color_comp,),
    hoverlabel=dict(namelength=-1, font=dict(size=18))   
    )




    data = [trace2,trace3]
    #     data = [trace1]
    
    if save ==True:
        largura = None
    else:
        largura = 1300
    
    
    layout = go.Layout(
        barmode='group',

        yaxis_title='<b>Número de Confirmados<b>',
        yaxis = dict(

            tickfont=dict(
                size=24,
                color='black',
            ),


            tickformat='n',
            type=None,

        ),
        xaxis_title="<b>Dias<b>",
        xaxis = dict(
            tickfont=dict(
                size=24,
                color='black',
            ),
    #         font = dict(size=20)
#             tickformat ='%d/%m'

        ),

        title=dict(
            text='<b>Número Total de Confirmados (A partir do Caso 100) - {} vs {}<b>'.format(pais_name,pais_comp_name),
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font = dict(
                size=30,
            )
        ),

        legend=go.layout.Legend(
            x=0.2,
            y=0.7,
    #         traceorder="normal",
            orientation='v',
            font=dict(
                family="sans-serif",
                size=28,
                color="black"
            ),
            bgcolor= 'rgba(0,0,0,0)' ,
    #         bordercolor="Black",
        #     borderwidth=2
        ),

        height = 800,

        width = largura,

        font=dict(
            size=22,
        )
    )

    fig = go.Figure(data=data, layout=layout)
    
    pais_save = [pais_name,pais_comp_name]
    pais_save.sort()
    pais_save = [remove_acentos(p) for p in pais_save]
    
    if save==True:
        plot(fig, filename="../images/comparacao/comparacao_{}_vs_{}.html".format(pais_save[0],pais_save[1]), auto_open=False)
        plot(fig, filename="../../sample_pages/images/covid19/comparacao/comparacao_{}_vs_{}.html".format(pais_save[0],pais_save[1]), auto_open=False)


    else:
        fig.write_image("../images/comparacao/pdf/comparacao_{}_vs_{}.pdf".format(pais_save[0],pais_save[1]))

    return(fig)



def brasil_vis(dd, var_col, in_cities, escala, today, largura=None, save=False):
    wid = 10
    marker_size = 15


    if escala == 'lin':
        tick = 'n'
        tipo = None
    elif escala=='log':
        tick = None
        tipo = 'log'

    if var_col == 'deaths':
        x_name  = '<b>DATA<b>'
        y_name  = '<b>MOTES CONFIRMADAS<b>'
        title   = '<b>MORTES POR ESTADO EM {}<b>'.format(today)
    
    elif var_col == 'confirmed':
        x_name  = '<b>DATA<b>'
        y_name  = '<b>CASOS CONFIRMADAS<b>'
        title   = '<b>CASOS POR ESTADO EM {}<b>'.format(today)


    # in_cities = ['BRASIL','SP', 'RJ']
    cities = dd['city'].unique()
    drop_cities = [city for city in cities if city not in in_cities]
    drop_cities.sort()
    cities =  in_cities + drop_cities

    data = []

    for city in cities:

        if city in in_cities:
            just_legend = None
        else:
            just_legend = 'legendonly'
        
        mask = (dd['city']==city)

        trace = go.Scatter(
        name=city,
        x=dd[mask]['date'], 
        y=dd[mask][var_col],
    #     line=dict(color='#a14900', width=wid),
        line=dict(width=wid),
        mode='lines+markers',
        marker=dict(size=marker_size),
        hoverlabel=dict(namelength=-1, font=dict(size=18)),
        visible = just_legend
        )
        data.append(trace)


    layout = go.Layout(
        barmode='stack',

        yaxis_title=y_name,
        yaxis = dict(

            tickfont=dict(
                size=22,
                color='black',
            ),
            tickformat=tick,
            type=tipo,
        ),
        xaxis_title=x_name,
        xaxis = dict(
            tickfont=dict(
                size=22,
                color='black',
            ),
    #         font = dict(size=20)
        tickformat ='%d/%m'


        ),

        title=dict(
            text=title,
            x=0.5,
    #         y=0.9,
            xanchor='center',
            yanchor='top',
            font = dict(
                size=22,
            )
        ),

        legend=go.layout.Legend(
    #         x=0.05,
    #         y=0.99,
    #         traceorder="normal",
            orientation='v',
            font=dict(
                family="sans-serif",
                size=20,
                color="black"
            ),
            bgcolor= 'rgba(0,0,0,0)' ,
    #         bordercolor="Black",
        #     borderwidth=2
        ),

        height = 800,

        width = largura,

        font=dict(
            size=18,
        )
    )

    fig = go.Figure(data=data, layout=layout)


    if save==True:
        plot(fig, filename="../images/brasil/brasil_por_estado_{}.html".format(var_col), auto_open=False)
        plot(fig, filename="../../sample_pages/images/covid19/brasil/brasil_por_estado_{}.html".format(var_col), auto_open=False)
    else:
        pass

    return(fig)