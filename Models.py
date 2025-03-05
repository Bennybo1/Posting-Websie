from Main import Base
from sqlalchemy import create_engine, Integer, String, Date, Float, Boolean, Column, ForeignKey, CHAR





#database
class Users(Base):
	__tablename__ = "Users"
	id = Column("id", Integer, primary_key=True)
	username = Column("username", String(50))
	password = Column("password", String(100))

	def __init__(self, username, password):
		self.username = username
		self.password = password


class Posts(Base):
	__tablename__ = "Posts"
	id = Column(Integer, primary_key=True)  # Unique primary key for each post
	user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)  # Reference to Users' id
	date = Column(String(30), nullable=False)
	title = Column(String(50), nullable=False)
	description = Column(String(400), nullable=True)
	username = Column(String(50), nullable=False)
	edited = Column(Boolean, default=False)
	

	def __init__(self, user_id, date, title, description, username):
		self.user_id = user_id
		self.date = date
		self.title = title
		self.description = description
		self.username = username
		