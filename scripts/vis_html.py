import pandas as pd
from datetime import datetime

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




