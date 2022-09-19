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
    data = request.form.to_dict()
    data['under_30'] = bool(request.form.get('under_30'))
    # We want to keep the information that the user has input, so they can more easily correct inputs
    if not Recipe.validate_recipe(data):
        for key in data:
            session[key] = data[key]
        return redirect('/recipes/new')
    
    data['user_id'] = session['id']
    Recipe.add(data)
    return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    login_check()
    user_data = User.get_user_by_id({'id':session['id']})
    recipe_data = Recipe.get_one_by_id({'id':recipe_id})
    return render_template('view_recipe.html',title='Recipe Share',recipe=recipe_data,user=user_data)

@app.route('/recipes/edit/<int:recipe_id>')
def r_edit_recipe(recipe_id):
    login_check()
    recipe_data = Recipe.get_one_by_id({'id':recipe_id})
    if recipe_data.user_id != session['id']:
        flash("You must be the creator of a recipe to edit it")
        return redirect('/recipes')
    return render_template('edit_recipe.html',title='Recipe Share',recipe=recipe_data)

@app.route('/recipes/edit', methods=['POST'])
def f_edit_recipe():
    login_check()
    data = request.form.to_dict()
    data['under_30'] = bool(request.form.get('under_30'))
    Recipe.update(data)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    login_check()
    data = {'id':recipe_id}
    recipe_data = Recipe.get_one_by_id(data)
    if recipe_data.user_id != session['id']:
        flash("You must be the creator of a recipe to delete it")
        return redirect('/recipes')
    Recipe.delete(data)
    return redirect('/recipes')
