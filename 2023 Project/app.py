from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from nlp import gpt_text_generation
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

app.secret_key = 'your secret key'

@app.route('/')
def index():
        return render_template('index.html')


@app.route('/login.html', methods = ['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM studentaccount WHERE username = % s AND password = % s', (username, password,))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return redirect("/planetMap.html")
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg=msg)


@app.route("/Sign_up.html", methods = ['GET', 'POST'])
def Sign_up():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		progress = 0
		planet1 = 0
		planet2 = 0
		planet3 = 0
		planet4 = 0
		cursor.execute('SELECT * FROM studentaccount WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO studentaccount(email, username, password, progress) VALUES  (% s, % s, % s, %s)', (email, username, password, progress))
			cursor.execute('INSERT INTO progress_table(planet1, planet2, planet3, planet4) VALUES  (% s, % s, % s, %s)', (planet1, planet2, planet3, planet4))
			mysql.connection.commit()
			msg = 'You have successfully registered!'
			return redirect("/login.html")
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('Sign_up.html', msg=msg)


@app.route("/planetMap.html")
def map():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM studentaccount WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()	
		return render_template("planetMap.html", account = account)



def Level_Query(level):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT units FROM html WHERE planet = % s', (level, ))
	body = cursor.fetchone()
	return body

#Routes and functions for levels
global level
level = 0
@app.route("/Level.html", methods = ['GET'])
def XYZ():
	global level
	level = 0
	image = request.args.get('image')
	if image == "planet4LOCK.png":
		body = Level_Query(4)
		level = 4
	elif image == "planet3LOCK.png":
		body = Level_Query(3)
		level = 3
	elif image == "planet2LOCK.png":
		body = Level_Query(2)
		level = 2
	elif image == "planet1.png":
		body = Level_Query(1)
		level = 1
	# body = QuoteChange(body)
	return render_template('level.html', body = body)



	

def Find_Content(content_num):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT html{content_num} FROM html WHERE planet = {level}")
	body = cursor.fetchone()
	return body

@app.route("/content.html")
def content():
	num = request.args.get('num')
	body = Find_Content(num)
	return render_template("content.html", body = body)





@app.route("/Completed/", methods = ['POST'])
def complete():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("UPDATE studentaccount SET progress = '25' WHERE id = %s", (session['id'], ))
	mysql.connection.commit()
	return redirect("/planetMap.html")




@app.route("/help.html")
def Route():
	return render_template("help.html")

@app.route("/help.html", methods = ['POST'])
def chatbot():
	input_text = request.form["userinput"]
	input_text = str(input_text)
	response = gpt_text_generation.gpt2_model(input_text)
	print(response)
	return render_template("help.html", response = response)
	
	# Python code to fake the NLP	
	# response = ""
	# input_text = request.form["userinput"]
	# input_text = str(input_text)
	# if input_text[0] == "h" or input_text[0] == "H":
	# 	response = "To make a list in python you need to use brackets '[]'."
	# elif input_text[0] == "w" or input_text[0] == "W":
	# 	response = "The input function in python allows user input to be taken in and saved as a variable. the default data type for the input function is a string. the syntax for the input function is x = input('Prompt Text')"
	
	# return render_template("help.html", response = response)




if __name__ == '__main__':
    app.run(host = "localhost", port = int("5000"), debug = True)
    


	

