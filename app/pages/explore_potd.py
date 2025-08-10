# -------------------------------------------------------------------------
# Import libraries
# -------------------------------------------------------------------------
import streamlit as st
import numpy as np
import pandas as pd

import sys
import pathlib
import datetime

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
# from app.pages.helper_funcs import *
from recommender.version_epsilon.helper_funcs import *

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_data = path_total + 'data/'


# -------------------------------------------------------------------------
# Title
# -------------------------------------------------------------------------
st.set_page_config(
    page_title='Perfume of the Day',
    layout="wide",                # ← uses the full width
    initial_sidebar_state="auto"  # optional
)

st.title('Perfume of the Day')

st.write(':material/calendar_today: ', datetime.date.today())

# -------------------------------------------------------------------------
# Load data and choose perfume of the day
# -------------------------------------------------------------------------
today = datetime.date.toordinal(datetime.date.today())
df_fra_standard = pd.read_csv(f'{path_data}tms_lite/fra_standard.csv')
index_potd = df_fra_standard.sample(1, random_state=today-1).index[0]
potd = df_fra_standard.iloc[index_potd]

accord_data = [ str(potd.get(f'mainaccord{i}', '')) for i in range(1, 6) ]
# e.g. ['rose', 'woody', fruity, aromatic, floral]
df_notes_accords = pd.read_csv(f'{path_total}generated_data/notes.csv')

potd_all_notes = potd['Top'] + ', ' + potd['Middle'] + ', ' + potd['Base']
potd_all_notes_series = pd.Series(potd_all_notes.split(', '), name='note')
df_potd_notes_accords = pd.merge(left=potd_all_notes_series, right=df_notes_accords[['note_group', 'note']], how='left', on='note')
potd_accords = df_potd_notes_accords['note_group'].value_counts()

col1, col2 = st.columns([1,10])
with col1:
    img = get_img_fragrantica(potd['url'])
    st.image(image = img,
            width = 100,
            use_container_width = False)
with col2:
    # Name, Brand, Link
    st.header(':material/fragrance: {name} by {brand}'.format(name=potd['Perfume'],brand=potd['Brand']))
    st.link_button(
        'Find more details and Reviews at Fragrantica.com :material/arrow_outward: ',
        f"{potd['url']}",
    )

col1, col2= st.columns([4, 6])

with col1:
    st.subheader(':material/ent: Accords')
    display_accords(potd_accords)
    
with col2:
    st.subheader('𓏊 Notes')
    st.write(' ')
    st.write(f":material/clock_loader_10: Top: {potd['Top']}")
    st.write(f":material/clock_loader_40: Middle: {potd['Middle']}")
    st.write(f":material/clock_loader_90: Base: {potd['Base']}")