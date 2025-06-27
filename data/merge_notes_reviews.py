# merge fra_standard.csv and perfumes_table.csv (notes and reviews)
import pandas as pd
home = '../'
path_data = home + 'data/'

df_fra_standard = pd.read_csv(path_data + 'fra_standard.csv')

df_fra_reviews = pd.read_csv(path_data + 'perfumes_table.csv')
df_fra_reviews = df_fra_reviews[['reviews', 'url']]
reviews = df_fra_reviews['reviews'].convert_dtypes()
reviews = reviews.str.replace('\\n', ' ').str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
reviews = reviews[reviews != '']
reviews = reviews[reviews != r'\s+']
reviews_url = df_fra_reviews['url'].convert_dtypes().str.lower()[reviews.index]
df_reviews = pd.concat([reviews, reviews_url], axis=1)

df_notes_reviews = pd.merge(df_fra_standard, df_reviews, how='inner', on='url')

df_notes_reviews.to_csv('{}fra_reviews.csv'.format(path_data))