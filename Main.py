from flask import Flask, redirect, url_for, render_template, flash, request, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()

#Bp imports
#from file import blueprint name
app = Flask(__name__)
from Blueprints import auth_bp
app.register_blueprint(auth_bp)
from Blueprints import account_bp
app.register_blueprint(account_bp)
from Models import db



database = os.getenv("DATABASE")
host = os.getenv("HOST")
name = os.getenv("NAME")
password = os.getenv("PASSWORD")
secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{name}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secret_key

db.init_app(app)




#Account Creation and stuff
@app.route('/', methods=["GET"])
def home():
	return render_template('home.html')



if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run(debug=True)


