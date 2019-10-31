from flask import Flask, render_template, request, redirect, url_for, logging, session, json
import pymysql.cursors

from sqlalchemy import create_engine 
from sqlalchemy.orm import scoped_session, sessionmaker

# connection = pymysql.connect(host='127.0.0.1',
# 								port=8080, 
# 								user='root', 
# 								password='', 
# 								db='movie_theatre',
# 								charset='utf8mb4')

engine = create_engine("mysql+pymysql://aviral:test@localhost/movie_theatre")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

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

		db.execute("INSERT INTO user(username,password,email,account_type) VALUES(:username,:password,:email,:account_type)",
					{"username":username,"password":password,"email":email,"account_type":account_type})
		# db.execute("INSERT INTO user(username, password, email) VALUES(%s, %s, %s)", (username, password, email))
		db.commit()
		return redirect(url_for("login"))	
	return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		account_type = request.form['account_type']

		account = db.execute("SELECT * FROM user WHERE username = :username AND password = :password AND account_type = :account_type", 
			{"username": username, "password":password, "account_type":account_type}).rowcount
		
		print(account)
		# db.execute("SELECT * FROM user WHERE username=%s AND password=%s AND email=%s",(username,password,email))
		# account = db.fetchone()
		if(account):
			return redirect(url_for("home"))
		else:
			return "Please check the information you entered"
	return render_template("login.html")

		
if __name__ == "__main__" :
	app.run(debug = True)
