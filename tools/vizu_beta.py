import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')
date_time = datetime.today().strftime('%Y-%m-%d-%H-%M')


def show_colors(scaled_colours):
    fig, ax = plt.subplots(figsize=(len(scaled_colours), 1))

    ax.axis(xmin=0, xmax=len(scaled_colours))
    ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

    for index, colour in enumerate(scaled_colours):
        ax.axvspan(index, index + 1, color=colour)
    
    # return fig
    
   
def brasil_vis(dd,
               var_col,
               in_cities, 
               today,
               themes,
               save=False):

    if var_col == 'deaths':
        x_name  = '<b>DATA<b>'
        y_name  = '<b>MOTES CONFIRMADAS<b>'
        title   = '<b>MORTES POR ESTADO EM {}<b>'.format(today)
    
    elif var_col == 'confirmed':
        x_name  = '<b>DATA<b>'
        y_name  = '<b>CASOS CONFIRMADOS<b>'
        title   = '<b>CASOS POR ESTADO EM {}<b>'.format(today)


    # in_cities = ['BRASIL','SP', 'RJ']
    cities = dd['city'].unique()
    drop_cities = [city for city in cities if city not in in_cities]
    drop_cities.sort()
    # cities =  in_cities + drop_cities

    cities = in_cities

    colors =  themes['soft_colors']
    
    factor = int(np.ceil(len(cities)/len(colors)))    
    
    colors = factor * colors
    
    colors = themes['colors'] + colors
    
    
    data = []
    i=0
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
        line=dict(color=colors[i], width=themes['data']['line_width']),
        # line=dict(width=wid),
        mode='lines+markers',
        marker=dict(size=themes['data']['marker_size']),
        hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size'])),
        visible = just_legend,
        )
        data.append(trace)
        i+=1

    
    layout = get_layout(themes, title, x_name, y_name)

    fig = go.Figure(data=data, layout=layout)


    if save==True:
        plot(fig, filename="../images/brasil/brasil_por_estado_{}.html".format(var_col), auto_open=False)
        plot(fig, filename="../../sample_pages/images/covid19/brasil/brasil_por_estado_{}.html".format(var_col), auto_open=False)
    else:
        pass

    return(fig)



def get_layout(themes, title, x_name, y_name, tick=None, tipo=None):
    
    layout = go.Layout(
                
        barmode=themes['barmode'],
    
        title=dict(
            text=title,
            x=0.5,
    #         y=0.9,
            xanchor='center',
            yanchor='top',
            font = dict(
                size=themes['title']['size'],
                color=themes['title']['color']
            )
        ),

        xaxis_title=x_name,
        
        xaxis = dict(
            tickfont=dict(
                size=themes['axis_legend']['size'],
                color=themes['axis_legend']['color'],
            ),
        gridcolor=themes['axis_legend']['gridcolor'],
        zerolinecolor=themes['axis_legend']['gridcolor'],
        # linecolor=themes['axis_legend']['gridcolor'],
        # linewidth=2,
        # mirror=True,
        tickformat =themes['axis_legend']['tickformat']['x'],
        type=themes['axis_legend']['type']['x'],

        ),
        
        
        yaxis_title=y_name,
        
        yaxis = dict(
            tickfont=dict(
                size=themes['axis_legend']['size'],
                color=themes['axis_legend']['color'],
            ),
            gridcolor=themes['axis_legend']['gridcolor'],
            zerolinecolor=themes['axis_legend']['gridcolor'],
            # linecolor=themes['axis_legend']['gridcolor'],
            # linewidth=2,
            tickformat=tick,
            type=tipo,
        ),
        
        
        font=dict(
            size=themes['axis_tilte']['size'],
            color=themes['axis_tilte']['color']
        ),
        

        legend=go.layout.Legend(
            x=themes['legend']['position']['x'],
            y=themes['legend']['position']['y'],
            traceorder="normal",
            orientation='v',
            font=dict(
                family=themes['legend']['family'],
                size=themes['legend']['size'],
                color=themes['legend']['color']
            ),
            bgcolor=themes['legend']['bgcolor'] ,
            bordercolor=themes['legend']['bordercolor'],
            borderwidth=themes['legend']['borderwidth']
        ),


        height = themes['altura'],
        width = themes['largura'],
        

        paper_bgcolor=themes['paper_bgcolor'],
        plot_bgcolor=themes['plot_bgcolor'],
        
        annotations =[dict(
            showarrow=False,
            text = f"<b>{themes['source']['text']}<b>",
            
            x = themes['source']['position']['x'],
            y = themes['source']['position']['y'],
            

            
            xref="paper",
            yref="paper",

            align="left",
            
            # xanchor='right',
            xshift=0, yshift=0,
            
            font=dict(
                family=themes['source']['family'],
                size=themes['source']['size'],
                color=themes['source']['color']
                ),
        )]
        
    )
    
    
    return layout