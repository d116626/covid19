#!/usr/bin/python3
import pandas as pd
import pandas_gbq
import pydata_google_auth
import gspread
from gcloud import storage
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import os
import requests
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../../credentials/gabinete_sv_credentials.json"



def _get_credentials_gbq():

    SCOPES = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/drive',
    ]

    credentials = pydata_google_auth.get_user_credentials(
        SCOPES,
        # Set auth_local_webserver to True to have a slightly more convienient
        # authorization flow. Note, this doesn't work if you're running from a
        # notebook on a remote sever, such as over SSH or with Google Colab.
        auth_local_webserver=True,
    )

    return credentials


def to_gbq(df, 
            table_name, 
            schema_name='simula_corona',
            project_id='robusta-lab', 
            **kwargs):
    """
    write a dataframe in Google BigQuery
    """
    
    destination_table = f'{schema_name}.{table_name}'

    pandas_gbq.to_gbq(
        df,
        destination_table,
        project_id,
        credentials=_get_credentials_gbq(),
        **kwargs
    )

def read_gbq(query, 
            project_id='robusta-lab', 
            **kwargs):
    """
    write a dataframe in Google BigQuery
    """

    return pandas_gbq.read_gbq(
        query,
        project_id,
        credentials=_get_credentials_gbq(),
        **kwargs)
    
    


def to_storage(bucket,bucket_folder,file_name,path_to_file):
    
    client = storage.Client(project='gavinete-sv')
    bucket = client.get_bucket(f'{bucket}')
    blob = bucket.blob(f'{bucket_folder}/{file_name}')
    blob.upload_from_filename(f'{path_to_file}')
    
    print('Done!')
    
    

def read_sheets(sheet_name):


    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('../../credentials/gabinete-sv-9aed310629e5.json', scope)
    gc = gspread.authorize(credentials)

    wks = gc.open(sheet_name).sheet1

    data = wks.get_all_values()
    headers = data.pop(0)

    return pd.DataFrame(data, columns=headers)


def load_brasilIO():
    ####### IMPORT DATA ######
    url = 'https://brasil.io/api/dataset/covid19/caso/data?format=json'
    df_final = pd.DataFrame()

    while url != None:
        
        print(url)
        response = requests.get(url)
        data = response.text
        parsed = json.loads(data)
        url = parsed['next']
        df = pd.DataFrame(parsed['results']).sort_values(by='confirmed',ascending=False)
        df_final = pd.concat([df_final,df], axis=0)
        
    
    brio = df_final.copy()

    mask = ((brio['is_last']==True) & (brio['place_type']=='city') & (brio['confirmed_per_100k_inhabitants'].notnull()))
    cols = ['city_ibge_code','city','confirmed','deaths','date','state']
    brio = brio[mask][cols]

    return brio, df_final


def load_wcota():
    df = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
    df['state'] = df['state'].str.replace('TOTAL','BRASIL')
    # df.to_csv('brasil_states.csv', index=False)
    dd = df.drop(['country','deaths'],1)
    
    return dd


