from flask import Flask, redirect, url_for, render_template, flash, request, session, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from datetime import timedelta

from dotenv import load_dotenv
import os
load_dotenv()





#Bp imports
#from file import blueprint name
app = Flask(__name__)





database = os.getenv("DATABASE")
host = os.getenv("HOST")
name = os.getenv("NAME")
password = os.getenv("PASSWORD")
secret_key = os.getenv("SECRET_KEY")

engine = create_engine(f'mysql+mysqlconnector://{name}:{password}@{host}/{database}')
Session = sessionmaker(bind=engine) #makes a session so we can query
sesh = Session() #puts it into a variable we can use
Base = declarative_base()
app.secret_key = secret_key


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_HTTPONLY'] = True #dont allow js to edit
app.config['SESSION_COOKIE_SECURE'] = True  # Only over HTTPS secure connections are sent over


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #prevents unwanted tracking messages to waste memory and performance
#Account Creation and stuff
@app.route('/', methods=["GET"])
def home():
	return render_template('home.html')



if __name__ == "__main__":
	with app.app_context():
		# Create all tables in the database
		#also import bp to prevent import circles
		Base.metadata.create_all(bind=engine)
		from Blueprints import auth_bp, account_bp
		app.register_blueprint(auth_bp)
		app.register_blueprint(account_bp)
	app.run(debug=True)


