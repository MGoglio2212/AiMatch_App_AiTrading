import pandas as pd
import streamlit as st
import openpyxl
import numpy as np 
import base64 
import datetime as dt 
import os 


from DataProcessing import preprocessing

st.set_page_config(page_title="Daily Results", page_icon="📈")

start_date_gpt = dt.date(2023, 8, 14)

input_livetest, max_date_livetest, min_date_livetest = preprocessing("Flywall_test_6_mesi.xlsx", "Flywall_Historic_Result - EMBEDDINGS.xlsx")

### SIDEBAR 
st.sidebar.subheader("Select a day to check recommendations and results")

data_selection = st.sidebar.date_input("Select a date", 
                          min_value = min_date_livetest, 
                          max_value = max_date_livetest,
                          value = max_date_livetest)


d = data_selection.day
m = data_selection.month
y = data_selection.year 


#il display pdf come file pdf non funziona in cloud. 
#trasformo in immagine e mostro immagine

st.subheader("Selected Day Trading Recommendations")
st.write("Email sent around 9.27 AM EST to suggest ticker to buy / sell")
f1 = "Mail_Images_Censored/Gmail - Trading Recommendations - " + str(y) + str(m).zfill(2) + str(d).zfill(2) + ".pdf.jpg"

if os.path.isfile(f1):
    st.image(f1)
else:
    st.write("There is no Recommendations email for the selected day. It may be a weekend, public USA holiday, or an occasional technical error on email server may have occured. Please select another day")

st.divider()
## replico per strategie gpt 
if y <= 2023 and (m < 10 or (m == 10 and d <30)):
    f1 = "Mail_Images_Censored/Gmail - Trading Recommendations STRATEGIE GPT- " + str(y) + str(m).zfill(2) + str(d).zfill(2) + ".pdf.jpg"

    if os.path.isfile(f1):
        st.image(f1)
    else:
        if data_selection >= start_date_gpt: 
            st.write("There is no Recommendations email for the selected day. It may be a weekend, public USA holiday, or an occasional technical error on email server may have occured. Please select another day")
        else:
            st.write("Live test for GPT FILTERED STRATEGIES started from 14th Aug 2023. From Jan23 till Aug23 strategies were backtested and therefore no email is available")
