import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
