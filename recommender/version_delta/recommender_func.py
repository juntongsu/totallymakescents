import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


################################################# recommender_notes_func


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
    if df_rec_list.value_counts().values[0] == 1:
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
        n_common = 2
        recommendation_list = df_rec_list.value_counts().index[0:n_common].to_list()

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
            recommendation_list = ', '.join([recommendation_list, ', '.join(user_rec_list[n_user_rec+1:].values)])
        recommendation_list = recommendation_list.split(', ')

    return recommendation_list


################################################# combine_rec_lists_func


def recommender_newbie(path_data):
    df_rec_list = pd.read_csv('{}newbie_persian.csv'.format(path_data))
    return df_rec_list[['Perfume Name']]