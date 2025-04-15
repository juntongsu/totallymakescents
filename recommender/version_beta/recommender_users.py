import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

###Cleaning up Data Frame

old = pd.read_csv('../../data/Persian_Data.csv')
df = old[['User ID', 'Perfume Name','Sentiment']]
df = df.dropna()

user_ids = df['User ID'].unique()
user_frame = pd.DataFrame({'User ID':user_ids})
user_samp = user_frame.sample(frac=0.80, random_state=13)
selection = user_samp["User ID"]
persian_data_frame_clean = df.loc[(df['User ID'].isin(selection) )]

def enum_ratings(sentiment):
    if sentiment == "Positive":
        return 1.0
    if sentiment == "Negative":
        return -1.0
    else: 
        return 0.0

persian_data_frame_clean.update(persian_data_frame_clean["Sentiment"].apply(enum_ratings))

#####


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

def accuracy_index(user_1, user_2, frame_1,frame_2, weight = 1.0):
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

def adjust_rating_1(rating,user_1,user_2,frame_1,frame_2,weight=1.0):
    return rating*cos_index_1(user_1,user_2,frame_1,frame_2)*accuracy_index(user_1, user_2, frame_1,frame_2,weight)

def adjusted_frame_1(user_1,frame_1,frame_2, commonality=1,weight = 1.0):
    relevant_users = reference_users(user_1, frame_1,frame_2, commonality)
    new_frame = frame_2.loc[(frame_2['User ID'].isin(relevant_users))]
    for user_2 in relevant_users:
        adjust = new_frame.loc[(new_frame['User ID']==user_2), "Sentiment"].apply(adjust_rating_1,args=(user_1,user_2,frame_1,frame_2,weight))
        new_frame.update(adjust)
    return new_frame

def ratings(user_1,frame_1,frame_2, commonality=1,weight=1.0):
    known_perfumes = has_opinions(user_1, frame_1)

    adjusted_ratings = adjusted_frame_1(user_1,frame_1,frame_2,commonality,weight)
    adjusted_ratings = adjusted_ratings.loc[(~adjusted_ratings["Perfume Name"].isin(known_perfumes))]

    adjusted_ratings["Similarity"] = adjusted_ratings.groupby('Perfume Name')['Sentiment'].transform('sum')
    adjusted_ratings = adjusted_ratings[["Perfume Name", "Similarity"]].drop_duplicates()

    return adjusted_ratings

def recommender_users(user_1,frame_1,frame_2 = persian_data_frame_clean, commonality=2,weight=1, top=20):
    adjusted_ratings = ratings(user_1,frame_1,frame_2, commonality, weight)
    rec_list = adjusted_ratings.convert_dtypes().nlargest(top, 'Similarity', keep = "all")
    
    return rec_list[["Perfume Name", "Similarity"]]


### cleans input.csv

user_frame = pd.read_csv('input.csv',header=None)
user_frame.columns = ["Perfume Name","Sentiment"]

##For use if storing/collecting data. Set to 0 for now as we are not collecting user data
user_id = 0 

def add_user_id(frame, user_id = 0):
    count_row = frame.shape[0]
    id_row = np.repeat(user_id, count_row)
    frame["User ID"] = id_row
    return frame

user_frame = add_user_id(user_frame)


user_recommendation_list = recommender_users(user_id, user_frame)

print(user_recommendation_list)

