# import the packages we'll use
## For data handling
import pandas as pd
import numpy as np
from collections import Counter

old = pd.read_csv('Perfume1.csv')
df = old[['User ID', 'User Name', 'Perfume ID', 'Perfume Name','Sentiment']]
df = df.dropna()

samp = df.sample(frac=0.1, random_state=1)

test_perfume = samp.loc[30548,"Perfume Name"]

def likes_perfume(perfume, frame):
    selction = frame.loc[(frame['Perfume Name'] == perfume) & (frame['Sentiment'] == "Positive")]
    users = selction["User ID"].to_numpy()
    return np.unique(users)

def user_likes(user, frame):
    return frame.loc[(frame['User ID'] == user) & (frame['Sentiment'] == "Positive")]

def users_liked(perfume, frame):
    all_liked = pd.DataFrame()
    enjoyers = likes_perfume(perfume, frame)

    for enjoyer in enjoyers:
        all_liked = pd.concat([all_liked,user_likes(enjoyer,frame)])

    perfumes = all_liked["Perfume Name"].to_numpy()
    count_frequency = Counter(perfumes)
    return count_frequency.most_common()

def rec_list(perfume,frame):
    recs = []
    candidates = users_liked(perfume, frame)
    for candidate in candidates:
        if (candidate[1] > 1) and (candidate[0] != perfume):
            recs.append(candidate[0])
    if len(recs)>10:
        recs = recs[0:10]
    return recs

print(rec_list(test_perfume,df))


    