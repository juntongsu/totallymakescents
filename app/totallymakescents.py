import streamlit as st 
import pandas as pd 
import numpy as np 
import sys 
import pathlib
import time
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
# path_total = '../'

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
path_app = path_total + 'app/'
path_data = path_total + 'data/'
path_rec = path_total + 'recommender/'

from recommender.version_delta.recommender_func import *

# user_frame = pd.read_csv('{}input.csv'.format(path_app), header=None)
# user_frame.columns = ["Perfume Name", "Sentiment"]

st.title('TotallyMakeScents')
st.write("What’s it smell like in the rain, at the end of a hiking trail full of blossoms? What fragrance would a wizard wear in a magical world? Looking for a bittersweet scent for a farewell party. Tell us about your stroy, and we MAKESCENTS.")

language = 0
df_perf_names = pd.read_csv('{}cleaned_perf_names_{}.csv'.format(path_data, language))
perf_names = df_perf_names['Perfume']

# input_left_column_0, input_right_column_0 = st.columns(2)
client_perfume_0 = st.multiselect(
    'You like these perfumes:',
    perf_names,
    placeholder='Type to search in the library',
    help='I like it!',
    key='client_perfume_0')
# client_sentiemnt_0 = input_right_column_0.selectbox(
#     '',
#     sentiment_list,
#     key='client_sentiemnt_0')

input_left_column_1, input_right_column_1 = st.columns(2)
client_perfume_1 = input_left_column_1.multiselect(
    'You avoid these perfumes',
    perf_names,
    placeholder='Type to search in the library',
    help='Allergy help',
    key='client_perfume_1')
client_allergy_switch = input_right_column_1.toggle('You have allergy to one or more of these.')
if client_allergy_switch:
    client_allergy = input_right_column_1.multiselect(
        '',
        client_perfume_1,
        placeholder='Please specify',
        key='client_allergy')

ei_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extremely Extraverted (E)',
        'Extraverted',
        'Just A Little E',
        'Neutral',
        'Just A Little I',
        'Introverted', 
        'Extremely Introverted (I)'],
    value = ('Neutral'),
    key='ei_slider',
    help='Reorder.'
)

ns_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extremely Intuitive (N)',
        'Intuitive (N)',
        'Just A Little N',
        'Neutral',
        'Just A Little S',
        'Observant (S)', 
        'Extremely Observant (S)'],
    value = ('Neutral'),
    key='ns_slider',
    label_visibility='collapsed',
    help='This is a placeholder slider.'
)

tf_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extremely Thinking (T)',
        'Thinking (T)',
        'Just A Little T',
        'Neutral',
        'Just A Little F',
        'Feeling (F)', 
        'Extremely Feeling (F)'],
    value = ('Neutral'),
    key='tf_slider',
    label_visibility='collapsed',
    help='This is the real note-user slider.'
)

jp_slider = st.select_slider(
    'Your MBTI',
    options = [
        'Extremely Judging (J)',
        'Judging (J)',
        'Just A Little J',
        'Neutral',
        'Just A Little P',
        'Prospecting (P)', 
        'Extremely Prospecting (P)'],
    value = ('Neutral'),
    key='jp_slider',
    label_visibility='collapsed',
    help='This is a placeholder slider.'
)

button_left_column, button_mid_column, button_right_column = st.columns(3)
make_button = button_mid_column.button(
    'Totally Make Scents!',
    type='primary')

persian_data_frame_clean = pd.read_csv('{}cleaned_persian.csv'.format(path_data))
vec_top = pd.read_csv('{}cleaned_vec_top_{}.csv'.format(path_data, language))
vec_mid = pd.read_csv('{}cleaned_vec_mid_{}.csv'.format(path_data, language))
vec_base = pd.read_csv('{}cleaned_vec_base_{}.csv'.format(path_data, language))

dict_slider = {'Extremely Thinking (T)': 0., 'Thinking (T)': 0.2, 'Just A Little T': 0.4, 
            'Neutral': 0.5, 
            'Just A Little F': 0.6, 'Feeling (F)': 0.8, 'Extremely Feeling (F)': 1.}

n_recs = 20

if make_button:
    make_progress_bar = st.progress(0, text='Making Scents...')
    client_perfume = pd.Series((client_perfume_0 + client_perfume_1), dtype='string', name='Perfume Name')
    client_sentiment = pd.Series((np.concatenate((np.ones(len(client_perfume_0), dtype=int), np.ones(len(client_perfume_1), dtype=int)*(-1)))), dtype='int', name='Sentiment')
    df_client = pd.concat([client_perfume, client_sentiment], axis=1)
    client_id = 0 
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

        slider = pd.Series((tf_slider)).replace(dict_slider).values
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

        slider = pd.Series((tf_slider)).replace(dict_slider).values
        recommendation_list = combine_rec_lists(user_rec_list, note_rec_list, n_recs, slider)
    
    if len(client_allergy) > 0:
        df_fra_standard = pd.read_csv('{}fra_standard.csv'.format(path_data))
        rec_list_allergy_bool = client_allergy_finder(client_allergy, recommendation_list, df_fra_standard)
    
    output = pd.concat([recommendation_list, rec_list_allergy_bool], axis=1)
    output
    make_progress_bar.progress(100, text='We Made Some Scents for You')

    time.sleep(1)
    make_progress_bar.empty()