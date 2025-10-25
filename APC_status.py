import subprocess

"""
przydatne dane z apc:
STATUS : UPS status (online, charging, on battery etc)
BCHARGE : Current battery capacity charge percentage
TIMELEFT: Remaining runtime left on battery as estimated by the UPS
ENDAPC : Date and time of status information was written
"""

def get_ups_status():
    try:
        output = subprocess.check_output(['apcaccess', 'status'], text=True)
    except subprocess.CalledProcessError:
        return None, None

    status = None
    battery = None

    for line in output.splitlines():
        if line.startswith("STATUS"):
            status = line.split(":")[1].strip()
        elif line.startswith("BCHARGE"):
            battery = line.split(":")[1].strip().split()[0]

    return status, battery