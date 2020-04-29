from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
from difflib import SequenceMatcher

app = Flask(__name__)

app.secret_key = '9afd69d3d6ff1bdd87f0deb0'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'dbms'
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
	if user:
		if (user['password']==password):
			session['loggedin'] = True
			session['id'] = user['user_id']
			session['name'] = user['name']
			session['email'] = user['email_id']
			# Redirect to home page
			return redirect(url_for('home', name = user['name'], user_id = user['user_id']))
		else:
			return redirect(url_for('login', msg = 'wrong password'))

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
	password = str(request.form['psw'])
	cur = mysql.connection.cursor()
	cur.execute("SELECT MAX(user_id) FROM user")
	maxid = cur.fetchone()
	print(maxid)
	try:
		cmd = f'''INSERT INTO user (user_id, name, user_type, email_id, contact_num, location, password) VALUES ({maxid['MAX(user_id)'] + 1}, '{name}', 1, '{email}', '{phone}', '110025', '{password}')'''
	except:
		cmd = f'''INSERT INTO user (user_id, name, user_type, email_id, contact_num, location, password) VALUES (1, '{name}', 1, '{email}', '{phone}', '110025', '{password}')'''
	print(cmd)
	cur.execute(cmd)
	mysql.connection.commit()

	return redirect(url_for('login', msg = 'now you may login'))

@app.route('/home/<name>/<user_id>')
def home(name, user_id):
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	if 'mybooks' in session:
		session.pop('mybooks', None)

	return render_template('home.html', name = name, user_id = user_id)

@app.route('/search', methods = ['GET'])
def search():
	name = request.args.get('name', "")
	author = request.args.get('author', "")
	# description = request.args.get('description', "")
	genre = request.args.get('genre', "")

	cur = mysql.connection.cursor()

	search_results = []

	if True:
		name = name.lower().strip()
		suthor = author.lower().strip()
		genre = genre.lower().strip()

		if len(genre) == 0:
			cmd = f"SELECT * FROM unique_books WHERE lower(name) LIKE '%{name}%' AND lower(author) LIKE '%{author}%'"
		else:
			cmd = f"SELECT * FROM unique_books as u, book_genre_relation as b WHERE u.unique_id = b.unique_id AND lower(name) LIKE '%{name}%' AND lower(author) LIKE '%{author}%' AND lower(genre_name) LIKE '%{genre}%'"
		
		print(cmd)
		cur.execute(cmd)

		for result in cur.fetchall():
			search_results.append(result)

	# if len(author) > 0:
	# 	author.lower()
	# 	cmd = f"SELECT * FROM unique_books WHERE lower(author) LIKE '%{author}%'"
	# 	print(cmd)
	# 	cur.execute(cmd)

	# 	for result in cur.fetchall():
	# 		search_results.append(result)

	# if len(description) > 0:
	# 	print("Description: " + description)
	# 	description.lower()
	# 	cmd = f"SELECT * FROM all_books WHERE lower(description) LIKE '%{description}%'"
	# 	print(cmd)
	# 	cur.execute(cmd)

	# 	for result in cur.fetchall():
	# 		search_results.append(result)

	return render_template('search.html', search_results = search_results)

@app.route('/addbook', methods = ['GET', 'POST'])
def add_book():
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	if request.method == 'POST':
		
		# replace single with double quotes to safely insert in database

		bookname = request.form['name'].strip()
		author = request.form['author'].strip()
		description = request.form['description'].strip()
		transaction_type = request.form['transaction_type']

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

	return render_template('add-book.html')

# @app.route('/addbook2')
@app.route('/addbook2/<transaction_type>', methods = ['GET', 'POST'])
def add_book2(transaction_type):
	cur = mysql.connection.cursor()

	if request.method == 'POST':
		print(request.form)

		if request.form['book'] == 'none':
			print("HERE!!!", session['book_to_add'])

			# insert into unique_books

			cur.execute("SELECT MAX(unique_id) FROM unique_books")
			maxid = cur.fetchone()
			try:
				uid = maxid['MAX(unique_id)'] + 1
			except:
				uid = 1
			cmd = f"INSERT INTO unique_books VALUES ({uid}, '{session['book_to_add']['name']}', '{session['book_to_add']['author']}', 1, 0, 0, 1)"
			print(cmd)
			cur.execute(cmd)

		else:
			# update book_count in unique_books	

			cmd = f"SELECT * FROM unique_books WHERE unique_id = {request.form['book']}"
			print(cmd)
			cur.execute(cmd)
			unique_book = cur.fetchone()
			uid = unique_book['unique_id']
			cmd = f"UPDATE unique_books SET book_count = book_count + 1 WHERE unique_id = {uid}"
			print(cmd)
			cur.execute(cmd)

		# insert into all_books

		# cur = mysql.connection.cursor()
		cur.execute("SELECT MAX(book_id) FROM all_books")
		maxid = cur.fetchone()
		try:
			max_bid = maxid['MAX(book_id)'] + 1
		except:
			max_bid = 1
		cmd = f"INSERT INTO all_books VALUES ({max_bid}, '{session['book_to_add']['description']}', {session['book_to_add']['pagecount']}, {transaction_type}, {uid}, {session['id']})"
		print(cmd)
		cur.execute(cmd)

		# add to corresponding transaction_type table

		if transaction_type == '1':
			# cur.execute("SELECT MAX(book_id) FROM available_for_exchange")
			# maxid = cur.fetchone()
			cmd = f"INSERT INTO available_for_exchange VALUES ({max_bid}, '{session['book_to_add']['exchange-description']}')"
			print(cmd)
			cur.execute(cmd)

		elif transaction_type == '2':
			# cur.execute("SELECT MAX(book_id) FROM available_for_borrowing")
			# maxid = cur.fetchone()
			cmd = f"INSERT INTO available_for_borrowing VALUES ({max_bid}, {session['book_to_add']['price']}, {session['book_to_add']['num-of-days']})"
			print(cmd)
			cur.execute(cmd)

		elif transaction_type == '3':
			# cur.execute("SELECT MAX(book_id) FROM available_for_buying")
			# maxid = cur.fetchone()
			cmd = f"INSERT INTO available_for_buying VALUES ({max_bid}, {session['book_to_add']['price']})"
			print(cmd)
			cur.execute(cmd)
				
			# clear book details from session

		if len(request.form["genre1"]) > 0:
			cmd = f"SELECT * FROM genre WHERE lower(genre_name) = '{request.form['genre1'].lower()}'"
			cur.execute(cmd)

			if len(cur.fetchall()) == 0:					
				cmd = f"INSERT INTO genre VALUES ('{request.form['genre1'].lower()}')"
				print(cmd)
				cur.execute(cmd)

			cmd = f"INSERT INTO book_genre_relation VALUES ({uid}, '{request.form['genre1'].lower()}')"
			print(cmd)
			cur.execute(cmd)
			
		if len(request.form["genre2"]) > 0:
			cmd = f"SELECT * FROM genre WHERE lower(genre_name) = '{request.form['genre2'].lower()}'"
			cur.execute(cmd)
			
			if len(cur.fetchall()) == 0:								
				cmd = f"INSERT INTO genre VALUES ('{request.form['genre2'].lower()}')"
				print(cmd)
				cur.execute(cmd)

			cmd = f"INSERT INTO book_genre_relation VALUES ({uid}, '{request.form['genre2'].lower()}')"
			print(cmd)
			cur.execute(cmd)

		if len(request.form["genre3"]) > 0:
			cmd = f"SELECT * FROM genre WHERE lower(genre_name) = '{request.form['genre3'].lower()}'"
			cur.execute(cmd)
			
			if len(cur.fetchall()) == 0:								
				cmd = f"INSERT INTO genre VALUES ('{request.form['genre3'].lower()}')"
				print(cmd)
				cur.execute(cmd)

			cmd = f"INSERT INTO book_genre_relation VALUES ({uid}, '{request.form['genre3'].lower()}')"
			print(cmd)
			cur.execute(cmd)

		mysql.connection.commit()

		return redirect(url_for('success_page', msg = "Book added successfully!"))

	print(transaction_type)
	similar_books = session['similar_books']
	print(similar_books)
	print(type(similar_books))
	
	return render_template('add-book2.html', transaction_type = transaction_type, similar_books = similar_books)

@app.route('/mybooks')
def my_books():
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	cur = mysql.connection.cursor()
	# cur.execute(f"SELECT * FROM user WHERE user_id = '{user_id}'")
	cmd = f"SELECT * FROM all_books WHERE user_id = {session['id']}"
	cur.execute(cmd)
	books = cur.fetchall()
	print(books)

	session['mybooks'] = {}

	for book in books:
		print(book)
		cmd = f"SELECT * FROM unique_books WHERE unique_id = {book['unique_id']}"
		cur.execute(cmd)
		unique_book = cur.fetchone()
		book['name'] = unique_book['name']
		book['author'] = unique_book['author']

		if book['transaction_type'] == 1:
			print(book)
			cmd = f"SELECT * FROM available_for_exchange WHERE book_id = {book['book_id']}"
			cur.execute(cmd)
			exchange_book = cur.fetchone()
			print(exchange_book)
			if exchange_book is not None:
				book['exchange_with'] = exchange_book['exchange_with']

		elif book['transaction_type'] == 2:
			cmd = f"SELECT * FROM available_for_borrowing WHERE book_id = {book['book_id']}"
			cur.execute(cmd)
			lend_book = cur.fetchone()
			if lend_book is not None:
				book['price'] = lend_book['price']
				book['num_of_days'] = lend_book['num_of_days']

		elif book['transaction_type'] == 3:
			cmd = f"SELECT * FROM available_for_buying WHERE book_id = {book['book_id']}"
			cur.execute(cmd)
			sell_book = cur.fetchone()
			if sell_book is not None:
				book['price'] = sell_book['price']

		session['mybooks'][book['book_id']] = book

	return render_template('my-books.html', books = books)

@app.route('/mybooks/editbook/<book_id>', methods = ['GET','POST'])
def edit_book(book_id):
	if request.method == 'POST':
		cur = mysql.connection.cursor()

		print(request.form)

		cmd = f"UPDATE all_books SET description = '{request.form['description']}', page_count = '{request.form['page_count']}' WHERE book_id = {book_id};"	
		print(cmd)
		cur.execute(cmd)

		if request.form['transaction_type'] == '1':
			cmd = f"UPDATE available_for_exchange SET exchange_with = '{request.form['exchange-description']}' WHERE book_id = {book_id};"
			print(cmd)
			cur.execute(cmd)
		
		elif request.form['transaction_type'] == '2':
			cmd = f"UPDATE available_for_borrowing SET num_of_days = '{request.form['num_of_days']}', price = '{request.form['price']}' WHERE book_id = {book_id};"
			print(cmd)
			cur.execute(cmd)
		
		elif request.form['transaction_type'] == '3':
			cmd = f"UPDATE available_for_buying SET price = '{request.form['price']}' WHERE book_id = {book_id};"
			print(cmd)
			cur.execute(cmd)

		# commit the changes

		mysql.connection.commit()

		return redirect(url_for('success_page', msg = "Edited successfully!"))

	book_to_edit = session['mybooks'][book_id]
	session.pop('mybooks', None)
	print("Book to edit", book_to_edit)

	return render_template('edit-mybook.html', mybook = book_to_edit)

@app.route('/mybooks/deletebook/<book_id>', methods = ['POST'])
def delete_book(book_id):
	cur = mysql.connection.cursor()

	# get unique_id from all_books

	cmd = f"SELECT * FROM all_books WHERE book_id = {book_id }"
	print(cmd)
	cur.execute(cmd)
	book = cur.fetchone()
	print(book)
	unique_id = book['unique_id']
	print(unique_id)

	# delete from corresponding transaction type table

	cmd = f"DELETE FROM available_for_exchange WHERE book_id = { book_id }"
	print(cmd)
	cur.execute(cmd)

	cmd = f"DELETE FROM available_for_borrowing WHERE book_id = { book_id }"
	print(cmd)
	cur.execute(cmd)

	cmd = f"DELETE FROM available_for_buying WHERE book_id = { book_id }"
	print(cmd)
	cur.execute(cmd)

	# delete from all_books

	cmd = f"DELETE FROM all_books WHERE book_id = { book_id }"
	print(cmd)
	cur.execute(cmd)	

	# decrease book_count from unique_books

	cmd = f"UPDATE unique_books SET book_count = book_count - 1 WHERE unique_id = { unique_id }"
	print(cmd)
	cur.execute(cmd)

	# insert into archive

	try:
		cur.execute("SELECT MAX(transaction_id) FROM archive")
		maxid = cur.fetchone()
		max_tid = maxid['MAX(transaction_id)'] + 1

	except:
		max_tid = 1

	cmd = f"INSERT INTO archive VALUES ({max_tid}, {book_id}, {session['id']}, {book['transaction_type']})"
	print(cmd)
	cur.execute(cmd)

	# commit the changes

	mysql.connection.commit()

	return redirect(url_for('success_page', msg = "Deletion successful!"))

@app.route('/success/<msg>')
def success_page(msg):
	return render_template('success-page.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('name', None)
	session.pop('email', None)

	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True, port = 5001)
