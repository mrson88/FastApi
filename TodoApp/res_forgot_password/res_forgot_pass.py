import smtplib
import os
from email.mime.text import MIMEText

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import HTTPException

pass_mail = os.environ.get("PASS_MAIL")
mail_name = os.environ.get("MAIL_NAME")


def send_otp_email(email, otp):
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
    try:
        server.sendmail(mail_name, [email], message.as_string())
        print('Email sent successfully')
    except smtplib.SMTPException as e:
        print(f'Error: {e}')
        return False
    server.quit()
    # return True

    # Close the server connection


def send_fastapi_otp_email(email, otp):
    conf = ConnectionConfig(
        MAIL_USERNAME=mail_name,
        MAIL_PASSWORD=pass_mail,
        MAIL_FROM=mail_name,
        MAIL_PORT=587,
        MAIL_SERVER="smtp.hostinger.com",
        # MAIL_TLS=True,
        # MAIL_SSL=False,
        # USE_CREDENTIALS=True,
    )
    mail = FastMail(conf)
    message = MessageSchema(
        subject="OTP",
        recipients=[email],
        body=f"Your OTP is {otp}",
    )
    response = mail.send_message(message)
    print(response)
    # if response.status != 250:
    #     raise HTTPException(status_code=500, detail="Email sending failed")
    return True
