from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Инициализируем БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fish_app.db'
db = SQLAlchemy(app)


class Post(db.Model):
    """ Класс-модель для БД, отвечает за сохранение созданного поста в БД """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)


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
    # Проверка на тип метода
    if request.method == 'POST':
        # Если это отправка - то собираем данные и отправляем их в бд и возвращаем user на главную страницу
        title = request.form['title']
        content = request.form['content']

        post = Post(title=title, content=content)
        try:
            # Добавление в БД
            db.session.add(post)
            db.session.commit()
            return redirect('/main')
        except:
            return '<h3>При добавлении статьи возникла ошибка!</h3>'

    else:
        return render_template('create.html')


@app.route("/posts")
def posts():
    # Забираем все записи из БД
    posts = Post.query.all()

    return render_template('posts.html', posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
