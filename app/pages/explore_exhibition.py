import streamlit as st 
import pandas as pd
import sys
import pathlib

from st_files_connection import FilesConnection

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_image = path_app + 'images/'
path_data = path_total + 'data/'


sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
# from app.pages.helper_funcs import *
from recommender.version_epsilon.helper_funcs import *

st.set_page_config(
    page_title='Exhibition Room',
    layout="wide",
    initial_sidebar_state="auto"  # optional
)

col1, col2 = st.columns([2, 6])
with col1:
    # Logo
    # -------------------------------------------------------------------------
    st.image(image = path_image + 'tms-logo.png',
            width = 320,
            use_container_width = False)
with col2:
    st.title('Exhibition Room')

@st.cache_resource
def load_dataframe():
    conn = st.connection('gcs', type=FilesConnection)
    return conn.read("totallymakescents/data/combined_df_classify_reviews.parquet", input_format="parquet", ttl=600)

try:
    # st.write("📄 Loading data...")
    df_search = load_dataframe()
    # st.success("✅ Data loaded!")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

df_notes_accords = pd.read_csv(f'{path_total}generated_data/notes.csv')
df_exhibition = pd.read_parquet(f'{path_data}exhibition/')
# df_notes_accords = pd.read_csv('../generated_data/notes.csv')
# df_exhibition = pd.read_parquet('../data/exhibition/')

button_names = df_exhibition['user_input'].unique()

queries_container = st.container(border=True)
results_container = st.container(border=True)

with queries_container:
    for button_name in button_names:
        if st.button(button_name, key=button_name):
            with results_container:
                st.write('User query: ', button_name)
                st.divider()
                st.write('We made some scents for you... ')
                index = df_exhibition[df_exhibition['user_input'] == f"{button_name}"]['index'].astype(int)
                # urls = df_exhibition[df_exhibition['user_input'] == f"{button_name}"]['url']
                explanations = df_exhibition[df_exhibition['user_input'] == f"{button_name}"]['explanation']
                for idx, explanation in zip(index, explanations):
                    potd = df_search.iloc[idx]
                    accord_data = [ str(potd.get(f'mainaccord{i}', '')) for i in range(1, 6) ]

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
                    
                    st.write('Explanation: ')
                    st.write(explanation)