

import pandas as pd
import streamlit as st
import openpyxl


st.set_page_config(
    page_title="Main - AiMatch trading results"
)

st.sidebar.success("Select a page above.")

st.subheader("This app shows results of AiMatch trading strategies")
st.markdown(
"""
It is divided into 3 sections:
- 1: Live Test: results of livetest starting from Sep 22 -- Every day a strategy is defined at market open and evaluated at market close
- 2: Live Test Monthly Return: monthly returns of live test strategies
- 3: Daily Result: a check on daily result of livetest -- Emails with the strategy are shared to verifiy everything happened before market open and tickers to buy / sell were defined before market open
"""
)

st.divider()
st.write("Select a page on the left to start browsing results!")


