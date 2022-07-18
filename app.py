from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    introduction = db.Column(db.String(300), nullable=False)
    main_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/faculty')
def faculty():
    return render_template("faculty.html")


@app.route('/courses')
def courses():
    return render_template("courses.html")


@app.route('/read-feedback')
def read_feedback():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("read-feedback.html", articles=articles)


"""Create an page for each feedback's details that allow us to click on each article with unique url like - /read-feedback/1"""


@app.route('/read-feedback/<int:id>')
def feedback_details(id):
    article = Article.query.get(id)
    return render_template("feedback_details.html", article=article)


"""Create a button that allow us to delete any feedback from our database."""


@app.route('/read-feedback/<int:id>/delete')
def feedback_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/read-feedback")
    except TypeError:
        return "An error occurred during the process of deleting of an article."


"""Add to our write-feedback page methods in order that our write-feedback page can receive some data."""


@app.route('/write-feedback', methods=['POST', 'GET'])
def write_feedback():
    if request.method == "POST":
        title = request.form['title']
        introduction = request.form['introduction']
        main_text = request.form['main_text']

        article = Article(title=title, introduction=introduction, main_text=main_text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/read-feedback')
        except TypeError:
            return "An error occurred during the process of adding new article."
    else:
        return render_template("write-feedback.html")


"""If we want to update our article we need to create this new page with updates."""


@app.route('/read-feedback/<int:id>/update', methods=['POST', 'GET'])
def feedback_update(id):
    article = Article.query.get_or_404(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.introduction = request.form['introduction']
        article.main_text = request.form['main_text']

        try:
            db.session.commit()
            return redirect('/read-feedback')
        except TypeError:
            return "An error occurred during the process of updating of an article."
    else:
        return render_template("feedback_update.html", article=article)


if __name__ == "__main__":
    app.run(debug=True)

