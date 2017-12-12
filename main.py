from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('index.html',title="build-a-blog",
        blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['title']
        #validate blog_title server side validation
        blog_body = request.form['body']
        #validate blog_body server side validation
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog?id={}'.format(new_blog.id))
    else:
        return render_template('newpost.html')

@app.route('/blog', methods=['GET'])
def blog():

    blog_id = int(request.args.get('id'))

    return render_template('blog.html', blog=blog_id)


if __name__ == '__main__':
    app.run()
