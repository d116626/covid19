from paths import *
import pandas as pd
from datetime import datetime
from scripts.io import read_sheets
from scripts import manipulation
from scripts import io

def create_cards(df_states, vale):
    firstDay   = min(df_states['date'])
    lastDay    = max(df_states['date'])
    firstDayDt = datetime.strptime(str(firstDay)[:10], "%Y-%m-%d")
    lastDayDt  = datetime.strptime(str(lastDay)[:10], "%Y-%m-%d")
    daysOutbreak = (lastDayDt - firstDayDt).days

    today_data = df_states.query(f"state=='BRASIL' & date=='{lastDay}'")
    todayCases     = today_data['confirmed'].values[0]
    todayNewCases  = today_data['new_cases'].values[0]
    todayCasesPerc = todayNewCases/(todayCases -todayNewCases)

    todayDeaths   = today_data['deaths'].values[0]
    todayNewDeaths = today_data['new_deaths'].values[0]
    todayDeathsPerc = todayNewDeaths/(todayDeaths -todayNewDeaths)
    

    todayValeSuspects   = vale['suspeitas'].astype(int).sum()
    todayValeCases   = vale['confirmados'].astype(int).sum()
    todayValeDeaths   = vale['mortes'].astype(int).sum()



    replace_vars = {'daysOutbreak':daysOutbreak,
                    'todayNewCases':"{:,d}".format(todayNewCases),'todayCasesPerc':"{:.1%}".format(todayCasesPerc), "todayCases":"{:,d}".format(todayCases),
                    'todayNewDeaths':"{:,d}".format(todayNewDeaths),'todayDeathsPerc':"{:.1%}".format(todayDeathsPerc), "todayDeaths":"{:,d}".format(todayDeaths),
                    "todayValeSuspects":"{:,d}".format(todayValeSuspects),"todayValeCases":"{:,d}".format(todayValeCases),"todayValeDeaths":"{:,d}".format(todayValeDeaths)
                    }


    final_lines = []
    with open(r'../images/storage/br_indicator_model.html', mode='r') as f:
        for line in f.readlines():
            final_lines.append(line)

    for i in range(len(final_lines)):
        for var in replace_vars.keys():
            if var in final_lines[i]:
                final_lines[i] = final_lines[i].replace(var,str(replace_vars[var]))

    with open(r'../images/storage/br_indicator_final.html', mode='w') as new_f:

        new_f.writelines(final_lines)

    # return final_lines
    
    
    
def update_html():


    df = read_sheets('covid19_estados')

    df_states = manipulation.manipule_mytable(df)

    vale = read_sheets('covid19_vale_do_paraiba_e_litoral_norte').replace('',0)

    create_cards(df_states,vale)

    name= "br_indicator_final.html"
    path= f"../images/storage/{name}"

    io.to_storage(bucket='sv-covid19',
            bucket_folder='brasil',
            file_name=name,
            path_to_file=path)

if __name__ == "__main__":
    
    update_html()
