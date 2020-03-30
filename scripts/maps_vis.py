import folium
import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap

import branca.colormap as cm
import branca

def get_map(dd_final,variavel, ufs):
    
    #min and max color map range
    minn = min(dd_final[variavel])
    maxx = max(dd_final[variavel])

    #create a equal divised range
    indexx = [minn]
    n_divisions = 4
    factor = round(((maxx - minn)/n_divisions))
    for i in range(1,n_divisions):
        number  = minn+i*factor
        indexx.append(number)
    indexx.append(maxx)

    #add the colors to colormap
    # ['#DB4325','#ECA14D','#E6E1BC','#5BC2AF','#096264']
    colors = ['#E6E1BC','#ECA14D','#F9A602','#F05E23','#883002']
    colormap = colormap = cm.LinearColormap(colors=colors, index=indexx,vmin=round(minn),vmax=maxx)


    #create map
    mymap = folium.Map(location=[-15.734392, -54.026147], zoom_start=5,tiles=None)
    
    #def type
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)

    #legend caption

    colormap.caption = "Número de Casos"


    #add color in polygons
    style_function = lambda x: {"weight":0.5, 
                                'color':'black',
                                'fillColor':'rgba(0,0,0,0)', 
                                'fillOpacity':0.75}

    #add edge in map
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.01, 
                                    'weight': 1.4}
    
    
        
    
    NIL=folium.features.GeoJson(
            ufs,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            #show the chosen variables
            tooltip=folium.features.GeoJsonTooltip(
                fields=['Estado','Casos','Mortes','Data'],
    #             aliases=['Neighborhood','% of foreign resident population'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                sticky=True
            )
        )
        
    mymap.add_child(NIL)





    #add color in polygons
    style_function = lambda x: {"weight":0.5, 
                                'color':'black',
                                'fillColor':colormap(x['properties'][variavel]), 
                                'fillOpacity':0.75}

    #add edge in map
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    
    NIL=folium.features.GeoJson(
            dd_final,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            #show the chosen variables
            tooltip=folium.features.GeoJsonTooltip(fields=['Estado','Município','Casos'],
    #             aliases=['Neighborhood','% of foreign resident population'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                sticky=True
            )
    )
    
    
    colormap.add_to(mymap)
    mymap.add_child(NIL) 

    return(mymap)

