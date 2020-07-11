from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)                                                 ## initiates the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'           ## configure the db uri
db = SQLAlchemy(app)                                                  ## initiates the db

class Todo(db.Model):                                                 ## creates the model
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id                                    ## %r returns the self.id

@app.route('/', methods=['POST', 'GET'])                              ## because we added the methods array, we can now get and post, instead
def index():  ## of only get
  if request.method == 'POST':
    task_content = request.form['content']                          ## get the content of the form and put in task_content var
    new_task = Todo(content=task_content)                           ## create a new Todo instance with the content = to form content

    try:
      db.session.add(new_task)                                      ## add Todo instance to db
      db.session.commit()                                           ## commit that to the db
      return redirect('/')                                          ## redirect to home page with the new todo added
    except:
      return 'There was an issue adding your task.'

  else:
    tasks = Todo.query.order_by(Todo.date_created).all()            ## get all tasks from db and order by date created
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)

  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was a problem trying to delete that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  task = Todo.query.get_or_404(id)

  if request.method == 'POST':
    task.content = request.form['content']

    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue updating your task'

  else:
    return render_template('update.html', task=task)


if __name__ == "__main__":
  app.run(debug=True)