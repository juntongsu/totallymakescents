import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def find_overlap(df_persian, df_data_notes, language):
    perf_name_overlap = []
    perf_url_overlap = []
    if language == 0:
        perf_name_unique = df_persian['Perfume Name'].drop_duplicates().str.lower().str.replace(' ', '-').convert_dtypes().to_list()
        perf_name_original = df_persian['Perfume Name'].drop_duplicates().convert_dtypes().to_list()
        perf_name_data_notes = df_data_notes['Perfume'].convert_dtypes()
        perf_url_data_notes = df_data_notes['url'].convert_dtypes()
        perf_rate_data_notes = df_data_notes['Rating Count'].convert_dtypes()
        
    elif language == 1:
        perf_name_unique = df_persian['Perfume Name'].drop_duplicates().convert_dtypes().to_list()
        perf_name_original = perf_name_unique
        perf_name_data_notes = df_data_notes['name'].convert_dtypes()
        perf_url_data_notes = df_data_notes['url'].convert_dtypes()
        perf_rate_data_notes = df_data_notes['rating_count'].fillna('0 c').str.split(' ').str[0].astype('int')
    
    for i in range(len(perf_name_original)):
        perf_name_multi = perf_name_data_notes[perf_name_data_notes == perf_name_unique[i]]
        if len(perf_name_multi) == 1:
            perf_name_overlap += [perf_name_original[i]]
            perf_url_overlap += perf_url_data_notes[perf_name_data_notes == perf_name_unique[i]].to_list()
        elif len(perf_name_multi) > 1:
            perf_rate_multi = perf_rate_data_notes[perf_name_data_notes == perf_name_unique[i]]
            if perf_rate_multi.sort_values(ascending=False).values[0] > 3*perf_rate_multi.sort_values(ascending=False).values[1]:
                perf_name_overlap += [perf_name_original[i]]
                perf_url_multi = perf_url_data_notes[perf_name_data_notes == perf_name_unique[i]]
                perf_url_overlap += [perf_url_multi[perf_rate_multi.idxmax()]]
    
    perf_name_overlap = pd.Series(perf_name_overlap, dtype='string').rename('Perfume')
    perf_url_overlap = pd.Series(perf_url_overlap, dtype='string').rename('url')
    # print('Found {} overlap perfumes between datasets'.format(len(perf_name_overlap)))
    perf_overlap = pd.concat([perf_name_overlap, perf_url_overlap], axis=1)
    return perf_overlap

def notes_vec_prep(perf_overlap, df_data_notes, language):
    if language == 0:
        df_perf_notes = df_data_notes[(df_data_notes['url'].isin(perf_overlap['url']))][['Perfume', 'Top', 'Middle', 'Base']]
        
        perf_name_lower = pd.Series(perf_overlap['Perfume'].str.lower().str.replace(' ', '-').convert_dtypes(), name='Lower')
        perf_name_dict = pd.concat([perf_overlap['Perfume'], perf_name_lower], axis=1)
        perf_names = df_perf_notes['Perfume'].convert_dtypes()
        perf_index = perf_names.reset_index().set_index('Perfume').loc[perf_name_dict.Lower].reset_index().set_index('index').index
        perf_names = perf_name_dict.set_index(perf_index)['Perfume'].sort_index()

        vec_top = df_perf_notes['Top'].str.get_dummies(sep=', ').astype('float')
        vec_mid = df_perf_notes['Middle'].str.get_dummies(sep=', ').astype('float')
        vec_base = df_perf_notes['Base'].str.get_dummies(sep=', ').astype('float')
    elif language == 1:
        df_perf_notes = df_data_notes[df_data_notes['url'].isin(perf_overlap['url'])][['name', 'top_notes', 'middle_notes', 'bottom_notes']]
        perf_names = pd.Series(df_perf_notes['name'].convert_dtypes(), name='Perfume')
        
        vec_top = df_perf_notes['top_notes'].str.replace(r".\]", "", regex=True).str.replace(r"\[.", "", regex=True).str.replace("', '", ", ", regex=False).str.get_dummies(sep=', ').astype('float')
        vec_mid = df_perf_notes['middle_notes'].str.replace(r".\]", "", regex=True).str.replace(r"\[.", "", regex=True).str.replace("', '", ", ", regex=False).str.get_dummies(sep=', ').astype('float')
        vec_base = df_perf_notes['bottom_notes'].str.replace(r".\]", "", regex=True).str.replace(r"\[.", "", regex=True).str.replace("', '", ", ", regex=False).str.get_dummies(sep=', ').astype('float')

    print('Top notes: {}, middle notes: {}, base notes: {}'.format(vec_top.shape[1], vec_mid.shape[1], vec_base.shape[1]))
    return perf_names, vec_top, vec_mid, vec_base

def input_perfume():
    # user_perfume = perf_overlap['Perfume'].sample(n=5, random_state=1).values
    # user_sentiment = np.random.choice((-1., 1.), 5)

    # user_perfume = df_persian['Perfume Name'][df_persian['User ID'] == 38947].reset_index(drop=True)
    # user_sentiment = df_persian['Sentiment'][df_persian['User ID'] == 38947].to_numpy()
    # user_sentiment = np.where(user_sentiment == 'Positive', 1., -1.)

    # df_input = pd.concat([user_perfume, pd.Series(user_sentiment, dtype=int)], axis=1)
    # df_input.to_csv('{}input.csv'.format(path_data), header=False, index=False)

    df_input = pd.read_csv('input.csv', header=None)
    user_perfume = df_input.iloc[:, 0].to_list()
    user_sentiment = df_input.iloc[:, 1].to_numpy()

    print('User Opinions:')
    for i in range(len(user_sentiment)):
        print('{}, {}'.format(user_perfume[i], user_sentiment[i]))
    return user_perfume, user_sentiment

def user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base):
    for i in range(len(user_sentiment)):
        if i == 0:
            user_top = vec_top.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
            user_mid = vec_mid.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
            user_base = vec_base.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
        else:
            user_top = user_top.add(vec_top.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)
            user_mid = user_mid.add(vec_mid.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)
            user_base = user_base.add(vec_base.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)

    return user_top, user_mid, user_base

def recommender_notes(perf_names, vec_top, vec_mid, vec_base, user_perfume, user_top, user_mid, user_base, temperature):
    vec_allnotes = vec_top.add(vec_mid.add(vec_base, fill_value=0), fill_value=0)
    user_allnotes = user_top.add(user_mid.add(user_base, fill_value=0), fill_value=0)
    
    user_top = user_top.apply(np.sum, axis=0)
    user_mid = user_mid.apply(np.sum, axis=0)
    user_base = user_base.apply(np.sum, axis=0)
    user_allnotes = user_allnotes.apply(np.sum, axis=0)

    user_top = np.reshape(user_top, (1, -1))
    user_mid = np.reshape(user_mid, (1, -1))
    user_base = np.reshape(user_base, (1, -1))
    user_allnotes = np.reshape(user_allnotes, (1, -1))

    sim_top = cosine_similarity(user_top, vec_top)[0]
    sim_mid = cosine_similarity(user_mid, vec_mid)[0]
    sim_base = cosine_similarity(user_base, vec_base)[0]
    sim_allnotes = cosine_similarity(user_allnotes, vec_allnotes)[0]

    sim_total = sim_top * temperature[0] + sim_mid * temperature[1] + sim_base * temperature[2] + sim_allnotes * temperature[-1] 
        
    sim_total = pd.Series(sim_total, index=perf_names.index, name='Score')
    df_sim_total = pd.concat([perf_names, sim_total], axis=1)

    rec_list = df_sim_total.nlargest(20+len(user_perfume), 'Score', keep='all')
    rec_list = rec_list.drop(rec_list[rec_list['Perfume'].isin(user_perfume)].index)#.reset_index(drop=True)

    # print(rec_list)
    
    return rec_list