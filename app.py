from flask import Flask, render_template, request, redirect, url_for, logging, session, json, g
import pymysql.cursors
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import * 
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

# connection = pymysql.connect(host='127.0.0.1',
# 								port=8080, 
# 								user='root', 
# 								password='', 
# 								db='movie_theatre',
# 								charset='utf8mb4')

# engine = create_engine("mysql+pymysql://aviral:test@localhost/movie_theatre")
# db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://aviral:test@localhost/movie_theatre"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.urandom(24)
db.init_app(app)

@app.before_request
def before_request():
	g.account_type = None
	g.user = None
	if 'user' in session:
		g.user = session['user']
		g.account_type = session['account_type']

@app.route("/")
def home():
	return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
	if request.method == "POST" :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		account_type = request.form['account_type']

		account = User.query.filter_by(email = email).count()

		if (account) :
			return render_template("error.html", message = "An account with this email ID already exists", 
				x = "Click Here to Login", function = "login")

		account = User.query.filter_by(username = username).count()

		if (account) :
			return render_template("error.html", message = "This username is taken", 
			x = "Click Here to signup", function = "signup" )

		user = User(username = username, password = password, email = email, account_type = account_type)
		
		user.add()
		return redirect(url_for("login"))	
	if g.user :
		return render_template('logout.html', message = "You are already logged in")
	return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		account_type = request.form['account_type']

		account = User.query.filter(and_(User.username == username, 
			User.password == password, User.account_type == account_type)).count()


		if(account):
			session['user'] = username
			session['account_type'] = account_type
			return redirect(url_for(account_type))
		else:
			return "Please check the information you entered"

	if g.user :
		return render_template('logout.html', message = "You are already logged in")

	return render_template("login.html")

#Theatre Owner Section
@app.route("/theatre_owner")
def theatre_owner():
	if g.account_type != "theatre_owner" :
		return "<h1>You do not have access to this page. Only theatre owners can access this page.</h1>"

	return render_template("theatre_owner.html")


@app.route("/theatre_owner/profile")
def theatre_profile():
	if g.account_type != "theatre_owner" :
		return "<h1>You do not have access to this page. Only theatre owners can access this page.</h1>"

	user = User.query.filter_by(username = g.user).first()
	theatre = Theatre.query.filter_by(owner_id = user.id).first()

	if theatre == None:
		return render_template('error.html', message = "You have not yet created your theatre profile.", 
			function = "theatre_owner", x = "Go Back")	

	return render_template("theatre_profile.html", theatre = theatre)


@app.route("/theatre_owner/create_profile", methods = ["GET", "POST"])
def create_profile():
	if g.account_type != "theatre_owner" :
		return "<h1>You do not have access to this page. Only theatre owners can access this page.</h1>"
	user = User.query.filter_by(username = g.user).first()
	theatre = Theatre.query.filter_by(owner_id = user.id).first()
	if theatre != None :
		return '<h1>You have already created your theatre profile.</h1>'
	if request.method == "POST" :
		name = request.form['theatre_name']
		address = request.form['address']
		owner_id = User.query.filter_by(username = g.user).first().id 

		theatre = Theatre(owner_id = owner_id, name = name, address = address)
		theatre.add()

		return redirect(url_for('theatre_owner'))
	return render_template('create_theatre_profile.html')


@app.route("/theatre_owner/make_movie_request", methods = ["GET", "POST"])
def make_movie_request():
	if g.account_type != "theatre_owner" :
		return "<h1>You do not have access to this page. Only theatre owners can access this page.</h1>"
	user = User.query.filter_by(username = g.user).first()
	theatre = Theatre.query.filter_by(owner_id = user.id).first()
	if theatre == None:
		return render_template('error.html', message = "To make a movie request, you need to make your theatre profile.", 
			function = "theatre_owner", x = "Go Back")
	if request.method == "POST" :
		movie_name = request.form['movie_name']
		language = request.form['language']
		time = request.form['time']

		user = User.query.filter_by(username = g.user).first()
		theatre = Theatre.query.filter_by(owner_id = user.id).first()
		movie = Movie(name = movie_name, language = language, time = time, theatre_id = theatre.id, is_approved = "NA")

		movie.add()
		return redirect(url_for('theatre_owner'))
	return render_template('make_movie_request.html')


@app.route("/view_my_details")
def view_my_details():
	if g.user == None :
		return "<h1>You are not logged in.</h1>"
	user = User.query.filter_by(username = g.user).first()
	return render_template("view_my_details.html", user = user)

#Admin Section
@app.route("/admin")
def admin():
	if g.account_type != "admin" :
		return "<h1>Only admins can access this page</h1>"
	return render_template('admin.html')

# @app.route("/admin/view_theatres")
# def view_theatres():
# 	if g.account_type != "admin" :
# 		return "<h1>You do not have access to this page. Only admins can access this page.</h1>"


@app.route("/admin/movie_requests", methods = ["GET", "POST"])
def movie_requests():
	if g.account_type != "admin" :
		return "<h1>You do not have access to this page. Only admins can access this page.</h1>"

	if request.method == "POST" :
		try :
			movie_id = request.form['NO']
			movie = Movie.query.get(movie_id)
			movie.is_approved = "NO"
		except :
			movie_id = request.form['YES']
			movie = Movie.query.get(movie_id)
			movie.is_approved = "YES"
		# if (request.form['YES'] == null) :
		# 	movie_id = request.form['NO']
		# 	movie = Movie.query.get(movie_id)
		# 	movie.is_approved = "NO"
		# else :	
		# 	movie_id = request.form['YES']
		# 	movie = Movie.query.get(movie_id)
		# 	movie.is_approved = "YES"
		db.session.commit()
	movies = Movie.query.filter_by(is_approved = "NA").all()
	return render_template('movie_requests.html', movies = movies)

@app.route("/admin/movie_status", methods = ["GET", "POST"])
def movie_status():
	if g.account_type != "admin" :
		return "<h1>You do not have access to this page. Only admins can access this page.</h1>"
	if request.method == "POST" :
		movie_id = request.form['change']
		movie = Movie.query.get(movie_id)
		if (movie.is_approved == "YES") :
			movie.is_approved = "NO"
			db.session.commit()
		else :
			movie.is_approved = "YES"
			db.session.commit()

		movies = Movie.query.all()
		return render_template('movie_status.html', movies = movies)		

	movies = Movie.query.all()
	return render_template('movie_status.html', movies = movies)		


@app.route("/customer")
def customer():
	if g.account_type != "customer" :
		return "<h1>This page can only be accessed by customers.</h1>"
	return "<h1>Welcome to the customer section.</h1>"

@app.route("/movies", methods = ["GET", "POST"])
def movies():
	if request.method == "POST" :
		language = request.form['search']
		movies = Movie.query.filter(and_(Movie.is_approved == "YES", Movie.language == language)).all()
		return render_template('movies.html', movies = movies)
	movies = Movie.query.filter_by(is_approved = "YES").all()
	return render_template("movies.html", movies = movies)


# @app.route("/edit_profile")
# def edit_profile():
# 	if !g.user :
# 		return render_template("error.html", message = "You are not logged in." )


@app.route("/dropsession")
def dropsession():
	session.pop('user', None)
	session.pop('account_type', None)
	return redirect(url_for('home'))

		
if __name__ == "__main__" :
	app.run(debug = True)
