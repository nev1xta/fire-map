from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort

from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm, PositionForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        admin = db_sess.query(User).filter(User.login == 'admin').first()

        if user and user.check_password(form.password.data):
            if user != admin:
                return render_template('login.html',
                                       message="Вы не имеете доступ",
                                       form=form)
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/", methods=['GET'])
def index():
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.login != 'admin').all()
    admin = db_sess.query(User).filter(User.login == 'admin').first()

    if current_user != admin:
        return redirect('/login')

    if request.method == 'GET':
        return render_template("index.html", users=users, admin=admin)


@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def get_position(id):
    form = PositionForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            form.fio.data = user.fio
            form.password.data = user.hashed_password
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        if user:
            user.fio = form.fio.data
            user.set_password(form.password.data)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('user.html', title='Редактирование пользователя',
                           form=form)


@app.route('/user_del/<int:id>', methods=['GET', 'POST'])
@login_required
def user_del(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        db_sess.delete(user)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            fio=form.fio.data,
            login=form.login.data,
            position_name=form.position.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/fire-map_data.db")
    app.run()


if __name__ == '__main__':
    main()
