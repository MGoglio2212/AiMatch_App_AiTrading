
import pandas as pd
import streamlit as st
from io import BytesIO
import numpy as np 
import openpyxl 


# --- Definizione costanti e configurazione ---
COLONNA_FILTRO_AZIONE = 'action' 
COLONNA_FILTRO_STRATEGIA = 'classe_strategia'
COLONNA_FILTRO_RANK = 'rank_day'
VALORE_SHORT = -1

st.set_page_config(page_title="Comparison Interactive Brokers vs Teorico", page_icon="📈")

# --- 1. Funzione di caricamento e pre-elaborazione dati ---
# --- Lettura e pulizia delle colonne ---
@st.cache_data
def load_and_preprocess_data(file_path):
    
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        
        df[COLONNA_FILTRO_AZIONE] = pd.to_numeric(df[COLONNA_FILTRO_AZIONE], errors='coerce')
        df.dropna(subset=[COLONNA_FILTRO_AZIONE], inplace=True)
        
        if COLONNA_FILTRO_STRATEGIA in df.columns:
            df[COLONNA_FILTRO_STRATEGIA] = df[COLONNA_FILTRO_STRATEGIA].astype(str).str.strip().str.lower()
        
        return df
    except FileNotFoundError:
        st.error(f"Errore: File '{file_path}' non trovato.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Errore nel caricamento del file Excel o nella conversione dati: {e}")
        return pd.DataFrame() 

# Caricamento dati (avviene una sola volta grazie al caching)
df_base = load_and_preprocess_data("input_strategie.xlsx")

if df_base.empty:
    st.stop()

# --- 2. Combobox con filtri ---

strategie_disponibili = df_base[COLONNA_FILTRO_STRATEGIA].dropna().unique() if COLONNA_FILTRO_STRATEGIA in df_base.columns else []
opzioni_strategia = sorted(list(strategie_disponibili))

opzioni_direzione = ['Long & Short', 'Long', 'Short'] 
opzioni_rank = ['All', 'Top1 Rank'] 

st.sidebar.subheader("Seleziona Filtri")

selected_option_str = st.sidebar.selectbox(
    "1. Scegli la strategia da filtrare:",
    opzioni_strategia,
    index=0
)

selected_option_dir = st.sidebar.selectbox(
    "2. Scegli la direzione da filtrare:",
    opzioni_direzione
)

selected_option_ran = st.sidebar.selectbox(
    "3. Scegli il rank da filtrare:",
    opzioni_rank
)

# --- 3. Calcolo colonna rank unica per strategie long o short 
# Copia del DataFrame iniziale per le modifiche
df_risultato = df_base.copy()

if selected_option_dir == 'Long':
    df_risultato[COLONNA_FILTRO_RANK] = df_risultato['rank_day_pos']
elif selected_option_dir == 'Short':
    df_risultato[COLONNA_FILTRO_RANK] = df_risultato['rank_day_neg']
elif selected_option_dir == 'Long & Short':
    df_risultato[COLONNA_FILTRO_RANK] = df_risultato[['rank_day_pos','rank_day_neg']].min(axis=1)


# --- 4. Filtraggio Sequenziale ---
filtri_attivi = []

# --- Filtro Strategia ---
if selected_option_str != 'All':
    df_risultato = df_risultato[df_risultato[COLONNA_FILTRO_STRATEGIA] == selected_option_str]
    filtri_attivi.append(f"Strategia: **{selected_option_str}**")

# --- Filtro Direzione ---
if selected_option_dir == 'Short':
    df_risultato = df_risultato[df_risultato[COLONNA_FILTRO_AZIONE] == VALORE_SHORT]
    filtri_attivi.append("Direzione: **Short**")

elif selected_option_dir == 'Long':
    # Filtra tutti gli 'action' diversi da VALORE_SHORT (-1), che sono Long
    df_risultato = df_risultato[df_risultato[COLONNA_FILTRO_AZIONE] != VALORE_SHORT]
    filtri_attivi.append("Direzione: **Long**")
else:
    filtri_attivi.append("Direzione: **Long & Short**")

# --- Filtro Rank 1 (Top1) ---
if selected_option_ran == 'Top1 Rank':
    # Filtra i titoli con il rank più alto (posizione 1) nel set filtrato
    if COLONNA_FILTRO_RANK in df_risultato.columns: 
        df_risultato = df_risultato[df_risultato[COLONNA_FILTRO_RANK] == 1]
        filtri_attivi.append("Rank: **Top1**")
    else:
        st.warning(f"Attenzione: La colonna '{'rank_day'}' non è disponibile per il filtro Top1.")

        
    
# --- 5. Visualizzazione e Download ---

st.subheader("Risultati del Filtro")

if filtri_attivi:
    st.markdown(f"**Filtri Applicati:** {', '.join(filtri_attivi)}")
else:
    st.markdown("**Nessun filtro strategico applicato (DataFrame Completo).**")


df_risultato = df_risultato[df_risultato['Date'] >= '2023-01-01']
st.info(f"Numero Tickers: **{len(df_risultato)}** tickers")

# Mostra i risultati
st.dataframe(df_risultato[['date','Date','ticker','action',COLONNA_FILTRO_RANK,'rendimento_strategia','Open','Close','averageVolume','is_shortable']])

# Funzione per convertire il DataFrame in Excel
@st.cache_data
def to_excel(df_to_export):
    """Converte un DataFrame in formato Excel in memoria (BytesIO) usando openpyxl."""
    output = BytesIO()
  
    with pd.ExcelWriter(output, engine='openpyxl') as writer: 
        df_to_export.to_excel(writer, index=False, sheet_name='Risultato_Filtro')
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(df_risultato)
    
# Crea un nome file dinamico
nome_dir = selected_option_dir.replace(' ', '_').replace('&', 'e')
nome_str = selected_option_str.replace(' ', '_')
nome_rank = selected_option_ran.replace(' ', '')
file_name = f"dati_{nome_str}_{nome_dir}_{nome_rank}.xlsx"
    
st.download_button(
    label=f"Download File Excel Filtrato ({len(df_risultato)} righe)",
    data=excel_data,
    file_name=file_name,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)