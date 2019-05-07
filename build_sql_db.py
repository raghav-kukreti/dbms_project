import sqlite3
import json
import pandas as pd

def main():
	conn = sqlite3.connect("movie_db.db")
	cursor = conn.cursor()
	df = pd.read_csv('mini_metadata.csv')
	# print(df.genres)
	# for i in range()
	idx = 0
	# print(df.columns)

	for i in df.iterrows(): 
		if df['genres'][idx] == "[]":
			pass
		else:
			genre_data = df['genres'][idx][1:len(df['genres'][idx]) - 1]
			movie_title = df['title'][idx]
			language = df['original_language'][idx]
			popularity = df['popularity'][idx]
			synopsis = df['overview'][idx]

			insert_data = "INSERT INTO MOVIES(title, genre, language, synopsis, popularity) VALUES(?,?,?,?,?)"
			cursor.execute(insert_data, (movie_title, genre_data, language, synopsis, popularity))
			# print(movie_title, popularity)
		idx += 1	
		# print(i,j)

	conn.commit()
if __name__ == '__main__':
	main()