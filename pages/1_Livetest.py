

import pandas as pd
import streamlit as st
import openpyxl
import numpy as np 
import base64 
from DataProcessing import my_filter_strategy, my_filter_benchmark


st.set_page_config(page_title="Live test", page_icon="📈")

#livetest_result = pd.read_excel(r"C:\Progetti\AIMatch\Streamlit_App\App\input_strategie.xlsx")
livetest_result = pd.read_excel("input_strategie.xlsx")


#benchmark = livetest_result[livetest_result['classe_strategia'] == 'benchmark']

livetest_result = livetest_result[livetest_result['classe_strategia'] != 'benchmark']

livetest_result['averageVolume'] = livetest_result['averageVolume'].fillna(0)
livetest_result['controvalore'] = livetest_result['averageVolume'] * livetest_result['Open']



livetest_result['Date'] = pd.to_datetime(livetest_result['date'].str[3:11], format='%Y%m%d')
livetest_result = livetest_result[livetest_result['Date'].notnull()]
livetest_result['Date'] = livetest_result['Date'].astype('datetime64[ns]')
livetest_result["Date"] = pd.to_datetime(livetest_result["Date"]).dt.date

#benchmark = benchmark[benchmark['Date'].notnull()]
#benchmark['Date'] = benchmark['Date'].astype('datetime64[ns]')
#benchmark["Date"] = pd.to_datetime(benchmark["Date"]).dt.date


max_date_livetest = livetest_result.Date.max()
min_date_livetest = livetest_result.Date.min()

max_volume = int(livetest_result.averageVolume.max())

### SIDEBAR 
st.sidebar.subheader("Parameter Selection")

data_inizio = st.sidebar.date_input("Select starting date", 
                          min_value = min_date_livetest, 
                          max_value = max_date_livetest,
                          value = min_date_livetest)

data_fine = st.sidebar.date_input("Select end date", 
                          min_value = min_date_livetest, 
                          max_value = max_date_livetest,
                          value = max_date_livetest)

add_selectbox_strategia = st.sidebar.selectbox("Select AiMatch strategy",
        ("GPT Filtered - All stocks Short",
        "GPT Filtered - All stocks Short - Up to Rank 10",
         "GPT Filtered - All stocks Long",
         'GPT Filtered - All stocks Long & Short',        
        'GPT Filtered - Top1 stock Short',
        'GPT Filtered - Top1 stock Long',
        'GPT Filtered - Top1 stock Long & Short',
        "All stocks Short",
        "All stocks Long",
        'All stocks Long & Short', 
        'Top1 stock Short',
        'Top1 stock Long',
        'Top1 stock Long & Short',
        "GPT ONLY - All stocks Long",
        'GPT ONLY - Top1 stock Long'
))

add_selectbox_min_price = st.sidebar.number_input(label = "Select min opening price", 
                                                   value = 0 ,
                                                   min_value= 0 ,
                                                   max_value = 1000000) 
add_selectbox_max_price = st.sidebar.number_input(label = "Select max opening price", 
                                                   value = 1000000 ,
                                                   min_value= 0 ,
                                                   max_value = 1000000) 


add_selectbox_min_controvalore = st.sidebar.number_input(label = "Select min equivalent value (avg volume * price) ", 
                                                   value = 0 ,
                                                   min_value= 0 ,
                                                   max_value = 1000000000000) 
add_selectbox_max_controvalore = st.sidebar.number_input(label = "Select max equivalent value (avg volume * price)", 
                                                   value = 1000000000000 ,
                                                   min_value= 0 ,
                                                   max_value = 1000000000000) 

# checkbox per filtrare solo ticker shortable
add_checkbox_shortable = st.sidebar.checkbox("Mostra solo ticker shortable", value=False)


st.sidebar.caption("Standard strategies are available since mid September 2022 (with a gap from mid Oct 22 till start Nov 22)")
st.sidebar.caption("GPT Filtered strategies are available since Jan 2023")



livetest_result = livetest_result[(livetest_result['Date'] >= data_inizio) & (livetest_result['Date'] <= data_fine)]

livetest_result = my_filter_strategy(add_selectbox_strategia, livetest_result)



livetest_result = livetest_result[(livetest_result['controvalore'] >= add_selectbox_min_controvalore) & 
                                  (livetest_result['controvalore'] <= add_selectbox_max_controvalore)]

livetest_result = livetest_result[(livetest_result['Open'] >= add_selectbox_min_price) & 
                                  (livetest_result['Open'] <= add_selectbox_max_price)]


if add_checkbox_shortable is True:
    livetest_result = livetest_result[livetest_result['is_shortable'] == 1]

#benchmark = benchmark[(benchmark['Date'] >= data_inizio) & (benchmark['Date'] <= data_fine)]
#benchmark = my_filter_benchmark(add_selectbox_benchmark, benchmark)

analisi = livetest_result[['Date','rendimento_strategia']].groupby(['Date']).mean().rename(columns= {'rendimento_strategia':'result'}).reset_index()
analisi['result'] = (analisi['result'] * 100).fillna(0)
analisi['result'] = analisi.apply(lambda row: 1 + (row.result / 100), axis = 1)

#benchmark = benchmark[['Date','rendimento_strategia']].groupby(['Date']).mean().rename(columns= {'rendimento_strategia':'result_benchmark'}).reset_index()
#benchmark['result_benchmark'] = (benchmark['result_benchmark'] * 100).fillna(0)
#benchmark['result_benchmark'] = benchmark.apply(lambda row: 1 + (row.result_benchmark / 100), axis = 1)


#analisi = benchmark[['Date','result_benchmark']].merge(analisi , how = 'left', on = 'Date')
analisi['result'] = analisi['result'].fillna(1)

analisi['return_strategia'] = analisi['result'].cumprod()
#analisi['return_benchmark'] = analisi['result_benchmark'].cumprod()




final = analisi.tail(1).reset_index()


return_strategia = final['return_strategia'].iloc[0]
max_return_strategia = analisi['result'].max()  
min_return_strategia = analisi['result'].min()  



#return_benchmark = final['return_benchmark'].iloc[0]
#max_return_benchmark = analisi['result_benchmark'].max()  
#min_return_benchmark = analisi['result_benchmark'].min()    


numero_titoli = len(livetest_result)
numero_giorni_con_trading = len(analisi)


## aggiungo la % di ticker per cui la strategia ci ha preso (quindi ha rendimento positivo)
livetest_result['correct'] = np.where(livetest_result['rendimento_strategia'] > 0, 1, 0)
pct_correct = livetest_result['correct'].mean()

##stessa cosa per la % di giorni 
analisi['correct'] = np.where(analisi['result'] > 1, 1, 0)
pct_days_correct = analisi['correct'].mean()


st.subheader("Selected Strategy")
st.write("Following graph shows cumulative return for the selected strategy")

st.line_chart(data=analisi, x = 'Date', y =  ['return_strategia'], use_container_width=True)

st.divider()

st.subheader("Selected Strategy Returns")
col1, col2, col3 = st.columns(3)
col1.metric("Return in the selected period", '{:.1%}'.format(return_strategia - 1))
col2.metric("Max Daily Return",'{:.1%}'.format(max_return_strategia - 1))
col3.metric("Min Daily Return", '{:.1%}'.format(min_return_strategia - 1))

st.subheader("Selected Strategy win rate")
col1, col2, col3 = st.columns(3)
col1.metric("% ticker with positive return",'{:.1%}'.format(pct_correct))
col2.metric("% days with positive return",'{:.1%}'.format(pct_days_correct))


st.subheader("Selected Strategy Trading Activity")
col1, col2, col3 = st.columns(3)
col1.metric("Number of stocks traded in the period", numero_titoli)
col2.metric("Number of days with at least one stock traded in the period",numero_giorni_con_trading)
col3.metric("Average number of stock per trading day", f"{numero_titoli/numero_giorni_con_trading:.1f}")


#st.subheader("Selected Benchmark Returns")
#col1, col2, col3 = st.columns(3)
#col1.metric("Return in the selected period", '{:.1%}'.format(return_benchmark - 1))
#col2.metric("Max Daily Return",'{:.1%}'.format(max_return_benchmark - 1))
#col3.metric("Min Daily Return", '{:.1%}'.format(min_return_benchmark - 1))


if add_selectbox_max_controvalore != 1000000000000 or add_selectbox_min_controvalore != 0:
    st.write("Il controvalore è dato dal prezzo open del giorno X moltiplicato per la versione più aggiornata disponibile del dato di yahoo finance (averageVolume)")
    st.write("Non rappresenta quindi il controvalore calcolato al momento in cui il ticker è stato raccomandato")
