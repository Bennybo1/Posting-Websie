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
	
	return redirect(url_for('auth_bp.login'))


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
	
	return redirect(url_for('auth_bp.login'))



@account_bp.route('/account', methods=["GET"])
def account():
	if 'name' in session:
		username = session.get("name")
		return render_template("account.html", username=username)
	
	
	return redirect(url_for('auth_bp.login'))





@account_bp.route('/logout', methods=["GET"])
def logout():
	username = session.get('name')
	flash(f"Successfully Logged Out of {username}!", "good")
	session.pop('name', None)
	
	return redirect(url_for('auth_bp.login'))


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

@account_bp.route('/edit', methods=['POST', 'GET'])
def edit():
	if 'name' in session:
		
		if request.method == "GET":
			post_id = request.args.get('post_id')
			if post_id == None:
				flash("Cannot Find Post To Edit!", "error2")
				return redirect(url_for("account_bp.account"))
			current_post = sesh.query(Posts).filter(Posts.id == post_id).first()
			old_title = current_post.title
			old_desc = current_post.description
			return render_template("edit.html", post_id=post_id, old_title=old_title, old_desc=old_desc)
			

		elif request.method == "POST":
			old_title = request.form.get("title")
			old_desc = request.form.get("description")
			new_title = request.form.get('new_title')
			new_desc = request.form.get('new_description')
			post_id = request.form.get('post_id')
			

			if not new_title:
				flash("Title Cannot Be Empty!", "info2")
			elif len(new_desc) > 399:
				flash("Description Cannot Exceed 399 Characters!", "info2")

			elif len(new_title) > 39:
				flash("Title Cannot Exceed 39 Characters!", "info2")
			else:
				post_to_edit = sesh.query(Posts).filter(Posts.id == post_id).first()
				post_to_edit.title = new_title
				post_to_edit.description = new_desc
				post_to_edit.edited = True
				sesh.commit()
				flash("Successfully Edited Post!", "good2")
				return redirect(url_for("account_bp.account"))
				
			current_post = sesh.query(Posts).filter(Posts.id == post_id).first()
			old_title = current_post.title
			old_desc = current_post.description
			return render_template("edit.html", post_id=post_id, old_title=old_title, old_desc=old_desc)
	
	return redirect(url_for('auth_bp.login'))
