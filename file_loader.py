
def load_settings(filename="settings_config.txt"):
    with open(filename, "r") as file:
        for line in file:
            if line.startswith("first_battery_threshold"):
                first_battery_threshold = line.split("=")[1].strip()
            elif line.startswith("second_battery_threshold"):
                second_battery_threshold = int(line.split("=")[1].strip())
            elif line.startswith("time_counter"):
                time_counter = int(line.split("=")[1].strip())
            elif line.startswith("time_threshold"):
                time_threshold = line.split("=")[1].strip()
            elif line.startswith("period"):
                period = line.split("=")[1].strip()

        return first_battery_threshold, second_battery_threshold, time_counter, time_threshold, period


def load_emial_sender_data(filename="email_config.txt"):
    recipients = []
    inside_block = False

    with open(filename, "r") as file:
        for line in file:
            if line.startswith("SMTP_Server"):
                SMTP_Server = line.split("=")[1].strip()
            elif line.startswith("SMTP_Port"):
                SMTP_Port = int(line.split("=")[1].strip())
            elif line.startswith("IMAP_Port"):
                IMAP_Port = int(line.split("=")[1].strip())
            elif line.startswith("SMTP_User"):
                SMTP_User = line.split("=")[1].strip()
            elif line.startswith("SMTP_Password"):
                SMTP_Password = line.split("=")[1].strip()
            elif line.startswith("Sender_Email"):
                Sender_Email = line.split("=")[1].strip()
            elif line.startswith("IMAP_SERVER"):
                IMAP_SERVER = line.split("=")[1].strip()

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

        return SMTP_Server, SMTP_Port, IMAP_Port, SMTP_User, SMTP_Password, Sender_Email, recipients, IMAP_SERVER

def load_recipients(filename="email_config.txt"):
    recipients = []
    inside_block = False

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if line == "Recipients:":
                inside_block = True
                continue
            if line == "END":
                break

            if inside_block:
                recipients.append(line)

    return recipients