# Библиотеки для приложения и БД
import datetime
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# Библиотеки для безопасности, входа в аккаунт
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
# Инициализируем БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fish_app.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)


class Post(db.Model):
    """ Класс-модель для БД, отвечает за сохранение созданного поста в БД """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Внешний ключ на таблицу User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)


class User(db.Model):
    """ Класс-модель для БД, таблица данных пользователя """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)


@app.route("/")
def root():
    return "<h1>Не забудь добавить /main в адрес</h1>"


@app.route("/main")
def main_page():
    return render_template("main.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/create", methods=['POST', 'GET'])
def create():
    user_id = session.get('user_id')   # тот же ключ, что в login/register
    print("user_id из сессии:", user_id)

    if not user_id:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        post = Post(title=title, content=content, user_id=user_id)  # ВАЖНО: user_id, не id
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/main')
        except Exception as e:
            print("Ошибка при добавлении поста:", e)
            return '<h3>При добавлении статьи возникла ошибка!</h3>'

    return render_template('create.html')


@app.route("/posts")
def posts():

    # Забираем все записи из БД
    posts = Post.query.all()

    return render_template('posts.html', posts=posts)



# Функция получения страницы конкретного текста по Id
@app.route("/one_post_page/<int:post_id>")
def one_post_page(post_id):
    # Получаем текст по id иначе возвращаем ошибку 404
    post = Post.query.get_or_404(post_id)
    print(post_id)
    # Возвращаем страницу с текстом
    return render_template("one_post_page.html", post=post)


# Функция отправки данных страницы авторизации в бд
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()

            # используем один ключ session: user_id
            session['user_id'] = user.id
            session['username'] = user.username

            print("Пользователь зарегистрирован")
            return redirect('/main')
        except Exception as e:
            print("Ошибка при регистрации:", e)
            return '<h3>При добавлении пользователя возникла ошибка!</h3>'
    # GET-запрос
    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/main')
        else:
            return render_template('login.html', error="Неверный email или пароль")

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/main')


# Запуск программы
if __name__ == '__main__':
    # Используя весь контекст программы
    with app.app_context():
        # Создание всех моделей
        db.create_all()
    # Запуск с логированием
    app.run(debug=True)
