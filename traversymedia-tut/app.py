from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

## DB Config
ENV = 'dev'

if ENV == 'dev':
  app.debug = True
  #! CHANGE FOR YOUR USERNAME AND PASSWORD
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<USERNAME>:<PASSWORD>@localhost/flaskfeedback'
else:
  app.debug = False
  app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

## DB Model
class Feedback(db.Model):
  __tablename__ = 'feedback'
  id = db.Column(db.Integer, primary_key=True)
  customer = db.Column(db.String(250), unique=True)
  professional = db.Column(db.String(250))
  rating = db.Column(db.Integer)
  comments = db.Column(db.Text())

  def __init__(self, customer, professional, rating, comments):
    self.customer = customer
    self.professional = professional
    self.rating = rating
    self.comments = comments

## Routes
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
  if request.method == 'POST':
    customer = request.form['customer']
    professional = request.form['professional']
    rating = request.form['rating']
    comments = request.form['comments']
  # print(customer, professional, rating, comments)
  if customer == '' or professional == '':
    return render_template('index.html', message='Please enter required fields.')
  # if customer doesn't exist on our db
  if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
    data = Feedback(customer, professional, rating, comments)
    db.session.add(data)
    db.session.commit()
    send_mail(customer, professional, rating, comments)
    return render_template('success.html')
  return render_template('index.html', message='You have already submitted feedback. Thank you!')

## Run App
if (__name__ == '__main__'):
  app.run()