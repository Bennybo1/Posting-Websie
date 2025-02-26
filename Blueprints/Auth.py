from flask import Blueprint, render_template, session, url_for, request, flash, redirect
import bcrypt
#gets out database info and models
from Models import Users
from Main import sesh

#creates our blueprint
auth_bp = Blueprint("auth_bp", __name__, static_folder="static", template_folder="templates")






@auth_bp.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		existing_user = sesh.query(Users).filter(Users.username == username).first()
		#filtered result ex: Jim | JimLikesCows@_Mo0
		#So all we have to do it check if the password is equal to the Users.password because there is only one!
							#use the name existing user because thats the name of the query we made up there
		if existing_user and bcrypt.checkpw(password.encode(), existing_user.password.encode()):
			try:
				flash("Successfully Logged in", "good")
				session['name'] = username
				return redirect(url_for("account_bp.account", username=username))
				

			except Exception as e:
				flash(f"Error Loging In. {e}", "error")
		else:
			flash("Username Or Password is Incorrect", "info")
	return render_template('login.html')





@auth_bp.route('/sign_up', methods=["GET", "POST"])
def sign_up():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]


		existing_user = sesh.query(Users).filter(Users.username == username).first()
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
					
					
					sesh.add(passed_data)
					sesh.commit()
					flash("Successfully Made Account", "good")
					session['name'] = username
					return redirect(url_for("account_bp.account", username=username))
					
				except Exception as e:
					sesh.rollback()
					flash(f"Error Making Account. {e}", "error")
					

	return render_template('sign_up.html')