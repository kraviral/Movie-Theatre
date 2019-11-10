from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(255), nullable =False)
	password = db.Column(db.String(255), nullable = False)
	email = db.Column(db.String(255), nullable = False)
	account_type = db.Column(db.String(255), nullable = False)
	movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable = True)

	def add(self):
		db.session.add(self)
		db.session.commit()

class Theatre(db.Model):
	__tablename__ = "theatres"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(255), nullable = False)
	address = db.Column(db.String(255), nullable = False)
	owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
	movies = db.relationship("Movie", backref = "theatre", lazy=True)

	def add(self):
		db.session.add(self)
		db.session.commit()

class Movie(db.Model):
	__tablename__ = "movies"
	id = db.Column(db.Integer, primary_key = True)
	theatre_id = db.Column(db.Integer, db.ForeignKey("theatres.id"), nullable = False)
	name = db.Column(db.String(255), nullable = False)
	language = db.Column(db.String(255), nullable = False)
	time = db.Column(db.Integer, nullable = False)
	is_approved = db.Column(db.String(10), nullable = False)
	poster_url = db.Column(db.String(255), nullable = True)

	def add(self):
		db.session.add(self)
		db.session.commit()