import os
import uuid
from flask import (jsonify, render_template, redirect, url_for,
                   request, send_from_directory)
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..model_training.predict_species import predict_mushroom_species
from .db_models import User, Comment, Mushroom
from .forms import RegistrationForm, LoginForm
from .mushroom_table import mushroom_species
from .app_config import app, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        redirect_url = url_for('homepage')
        return jsonify({'redirect': redirect_url})
    elif request.method == 'POST':
        return jsonify({'error': 'User with given login already exists'}), 400
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            redirect_url = url_for('homepage')
            return jsonify({'redirect': redirect_url})
        else:
            return jsonify({'error': 'Invalid username or password'}), 400
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/mushroom/<int:mushroom_id>', methods=['GET', 'POST'])
def mushroom_detail(mushroom_id):
    mushroom = Mushroom.query.get_or_404(mushroom_id)
    user = User.query.get(mushroom.user_id)
    if request.method == 'POST':
        text = request.form['text']
        new_comment = Comment(
            user_id=current_user.id,
            text=text,
            mushroom=mushroom)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('mushroom_detail', mushroom_id=mushroom_id))
    return render_template(
        'mushroom_detail.html',
        mushroom=mushroom,
        user=user)


@app.route('/upload', methods=['GET', 'POST'])
def upload_mushroom():
    if request.method == 'POST':
        file = request.files['file']
        if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({'error': 'Invalid file format.'}), 400

        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        species, odds = predict_mushroom_species(file_path)
        new_mushroom = Mushroom(
            image_path=f'images/{filename}',
            user_id=current_user.id,
            species=species,
            odds=odds)
        db.session.add(new_mushroom)
        db.session.commit()

        redirect_url = url_for('mushroom_detail', mushroom_id=new_mushroom.id)
        return jsonify({'redirect': redirect_url})

    redirect_url = url_for('homepage')
    return jsonify({'redirect': redirect_url})


@app.route('/')
def homepage():
    mushrooms = Mushroom.query.all()
    return render_template(
        'homepage.html',
        mushrooms=mushrooms,
        mushroom_species=mushroom_species)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
