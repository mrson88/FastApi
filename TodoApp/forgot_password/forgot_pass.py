import smtplib
import os
from email.mime.text import MIMEText
from random import randint

pass_mail = os.environ.get("PASS_MAIL")
mail_name = os.environ.get("MAIL_NAME")


def send_otp_email(email):
    print(mail_name)
    print(pass_mail)
    # Generate an OTP
    otp = str(randint(100000, 999999))

    # Create a message object
    message = MIMEText(f"Your OTP is {otp}")
    message["Subject"] = "Your OTP"
    message["From"] = mail_name
    message["To"] = email

    # Set up a connection to the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    # Log in to the email server
    server.login(mail_name, pass_mail)

    # Send the message
    server.sendmail(email, [email], message.as_string())

    # Close the server connection
    server.quit()

    return otp
