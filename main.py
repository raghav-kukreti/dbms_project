from models.user import User
import sqlite3
import os
import operator
# from time import sleep
import json
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def retrieve_title_using_id(id):
	movie_conn = sqlite3.connect("movie_db.db")
	movie_cursor = movie_conn.cursor()

	query = "SELECT title, synopsis FROM MOVIES WHERE id=?"
	movie_cursor.execute(query, (id,))

	results = movie_cursor.fetchall()

	return results

def set_lang_code(language):
	language = language.lower()
	if language == "english":
		return "en"
	elif language == "french":
		return "fr"
	elif language == "japanese":
		return "ja"
	elif language == "chinese":
		return "cn"
	elif language == "german":
		return "de"
	elif language == "italian":
		return "it"
	elif language == "russian":
		return "ru"
	elif language == "arabic":
		return "ar"
	elif language == "xhosa":
		return "xh"
	elif language == "dutch":
		return "nl"
	elif language == "spanish":
		return "es"
	else:
		return "en"
def calculate_movie_recs(user):
	movie_conn = sqlite3.connect("movie_db.db")
	user_conn = sqlite3.connect("user_db.db")

	movie_cursor = movie_conn.cursor()
	user_cursor = user_conn.cursor()
	
	retrieve_genres = "SELECT id, genre FROM MOVIES"
	movie_cursor.execute(retrieve_genres)
	
	genre_results = movie_cursor.fetchall()
	my_genres = user.genres
	my_languages = user.languages

	movie_dict = dict()
	for i in range(501):
		movie_dict[i] = 0
	# print(genre_results[0])
			# print(genre_obj[0])
	# print(genre_results[0][0], genre_results[1])
	for genre in my_genres:
		for genre_obj in genre_results:
			# print(genre_obj[1].lower())
			if genre in genre_obj[1].lower():
				movie_dict[int(genre_obj[0])] += 10


	retrieve_lang = "SELECT id, language FROM MOVIES"
	movie_cursor.execute(retrieve_lang)
	language_results = movie_cursor.fetchall()

	# print(language_results[1])
	for language in my_languages:
		code = set_lang_code(language)
		for lang_obj in language_results:
			if code == lang_obj[1]:
				if code == "en":
					movie_dict[lang_obj[0]] += 10
				elif code == "fr":
					movie_dict[lang_obj[0]] += 30
				elif code == "ja":
					movie_dict[lang_obj[0]] += 50
				elif code == "cn":
					movie_dict[lang_obj[0]] += 30
				elif code == "de":
					movie_dict[lang_obj[0]] += 50
				elif code == "it":
					movie_dict[lang_obj[0]] += 30
				elif code == "ru":
					movie_dict[lang_obj[0]] += 60
				elif code == "ar":
					movie_dict[lang_obj[0]] += 40
				elif code == "xh":
					movie_dict[lang_obj[0]] += 70
				elif code == "nl":
					movie_dict[lang_obj[0]] += 70
				elif code == "es":
					movie_dict[lang_obj[0]] += 30
				else:
					movie_dict[lang_obj[0]] += 10
					
	sorted_d = sorted(movie_dict.items(), key=operator.itemgetter(1),reverse=True)
	# print(sorted_d)
	print("Your top 5 recommendations are : ")
	for i in range(10):
		print(bcolors.HEADER + retrieve_title_using_id(sorted_d[i][0])[0][0] + bcolors.ENDC, ":",  retrieve_title_using_id(sorted_d[i][0])[0][1])
		print()
		# print(retrieve_title_using_id(sorted_d[i][0])[0], " : " ,retrieve_title_using_id(sorted_d[i][0])[1])

	user_conn.commit()

def find_similar_users(user):
	current_user = user

	conn = sqlite3.connect('user_db.db') 
	cursor = conn.cursor() 
	my_languages = current_user.languages
	my_genres = current_user.genres

	retrieve_users = "SELECT * FROM USERS WHERE username!=?"
	cursor.execute(retrieve_users, (current_user.username,))
	all_users = cursor.fetchall()
	recs_users = dict()
	for user_tuple in all_users:
		uid = user_tuple[0]
		user_genres = user_tuple[5]
		user_languages = user_tuple[6]

		genre_score = 0
		language_score = 0
		for elem in my_genres:
			if elem in user_genres:
				genre_score += 5
		for elem in my_languages:
			if elem in user_languages:
				language_score += 2.5

		net_score = genre_score + language_score
		recs_users[uid] = net_score
	print("Users with similar taste : score")
	for key, value in recs_users.items():
		retrieve_neighbor = "SELECT username FROM USERS WHERE id=?"
		cursor.execute(retrieve_neighbor, (key,))
		print(cursor.fetchall()[0][0], value)
	# print(recs_users)

	conn.commit()

def user_onboarding(user):
	print("You seem to be a first time user, let's get a few details and set you up.")
	first_name = input("First name: ")
	last_name = input("Last name: ")
	genres = list(input("Enter the genres you like (comma separated): ").split(", "))
	languages = list(input("Enter the languages you understand (comma separated): ").split(", "))

	user.set_extra(genres, languages, first_name, last_name);

	print("User onboarding complete. Calculating recommendations & logging you in...")
	# sleep(1)
	return user

def login_loop(user_obj):
	username = user_obj.username
	password = user_obj.password
	genres = user_obj.genres
	first_name = user_obj.first_name
	last_name = user_obj.last_name
	languages = user_obj.languages

	conn = sqlite3.connect("user_db.db")
	cursor = conn.cursor()

	print("Login successful, let's proceed")
	# sleep(1)
	os.system('clear')
	opt = 0
	while(opt != 4):
		print("Choose what to do,", first_name)
		print("1. Display my recommendations")
		print("2. Edit movie preferences")
		print("3. Explore neighbours")
		print("4. Exit")
		opt = int(input("> "))

		if opt == 1:
			current_user = User(username, password)
			current_user.set_extra(genres, languages, first_name, last_name)
			calculate_movie_recs(current_user)
		elif opt == 2:
			print("Choose what to edit: ")
			print("1. Genres")
			print("2. Languages")
			opt_inner = int(input("> "))
			if opt_inner == 1:
				print("Choose what to do: ")
				print("1. Add")
				print("2. Delete")
				print("3. Edit")	
				opt_inner_two = int(input("> "))
				if opt_inner_two == 1:
					print("Enter genre to add : ")
					new_genre = input("> ")
					genres.append(new_genre)
				elif opt_inner_two == 2:
					print(genres)
					print("Choose what to delete [value]: ")
					idx = input("> ")
					genres = [genre for genre in genres if genre != idx]
					print("Successfully deleted!")
				elif opt_inner_two == 3:
					print(genres)
					print("Choose what to edit [value]: ")
					val = input("> ")
					idx = genres.index(val)
					print("Enter new value: ")
					new_val = input("> ")
					if idx < len(genres) and idx >= 0:
						genres[idx] = new_val
					else:
						print("element doesn't exist")
				else:
					print("Wrong option!")

				genre_dump = json.dumps(genres)
				update_query = "UPDATE USERS SET genre_json = ? WHERE username = ?"

				cursor.execute(update_query, (genre_dump, username))
				conn.commit()

			elif opt_inner == 2:
				print("Choose what to do: ")
				print("1. Add")
				print("2. Delete")
				print("3. Edit")	
				opt_inner_two = int(input("> "))
				if opt_inner_two == 1:
					print("Enter language to add : ")
					new_language = input("> ")
					languages.append(new_language)
				elif opt_inner_two == 2:
					print(languages)
					print("Choose what to delete [value]: ")
					idx = input("> ")
					languages = [language for language in languages if language != idx]
					print("Successfully deleted!")
				elif opt_inner_two == 3:
					print(languages)
					print("Choose what to edit [value]: ")
					val = input("> ")
					idx = languages.index(val)
					print("Enter new value: ")
					new_val = input("> ")
					if idx < len(languages) and idx >= 0:
						languages[idx] = new_val
					else:
						print("element doesn't exist")
				else:
					print("Wrong option!")

				language_dump = json.dumps(languages)
				update_query = "UPDATE USERS SET lang_json = ? WHERE username = ?"

				cursor.execute(update_query, (language_dump, username))
				conn.commit()
				
			else :
				print("Wrong option!")


		elif opt == 3:
			# pass
			current_user = User(username, password)
			current_user.set_extra(genres, languages, first_name, last_name)
			find_similar_users(current_user)
		elif opt == 4:
			pass
		else:
			print("Wrong option!")

def main():
	conn = sqlite3.connect('user_db.db') 
	cursor = conn.cursor() 

	print("Movie Recommendation Engine v1")
	print("Login with existing credentials, or create a new account.\n")
	username = input("Username: ")
	password = input("Password: ")
	
	sql_command = "SELECT * FROM USERS WHERE username=?"	
	cursor.execute(sql_command, (username,))

	check = cursor.fetchall()
	if len(check) == 0:
		temp_user = User(username, password)
		final_user = user_onboarding(temp_user) 
		genres_json = json.dumps(final_user.genres)
		languages_json = json.dumps(final_user.languages)
		cursor.execute("INSERT INTO USERS(username, password, first_name, last_name, genre_json, lang_json, movie_recs_json, user_recs_json) VALUES (?,?,?,?,?,?,?,?)", (username, password, final_user.first_name, final_user.last_name, genres_json, languages_json, "", ""))
		conn.commit()
		login_loop(final_user)
	else :
		cursor.execute("SELECT * FROM USERS WHERE username=? AND password=?", (username, password,))
		check_two = cursor.fetchall()

		if len(check_two) == 0:
			print("You seem to have entered an incorrect username/password combo")
		
		else:
			# Login successful
			# Fetch user recommendations and other data and save to object.
			user_tuple = check_two[0]
			current_user = User(user_tuple[1], user_tuple[2])
			# 5,6 -> genres and languages_json
			genres = json.loads(user_tuple[5])
			languages = json.loads(user_tuple[6])

			# for elem in check_two:
				# print(type(elem))
				# print(elem[1])
			# print(type(check_two))
			current_user.set_extra(genres, languages, user_tuple[3], user_tuple[4])
			login_loop(current_user)
			# pass
	# print(check)
	conn.commit() # Need this to save changes to the database 

if __name__ == '__main__':
	main()
