from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


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
		