from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'root'

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
    return render_template('blog.html',title="build-a-blog",
        blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        
        if len(blog_title) <= 0:
            blog_title_error = "Please include a blog title"
            return render_template('newpost.html', form=form, blog_title_error=blog_title_error)
        
        
        if len(blog_body) <= 0:
            body_error = "Please include a post body"
            return render_template('newpost.html', form=form, body_error=body_error)

        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

        return redirect('/blog?id={}'.format(new_blog.id))
    else:
        return render_template('newpost.html')

@app.route('/blog', methods=['GET'])
def blog():

    if request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('blog.html', blog=blog)
    else:
        return render_template('titlebody.html', blog=blog)

if __name__ == '__main__':
    app.run()
