###
# find overlap perfumes between fra_reviews_merged.parquet and cleaned_persian.csv
###
import pandas as pd
home = '../'
path_data = home + 'data/'

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

df_features_reviews_merge = pd.read_parquet(path_data + 'fra_reviews_merged.parquet')
df_persian = pd.read_csv(path_data + 'cleaned_persian.csv')

perf_overlap = find_overlap(df_persian, df_features_reviews_merge)
perf_overlap.to_parquet('{}perf_names_overlap.parquet'.format(path_data))