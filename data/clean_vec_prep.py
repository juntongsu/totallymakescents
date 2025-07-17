###
# vec prep for top, middle, base notes, and the accords
###
import pandas as pd
home = '../'
path_data = home + 'data/'

def notes_accords_vec_prep(df_data_notes):    
    perf_names = df_data_notes['Perfume'].convert_dtypes()
    vec_top = df_data_notes['Top'].str.get_dummies(sep=', ').astype('float')
    vec_mid = df_data_notes['Middle'].str.get_dummies(sep=', ').astype('float')
    vec_base = df_data_notes['Base'].str.get_dummies(sep=', ').astype('float')

    df_accords = df_data_notes[['mainaccord1', 'mainaccord2', 'mainaccord3', 'mainaccord4', 'mainaccord5']].astype('str').agg(','.join, axis=1)
    vec_accords = df_accords.str.get_dummies(sep=',').drop(columns=['nan'])

    print('Top notes: {}, middle notes: {}, base notes: {}, accords: {}'.format(vec_top.shape[1], vec_mid.shape[1], vec_base.shape[1], vec_accords.shape[1]))
    return perf_names, vec_top, vec_mid, vec_base, vec_accords

df_features_reviews_merge = pd.read_parquet(path_data + 'fra_reviews_merged.parquet')
perf_names, vec_top, vec_mid, vec_base, vec_accords = notes_accords_vec_prep(df_features_reviews_merge)

pd.DataFrame(perf_names).to_parquet('{}perf_names.parquet'.format(path_data))
pd.DataFrame(vec_top).to_parquet('{}vec_top.parquet'.format(path_data))
pd.DataFrame(vec_mid).to_parquet('{}vec_mid.parquet'.format(path_data))
pd.DataFrame(vec_base).to_parquet('{}vec_base.parquet'.format(path_data))
pd.DataFrame(vec_accords).to_parquet('{}vec_accords.parquet'.format(path_data))