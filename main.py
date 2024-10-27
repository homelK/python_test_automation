from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime

# Flask app initialization and configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap5(app)

# initialization a text area from CKEditor
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

class BlogForm(FlaskForm):
    csrf_token = app.config['SECRET_KEY']
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Blog Post Subtitle", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL()])
    body = CKEditorField('Blog Content')
    submit = SubmitField("Send post")

@app.route('/', methods=["GET"])
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)

@app.route('/post/<int:post_id>', methods=["GET"])
def show_post(post_id):
    requested_post = BlogPost.query.filter(BlogPost.id == post_id).one_or_none()
    return render_template("post.html", post=requested_post)

@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    form = BlogForm()
    if form.validate_on_submit():
        new_post = BlogPost()
        new_post.title = form.title.data
        new_post.subtitle = form.subtitle.data
        new_post.date = datetime.date.today().strftime("%B %d, %Y")
        new_post.body = form.body.data
        new_post.author = form.author.data
        new_post.img_url = form.url.data
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form)

@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    post_to_edit = BlogPost.query.filter(BlogPost.id == post_id).one_or_none()
    form = BlogForm(
        title=post_to_edit.title,
        subtitle=post_to_edit.subtitle,
        author=post_to_edit.author,
        url=post_to_edit.img_url,
        body=post_to_edit.body
    )
    if form.validate_on_submit():
        post_to_edit.title = form.title.data
        post_to_edit.subtitle = form.subtitle.data
        post_to_edit.img_url = form.url.data
        post_to_edit.author = form.author.data
        post_to_edit.body = form.body.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_to_edit.id))
    return render_template("make-post.html", form=form, post_id=post_id)

@app.route("/delete/<int:post_id>", methods=["GET"])
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, port=5003)
