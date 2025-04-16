import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

###Cleaning up Data Frame

old = pd.read_csv('../../data/Persian_Data.csv')
df = old[['User ID', 'Perfume ID', 'Perfume Name','Sentiment']]
df = df.dropna()

##Remove perfumes with same name and different ids
black_list = {15195,9500,15615}
df = df.loc[(~df["Perfume ID"].isin(black_list))][['User ID','Perfume Name','Sentiment']]

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


ef has_opinions(user, frame):
    return set(frame.loc[(frame['User ID'] == user)]["Perfume Name"])

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

def lazy_recommender(user_1,frame_1,frame_2 = persian_data_frame_clean, commonality=2, top=20, type="sum"):
    adjusted_ratings = lazy_ratings(user_1,frame_1,frame_2, commonality, type)
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


lazy_list = lazy_recommender(user_id, user_frame)

print(lazy_list)

