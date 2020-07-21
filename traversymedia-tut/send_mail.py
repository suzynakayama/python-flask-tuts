import smtplib
from email.mime.text import MIMEText

#! CHANGE USERNAME, PASSWORD, SENDER_EMAIL, and RECEIVER_EMAIL
def send_mail(customer, professional, rating, comments):
  port = 2525
  smtp_server = 'smtp.mailtrap.io'
  login = '<USERNAME>'
  password = '<PASSWORD>'
  message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Professional: {professional}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"
  
  sender_email = '<SENDER_EMAIL>'
  receiver_email = '<RECEIVER_EMAIL>'
  msg = MIMEText(message, 'html')
  msg['Subject'] = 'Feedback'
  msg['From'] = sender_email
  msg['To'] = receiver_email

  ## Send email
  with smtplib.SMTP(smtp_server, port) as server:
    server.login(login, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())