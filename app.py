from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
from difflib import SequenceMatcher

app = Flask(__name__)

app.secret_key = '9afd69d3d6ff1bdd87f0deb0'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dbmsproject'
app.config['MYSQL_DB'] = 'database1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
@app.route('/login')
def login():
	if 'loggedin' in session:
		return redirect(url_for('home', name = session['name'], user_id = session['id']))

	return render_template('login.html', msg = 'hola')

@app.route('/checkuser', methods = ['POST'])
def check_user():
	email = str(request.form['email'])
	password = str(request.form['psw'])

	cur = mysql.connection.cursor()
	cur.execute(f"SELECT * FROM user WHERE email_id = '{email}'")
	user = cur.fetchone()
	print(user)

	if user:
		session['loggedin'] = True
		session['id'] = user['user_id']
		session['name'] = user['name']
		session['email'] = user['email_id']
		# Redirect to home page
		return redirect(url_for('home', name = user['name'], user_id = user['user_id']))
	# print(id)
	else:
		return redirect(url_for('login', msg = 'Login failed'))

	# if len(user) == 1:
		# return redirect(url_for('home', name = user['name'], user_id = id))

@app.route('/createaccount')
def create_account():
	return render_template('create_account.html')

@app.route('/signup', methods = ['POST'])
def sign_up():
	name = str(request.form['name'])
	email = str(request.form['email'])
	phone = str(request.form['phone'])

	cur = mysql.connection.cursor()
	cur.execute("SELECT MAX(user_id) FROM user")
	maxid = cur.fetchone()
	print(maxid)
	cmd = f'''INSERT INTO user (user_id, name, coins, email_id, contact_num) VALUES ({maxid['MAX(user_id)'] + 1}, '{name}', 100, '{email}', '{phone}')'''
	print(cmd)
	cur.execute(cmd)
	mysql.connection.commit()

	return 'Inserted!'

@app.route('/home/<name>/<user_id>')
def home(name, user_id):
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	return render_template('home.html', name = name, user_id = user_id)

@app.route('/addbook', methods = ['GET', 'POST'])
def add_book():
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	if request.method == 'POST':
		bookname = request.form['name']
		author = request.form['author']
		description = request.form['description']
		# print(request.form)
		transaction_type = request.form['transaction_type']

		print(bookname)
		print(author)

		session['book_to_add'] = request.form
		print(request.form)

		cur = mysql.connection.cursor()
		cmd = f"SELECT * FROM unique_books"
		cur.execute(cmd)
		unique_books = cur.fetchall()
		
		similar_books = []

		for book in unique_books:
			if SequenceMatcher(None, bookname.lower(), book['name'].lower()).ratio() >= 0.8 and SequenceMatcher(None, author.lower(), book['author'].lower()).ratio() >= 0.8:
				similar_books.append(book)

		session['similar_books'] = similar_books
		
		return redirect(url_for('add_book2', transaction_type = transaction_type))

	return render_template('add_book.html')

# @app.route('/addbook2')
@app.route('/addbook2/<transaction_type>', methods = ['GET', 'POST'])
def add_book2(transaction_type):
	if request.method == 'POST':
		print(request.form, "<---")
		if request.form['book'] == 'none':
			print(session['book_to_add']['author'])

			# insert into unique_books

			cur = mysql.connection.cursor()
			cur.execute("SELECT MAX(unique_id) FROM unique_books")
			maxid = cur.fetchone()
			max_uid = maxid['MAX(unique_id)'] + 1
			cmd = f"INSERT INTO unique_books VALUES ({max_uid}, '{session['book_to_add']['name']}', '{session['book_to_add']['author']}', 1, 0, 0, 1)"
			print(cmd)
			cur.execute(cmd)
			mysql.connection.commit()

			# insert into all_books

			cur = mysql.connection.cursor()
			cur.execute("SELECT MAX(book_id) FROM all_books")
			maxid = cur.fetchone()
			cmd = f"INSERT INTO all_books VALUES ({maxid['MAX(book_id)'] + 1}, '{session['book_to_add']['description']}', {session['book_to_add']['pagecount']}, {transaction_type}, {max_uid}, {session['id']})"
			cur.execute(cmd)
			mysql.connection.commit()

			return "Added successfully"
		
		return "Not added"

	print(transaction_type)

	similar_books = session['similar_books']

	print(similar_books)
	print(type(similar_books))
	
	return render_template('add_book2.html', transaction_type = transaction_type, similar_books = similar_books)

@app.route('/mybooks/<user_id>')
def my_books(user_id):
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	cur = mysql.connection.cursor()
	# cur.execute(f"SELECT * FROM user WHERE user_id = '{user_id}'")
	cmd = f"SELECT * FROM all_books WHERE user_id = {user_id}"
	cur.execute(cmd)
	books = cur.fetchall()
	print(books)

	for i in range(len(books)):
		print(books[i])
		cmd = f"SELECT * FROM unique_books WHERE unique_id = {books[i]['unique_id']}"
		cur.execute(cmd)
		unique_book = cur.fetchone()
		books[i]['name'] = unique_book['name']
		books[i]['author'] = unique_book['author']

	return render_template('my_books.html', books = books)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('name', None)
	session.pop('email', None)

	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True, port = 5001)