from email.message import EmailMessage
import smtplib

def load_emails(filename="email_config.txt"):
    recipients = []
    inside_block = False

    with open(filename, "r") as file:
        for line in file:
            if line.startswith("SMTP_Server"):
                SMTP_Server = line.split("=")[1].strip()
            elif line.startswith("SMTP_Port"):
                SMTP_Port = int(line.split("=")[1].strip())
            elif line.startswith("SMTP_User"):
                SMTP_User = line.split("=")[1].strip()
            elif line.startswith("SMTP_Password"):
                SMTP_Password = line.split("=")[1].strip()
            elif line.startswith("Sender_Email"):
                Sender_Email = line.split("=")[1].strip()

        file.seek(0)

        for line in file:
            line = line.strip()

            if line == "Recipients:":
                inside_block = True
                continue

            if line == "END":
                inside_block = False
                continue

            if inside_block:
                recipients.append(line)

        return SMTP_Server, SMTP_Port, SMTP_User, SMTP_Password, Sender_Email, recipients


def send_massage(subject, msg):
    SMTP_Server, SMTP_Port, SMTP_User, SMTP_Password, Sender_Email, recipients = load_emails()

    for recipient in recipients:
        email = EmailMessage()
        email['From'] = Sender_Email
        email['To'] = recipient
        email['Subject'] = subject
        email.set_content(msg)

        with smtplib.SMTP(SMTP_Server, SMTP_Port) as server:
            server.starttls()
            server.login(SMTP_User, SMTP_Password)
            server.send_message(email)
            server.quit()

        print("Email to "+recipient+" has been send")
        print(subject)
        print()
        print(msg)

SMTP_Server, SMTP_Port, SMTP_User, SMTP_Password, Sender_Email, recipients = load_emails()
print(SMTP_Server)
print()
print(SMTP_Port)
print()
print(SMTP_User)
print()
print(SMTP_Password)
print()
print(Sender_Email)
print()
print(recipients)