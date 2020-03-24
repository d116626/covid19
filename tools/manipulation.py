import pandas as pd
import numpy as np

def create_br_not_sp(df):
    ### GET ONLY DA STATES TO MAKE THE BRASIL DATA
    mask = df['place_type'] == 'state'
    df['city'] = np.where(mask,df['state'],df['city'] )

    ### SUM STATES DATA
    mask = (df['place_type']=='state')
    df_brasil = df[mask].groupby(by=['date'], as_index=False).sum()

    ### FILL DATA FOR BRASIL
    df_brasil['city']='Brasil'
    df_brasil['city_ibge_code']=0
    df_brasil['estimated_population_2019'] = 209*10**6
    df_brasil['death_rate'] = np.nan
    df_brasil['is_last'] = [False for i in range(len(df_brasil)-1)] + [True]
    df_brasil['place_type'] = 'country'
    df_brasil['state'] = 'BR'


    ### SUM STATES DATA
    mask = (df['place_type']=='state') & (df['state']!='SP')
    not_sp = df[mask].groupby(by=['date'], as_index=False).sum()

    ### FILL DATA FOR BRASIL
    not_sp['city']='Exceto SP'
    not_sp['city_ibge_code']=1
    not_sp['estimated_population_2019'] = 209*10**6 - 45919049
    not_sp['death_rate'] = np.nan
    not_sp['is_last'] = [False for i in range(len(not_sp)-1)] + [True]
    not_sp['place_type'] = 'state'
    not_sp['state'] = 'not_sp'

    df = pd.concat([df_brasil[df.columns],not_sp[df.columns],df],axis=0)

    return df 