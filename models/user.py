class User:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.genres = list()
		self.languages = list()
		self.recs_movie = dict()
		self.recs_users = dict()
		self.first_name = ""
		self.last_name = ""
		
	def set_extra(self, genres, languages, first_name, last_name):
		self.genres = genres
		self.languages = languages
		self.first_name = first_name
		self.last_name = last_name
