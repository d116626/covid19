import numpy as np
import pandas as pd
import yaml

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline

from vis_layout import get_layout
from manipulation import normalize_cols, remove_acentos


from paths import *
import pandas as pd
from datetime import datetime
from scripts.io import read_sheets
from scripts import manipulation
from scripts import io

import folium
import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap

import branca.colormap as cm
import branca

def taubate_daily(df, themes, adjusts, config_daily, save=False):
    
    data=[]

    for status in adjusts.keys():
        trace = go.Bar(
            name=adjusts[status]['nome'],
            x=df['data'], 
            y=df[status],
            marker=dict(color=adjusts[status]['cor'],),
            hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
        )
        
        data.append(trace)

    layout = get_layout(themes=themes,title=' ' ,x_name='Data',y_name = ' ')

    fig = go.Figure(data=data, layout=layout)
    
    if save==True:
        name= f"{config_daily['save_name']}"
        path= f"{config_daily['path_save']}{name}"
        plot(fig, filename=path, auto_open=False)
        io.to_storage(bucket=config_daily['bucket'],
                        bucket_folder=config_daily['bucket_folder'],
                        file_name=name,
                        path_to_file=path)

    
    return fig


def taubate_cum(df, themes, adjusts, config_cumulative, save=False):
    
    data = []
    
    for status in adjusts.keys():               
        trace = go.Scatter(
            name=adjusts[status]['nome'],
            x=df['data'], 
            y=df[status],
            marker=dict(color=themes['data']['marker']['color'],size=themes['data']['marker']['size']),
            line=dict(width=themes['data']['line_width'], color=adjusts[status]['cor']),
            mode='lines+markers',
            hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
        )
        
        data.append(trace)

    layout = get_layout(themes=themes,title=' ' ,x_name='Data',y_name = ' ')

    fig = go.Figure(data=data, layout=layout)
    
    if save==True:
        name= f"{config_cumulative['save_name']}"
        path= f"{config_cumulative['path_save']}{name}"
        plot(fig, filename=path, auto_open=False)
        io.to_storage(bucket=config_cumulative['bucket'],
                        bucket_folder=config_cumulative['bucket_folder'],
                        file_name=name,
                        path_to_file=path)
    
    
     
    return fig.update_layout(hovermode = 'x unified')


def get_map_taubate(df,status_adjusts, config_map, save=False):
    mymap = folium.Map(location=[ -23.021628, -45.556273 ], zoom_start=13,tiles=None,control_scale=False, max_bounds=True, max_zoom=9,max_lat=-22.956844, min_lat=-23.084949, min_lon= -45.726182, max_lon=-45.437983)

    #def type
    folium.TileLayer('CartoDB positron',control=False).add_to(mymap)

    for status in df['status'].value_counts(ascending=False).index.tolist():
        
        dd = df.query(f'status == "{status}"')
        dd['count']=1
        bairro_table = dd.groupby(['bairro','lat','lon'], as_index=False).sum().sort_values(by='count', ascending=False)
        
        for bairro in bairro_table.bairro.unique():
            mask = bairro_table['bairro']==bairro
            bairro_row = bairro_table[mask]
        # mymap.add_child(NIL)
            r   = int(bairro_row['count'].values[0]+1)*30
            lat = bairro_row['lat'].values[0]
            lon = bairro_row['lon'].values[0]


            text = status_adjusts[status]['text'].format(str(bairro_row['bairro'].values[0]) , str(bairro_row['count'].values[0]))
            tooltip = folium.Tooltip(text)
            
            
            folium.Circle(
                radius=r,
                location=[lat,lon],
                tooltip=tooltip,
                color=status_adjusts[status]['color'],
                fill=True,
            ).add_to(mymap)

    if save==True:
        mymap.save(f'{config_map["path_save"]}{config_map["save_name"]}')

        print('Upload vale map..')
        io.to_storage(bucket=config_map['bucket'],
                bucket_folder=config_map['bucket_folder'],
                file_name=config_map['save_name'],
                path_to_file=f'{config_map["path_save"]}{config_map["save_name"]}')
        
        # os.remove(f'{config_map["path_save"]}{config_map["save_name"]}')
    
    return mymap


def taubate_update_html(casos_taubate, config_embed, save=False):

    lastDay    = max(casos_taubate['data'])
    todayDate  = lastDay.strftime("%d/%m/%Y")
    firstDay   = '2020-03-12'
    firstDayDt = datetime.strptime(str(firstDay)[:10], "%Y-%m-%d")
    lastDayDt  = datetime.strptime(str(lastDay)[:10], "%Y-%m-%d")
    daysOutbreak = (lastDayDt - firstDayDt).days


    today_data = casos_taubate.query(f"data=='{lastDay}'")
    todayCases     = today_data['confirmado_sum'].values[0]
    todayNewCases  = today_data['confirmado'].values[0]
    todayCasesPerc = todayNewCases/(todayCases - todayNewCases)

    todayDeaths   = today_data['obito_sum'].values[0]
    todayNewDeaths = today_data['obito'].values[0]
    todayDeathsPerc = todayNewDeaths/(todayDeaths -todayNewDeaths)
    
    todaySuspects     = today_data['analise_sum'].values[0]
    todayNewSuspects  = today_data['analise'].values[0]
    todaySuspectsPerc = todayNewSuspects/(todaySuspects - todayNewSuspects)
    
    todayRecover     = today_data['descartado_sum'].values[0]
    todayNewRecover  = today_data['descartado'].values[0]
    todayRecoverPerc = todayNewRecover/(todayRecover - todayNewRecover)



    replace_vars = {'daysOutbreak':daysOutbreak, "todayDate":todayDate,
                    'todayNewCases':"{:,d}".format(todayNewCases),'todayCasesPerc':"{:.1%}".format(todayCasesPerc), "todayCases":"{:,d}".format(todayCases),
                    'todayNewDeaths':"{:,d}".format(todayNewDeaths),'todayDeathsPerc':"{:.1%}".format(todayDeathsPerc), "todayDeaths":"{:,d}".format(todayDeaths),
                    'todayNewSuspects':"{:,d}".format(todayNewSuspects),'todaySuspectsPerc':"{:.1%}".format(todaySuspectsPerc), "todaySuspects":"{:,d}".format(todaySuspects),
                    'todayNewRecover':"{:,d}".format(todayNewRecover),'todayRecoverPerc':"{:.1%}".format(todayRecoverPerc), "todayRecover":"{:,d}".format(todayRecover),
                    
                    }


    final_lines = []
    with open(r'{}'.format(config_embed['path'] + config_embed['model_name']), mode='r') as f:
        for line in f.readlines():
            final_lines.append(line)

    for i in range(len(final_lines)):
        for var in replace_vars.keys():
            if var in final_lines[i]:
                final_lines[i] = final_lines[i].replace(var,str(replace_vars[var]))

    css = []
    with open(r'{}'.format(config_embed['path'] + config_embed['css_name']), mode='r') as f:
        for line in f.readlines():
            css.append(line)
    final_html = []
    for line in final_lines:
        if "getCSS" in line:
            for cssLine in css:
                final_html.append("    "+cssLine)
            
            final_html.append('\n')
        else:
            final_html.append(line)
            
        
    with open(r'{}'.format(config_embed['path'] + config_embed['save_name']), mode='w') as new_f:

        new_f.writelines(final_html)

    if save==True:
            
        io.to_storage(bucket=config_embed['bucket'],
                bucket_folder=config_embed['bucket_folder'],
                file_name=config_embed['save_name'],
                path_to_file=config_embed['path']+config_embed['save_name'])

        print("Embed html uploaded!")


    
    
    


    
    