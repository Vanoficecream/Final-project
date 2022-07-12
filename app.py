from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

"""Create class, 4 columns: id, title, introductory, text, """
"""1) The id of the article must be unique for that we use primary_key=True."""
"""2) The max length of title part is 100, also we apply nullable=False so our title can't be null."""
"""3) The max length of introductory part is 300, also we apply nullable=False so our intro part can't be null."""
"""4) Create the main text column with datatype - Text."""
"""5) Import datetime library to implement a function that allow us to see what time and date the article was created."""


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    introduction = db.Column(db.String(300), nullable=False)
    main_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


"""Access main page"""
"""Access also home page"""


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


"""Access page - about"""


@app.route('/about')
def about():
    return render_template("about.html")


"""Read the articles from our database"""


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


"""Create an page for each article's details that allow us to click on each article with unique url like - /posts/1"""


@app.route('/posts/<int:id>')
def post_details(id):
    article = Article.query.get(id)
    return render_template("post_details.html", article=article)


"""Create a button that allow us to delete any article from our database."""


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except TypeError:
        return "An error occurred during the process of deleting of an article."


"""Add to our create-article page methods in order that our create-article page can receive some data."""


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        introduction = request.form['introduction']
        main_text = request.form['main_text']

        article = Article(title=title, introduction=introduction, main_text=main_text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except TypeError:
            return "An error occurred during the process of adding new article."
    else:
        return render_template("create-article.html")


"""If we want to update our article we need to create this new page with updates."""


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get_or_404(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.introduction = request.form['introduction']
        article.main_text = request.form['main_text']

        try:
            db.session.commit()
            return redirect('/posts')
        except TypeError:
            return "An error occurred during the process of updating of an article."
    else:
        return render_template("post_update.html", article=article)


if __name__ == "__main__":
    app.run(debug=True)

