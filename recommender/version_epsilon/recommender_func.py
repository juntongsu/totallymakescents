import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


################################################# recommender_notes_func
def find_overlap(df_persian, df_data_notes):
    perf_name_overlap = []
    perf_url_overlap = []

    perf_name_original = df_persian['Perfume Name'].drop_duplicates().convert_dtypes().to_list()
    perf_name_data_notes = df_data_notes['Perfume'].convert_dtypes()
    perf_url_data_notes = df_data_notes['url'].convert_dtypes()
    perf_rate_data_notes = df_data_notes['Rating Count'].convert_dtypes()
            
    for i in range(len(perf_name_original)):
        perf_name_multi = perf_name_data_notes[perf_name_data_notes == perf_name_original[i]]
        if len(perf_name_multi) == 1:
            perf_name_overlap += [perf_name_original[i]]
            perf_url_overlap += perf_url_data_notes[perf_name_data_notes == perf_name_original[i]].to_list()
        elif len(perf_name_multi) > 1:
            perf_rate_multi = perf_rate_data_notes[perf_name_data_notes == perf_name_original[i]]
            if perf_rate_multi.sort_values(ascending=False).values[0] > 3*perf_rate_multi.sort_values(ascending=False).values[1]:
                perf_name_overlap += [perf_name_original[i]]
                perf_url_multi = perf_url_data_notes[perf_name_data_notes == perf_name_original[i]]
                perf_url_overlap += [perf_url_multi[perf_rate_multi.idxmax()]]
    
    perf_name_overlap = pd.Series(perf_name_overlap, dtype='string').rename('Perfume')
    perf_url_overlap = pd.Series(perf_url_overlap, dtype='string').rename('url')
    # print('Found {} overlap perfumes between datasets'.format(len(perf_name_overlap)))
    perf_overlap = pd.concat([perf_name_overlap, perf_url_overlap], axis=1)
    return perf_overlap

def notes_accords_vec_prep(df_data_notes):    
    perf_names = df_data_notes['Perfume'].convert_dtypes()
    vec_top = df_data_notes['Top'].str.get_dummies(sep=', ').astype('float')
    vec_mid = df_data_notes['Middle'].str.get_dummies(sep=', ').astype('float')
    vec_base = df_data_notes['Base'].str.get_dummies(sep=', ').astype('float')

    df_accords = df_data_notes[['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']].astype('str').agg(','.join, axis=1)
    vec_accords = df_accords.str.get_dummies(sep=',')#.drop(columns=['nan'])

    print('Top notes: {}, middle notes: {}, base notes: {}, accords: {}'.format(vec_top.shape[1], vec_mid.shape[1], vec_base.shape[1], vec_accords.shape[1]))
    return perf_names, vec_top, vec_mid, vec_base, vec_accords

def user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base, vec_accords):
    for i in range(len(user_sentiment)):
        if i == 0:
            user_top = vec_top.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
            user_mid = vec_mid.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
            user_base = vec_base.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
            user_accords = vec_accords.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i]
        else:
            user_top = user_top.add(vec_top.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)
            user_mid = user_mid.add(vec_mid.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)
            user_base = user_base.add(vec_base.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)
            user_accords = user_accords.add(vec_accords.loc[perf_names[perf_names == user_perfume[i]].index] * user_sentiment[i], fill_value=0.)

    return user_top, user_mid, user_base, user_accords

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


################################################# recommender_users_func


def enum_ratings(sentiment):
    if sentiment == "Positive":
        return 1.0
    if sentiment == "Negative":
        return -1.0
    else: 
        return 0.0

def has_opinions(user, frame):
    return set(frame.loc[(frame['User ID'] == user)]["Perfume Name"])

def share_opinions(user_1, user_2, frame_1,frame_2):
    return has_opinions(user_1,frame_1).intersection(has_opinions(user_2,frame_2))

def reference_users(user_1, frame_1,frame_2, commonality=1):
    users= set(frame_2['User ID'])
    relevant_users=set()
    for user_2 in users:
        if len(share_opinions(user_1,user_2,frame_1,frame_2))>= commonality:
            relevant_users.add(user_2)
    return relevant_users

def accuracy_index(user_1, user_2, frame_1,frame_2, weight = 1):
    ind = len(share_opinions(user_1, user_2, frame_1,frame_2))/len(has_opinions(user_1, frame_1))
    return ind**weight

def sentiment_vector(user, frame, perfumes = "ALL"):
    if perfumes == "ALL":
        sentiment = frame.loc[(frame["User ID"] == user)][["Perfume Name","Sentiment"]]
    else:
        sentiment = frame.loc[((frame["User ID"] == user) & (frame["Perfume Name"].isin(perfumes)))][["Perfume Name","Sentiment"]]
    
    sentiment = sentiment.sort_values(by="Perfume Name")

    return sentiment["Sentiment"].to_numpy()

def cos_index_1(user_1,user_2,frame_1,frame_2):
    shared = share_opinions(user_1, user_2, frame_1,frame_2)
    vector_1 = sentiment_vector(user_1, frame_1, shared)
    vector_2 = sentiment_vector(user_2, frame_2, shared)
    return cosine_similarity([vector_1],[vector_2])[0][0]

def multiplier(user_1,user_2,frame_1,frame_2,weight=1.0):
    return cos_index_1(user_1,user_2,frame_1,frame_2)*accuracy_index(user_1, user_2, frame_1,frame_2,weight)

def adjust_rating_1(rating, multi):
    return rating*multi

def adjusted_frame_1(user_1,frame_1,frame_2, commonality=1,weight = 1):
    relevant_users = reference_users(user_1, frame_1,frame_2, commonality)
    new_frame = frame_2.loc[(frame_2['User ID'].isin(relevant_users))]
    for user_2 in relevant_users:
        m = multiplier(user_1,user_2,frame_1,frame_2,weight)
        adjust = new_frame.loc[(new_frame['User ID']==user_2), "Sentiment"].apply(adjust_rating_1,args=([m]))
        new_frame.update(adjust)
    return new_frame

def ratings(user_1,frame_1,frame_2, commonality=1,weight=1, type = "sum"):
    known_perfumes = has_opinions(user_1, frame_1)

    adjusted_ratings = adjusted_frame_1(user_1,frame_1,frame_2,commonality,weight)
    adjusted_ratings = adjusted_ratings.loc[(~adjusted_ratings["Perfume Name"].isin(known_perfumes))]

    adjusted_ratings["Similarity"] = adjusted_ratings.groupby('Perfume Name')['Sentiment'].transform(type)
    adjusted_ratings = adjusted_ratings[["Perfume Name", "Similarity"]].drop_duplicates()

    return adjusted_ratings

def recommender_users(user_1,frame_1,frame_2, commonality=2,weight=1, top=20, type="sum"):
    adjusted_ratings = ratings(user_1,frame_1,frame_2, commonality, weight, type)
    rec_list = adjusted_ratings.convert_dtypes().nlargest(top, 'Similarity', keep = "all")
    
    return rec_list[["Perfume Name", "Similarity"]]

def add_user_id(frame, user_id = 0):
    count_row = frame.shape[0]
    id_row = np.repeat(user_id, count_row)
    frame["User ID"] = id_row
    return frame


################################################# recommender_lazy_func


def has_positive_opinions(user, frame):
    return set(frame.loc[((frame['User ID'] == user)&(frame["Sentiment"]==1.0))]["Perfume Name"])

def share_positive_opinions(user_1, user_2, frame_1,frame_2):
    return has_positive_opinions(user_1,frame_1).intersection(has_positive_opinions(user_2,frame_2))

def positive_reference_users(user_1, frame_1,frame_2, commonality=1):
    users= set(frame_2['User ID'])
    relevant_users=set()
    for user_2 in users:
        if len(share_positive_opinions(user_1,user_2,frame_1,frame_2))>= commonality:
            relevant_users.add(user_2)
    return relevant_users 
 
def lazy_frame(user_1,frame_1,frame_2, commonality=1):
    relevant_users = positive_reference_users(user_1, frame_1,frame_2, commonality)
    new_frame = frame_2.loc[(frame_2['User ID'].isin(relevant_users))]
    return new_frame

def lazy_ratings(user_1,frame_1,frame_2, commonality=1, type = "sum"):
    known_perfumes = has_opinions(user_1, frame_1)

    adjusted_ratings = lazy_frame(user_1,frame_1,frame_2,commonality)
    adjusted_ratings = adjusted_ratings.loc[(~adjusted_ratings["Perfume Name"].isin(known_perfumes))]

    adjusted_ratings["Similarity"] = adjusted_ratings.groupby('Perfume Name')['Sentiment'].transform(type)
    adjusted_ratings = adjusted_ratings[["Perfume Name", "Similarity"]].drop_duplicates()

    return adjusted_ratings

def lazy_recommender(user_1,frame_1,frame_2, commonality=1, top=20, type="sum"):
    adjusted_ratings = lazy_ratings(user_1,frame_1,frame_2, commonality, type)
    rec_list = adjusted_ratings.convert_dtypes().nlargest(top, 'Similarity', keep = "all")
    
    return rec_list[["Perfume Name", "Similarity"]]


################################################# combine_rec_lists_func


def combine_rec_lists(user_rec_list, note_rec_list, n_recs, slider):
    df_rec_list = pd.concat([user_rec_list, note_rec_list], axis=1)
    ### no overlap
    if df_rec_list.value_counts().values[0] == 1:
        if slider == 0.:
            recommendation_list = note_rec_list
        elif slider == 1.:
            recommendation_list = user_rec_list
        else:
            n_user_rec = int(n_recs * slider)
            n_note_rec = n_recs - n_user_rec
            user_rec_list = user_rec_list[user_rec_list.index <= n_user_rec]
            note_rec_list = note_rec_list[note_rec_list.index <= n_note_rec]

            if n_user_rec == n_note_rec:
                for s in range(n_user_rec):
                    if s == 0:
                        recommendation_list = ', '.join([user_rec_list[s], note_rec_list[s]])
                    else:
                        recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
            elif n_user_rec > n_note_rec:
                for s in range(n_note_rec):
                    if s == 0:
                        recommendation_list = ', '.join([user_rec_list[s], note_rec_list[s]])
                    else:
                        recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
                recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list[n_note_rec+1:].values)])
            else:
                for s in range(n_user_rec):
                    if s == 0:
                        recommendation_list = ', '.join([user_rec_list[s], note_rec_list[s]])
                    else:
                        recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
                recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list[n_user_rec+1:].values)])
            recommendation_list = recommendation_list.split(', ')

    ### overlap
    else:
        n_common = len(df_rec_list.value_counts().values[df_rec_list.value_counts().values > 1])
        # n_common = 2
        recommendation_list = df_rec_list.value_counts().index[0:n_common].to_list()
        if slider == 0.:
            n_note_rec = n_recs - n_common
            note_rec_list[~note_rec_list.values.isin(recommendation_list)].reset_index(drop=True)
            note_rec_list = note_rec_list[note_rec_list.index <= n_note_rec]
            recommendation_list = ', '.join(recommendation_list)
            recommendation_list = ', '.join([recommendation_list, ', '.join(note_rec_list.values)])
        elif slider == 1.:
            n_user_rec = n_recs - n_common
            user_rec_list = user_rec_list[~user_rec_list.values.isin(recommendation_list)].reset_index(drop=True)
            user_rec_list = user_rec_list[user_rec_list.index <= n_user_rec]
            recommendation_list = ', '.join(recommendation_list)
            recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list.values)])
        else:
            n_user_rec = int((n_recs - n_common) * slider)
            n_note_rec = (n_recs - n_common) - n_user_rec
            user_rec_list = user_rec_list[~user_rec_list.values.isin(recommendation_list)].reset_index(drop=True)
            user_rec_list = user_rec_list[user_rec_list.index <= n_user_rec]
            note_rec_list[~note_rec_list.values.isin(recommendation_list)].reset_index(drop=True)
            note_rec_list = note_rec_list[note_rec_list.index <= n_note_rec]

            recommendation_list = ', '.join(recommendation_list)

            if n_user_rec == n_note_rec:
                for s in range(n_user_rec):
                    recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
            elif n_user_rec > n_note_rec:
                for s in range(n_note_rec):
                    recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
                recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list[n_note_rec+1:].values)])
            else:
                for s in range(n_user_rec):
                    recommendation_list = ', '.join([recommendation_list, user_rec_list[s], note_rec_list[s]])
                recommendation_list = ', '.join([recommendation_list, ', '.join(note_rec_list[n_user_rec+1:].values)])
            recommendation_list = recommendation_list.split(', ')

    return pd.Series(recommendation_list, name='Perfume Name')


################################################# combine_rec_lists_func


def recommender_newbie(path_data):
    df_rec_list = pd.read_csv('{}newbie_persian.csv'.format(path_data))
    return df_rec_list[['Perfume Name']]


################################################# allergy_finder_func


def names_to_notes(df_fra_standard, this_client_name):
    this_client_top = df_fra_standard[df_fra_standard['Perfume'].isin([this_client_name])]['Top'].convert_dtypes()
    this_client_mid = df_fra_standard[df_fra_standard['Perfume'].isin([this_client_name])]['Middle'].convert_dtypes()
    this_client_base = df_fra_standard[df_fra_standard['Perfume'].isin([this_client_name])]['Base'].convert_dtypes()
    this_client_note = pd.Series(pd.concat([this_client_top, this_client_mid, this_client_base]).str.cat(sep=', ').split(', '), dtype='string').drop_duplicates()
    return this_client_note

def client_allergy_finder(client_perfume, client_allergy, recommendation_list, df_fra_standard):
    for i in range(len(client_allergy)):
        client_allergy_name = client_allergy[i]
        if i == 0:
            client_allergy_note = names_to_notes(df_fra_standard, client_allergy_name)
        else:
            client_warn_note = names_to_notes(df_fra_standard, client_allergy_name)
            client_allergy_note = pd.Series(list(set(client_warn_note) & set(client_allergy_note)))
    
    if len(client_allergy_note) == 0:
        rec_list_allergy_bool = pd.Series(np.ones(len(recommendation_list)), dtype='bool', name='Allergy Risk')
    else:
        client_perfume_2 = client_perfume[~client_perfume.isin(client_allergy)]
        client_safe_note = names_to_notes(df_fra_standard, client_perfume_2)
        client_allergy_note = pd.concat([client_safe_note, client_safe_note, client_allergy_note]).drop_duplicates(keep=False)
        
        rec_list_allergy_bool = []
        for rec_list_name in recommendation_list:
            rec_list_note = names_to_notes(df_fra_standard, rec_list_name)
            rec_list_allergy_bool.append(rec_list_note.isin(client_allergy_note).any())
        rec_list_allergy_bool = pd.Series(rec_list_allergy_bool, dtype='bool', name='Allergy Risk')
    
    return client_allergy_note, rec_list_note, rec_list_allergy_bool