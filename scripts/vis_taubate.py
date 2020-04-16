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



def taubate_faixas(confirmados, themes, config, save=False):
    
    bins = pd.IntervalIndex.from_tuples([(0, 20), (21, 30), (31, 40), (41, 50), (51, 60), (61, 70), (71, 80),(81, 90),(91, 200)])
    bined = pd.cut(confirmados['idade'].astype(int), bins).value_counts()

    idades = pd.DataFrame(data = bined.index.tolist(), columns=['faixa'])
    idades['quantidade'] = bined.values.tolist()

    idades = idades.sort_values(by='faixa')

    labels = ['0 a 20', '21 a 30', '31 a 40', '41 a 50',' 51 a 60',' 61 a 70',' 71 a 80',' 81 a 90','+91']
    idades['faixa'] = labels
    
    trace = go.Bar(
        name=adjusts[status]['nome'],
        x=idades['quantidade'], 
        y=idades['faixa'],
        marker=dict(color=themes['data']['marker']['color'],
                   line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
                   ),
        hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size'])),
        orientation='h'
    )

    data = [trace]


    from scripts import vis_layout


    layout = vis_layout.get_layout(themes)

    fig = go.Figure(data, layout)
    
    
    if save == True:
        name= f"{config['save_name']}"
        path= f"{config['path_save']}{name}"
        
        plot(fig, filename=path, auto_open=False)
        
        io.to_storage(bucket=config['bucket'],
                        bucket_folder=config['bucket_folder'],
                        file_name=name,
                        path_to_file=path)

    return fig



def taubate_pie(confirmados, themes, config, save=False):

    trace = go.Pie(
        labels=confirmados['sexo'].value_counts().index,
        values=confirmados['sexo'].value_counts().values,
        hoverinfo='label+percent',
        textinfo='value',
        textfont_size=30,
        marker=dict(
            colors=themes['colors'], 
            line=dict(color=themes['data']['marker']['color'], width=themes['data']['line_width'])
        ),
        hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))
    )

    data = [trace]


    from scripts import vis_layout


    layout = vis_layout.get_layout(themes)

    fig = go.Figure(data, layout)
    
    if save == True:
        name= f"{config['save_name']}"
        path= f"{config['path_save']}{name}"

        plot(fig, filename=path, auto_open=False)

        io.to_storage(bucket=config['bucket'],
                        bucket_folder=config['bucket_folder'],
                        file_name=name,
                        path_to_file=path)

    return fig


def get_map_taubate(df,status_adjusts, config_map, save=False):
    mymap = folium.Map(location=[ -23.021628, -45.556273 ], zoom_start=13,tiles=None,control_scale=False, max_bounds=True, max_zoom=9,max_lat=-22.883089, min_lat=-23.292957, min_lon= -45.866733, max_lon=-45.117794)

    folium.TileLayer('CartoDB positron',control=False).add_to(mymap)


    
    dd = df.copy()
    dd['count']=1
    bairos_list = dd.groupby(['bairro','status','lat','lon'], as_index=False).sum().sort_values(by='count', ascending=False)['bairro'].unique()

    for bairro in bairos_list:

        dd = df.query(f'bairro == "{bairro}"')
        dd['count']=1
        bairro_table = dd.groupby(['bairro','status','lat','lon'], as_index=False).sum().sort_values(by='count', ascending=False)

        status_list = bairro_table.sort_values(by='count', ascending=False)['status'].to_list()
        
        for status in status_list:

            mask = bairro_table['status']==status
            bairro_row = bairro_table[mask]
            
             
            r   = int(bairro_row['count'].values[0])*40
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


def taubate_update_html(tb_cases, config_embed, save=False):

    lastDay    = max(tb_cases['data'])
    todayDate  = lastDay.strftime("%d/%m/%Y")
    firstDay   = '2020-03-12'
    firstDayDt = datetime.strptime(str(firstDay)[:10], "%Y-%m-%d")
    lastDayDt  = datetime.strptime(str(lastDay)[:10], "%Y-%m-%d")
    daysOutbreak = (lastDayDt - firstDayDt).days

    today_data =  tb_cases.query(f"data =='{lastDay}'")
    
    todayDeaths   = today_data['obito'].values[0]
    todayNewDeaths = today_data['obito_day'].values[0]
    todayDeathsPerc = todayNewDeaths/(todayDeaths -todayNewDeaths)

    today_data = tb_cases.query(f"data=='{lastDay}'")
    todayCases     = today_data['confirmado'].values[0] - todayDeaths
    todayNewCases  = today_data['confirmado_day'].values[0]
    todayCasesPerc = todayNewCases/(todayCases - todayNewCases)


    todayRecover     = today_data['descartado'].values[0]
    todayNewRecover  = today_data['descartado_day'].values[0]
    todayRecoverPerc = todayNewRecover/(todayRecover - todayNewRecover)


    todaySuspects     = today_data['em_analise'].values[0]
    todayNewSuspects  = today_data['em_analise_day'].values[0]
    todaySuspectsPerc = todayNewSuspects/(todaySuspects - todayNewSuspects)



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


    
    
    


    
    