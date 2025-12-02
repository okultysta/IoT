import file_loader


def add_recipient(new_email, filename="email_config.txt"):
    lines = []
    recipients = file_loader.load_recipients(filename)

    # Jeżeli email już istnieje → nic nie rób
    if new_email in recipients:
        return False

    with open(filename, "r") as file:
        lines = file.readlines()

    with open(filename, "w") as file:
        inside_block = False
        for line in lines:
            stripped = line.strip()

            if stripped == "Recipients:":
                inside_block = True

            if stripped == "END" and inside_block:
                file.write(new_email + "\n")
                inside_block = False

            file.write(line)
    return True

def delete_recipient(email, filename="email_config.txt"):
    lines = []
    recipients = file_loader.load_recipients(filename)

    if email not in recipients:
        print("Email is not on the list")
        return False

    with open(filename, "r") as file:
        lines = file.readlines()

    with open(filename, "w") as file:
        for line in lines:
            stripped = line.strip()
            if stripped != email:
                file.write(line)

    return True

delete_recipient("pomidor@g.pl")