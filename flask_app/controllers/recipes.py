from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

# We want this helper function to help dry-out route guards
def login_check():
    if not session:
        flash("Please Register/Login to access the site")
        return redirect('/')

@app.route('/recipes')
def all_recipes():
    login_check()
    user_id = { 'id': session['id'] }
    user_data = User.get_user_by_id(user_id)
    recipes_data = Recipe.get_all()
    return render_template('all_recipes.html',title='Recipe Share',user=user_data,recipes=recipes_data)

@app.route('/recipes/new')
def r_new_recipe():
    login_check()
    return render_template('new_recipe.html',title='Recipe Share')

@app.route('/recipes/create', methods=['POST'])
def f_new_recipe():
    login_check()
    data = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'instructions': request.form.get('instructions'),
        'date_made': request.form.get('date_made'),
        'under_30': bool(request.form.get('under_30')),
    }
    # We want to keep the information that the user has input, so they can more easily correct inputs
    if not Recipe.validate_recipe(data):
        for key in data:
            session[key] = data[key]
        return redirect('/recipes/new')
    
    data['user_id'] = session['id']
    Recipe.add(data)
    return redirect('/recipes')
