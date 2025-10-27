import APC_status
import emailSender
import time as tm

msg = ""
subject = ""

comm_lost_send = False
on_battery_mode_send = False
battery_below_50_send = False
battery_below_20_send = False
online_send = False
exception_send = False

time_counter = 0
time_threshold = 3600


while True:

    status, battery, time_left, date, time, time_zone = APC_status.get_ups_status()
    if (status is None) & (exception_send == False):
        subcejt = "UPS: Exception warning"
        msg = """WARNING: Caught exception in subprocess. Unable to read UPS status."""
        emailSender.send_massage(subcejt, msg)
        exception_send = True
        time_counter = 0
    else:
        if (status == "COMMLOST") & (comm_lost_send==False):
            subcejt = "UPS: Lost communication"
            msg = """WARNING: Communication with APC was lost.
            """+"\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
            comm_lost_send = True
            on_battery_mode_send = False
            battery_below_50_send = False
            battery_below_20_send = False
            online_send = False
            exception_send = False
            time_counter = 0
            emailSender.send_massage(subcejt, msg)

        elif status == "ONBATT":
            if  on_battery_mode_send == False:

                if comm_lost_send:
                    msg = "Info: Communication has been restored."

                subcejt = "UPS: Lost power source"
                msg += """\r\nWARNING: The power source is off. APC has switched to battery mode.
                """ + "\r\nCurrent battery charge level is " + str(battery)+"""%.
                """ + "\r\nEstimated by APC time till battery runs out: " + str(time_left) +"""
                """+"\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
                on_battery_mode_send = True
                comm_lost_send = False
                online_send = False
                exception_send = False
                time_counter = 0
                emailSender.send_massage(subcejt, msg)
            elif (float(battery)<50) & (float(battery)>=20) & (battery_below_50_send==False):
                subcejt = "UPS: Battery half empty"
                msg = """ALERT: The battery charge level has dropped below 50%.
                """ + "\r\nCurrent battery charge level is " + str(battery) + """%.
                """ + "\r\nEstimated by APC time till battery runs out: " + str(time_left) + """
                """ + "\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
                battery_below_50_send = True
                time_counter = 0
                emailSender.send_massage(subcejt, msg)
            elif (float(battery)<20) & (battery_below_20_send==False):
                subcejt = "UPS: BATTERY CRITICALLY LOW"
                msg = """EMERGENCY: The battery charge level has dropped below 20%. Take the necessary actions to prevent system failure.
                """ + "\r\nCurrent battery charge level is " + str(battery) + """%.
                """ + "\r\nEstimated by APC time till battery runs out: " + str(time_left) + """
                """ + "\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
                battery_below_20_send = True
                time_counter = 0
                emailSender.send_massage(subcejt, msg)

        elif (status == "ONLINE") & (online_send==False):
            subcejt = "UPS: Power source active"
            msg = "Info: "
            if comm_lost_send:
                msg += "Communication has been restored. "

            if on_battery_mode_send:
                msg += "Power source has been restored and provides energy."
                on_battery_mode_send = False
            else:
                msg += "Power source is active and provides energy."

            msg += "\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
            comm_lost_send = False
            on_battery_mode_send = False
            battery_below_50_send = False
            battery_below_20_send = False
            exception_send = False
            emailSender.send_massage(subcejt, msg)
            online_send = True
            time_counter = 0

    if time_counter >= time_threshold:
        comm_lost_send = False
        on_battery_mode_send = False
        battery_below_50_send = False
        battery_below_20_send = False
        online_send = False
        exception_send = False
        time_counter = 0

    time_counter += 5
    tm.sleep(5)