import smtplib
import os
from email.mime.text import MIMEText
from random import randint


def send_otp_email(email, otp):
    pass_mail = os.environ.get("PASS_MAIL")
    mail_name = os.environ.get("MAIL_NAME")

    # Generate an OTP
    # otp = str(randint(100000, 999999))

    # Create a message object
    message = MIMEText(f"Your OTP is {otp}")
    message["Subject"] = "Your OTP"
    message["From"] = mail_name
    message["To"] = email

    # Set up a connection to the SMTP server
    server = smtplib.SMTP("smtp.hostinger.com", 587)
    server.ehlo()
    server.starttls()

    # Log in to the email server
    server.login(mail_name, pass_mail)

    # Send the message
    check_otp = server.sendmail(mail_name, [email], message.as_string())
    print(check_otp)
    # Close the server connection
    server.quit()
    if check_otp != {}:
        return
    return False