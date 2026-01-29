
import pandas as pd 



def preprocessing(file, file_embeddings):

    filename_livetest = file

    #input_livetest = pd.read_excel(filename_livetest, skiprows=2, usecols="A:P")
    input_livetest = pd.read_excel(filename_livetest)
    input_livetest = input_livetest[input_livetest['Date'].notnull()]
    input_livetest['Date'] = input_livetest['Date'].astype('datetime64[ns]')
    input_livetest["Date"] = pd.to_datetime(input_livetest["Date"]).dt.date


    input_livetest['all_ls'] = input_livetest.apply(lambda row: 1 + (row.all_ls / 100), axis = 1)
    input_livetest['all_l'] = input_livetest.apply(lambda row: 1 + (row.all_l / 100), axis = 1)
    input_livetest['t1_ls'] = input_livetest.apply(lambda row: 1 + (row.t1_ls / 100), axis = 1)
    input_livetest['t1_l'] = input_livetest.apply(lambda row: 1 + (row.t1_l / 100), axis = 1)
    input_livetest['t1_s'] = input_livetest.apply(lambda row: 1 + (row.t1_s / 100), axis = 1)
    input_livetest['all_s'] = input_livetest.apply(lambda row: 1 + (row.all_s / 100), axis = 1)
    
    input_livetest['gpt_all_ls'] = input_livetest.apply(lambda row: 1 + (row.gpt_all_ls / 100), axis = 1)
    input_livetest['gpt_all_l'] = input_livetest.apply(lambda row: 1 + (row.gpt_all_l / 100), axis = 1)
    input_livetest['gpt_t1_ls'] = input_livetest.apply(lambda row: 1 + (row.gpt_t1_ls / 100), axis = 1)
    input_livetest['gpt_t1_l'] = input_livetest.apply(lambda row: 1 + (row.gpt_t1_l / 100), axis = 1)
    input_livetest['gpt_t1_s'] = input_livetest.apply(lambda row: 1 + (row.gpt_t1_s / 100), axis = 1)
    input_livetest['gpt_all_s'] = input_livetest.apply(lambda row: 1 + (row.gpt_all_s / 100), axis = 1)    

    input_livetest['dj'] = input_livetest.apply(lambda row: 1 + (row.dj / 100), axis = 1)
    input_livetest['nasdaq'] = input_livetest.apply(lambda row: 1 + (row.nasdaq / 100), axis = 1)
    input_livetest['sp500'] = input_livetest.apply(lambda row: 1 + (row.sp500 / 100), axis = 1)


    filename_livetest_embeddings = file_embeddings

    #input_livetest = pd.read_excel(filename_livetest, skiprows=2, usecols="A:P")
    input_livetest_embeddings = pd.read_excel(filename_livetest_embeddings)
    input_livetest_embeddings = input_livetest_embeddings[input_livetest_embeddings['Date'].notnull()]
    input_livetest_embeddings['Date'] = input_livetest_embeddings['Date'].astype('datetime64[ns]')
    input_livetest_embeddings["Date"] = pd.to_datetime(input_livetest_embeddings["Date"]).dt.date


    input_livetest_embeddings['embeddings_all_l'] = input_livetest_embeddings.apply(lambda row: 1 + (row.embeddings_all_l / 100), axis = 1)
    input_livetest_embeddings['embeddings_t1_l'] = input_livetest_embeddings.apply(lambda row: 1 + (row.embeddings_t1_l / 100), axis = 1)

    input_livetest = input_livetest.merge(input_livetest_embeddings[['Date','embeddings_all_l','embeddings_t1_l','liquidita']], how = 'left', on = ('Date','liquidita'))

    max_date_livetest = input_livetest.Date.max()
    min_date_livetest = input_livetest.Date.min()

    return input_livetest, max_date_livetest, min_date_livetest




def my_filter_strategy (selection, df):
    if selection == 'All stocks Long & Short':
        df = df[df['classe_strategia'] == 'Base']
        return df
    elif selection == "All stocks Long":
        df = df[(df['classe_strategia'] == 'Base') & (df['action'] == 1)]
        return df
    elif selection == 'Top1 stock Long & Short':
        df = df[(df['classe_strategia'] == 'Base') & ((df['rank_day_pos'] == 1) | (df['rank_day_neg'] == 1))]
        return df
    elif selection == 'Top1 stock Long':
        df = df[(df['classe_strategia'] == 'Base') & (df['action'] == 1) & (df['rank_day_pos'] == 1)]
        return df
    elif selection ==  "All stocks Short":
        df = df[(df['classe_strategia'] == 'Base') & (df['action'] == -1)]
        return df
    elif selection == 'Top1 stock Short':
        df = df[(df['classe_strategia'] == 'Base') & (df['action'] == -1) & (df['rank_day_neg'] == 1)]
        return df
    if selection == 'GPT Filtered - All stocks Long & Short':
        df = df[(df['classe_strategia'] == 'GPT_Filtered')]
        return df
    elif selection == "GPT Filtered - All stocks Long":
        df = df[(df['classe_strategia'] == 'GPT_Filtered') & (df['action'] == 1)]
        return df
    elif selection == 'GPT Filtered - Top1 stock Long & Short':
        df = df[(df['classe_strategia'] == 'GPT_Filtered') & ((df['rank_day_pos'] == 1) | (df['rank_day_neg'] == 1))]
        return df
    elif selection == 'GPT Filtered - Top1 stock Long':
        df = df[(df['classe_strategia'] == 'GPT_Filtered') & (df['action'] == 1) & (df['rank_day_pos'] == 1)]
        return df
    elif selection ==  "GPT Filtered - All stocks Short":
        df = df[(df['classe_strategia'] == 'GPT_Filtered') & (df['action'] == -1)]
        return df
    elif selection ==  "GPT Filtered - All stocks Short - Up to Rank 10":
        df = df[(df['classe_strategia'] == 'GPT_Filtered_rank10') & (df['action'] == -1)]
        return df
    elif selection == 'GPT Filtered - Top1 stock Short':
        df = df[(df['classe_strategia'] == 'GPT_Filtered') & (df['action'] == -1) & (df['rank_day_neg'] == 1)]
        return df
    elif selection == 'GPT ONLY - All stocks Long':
        df = df[(df['classe_strategia'] == 'GPT_Only') & (df['action'] == 1)]
        return df
    elif selection == 'GPT ONLY - Top1 stock Long':
        df = df[(df['classe_strategia'] == 'GPT_Only') & (df['action'] == 1) & (df['rank_day_pos'] == 1)]
        return df
    else:
        return ''




def preprocessing_backtest(file, sheet):
    xx = pd.read_excel(file, sheet_name= sheet)
    xx = xx[['Date', 't1_ls', 't1_l', 'all_ls', 'all_l', 'dj','nasdaq']]
    xx['Date'] = xx['Date'].astype('datetime64[ns]')
    xx["Date"] = pd.to_datetime(xx["Date"]).dt.date

    xx['dj_lag'] = xx['dj'].shift(1)
    xx['nasdaq_lag'] = xx['nasdaq'].shift(1)

    xx['dj'] = xx.apply(lambda row: 1 + ((row.dj - row.dj_lag)/row.dj_lag), axis = 1)
    xx['nasdaq'] = xx.apply(lambda row: 1 + ((row.nasdaq - row.nasdaq_lag)/row.nasdaq_lag), axis = 1)

    max_date = xx.Date.max()
    min_date = xx.Date.min()

    return xx , max_date , min_date



def my_recode_strategy(selection):
    if selection == 'All stocks Long & Short':
        return 'all_ls'
    elif selection == "All stocks Long":
        return 'all_l'
    elif selection == 'Top1 stock Long & Short':
        return 't1_ls'
    elif selection == 'Top1 stock Long':
        return 't1_l'
    elif selection ==  "All stocks Short":
        return 'all_s'
    elif selection == 'Top1 stock Short':
        return 't1_s'
    if selection == 'GPT Filtered - All stocks Long & Short':
        return 'gpt_all_ls'
    elif selection == "GPT Filtered - All stocks Long":
        return 'gpt_all_l'
    elif selection == 'GPT Filtered - Top1 stock Long & Short':
        return 'gpt_t1_ls'
    elif selection == 'GPT Filtered - Top1 stock Long':
        return 'gpt_t1_l'
    elif selection ==  "GPT Filtered - All stocks Short":
        return 'gpt_all_s'
    elif selection == 'GPT Filtered - Top1 stock Short':
        return 'gpt_t1_s'    
    elif selection == 'GPT ONLY - All stocks Long':
        return 'embeddings_all_l'    
    elif selection == 'GPT ONLY - Top1 stock Long':
        return 'embeddings_t1_l'    
    else:
        return ''



def my_recode_benchmark(selection):
    if selection == 'Dow Jones':
        return 'dj'
    elif selection == "S&P500":
        return 'sp500'
    elif selection == 'Nasdaq':
        return 'nasdaq'
    else:
        return ''



def my_filter_benchmark(selection, df):
    if selection == 'Dow Jones':
        df = df[df['ticker'] == '^DJI']
        return df
    elif selection == "S&P500":
        df = df[df['ticker'] == '^GSPC']
        return df
    elif selection == 'Nasdaq':
        df = df[df['ticker'] == '^IXIC']
        return df
    else:
        return ''


def preprocessing_embeddings(file):

    filename_livetest = file

    #input_livetest = pd.read_excel(filename_livetest, skiprows=2, usecols="A:P")
    input_livetest = pd.read_excel(filename_livetest)
    input_livetest = input_livetest[input_livetest['Date'].notnull()]
    input_livetest['Date'] = input_livetest['Date'].astype('datetime64[ns]')
    input_livetest["Date"] = pd.to_datetime(input_livetest["Date"]).dt.date


    input_livetest['embeddings_all_l'] = input_livetest.apply(lambda row: 1 + (row.embeddings_all_l / 100), axis = 1)
    input_livetest['embeddings_t1_l'] = input_livetest.apply(lambda row: 1 + (row.embeddings_t1_l / 100), axis = 1)

    input_livetest['dj'] = input_livetest.apply(lambda row: 1 + (row.dj / 100), axis = 1)
    input_livetest['nasdaq'] = input_livetest.apply(lambda row: 1 + (row.nasdaq / 100), axis = 1)
    input_livetest['sp500'] = input_livetest.apply(lambda row: 1 + (row.sp500 / 100), axis = 1)
    
    max_date_livetest = input_livetest.Date.max()
    min_date_livetest = input_livetest.Date.min()

    return input_livetest, max_date_livetest, min_date_livetest