import numpy as np
import pandas as pd

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline

from paths import *

from scripts.vis_dash import remove_acentos
from scripts.vis_dash import normalize_cols
from scripts import manipulation
from scripts.io import read_sheets
from scripts import scrap_data
from scripts import vis_dash
from scripts import io

from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')

import yaml

# from scripts import scrap_data
# df, df_new = scrap_data.load_data()

#### Load Data
df = io.load_total_table()

firstDay = datetime.strptime('2019-12-29', "%Y-%m-%d")
lastDay = datetime.strptime(str(max(df['date']))[:10], "%Y-%m-%d")
daysOutbreak = (lastDay - firstDay).days
latestDate=today

confirmedCases  = df[df['date']==today]['confirmed'].sum()
confirmedDeaths = df[df['date']==today]['confirmed'].sum()

#### TABLE FOR ALL COUNTRYS
df_all_countrys = manipulation.create_all_country_total_data(df)

#### TABLE FOR SINGLE COUNTRYS
df_single_country =manipulation.create_single_country_data(df)

names_ids = df.sort_values(by='confirmed', ascending=False)[['countryname','countrycode']].drop_duplicates(keep='first')
avaliable_geoids = names_ids['countrycode'].unique()
avaliable_countrynames = names_ids['countryname'].unique()


import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
				assets_folder='../assets/',
				external_stylesheets =[dbc.themes.BOOTSTRAP],
				meta_tags=[
					{"name": "author", "content": "Jun Ye"},]
				
				)

app.title = 'Coronavirus COVID-19 Global Monitor'

app.config['suppress_callback_exceptions'] = True # This is to prevent app crash when loading since we have plot that only render when user clicks.

dropdown1 =  dcc.Dropdown(
	id='selected_country',
	options=[{'label':i, 'value':j} for i,j in zip(avaliable_countrynames,avaliable_geoids)],
	# value=['US','IT','ES','DE', 'CN','FR','UK','BR'],
	value=['BR','US'],

	multi=True
)



# dropdown2 = dcc.Dropdown(
#     id='selected_country2',
#     options=[{'label':i, 'value':j} for i,j in zip(avaliable_countrynames,avaliable_geoids)],
#     value='BR'
# )

# print(confirmedCases)

from scripts import dash_statics


header = dash_statics.header(latestDate,confirmedCases)

card1 = dash_statics.cards(daysOutbreak)



app.layout = html.Div(style={'backgroundColor': '#fafbfd'},
	children = [
		
		dbc.Row(
			dbc.Col(header)
			),

    	dbc.Row([
			dbc.Col(card1),
		]),
		
		dbc.Row(
			dbc.Col(dropdown1)
			),
	
		dbc.Row([
			dbc.Col(
				dcc.Graph(id='country-graphic11'),
				# width=5,
				md=6,
			),
		
			dbc.Col(
				dcc.Graph(id='country-graphic12'),
				# width=5,
				md=6,
			),
		
		]),
	
	
		dbc.Row([

			dbc.Col(
				dcc.Graph(id='country-graphic21'),
				# width=5,
				md=6,
			),
			
			dbc.Col(
				dcc.Graph(id='country-graphic22'),
				# width=5,
				md=6,
			),
			
		]),
		
		

		# dbc.Row(
		#         dbc.Col(dropdown2),
		# ),
		
		# dbc.Row( 
		#     dbc.Col(dcc.Graph(id='country-graphic2')),
		# ),
		
		# html.Div([ 
		#     html.Iframe(src = "https://storage.cloud.google.com/sv-covid19/maps/cidades_estados.html?hl=pt-br", height=820, width=980)
			
		# ],className='row',style={'aling':'center'},),

])

# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })


@app.callback(
	[Output(component_id = 'country-graphic11', component_property = 'figure'),
	 Output(component_id = 'country-graphic12', component_property = 'figure'),
	 Output(component_id = 'country-graphic21', component_property = 'figure'),
	 Output(component_id = 'country-graphic22', component_property = 'figure')],
	
	[Input(component_id = 'selected_country', component_property= 'value')]
)
def update_graph(geoids):
	
	themes = yaml.load(open('../themes/custom_colorscales_dash.yaml', 'r'), Loader=yaml.FullLoader)

	fig11 = vis_dash.total_casos(
		df            = df_all_countrys,
		mask_countrys = df_all_countrys['countrycode'].isin(geoids),
		themes        = themes['all_world_dash'],
		var           = 'cases',
		date          = today,
		save          = False
		)
	
	fig12 = vis_dash.total_casos(
		df            = df_all_countrys,
		mask_countrys = df_all_countrys['countrycode'].isin(geoids),
		themes        = themes['all_world_dash'],
		var           = 'deaths',
		date          = today,
		save          = False
		)
	
	fig21 = vis_dash.total_casos(
		df            = df_all_countrys,
		mask_countrys = df_all_countrys['countrycode'].isin(geoids),
		themes        = themes['all_world_dash'],
		var           = 'new_cases',
		date          = today,
		save          = False
		)
	
	fig22 = vis_dash.total_casos(
		df            = df_all_countrys,
		mask_countrys = df_all_countrys['countrycode'].isin(geoids),
		themes        = themes['all_world_dash'],
		var           = 'new_deaths',
		date          = today,
		save          = False
		)

	return fig11, fig12, fig21, fig22

# @app.callback(
#     Output(component_id = 'country-graphic2', component_property = 'figure'),
#     [Input(component_id = 'selected_country2', component_property= 'value')]
# )
# def update_graph2(geoid):
	
#     themes = yaml.load(open('../themes/custom_colorscales_dash.yaml', 'r'), Loader=yaml.FullLoader)

#     fig = vis_dash.total_by_country_dash(
#         df     = df_single_country,
#         geoid  = geoid,
#         themes = themes['by_country_dash'],
#         data   = today,
#         save   = False
#         )
	
#     return fig

if __name__ == '__main__':
	app.run_server(debug=True)








