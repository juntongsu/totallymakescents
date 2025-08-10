from recommender_users_func import *

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