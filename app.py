from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
from difflib import SequenceMatcher
import config

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from figure import create_figure

app = Flask(__name__)

app.secret_key = '9afd69d3d6ff1bdd87f0deb0'

user_types = {1: 'school student', 2: 'college student', 3: "professor"}

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = config.MMYSQL_CURSORCLASS

mysql = MySQL(app)

@app.route('/')
@app.route('/login')
@app.route('/login/<msg>')
def login(msg = 'hola'):
	if 'loggedin' in session:
		return redirect(url_for('home', name = session['name'], user_id = session['id']))

	return render_template('login.html', msg = msg)

@app.route('/checkuser', methods = ['POST'])
def check_user():
	email = str(request.form['email'])
	password = str(request.form['psw'])
	cur = mysql.connection.cursor()
	cur.execute(f"SELECT * FROM user WHERE email_id = '{email}'")
	user = cur.fetchone()
	if user:
		if (user['password'] == password):
			session['loggedin'] = True
			session['id'] = user['user_id']
			session['name'] = user['name']
			session['email'] = user['email_id']
			session['user_type'] = user['user_type']
			# Redirect to home page
			return redirect(url_for('home', name = user['name'], user_id = user['user_id']))
		else:
			return redirect(url_for('login', msg = 'Wrong email or password'))

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
	location = str(request.form['location'])
	user_type = request.form['user_type']

	cur = mysql.connection.cursor()
	cur.execute("SELECT MAX(user_id) FROM user")
	maxid = cur.fetchone()
	print(maxid)

	# insert into user table

	try:
		cmd = f'''INSERT INTO user (user_id, name, email_id, contact_num, location, password, user_type) VALUES ({maxid['MAX(user_id)'] + 1}, '{name}', '{email}', '{phone}', '{location}', '{password}', '{user_type}')'''
	except:
		cmd = f'''INSERT INTO user (user_id, name, email_id, contact_num, location, password, user_type) VALUES (1, '{name}', '{email}', '{phone}', '{location}', '{password}', '{user_type}')'''
	
	print(cmd)
	cur.execute(cmd)
	mysql.connection.commit()

	return redirect(url_for('login', msg = 'now you can login'))

@app.route('/home/<name>/<user_id>')
def home(name, user_id):
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	cur = mysql.connection.cursor()

	if 'mybooks' in session:
		session.pop('mybooks', None)
	cur = mysql.connection.cursor()
	cmd = f"SELECT * from genre"
	cur.execute(cmd)
	available_genres = list(cur.fetchall())

	cmd = f"select new.genre_name from (select genre_name, count(*) as cnt from preferences group by genre_name) as new;"
	cur.execute(cmd)
	trending_genres = cur.fetchall()

	cmd = f'''select name from unique_books 
			where unique_id in (select * from (
			select unique_id from book_genre_relation 
			where genre_name in (select * from (
			select genre_name from preferences 
			where user_id = {session['id']}) as temp2)
			order by RAND()
			LIMIT 3) as temp1);'''
	
	cur.execute(cmd)
	recommendations = cur.fetchall()

	cmd = f'''select genre_name from (
			select new.genre_name, new.user_type, RANK() over (partition by new.user_type order by new.cnt desc) from (
			select genre_name,user_type, count(*) as cnt from preferences group by user_type, genre_name
        	) as new
			) as r where user_type = '{session['user_type']}';'''
	
	cur.execute(cmd)
	user_type_recommendations = cur.fetchall()

	return render_template('home.html', name = name, user_id = user_id, available_genres = available_genres, trending_genres = trending_genres, recommendations = recommendations, user_type_recommendations = user_type_recommendations)

@app.route('/search', methods = ['GET'])
def search():
	cur = mysql.connection.cursor()
	name = request.args.get('name', "")
	author = request.args.get('author', "")
	# description = request.args.get('description', "")
	genre = request.args.get('genre', "")

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

@app.route('/book/<unique_id>')
@app.route('/book/<unique_id>/<ttype>')
def ubook_page(unique_id, ttype = None):
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	cur = mysql.connection.cursor()

	# get unique_book details

	cmd = f"SELECT * FROM unique_books WHERE unique_id = {unique_id}"
	cur.execute(cmd)
	unique_book = cur.fetchone()

	if ttype is None:
		# get all_book details

		cmd = f"SELECT * FROM all_books WHERE unique_id = {unique_id}"
		cur.execute(cmd)
		all_books = cur.fetchall()

	else:

		cmd = f"SELECT * FROM all_books WHERE unique_id = {unique_id} AND transaction_type = {ttype}"
		cur.execute(cmd)
		all_books = cur.fetchall()

	# get genre details

	cmd = f"SELECT genre_name FROM book_genre_relation WHERE unique_id = {unique_id}"
	cur.execute(cmd)
	genres = cur.fetchall()
	unique_book['genres'] = []

	for genre in genres:
		unique_book['genres'].append(genre['genre_name'])

	# get reviews

	cmd = f"SELECT * FROM review WHERE unique_id = {unique_id}"
	cur.execute(cmd)
	reviews = cur.fetchall()
	unique_book['reviews'] = []

	for review in reviews:
		cmd = f"SELECT name, user_type FROM user WHERE user_id = {review['user_id']}"
		cur.execute(cmd)
		res = cur.fetchone()
		print(res)
		review['name'] = res['name']
		review['user_type'] = res['user_type']

		unique_book['reviews'].append(review)

	# get user details and respective transaction type details

	print("Allbooks:", all_books)

	for i in range(len(all_books)):
		cmd = f"SELECT * FROM user WHERE user_id = {all_books[i]['user_id']}"
		cur.execute(cmd)
		user = cur.fetchone()
		all_books[i].update(user)

		if all_books[i]['transaction_type'] == 1:
			cmd = f"SELECT * FROM available_for_exchange WHERE book_id = {all_books[i]['book_id']}"
		
		if all_books[i]['transaction_type'] == 2:
			cmd = f"SELECT * FROM available_for_borrowing WHERE book_id = {all_books[i]['book_id']}"

		if all_books[i]['transaction_type'] == 3:
			cmd = f"SELECT * FROM available_for_buying WHERE book_id = {all_books[i]['book_id']}"

		cur.execute(cmd)
		details = cur.fetchone()
		print("dets:", details)
		all_books[i].update(details)

	return render_template('ubook_page.html', unique_book = unique_book, all_books = all_books, user_types = user_types)

@app.route('/review', methods = ['POST'])
def review():
	cur = mysql.connection.cursor()

	user_id = session['id']
	rating = request.form['rating']
	title = request.form['title']
	body = request.form['body']
	unique_id = request.form['unique_id']

	try:
		cmd = f"INSERT INTO review VALUES ('{title}', {user_id}, '{body}', {unique_id})"
		print(cmd)
		cur.execute(cmd)

		cur.execute(f"SELECT review_count FROM unique_books WHERE unique_id = {unique_id}")
		review_count = cur.fetchone()
		print(review_count)
		review_count = review_count['review_count']

		cur.execute(f"SELECT rating FROM unique_books WHERE unique_id = {unique_id}")
		curr_rating = cur.fetchone()
		curr_rating = curr_rating['rating']

		# calculate new rating

		new_rating = (curr_rating * review_count + int(rating)) / (review_count + 1)

		# update unique_books

		cmd = f"UPDATE unique_books SET rating = {new_rating}, review_count = {review_count + 1}"
		cur.execute(cmd)

		msg = 'Review added successfully!'
	
	except Exception as e:
		print(e)
		msg = 'You have already added a review.'

	mysql.connection.commit()

	return redirect(url_for('success_page', msg = msg))

@app.route('/preferences')
@app.route('/preferences/<todo>/<genre>')
def preferences(todo = None, genre = None):
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	cur = mysql.connection.cursor()

	if todo is None:
		cmd = f"SELECT * from genre"
		cur.execute(cmd)
		available_genres = list(cur.fetchall())

		print(available_genres)

		cmd = f"SELECT genre_name FROM preferences WHERE user_id = {session['id']}"
		cur.execute(cmd)
		preferred_genres = cur.fetchall()

		print(preferred_genres)	

		for genre in preferred_genres:
			available_genres.remove(genre)

		print(available_genres)

		return render_template('preferences.html', available_genres = available_genres, preferred_genres = preferred_genres)

	elif todo == 'add':
		cmd = f"INSERT INTO preferences VALUES ({session['id']}, '{genre}', {session['user_type']})"
		cur.execute(cmd)

	elif todo == "remove":
		cmd = f"DELETE FROM preferences WHERE user_id = {session['id']} AND genre_name = '{genre}'"
		print(cmd)
		cur.execute(cmd)

	mysql.connection.commit()

	return redirect(url_for('preferences'))	

@app.route('/recommend/<unique_id>')
def recommend(unique_id):
	cur = mysql.connection.cursor()

	try:
		# add to recommendations
		cmd = f"INSERT INTO recommendations VALUES ({session['id']}, {unique_id})"
		cur.execute(cmd)

		# increment recommendation count in unique_bookss
		cmd = f"UPDATE unique_books SET recommendation_count = recommendation_count + 1 WHERE unique_id = {unique_id}"
		cur.execute(cmd)

		msg = "Recommended successfully!"

	except:
		msg = "You have already recommended this!"

	mysql.connection.commit()
	return redirect(url_for('success_page', msg = msg))

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
		print("Book to add form: ", request.form)

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
	if 'loggedin' not in session:
		return redirect(url_for('login'))

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
			cmd = f"INSERT INTO unique_books VALUES ({uid}, '{session['book_to_add']['name']}', '{session['book_to_add']['author']}', 0, 0, 0, 1)"
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
			print('session', session)
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
	print("mybooks", books)

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
	if 'loggedin' not in session:
		return redirect(url_for('login'))
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
	if 'loggedin' not in session:
		return redirect(url_for('login'))

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
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	return render_template('success-page.html', msg = msg)

@app.route('/analytics')
def analytics():
	pass

@app.route('/plot.png')
def plot_png():
	if 'loggedin' not in session:
		return redirect(url_for('login'))

	try:
		cur = mysql.connection.cursor()
		cmd = f'''select temp.genre_name, temp.transaction_type, count(*) as Total_Books from(select genre_name, transaction_type from archive s, book_genre_relation t where s.unique_id = t.unique_id) as temp group by temp.genre_name, temp.transaction_type with rollup;'''
		cur.execute(cmd)
		res = cur.fetchall()
		print(res)

		fig = create_figure(res)
		output = io.BytesIO()
		FigureCanvas(fig).print_png(output)
		return Response(output.getvalue(), mimetype='image/png')

	except:
		return redirect(url_for('success_page', msg = "Not enough data."))

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('name', None)
	session.pop('email', None)

	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True, port = 5001)
