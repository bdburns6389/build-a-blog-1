from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():

    blogs = Blog.query.all()
    print(blogs)
    print('hello')
    return render_template('blog.html',title="build-a-blog",
        blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        print ("hello")
        blog_title = request.form['blog_title']
        print(blog_title)
        if len(blog_title) <= 0:
            print("Empty blog title")
            blog_title_error = "Please include a blog title"
            return render_template('newpost.html', form=form, blog_title_error=blog_title_error)
        print("Good blog title")
        blog_body = request.form['blog_body']
        if len(blog_body) <= 0:
            print("Empty blog body")
            body_error = "Please include a post body"
            return render_template('newpost.html', form=form, body_error=body_error)
        print("Good blog body")
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        print("After post committed")
        return redirect('/blog?id={}'.format(new_blog.id))
    else:
        return render_template('newpost.html')

@app.route('/blog', methods=['GET'])
def blog():

    blog_id = int(request.args.get('id'))
    blog = Blog.query.filter_by(id=blog_id).first()

    return render_template('titlebody.html', blog=blog)

if __name__ == '__main__':
    app.run()
