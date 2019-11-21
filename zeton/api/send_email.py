# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def is_pass_rec_email(mail,sha):
    message = Mail(
        from_email='zeton@zeton.com', #fix me in this place should be registred sender mail
        to_emails=mail,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=f'<strong>Poniżej znajdziesz link do resetu hasła:</strong><br>http://127.0.0.1:5000/pass_rec/{sha}') #fix me destination domain
    try:
        sg = SendGridAPIClient('SG. ...')  #fix me in this place should be registred api key

        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
        return False

    return True
