import subprocess

def get_ups_status():

    try:
        output = subprocess.check_output(['apcaccess', 'status'], text=True)
    except subprocess.CalledProcessError:
        return None, None, None, None, None, None

    status = None
    battery = None
    time_left = None
    date = None
    time = None
    time_zone = None

    for line in output.splitlines():
        if line.startswith("STATUS"):
            status = line.split(":")[1].strip()
        elif line.startswith("BCHARGE"):
            battery = line.split(":")[1].strip().split()[0]
        elif line.startswith("TIMELEFT"):
            time_left = line.split(":")[1].strip()
        elif line.startswith("END APC"):
            date = line.split(":")[1].strip().split()[0]
            time = line.split(" ")[5].strip()
            time_zone = line.split(" ")[6].strip()

    return status, battery, time_left, date, time, time_zone