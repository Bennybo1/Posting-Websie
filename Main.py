from flask import Flask, redirect, url_for, render_template, flash, request, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime
from sqlalchemy import desc
app = Flask(__name__)
app.secret_key = 'Tottenham6th'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/blog_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


#database
class Users(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	username = db.Column("username", db.String(50))
	password = db.Column("password", db.String(100))

	def __init__(self, username, password):
		self.username = username
		self.password = password


class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)  # Unique primary key for each post
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Reference to Users' id
	date = db.Column(db.String(30), nullable=False)
	title = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(400), nullable=True)
	username = db.Column(db.String(50), nullable=False)
	

	def __init__(self, user_id, date, title, description, username):
		self.user_id = user_id
		self.date = date
		self.title = title
		self.description = description
		self.username = username
		




#Account Creation and stuff
@app.route('/', methods=["GET"])
def home():
	return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		existing_user = Users.query.filter_by(username=username).first()
		#filtered result ex: Jim | JimLikesCows@_Mo0
		#So all we have to do it check if the password is equal to the Users.password because there is only one!
							#use the name existing user because thats the name of the query we made up there
		if existing_user and bcrypt.checkpw(password.encode(), existing_user.password.encode()):
			try:
				flash("Successfully Logged in", "good")
				session['name'] = username
				return redirect(url_for("account", username=username))
				

			except Exception as e:
				flash(f"Error Loging In. {e}", "error")
		else:
			flash("Username Or Password is Incorrect", "info")
	return render_template('login.html')


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]


		existing_user = Users.query.filter_by(username=username).first()
		if existing_user: #is true
			flash("Name is Already Taken! Please Try another one", "info")

		else: #running a few checks
			if len(username) > 50:
				flash("Username Cannot Be Longer Than 50 Characters", "info")

			elif not username:
				flash("Username Cannot Be Empty")

			elif len(password) > 100:
				flash("Password Cannot Be Longer Than 100 Characters", "info")

			elif len(password) < 8:
				flash("Password Cannot Be Less Than 8 Characters", "info")
			elif len(username) < 3:
				flash("Username Cannot Be Less Than 3 Characters", "info")

			else:
				safe_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
				passed_data = Users(username, safe_password)
				try:
					
					
					db.session.add(passed_data)
					db.session.commit()
					flash("Successfully Made Account", "good")
					session['name'] = username
					return redirect(url_for("account", username=username))
					
				except Exception as e:
					db.session.rollback()
					flash(f"Error Making Account. {e}", "error")
					

	return render_template('sign_up.html')


@app.route('/account', methods=["GET"])
def account():
	if 'name' in session:
		username = session.get("name")
		return render_template("account.html", username=username)
	
	return redirect(url_for('home'))



#Posting and Viewing Content
@app.route('/view_posts', methods=["GET"])
def view_posts():
	if 'name' in session:
		username = session.get("name")
		posts = Posts.query.order_by(desc(Posts.id)).all()
		return render_template("view_posts.html", posts=posts)

	return redirect(url_for('home'))
	






@app.route('/post', methods=["POST", "GET"])
def post():
	if "name" in session:
		if request.method == "POST":
			username = session.get('name')
			title = request.form.get('title')
			description = request.form.get('description')
			
			now = datetime.now()
			formatted_date = now.strftime("%m-%d-%Y")
			user = Users.query.filter_by(username=username).first()


			if not user:
				flash("User not found.", "error2")


			elif not title:
				flash("Post Must Include Title", "info2")
				
			elif len(title) > 50:
				flash("Post Title Cannot Exceed 50 Characters", "info2")
				
			elif len(description) > 400:
				flash("Post Description Cannot Exceed 400 Characters", "info2")
				
			
			else:
				try:
					post_data = Posts(user.id, formatted_date, title, description, username)
					db.session.add(post_data)
					db.session.commit()
					flash(f"Successfully Posted '{title}'", "good2")
				except Exception as e:
					db.session.rollback()
					flash(f"Error Posting {title}. {e}", "error2")


		return render_template('post.html')
	return redirect(url_for('home'))



@app.route('/view_my_posts', methods=["GET"])
def view_my_posts():
	if "name" in session:
		username = session.get('name')
		posts = Posts.query.filter_by(username=username).order_by(desc(Posts.id)).all()
		return render_template('view_my_posts.html', posts=posts)
	return redirect(url_for('home'))

@app.route('/logout', methods=["GET"])
def logout():
	username = session.get('name')
	flash(f"Successfully Logged Out of {username}!", "good")
	session.pop('name', None)
	return redirect(url_for('home'))


@app.route('/delete', methods=["POST"])
def delete():
	post_id = request.form.get('post_id')
	
	post_to_delete = Posts.query.filter_by(id=post_id).first()
	title = post_to_delete.title
	if post_to_delete:
		db.session.delete(post_to_delete)
		db.session.commit()
		flash(f"Successfully Deleted Post '{title}'!", "good2")
		return redirect(url_for('view_my_posts'))

	else:
		flash(f"Error, Could not Delete Post '{title}'", "error2")
		return redirect(url_for('view_my_posts'))




if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run(debug=True)


# git test comment :)