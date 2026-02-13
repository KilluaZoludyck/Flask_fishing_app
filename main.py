from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def root():
    return "<h1>Не забудь добавить /main в адрес</h1>"


@app.route("/main")
def main_page():
    return render_template("main.html")


@app.route("/about")
def about_page():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True)
