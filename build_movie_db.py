import pandas as pd
import numpy as np
import json
 
def main():
	data = pd.read_csv("movies_metadata.csv")
	data = data.drop(['adult', 'tagline', 'spoken_languages', 'belongs_to_collection', 'budget', 'homepage', 'id', 'imdb_id', 'poster_path', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'status', 'video','vote_average', 'vote_count'], axis=1)
	
	data = data.dropna() # drop NaN valued rows
	data = data.head(500) # shorten data to just 500 entries
	data = data.sort_values(by=["popularity"], ascending=False) # most popular movies on top
	# print(data)
	data.to_csv('mini_metadata.csv') # write to file
if __name__ == '__main__':
	main()