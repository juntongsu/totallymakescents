import streamlit as st 
import pandas as pd 
import numpy as np 
import sys 
import pathlib
import time
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
# path_total = '../../'

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_image = path_app + 'images/'
path_data = path_total + 'data/'
path_rec = path_total + 'recommender/'

from recommender.version_delta.recommender_func import *

st.set_page_config(
    page_title='TotallyMakeScents Lite',
    layout="centered",
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
    st.title('TotallyMakeScents')
    # st.write("What’s it smell like in the rain, at the end of a hiking trail full of blossoms? What fragrance would a wizard wear in a magical world? Looking for a bittersweet scent for a farewell party. Tell us about your story, and we MAKESCENTS.")
    st.write('A personal perfume recommender based on your tastes. We tailor the recommendation list by consulting the users like you and hunting down the notes you like. Search and select the perfumes, and we MakeScents.')

df_perf_names = pd.read_csv('{}tms_lite/cleaned_perf_names_0.csv'.format(path_data))
perf_names = df_perf_names['Perfume']

# input_left_column_0, input_right_column_0 = st.columns(2)
client_perfume_0 = st.multiselect(
    'You like these perfumes:',
    perf_names,
    placeholder='Type to search in the library',
    key='client_perfume_0')
# client_sentiemnt_0 = input_right_column_0.selectbox(
#     '',
#     sentiment_list,
#     key='client_sentiemnt_0')

input_left_column_1, input_right_column_1 = st.columns(2)
client_perfume_1 = input_left_column_1.multiselect(
    'You avoid these perfumes',
    perf_names[~perf_names.isin(client_perfume_0)],
    placeholder='Type to search in the library',
    key='client_perfume_1')
client_allergy_switch = input_right_column_1.toggle('You have allergy to one or more of these.')
if client_allergy_switch:
    client_allergy = input_right_column_1.multiselect(
        '',
        client_perfume_1,
        placeholder='Please specify',
        key='client_allergy')

button_left_column, button_mid_column, button_right_column = st.columns(3)
make_button = button_mid_column.button(
    'Totally Make Scents!',
    type='primary')

st.write("Can't find what you need? The size of our perfume library Lite is 804. ")
st.page_link('pages/tms_pro.py', label='Use the perfume database with over 20,000 perfumes :material/arrow_outward: ', icon='🦾')

persian_data_frame_clean = pd.read_csv('{}tms_lite/cleaned_persian.csv'.format(path_data))

language = 0
perf_names = pd.read_csv('{}tms_lite/cleaned_perf_names_{}.csv'.format(path_data, language))
vec_top = pd.read_csv('{}tms_lite/cleaned_vec_top_{}.csv'.format(path_data, language))
vec_mid = pd.read_csv('{}tms_lite/cleaned_vec_mid_{}.csv'.format(path_data, language))
vec_base = pd.read_csv('{}tms_lite/cleaned_vec_base_{}.csv'.format(path_data, language)) 

n_recs = 20

if make_button:
    make_progress_bar = st.progress(0, text='Making Scents...')
    client_perfume = pd.Series((client_perfume_0 + client_perfume_1), dtype='string', name='Perfume Name')
    client_sentiment = pd.Series((np.concatenate((np.ones(len(client_perfume_0), dtype=int), np.ones(len(client_perfume_1), dtype=int)*(-1)))), dtype='int', name='Sentiment')
    df_client = pd.concat([client_perfume, client_sentiment], axis=1)
    client_id = 0 
    slider = 0.5
    client_frame = add_user_id(df_client)
    make_progress_bar.progress(30, text='Making Scents from Users Like You...')

    if len(client_sentiment) == 0:
        recommendation_list = recommender_newbie(path_data)
    elif len(client_perfume_0) == 0:
        make_progress_bar.progress(70, text='Making Scents from the Notes You Like...')
        client_top, client_mid, client_base = user_vec_prep(client_perfume, client_sentiment, perf_names, vec_top, vec_mid, vec_base)
        temperature = np.array((1, 2, 1, 1.5), dtype=float)
        note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, client_perfume, client_top, client_mid, client_base, temperature)
        recommendation_list = note_recommendation_list['Perfume'].reset_index(drop=True)
    elif len(client_sentiment) < 5:
        user_recommendation_list = lazy_recommender(client_id, client_frame, persian_data_frame_clean)
        user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
        
        make_progress_bar.progress(70, text='Making Scents from the Notes You Like...')
        client_top, client_mid, client_base = user_vec_prep(client_perfume, client_sentiment, perf_names, vec_top, vec_mid, vec_base)
        temperature = np.array((1, 2, 1, 1.5), dtype=float)
        note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, client_perfume, client_top, client_mid, client_base, temperature)
        note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
        df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)

        # slider = pd.Series((tf_slider)).replace(dict_slider).values
        recommendation_list = combine_rec_lists(user_rec_list, note_rec_list, n_recs, slider)
    else:
        user_recommendation_list = recommender_users(client_id, client_frame, persian_data_frame_clean)
        user_rec_list = user_recommendation_list['Perfume Name'].reset_index(drop=True)
        
        make_progress_bar.progress(70, text='Making Scents from the Notes You Like...')
        client_top, client_mid, client_base = user_vec_prep(client_perfume, client_sentiment, perf_names, vec_top, vec_mid, vec_base)
        temperature = np.array((1, 2, 1, 1.5), dtype=float)
        note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, client_perfume, client_top, client_mid, client_base, temperature)
        note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
        df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)

        # slider = pd.Series((tf_slider)).replace(dict_slider).values
        recommendation_list = combine_rec_lists(user_rec_list, note_rec_list, n_recs, slider)
    
    if client_allergy_switch and (len(client_allergy) > 0):
        make_progress_bar.progress(90, text='Checking Allergy...')
        df_fra_standard = pd.read_csv('{}tms_lite/fra_standard.csv'.format(path_data))
        client_allergy = pd.Series(client_allergy, dtype='string')
        client_allergy_note, rec_list_note, rec_list_allergy_bool = client_allergy_finder(client_perfume, client_allergy, recommendation_list, df_fra_standard)
        output = pd.concat([recommendation_list, rec_list_allergy_bool], axis=1)
    else:
        output = recommendation_list
    
    st.dataframe(output, hide_index=True)
    make_progress_bar.progress(100, text='We Made Some Scents for You')

    time.sleep(1)
    make_progress_bar.empty()