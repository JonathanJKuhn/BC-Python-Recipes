from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

@app.route('/recipes')
def all_recipes():
    if not session:
        flash("Please Register/Login to access the site")
        return redirect('/')
    data = { 'id': session['id'] }
    user_data = User.get_user_by_id(data)

    return render_template('all_recipes.html',title='Recipe Share',user=user_data)