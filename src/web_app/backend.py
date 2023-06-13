# backend.py
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, \
                        login_required, current_user
from src.web_app.models import db, User, Comment, Mushroom
import src.web_app.forms as forms
import uuid
from src.model_training.predict_species import predict_mushroom_species


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'src/web_app/static/images/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SECRET_KEY'] = 'tajny-klucz'

    db.init_app(app)
    Migrate(app, db)

    return app


app = create_app()
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Utwórz folder uploads, jeżeli nie istnieje
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data,
            method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('upload_file'))
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('upload_file'))


@app.route('/mushroom/<int:mushroom_id>', methods=['GET', 'POST'])
def mushroom_detail(mushroom_id):
    mushroom = Mushroom.query.get_or_404(mushroom_id)
    user = User.query.get(mushroom.user_id)
    if request.method == 'POST':
        text = request.form['text']
        new_comment = Comment(user_id=current_user.id, text=text, mushroom=mushroom)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('mushroom_detail', mushroom_id=mushroom_id))
    return render_template('mushroom_detail.html', mushroom=mushroom, user=user)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
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
        return redirect(url_for('mushroom_detail', mushroom_id=new_mushroom.id))
    mushrooms = Mushroom.query.all()
    return render_template('upload.html', mushrooms=mushrooms)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
