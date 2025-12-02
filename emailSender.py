
from email.message import EmailMessage
import smtplib

import time as tm ############################### do usunięcia

from imap_tools import MailBox, AND

import data_writer
import file_loader


def send_massage(recip ,subject, msg):
    SMTP_Server, SMTP_Port, IMAP_Port, SMTP_User, SMTP_Password, Sender_Email, recipients, IMAP_SERVER = file_loader.load_emial_sender_data()

    if recip is not None:
        recipients = [recip]

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


def check_emails():
    SMTP_Server, SMTP_Port, IMAP_Port, SMTP_User, SMTP_Password, Sender_Email, recipients, IMAP_SERVER = file_loader.load_emial_sender_data()

    with (MailBox(IMAP_SERVER).login(SMTP_User, SMTP_Password) as mailbox):
        for msg in mailbox.fetch(AND(seen=False)):
            print("From:", msg.from_) ############################### do usunięcia
            print("Topic:", msg.subject) ############################### do usunięcia
            print("Body:", msg.text or msg.html) ############################### do usunięcia
            if(msg.from_ in recipients):
                print("znam ten email") ############################### do usunięcia

                if(msg.subject == "GET"):
                    if(msg.text.startswith("Get Emails") or msg.html.startswith("Get Emails")):
                        print("wysyłam listę maili") ############################### do usunięcia
                        body = "\n".join(recipients)
                        send_massage(msg.from_, "Emails List", body)
                    elif(msg.text.startswith("Get Email Settings") or msg.html.startswith("Get Email Settings")):
                        print("wysyłam listę ustawień") ############################### do usunięcia
                        body = "Email Settings:\n"
                        body += "SMTP settings\n"
                        body += "SMTP_Server = " + str(SMTP_Server) + "\n"
                        body += "SMTP_Port = " + str(SMTP_Port) + "\n"
                        body += "SMTP_User = " + str(SMTP_User) + "\n"
                        body += "SMTP_Password = " + str(SMTP_Password) + "\n\n"

                        body += "IMAP settings\n"
                        body += "IMAP_SERVER = " + str(IMAP_SERVER) + "\n"
                        body += "IMAP_Port = " + str(IMAP_Port) + "\n\n"

                        body += "Sender_Email = " + str(Sender_Email) + "\n"

                        send_massage(msg.from_, "Email Settings", body)

                    elif (msg.text.startswith("Get Program Settings") or msg.html.startswith("Get Program Settings")):
                        first_battery_threshold, second_battery_threshold, time_counter, time_threshold, period = file_loader.emailSender.load_settings()
                        body = "Program Settings:\n"
                        body += "first_battery_threshold = " + str(first_battery_threshold)  + "\n"
                        body += "second_battery_threshold = " + str(second_battery_threshold) + "\n"
                        body += "time_counter = " + str(time_counter) + "\n"
                        body += "time_threshold = " + str(time_threshold) + "\n"
                        body += "period = " + str(period) + "\n"

                        send_massage(msg.from_, "Program Settings", body)

                    elif(msg.text.startswith("Get All") or msg.html.startswith("Get All")):
                        print("wysyłam wszystko") ############################### do usunięcia
                        body = "Settings:\n"
                        body += "SMTP settings\n"
                        body += "SMTP_Server = " + str(SMTP_Server) + "\n"
                        body += "SMTP_Port = " + str(SMTP_Port) + "\n"
                        body += "SMTP_User = " + str(SMTP_User) + "\n"
                        body += "SMTP_Password = " + str(SMTP_Password) + "\n\n"

                        body += "IMAP settings\n"
                        body += "IMAP_SERVER = " + str(IMAP_SERVER) + "\n"
                        body += "IMAP_Port = " + str(IMAP_Port) + "\n\n"

                        body += "Sender_Email = " + str(Sender_Email) + "\n\n"

                        body += "Recipients List\n"
                        body += "\n".join(recipients)

                        body += "Program Settings\n"
                        body += "first_battery_threshold = " + str(first_battery_threshold) + "\n"
                        body += "second_battery_threshold = " + str(second_battery_threshold) + "\n"
                        body += "time_counter = " + str(time_counter) + "\n"
                        body += "time_threshold = " + str(time_threshold) + "\n"
                        body += "period = " + str(period) + "\n"

                        send_massage(msg.from_, "All Info about settings", body)

                    else:
                        print("Nie znana komenda") ############################### do usunięcia
                        body = "Recived command:\n"
                        body += msg.text or msg.html
                        body += "\n is not recognized. Please try again."
                        send_massage(msg.from_, "Unknown command", body)
                        print("wysłałem") ############################### do usunięcia

                elif(msg.subject == "POST"):
                    if msg.text.startswith("Add Email = ") or msg.html.startswith("Add Email = "):
                        new_email = msg.text.split("=")[1].split(" ")[0].strip()
                        if data_writer.add_recipient(new_email):
                            body = "Email:\n" + str(new_email) + "\nwas successfully added."
                            send_massage(msg.from_, "Action was successful", body)
                        else:
                            body = "Unable to add email:\n" + str(new_email) + "\nEmail is already on the list."
                            send_massage(msg.from_, "Action Failed", body)

                    elif msg.text.startswith("Delete Email = ") or msg.html.startswith("Delete Email = "):
                        email = msg.text.split("=")[1].split(" ")[0].strip()
                        if data_writer.delete_recipient(email):
                            body = "Email:\n" + str(new_email) + "\nwas successfully deleted from the list."
                            send_massage(msg.from_, "Action was successful", body)
                        else:
                            body = "Unable to delete email:\n" + str(new_email) + "\nEmail is not on the list."
                            send_massage(msg.from_, "Action Failed", body)


                    else:
                        print("Nie znana komenda")  ############################### do usunięcia
                        body = "Recived command:\n"
                        body += msg.text or msg.html
                        body += "\n is not recognized. Please try again."
                        send_massage(msg.from_, "Unknown command", body)
                        print("wysłałem")  ############################### do usunięcia

                else:
                    body = "Method:\n" + str(msg.subject) + "\nin not recognized. Pleas Try again."
                    send_massage(msg.from_, "Unrecognized Method", body)






            else:
                print("nie znam tego emailu")
                body = "This email was not recognized. Please contact the administrator."
                send_massage(msg.from_, "Unknown email", body)


while True:
    check_emails()
    tm.sleep(5)

