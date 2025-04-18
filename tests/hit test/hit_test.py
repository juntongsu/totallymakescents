import pandas as pd
import numpy as np

from recommender_users_func import *
from recommender_notes_func import *
from recommender_lazy_func import *
from recommender_gamma_func import *





###Cleaning up Persian Data Frame

old = pd.read_csv('data/Persian_Data.csv')
df = old[['User ID', 'Perfume ID','Perfume Name','Sentiment']]
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
persian_data_frame_clean = persian_data_frame_clean.loc[(persian_data_frame_clean['Sentiment'] != 0)]

###Top 20 Perfumes
positive_perfumes = persian_data_frame_clean.loc[(persian_data_frame_clean['Sentiment'] == 1)]
positive_perfumes = positive_perfumes["Perfume Name"].value_counts()
positive_perfumes = pd.DataFrame({'Perfume Name':positive_perfumes.index})["Perfume Name"]
positive_perfumes = set(positive_perfumes[positive_perfumes.index < 20])


###Final Test 

final_test_frame = df.loc[(~df['User ID'].isin(selection) )]
final_test_frame.update(final_test_frame["Sentiment"].apply(enum_ratings))
final_test_frame = final_test_frame.loc[(final_test_frame['Sentiment'] != 0)]

user_counts = final_test_frame["User ID"].value_counts()
user_counts = pd.DataFrame({'User ID':user_counts.index, 'Count':user_counts.values})

final_testers = user_counts.loc[(user_counts['Count']>7 )]["User ID"]
final_test_frame = final_test_frame.loc[(final_test_frame["User ID"].isin(final_testers))]


####Selecting Initial Test 

#user_counts = persian_data_frame_clean["User ID"].value_counts()
#user_counts = pd.DataFrame({'User ID':user_counts.index, 'Count':user_counts.values})

#potential_testers = user_counts.loc[(user_counts['Count']>9 )]["User ID"]
#testers = potential_testers.sample(frac=0.30, random_state=13)

#remaining_testers = user_counts.loc[((~user_counts["User ID"].isin(testers))&(user_counts['Count']>9 ))]["User ID"]
#testers_2 = remaining_testers.sample(frac=0.43, random_state=13)

#test_user_frame = persian_data_frame_clean.loc[(persian_data_frame_clean["User ID"].isin(testers))]
#comparison_frame = persian_data_frame_clean.loc[(~persian_data_frame_clean["User ID"].isin(testers))]

#test_user_frame_2 = persian_data_frame_clean.loc[(persian_data_frame_clean["User ID"].isin(testers_2))]
#comparison_frame_2 = persian_data_frame_clean.loc[(~persian_data_frame_clean["User ID"].isin(testers_2))]


##### Generate random recs

random_sample_1 = perf_names["Perfume"].sample(n=20, random_state=1)
random_sample_1 = set(random_sample_1)

random_sample_2 = perf_names["Perfume"].sample(n=20, random_state=30)
random_sample_2 = set(random_sample_2)

random_sample_3 = perf_names["Perfume"].sample(n=20, random_state=42)
random_sample_3 = set(random_sample_3)


###Comparison Test For Single User

def hit_test(test_user,test_user_frame, comparison_frame, perf_names, vec_top, vec_mid, vec_base, state =1, n_recs = 20, sample_1 = random_sample_1, sample_2 = random_sample_2, sample_3 = random_sample_3, top_20 = positive_perfumes, i=0):
    user_data_all = test_user_frame.loc[(test_user_frame["User ID"] == test_user)]
    truncated_user_data = user_data_all.sample(frac=0.5, random_state=state)

    count =  truncated_user_data.loc[(truncated_user_data["User ID"]==test_user)]["User ID"].value_counts()
    count = count.iloc[0]

    print(test_user)

    known_perfumes = has_opinions(test_user, truncated_user_data)
    true_recs = set(user_data_all.loc[((~user_data_all["Perfume Name"].isin(known_perfumes))& (user_data_all["Sentiment"]==1))]["Perfume Name"])

    user_perfume, user_sentiment = input_perfume_2(truncated_user_data[["Perfume Name","Sentiment"]])
    user_top, user_mid, user_base = user_vec_prep(user_perfume, user_sentiment, perf_names, vec_top, vec_mid, vec_base)
    temperature = np.array((1, 2, 1, 1.5), dtype=int)
    note_recommendation_list = recommender_notes(perf_names, vec_top, vec_mid, vec_base, user_perfume, user_top, user_mid, user_base, temperature)
    user_sum_recommendation_list = recommender_users(test_user, truncated_user_data, comparison_frame,weight=1, type="sum")
    lazy_recommendation_list = lazy_recommender(test_user,truncated_user_data,comparison_frame)

    if language == 0:
        user_sum_rec_list = user_sum_recommendation_list['Perfume Name'].reset_index(drop=True)
        lazy_rec_list = lazy_recommendation_list['Perfume Name'].reset_index(drop=True)
        note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
    elif language == 1:
        user_sum_rec_list = user_sum_recommendation_list['Perfume Name'].reset_index(drop=True)
        note_rec_list = note_recommendation_list['Perfume'].reset_index(drop=True)
        lazy_rec_list = lazy_recommendation_list['Perfume Name'].reset_index(drop=True)


    user_sum_recs = set(user_sum_rec_list[user_sum_rec_list.index < n_recs])
    note_recs = set(note_rec_list[note_rec_list.index < n_recs])
    lazy_recs = set(lazy_rec_list[lazy_rec_list.index < n_recs])

    gamma_recs = set(recommender_gamma(test_user, truncated_user_data, comparison_frame, perf_names, vec_top, vec_mid, vec_base, n_recs = 20))

    rng_1_hits = len(true_recs.intersection(sample_1))
    rng_2_hits = len(true_recs.intersection(sample_2))
    rng_3_hits = len(true_recs.intersection(sample_3))
    rng_average = sum([rng_1_hits,rng_2_hits,rng_3_hits]) / len([rng_1_hits,rng_2_hits,rng_3_hits])
    gamma_hits = len(true_recs.intersection(gamma_recs))
    user_sum_hits = len(true_recs.intersection(user_sum_recs))
    note_hits = len(true_recs.intersection(note_recs))
    lazy_hits = len(true_recs.intersection(lazy_recs))
    top_20_hits = len(true_recs.intersection(top_20))

    results_frame = pd.DataFrame({'User':[test_user],"Known Perfumes":[count] ,"RNG":[rng_average],"User(Sum)":[user_sum_hits],"Notes":[note_hits],"Popularity":[lazy_hits],"Gamma":[gamma_hits],"Top 20":[top_20_hits]}, index=[i])

    return results_frame


def hit_test_all(test_users,test_user_frame, comparison_frame, perf_names, vec_top, vec_mid, vec_base):
    user_list = test_users.to_list()
    n = len(user_list)
    frames = [hit_test(user_list[ind],test_user_frame, comparison_frame, perf_names, vec_top, vec_mid, vec_base, i=ind) for ind in range(n)]

    results_frame = pd.concat(frames)

    return results_frame



hit_test_results = hit_test_all(final_testers,final_test_frame, persian_data_frame_clean, perf_names, vec_top, vec_mid, vec_base)
hit_test_results.to_csv('final_hit_results.csv') 
