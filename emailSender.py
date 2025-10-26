from email.message import EmailMessage
import smtplib

# Parametry połączenia do serwera SMTP
SMTP_Server = "smtp.zoho.eu"
SMTP_Port = 587
SMTP_User = "testapcsender@zohomail.eu"
SMTP_Password = "Student.251482"

Sender_Email = "testapcsender@zohomail.eu"
Email_Recipient = "testapcupsd@gmail.com"



def sendMassage(subject, msg):
    email = EmailMessage()
    email['From'] = Sender_Email
    email['To'] = Email_Recipient
    email['Subject'] = subject
    email.set_content(msg)

    with smtplib.SMTP(SMTP_Server, SMTP_Port) as server:
        server.starttls()
        server.login(SMTP_User, SMTP_Password)
        server.send_message(email)
        server.quit()

    print("Email sent!")
    print(subject)
    print()
    print(msg)

