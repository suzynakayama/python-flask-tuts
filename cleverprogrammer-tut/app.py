from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#! import requests

app = Flask(__name__)                                             ## the __name__ references this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'      ## 3 slashes (/) means it is relative to the app.py path
                                                                  ## and 4 slashes means it is an absolute path from the root directory
db = SQLAlchemy(app)

#! Models
class BlogPost(db.Model):
  id = db.Column(db.Integer, primary_key=True)                  ## this id will always be unique, that's why primary_key is true
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  author = db.Column(db.String(50), nullable=False, default='Anonymous')
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def __repr__(self):
    return 'Blog post ' + str(self.id)
#* After creating the Model, you need to create the DB: -on terminal-
#* python3                                ##run a python3 shell
#* from app import db
#* db.create_all()

# @app.route('/home/<string:name>')         ## we can have multiple routes and this is how you get the params, use <>, add type : var
# def hello(name):                          ## put the variable in the function
#  return 'Hello ' + name                   ## use the variable

@app.route('/')                                                   ## use decorator (@) with route to create the route
def index():
  return render_template('index.html')                            ## it renders the template found with the same name on the templates folder

@app.route('/posts', methods=['GET', 'POST'])
def posts():
  if request.method == 'POST':
    post_title = request.form['title']
    post_content = request.form['content']
    post_author = request.form['author']
    new_post = BlogPost(title=post_title, content=post_content, author=post_author)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')
  else:
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
  post = BlogPost.query.get_or_404(id)
  db.session.delete(post)
  db.session.commit()
  return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  post = BlogPost.query.get_or_404(id)
  if request.method == 'POST':
    post.title = request.form['title']
    post.content = request.form['content']
    post.author = request.form['author']
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('edit.html', post=post)

#! To get 3rd party API data install requests lib and use:
#! response = requests.get('https://jsonplaceholder.typicode.com/posts').json()
#! print(response)

if __name__ == '__main__':                                        ## if we are in developer mode
  app.run(debug=True)                                             ## turn debug mode on, so we can see the errors, not just a 404

