from flask import Blueprint, render_template, session, url_for, request, flash, redirect
from Models import Users, Posts
from Main import sesh
from datetime import datetime
from sqlalchemy import desc


account_bp = Blueprint("account_bp", __name__, static_folder="static", template_folder="templates")





#Posting and Viewing Content
@account_bp.route('/view_posts', methods=["GET"])
def view_posts():
	if 'name' in session:
		username = session.get("name")
		posts = sesh.query(Posts).order_by(desc(Posts.id)).all()
		return render_template("view_posts.html", posts=posts)

	return redirect(url_for('home'))





@account_bp.route('/view_my_posts', methods=["GET"])
def view_my_posts():
	if "name" in session:
		username = session.get('name')
		posts = sesh.query(Posts).filter(Posts.username == username).order_by(desc(Posts.id)).all()
		return render_template('view_my_posts.html', posts=posts)
	return redirect(url_for('home'))


@account_bp.route('/post', methods=["POST", "GET"])
def post():
	if "name" in session:
		if request.method == "POST":
			username = session.get('name')
			title = request.form.get('title')
			description = request.form.get('description')
			
			now = datetime.now()
			formatted_date = now.strftime("%m-%d-%Y")
			user = sesh.query(Users).filter(Users.username == username).first()


			if not user:
				flash("User not found.", "error2")


			elif not title:
				flash("Post Must Include Title", "info2")
				
			elif len(title) > 40:
				flash("Post Title Cannot Exceed 40 Characters", "info2")
				
			elif len(description) > 400:
				flash("Post Description Cannot Exceed 400 Characters", "info2")
				
			
			else:
				try:
					post_data = Posts(user.id, formatted_date, title, description, username)
					sesh.add(post_data)
					sesh.commit()
					flash(f"Successfully Posted '{title}'", "good2")
				except Exception as e:
					sesh.rollback()
					flash(f"Error Posting {title}. {e}", "error2")


		return render_template('post.html')
	return redirect(url_for('home'))



@account_bp.route('/account', methods=["GET"])
def account():
	if 'name' in session:
		username = session.get("name")
		return render_template("account.html", username=username)
	
	return redirect(url_for('home'))





@account_bp.route('/logout', methods=["GET"])
def logout():
	username = session.get('name')
	flash(f"Successfully Logged Out of {username}!", "good")
	session.pop('name', None)
	return redirect(url_for('home'))


@account_bp.route('/delete', methods=["POST"])
def delete():
	post_id = request.form.get('post_id')
	
	post_to_delete = sesh.query(Posts).filter(Posts.id == post_id).first()
	title = post_to_delete.title
	if post_to_delete:
		sesh.delete(post_to_delete)
		sesh.commit()
		flash(f"Successfully Deleted Post '{title}'!", "good2")
		return redirect(url_for('account_bp.view_my_posts'))

	else:
		flash(f"Error, Could not Delete Post '{title}'", "error2")
		return redirect(url_for('account_bp.view_my_posts'))
