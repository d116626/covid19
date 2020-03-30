import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline
import pandas as pd
import numpy as np

def show_colors(scaled_colours):
    fig, ax = plt.subplots(figsize=(len(scaled_colours), 1))

    ax.axis(xmin=0, xmax=len(scaled_colours))
    ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

    for index, colour in enumerate(scaled_colours):
        ax.axvspan(index, index + 1, color=colour)
    
    # return fig





def plot_simulation(final, columns, colors, config, leitos=1, perc_ventiladores=1):
    
    wid = 7
    marker_size = 5
    largura = None
    title   = "<b>{} - SEIR MODEL<b>".format(final['city_name'].tolist()[0])
    x_name  = "<b>Dias<b>"
    y_name  = "<b>Populacão<b>"
    
    
    data = []
    y_list = []
    i=0
    for col in columns.keys():
        trace = go.Scatter(
                name=columns[col],
                x=final['days'], 
                y=final[col],
                line=dict(color=colors[i], width=wid),
                # line=dict(width=wid),
                mode='lines+markers',
                marker=dict(size=marker_size),
                hoverlabel=dict(namelength=-1, font=dict(size=18))   
                )
        if col == 'quantidade_leitos':
                trace = go.Scatter(
                    name=columns[col],
                    x=final['days'], 
                    y=[leitos for i in range(len(final['days']))],
                    line=dict(color=colors[i], width=3),
                    # line=dict(width=wid),
                    mode='lines+markers',
                    marker=dict(size=1),
                    hoverlabel=dict(namelength=-1, font=dict(size=18))   
                    )
        elif col == 'ventiladores_existentes':
                trace = go.Scatter(
                    name=columns[col],
                    x=final['days'], 
                    y=round(final[col] * perc_ventiladores,0),
                    line=dict(color=colors[i], width=3),
                    # line=dict(width=wid),
                    mode='lines+markers',
                    marker=dict(size=1),
                    hoverlabel=dict(namelength=-1, font=dict(size=18))   
                    )
        data.append(trace)
        
        y_list.append(max(final[col]))
        
        i+=1



    


    layout = go.Layout(
        barmode='stack',

        yaxis_title=y_name,
        yaxis = dict(

            tickfont=dict(
                size=22,
                color='black',
            ),
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
            # y=0.9,
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
        ),
          
        hovermode = "x",

    )

    y_max = max(y_list)



    fig = go.Figure(data=data, layout=layout)
    
    t0   = 0 
    r_t0 = config['scenarios']['nothing']['R0']['upper_bound']
    
    t1   = config['scenarios']['isolation']['dates'][0]
    r_t1 = config['scenarios']['isolation']['R0']['upper_bound']
    
    t2   = config['scenarios']['lockdown']['dates'][0]
    r_t2 = config['scenarios']['lockdown']['R0']['upper_bound']
    
    uti_percent = config['model_parameters']['seir']['i3_percentage']['upper_bound']
    
    x_max = max(final['days'])
    
    fig.add_annotation(
        showarrow=False,
        x=x_max*0.9,
        y=y_max*0.95,
        xref="x",
        yref="y",
        align="left",
        text="<b>\
            t0  = {} dias - R0 = {}<br>\
            t1  = {} dias -  R0 = {}<br>\
            t1  = {} dias -  R0 = {}        <br>\
            UTI = {}% dos Infectados \
            <b>".format(t0,r_t0,
                        t1,r_t1,
                        t2,r_t2,
                        uti_percent),
        
        )

    return fig
