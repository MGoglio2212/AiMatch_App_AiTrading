
import pandas as pd
import streamlit as st
import openpyxl
import numpy as np 
import base64 
import altair as alt 
from DataProcessing import my_filter_strategy

st.set_page_config(page_title="LiveTest - Monthly Result", page_icon="📈")


#livetest_result = pd.read_excel(r"C:\Progetti\AIMatch\Streamlit_App\App\input_strategie.xlsx")
livetest_result = pd.read_excel("input_strategie.xlsx")

livetest_result['averageVolume'] = livetest_result['averageVolume'].fillna(0)
livetest_result['controvalore'] = livetest_result['averageVolume'] * livetest_result['Open']

livetest_result['Date'] = pd.to_datetime(livetest_result['date'].str[3:11], format='%Y%m%d')
livetest_result = livetest_result[livetest_result['Date'].notnull()]
livetest_result['Date'] = livetest_result['Date'].astype('datetime64[ns]')
livetest_result["Date"] = pd.to_datetime(livetest_result["Date"]).dt.date

max_volume = int(livetest_result.averageVolume.max())

### SIDEBAR 
st.sidebar.subheader("Parameter Selection")

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


#livetest_result = pd.read_excel(r"C:\Progetti\AIMatch\Streamlit_App\App\input_strategie.xlsx")


livetest_result = my_filter_strategy(add_selectbox_strategia, livetest_result)


livetest_result = livetest_result[(livetest_result['controvalore'] >= add_selectbox_min_controvalore) & 
                                  (livetest_result['controvalore'] <= add_selectbox_max_controvalore)]

livetest_result = livetest_result[(livetest_result['Open'] >= add_selectbox_min_price) & 
                                  (livetest_result['Open'] <= add_selectbox_max_price)]

if add_checkbox_shortable is True:
    livetest_result = livetest_result[livetest_result['is_shortable'] == 1]

analisi = livetest_result[['Date','rendimento_strategia']].groupby(['Date']).mean().rename(columns= {'rendimento_strategia':'result'}).reset_index()

analisi['result'] = (analisi['result'] * 100).fillna(0)
analisi['result'] = analisi.apply(lambda row: 1 + (row.result / 100), axis = 1)

analisi = analisi[(analisi['result'].notnull())]

analisi['year'] = analisi.apply(lambda row: row.Date.year, axis = 1)
analisi['month'] = analisi.apply(lambda row: row.Date.month, axis = 1)
analisi['yearmonth'] = analisi.apply(lambda row: str(row.year).zfill(4) + str(row.month).zfill(2), axis = 1)


analisi_2 = (
    analisi[['yearmonth', 'result']]
    .groupby('yearmonth', as_index=False)
    .agg(return_strategia=('result', 'prod'))
)

analisi_2['return_strategia'] = analisi_2['return_strategia'] - 1


asse_x = alt.X("yearmonth:N", 
                title="YearMonth",
                )

asse_y= alt.Y("return_strategia:Q" ,

                title="Monthly Return",  
                axis=alt.Axis(format=".0%"),
                )


chart = (
        alt.Chart(analisi_2)
        .mark_bar()
        .encode(
            x=asse_x,
            y=asse_y,
        )
    )

st.altair_chart(chart , use_container_width=True)

if add_selectbox_max_controvalore != 1000000000000 or add_selectbox_min_controvalore != 0:
    st.write("Il controvalore è dato dal prezzo open del giorno X moltiplicato per la versione più aggiornata disponibile del dato di yahoo finance (averageVolume)")
    st.write("Non rappresenta quindi il controvalore calcolato al momento in cui il ticker è stato raccomandato")

analisi_2['return_strategia'] = analisi_2['return_strategia'].apply('{:.1%}'.format)

st.table(analisi_2[['yearmonth','return_strategia']])