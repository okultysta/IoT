import APC_status
import emailSender
import test_outputs
import time as tm

msg = ""
subject = ""

comm_lost_send = False
on_battery_mode_send = False
battery_below_50_send = False
battery_below_20_send = False
online_send = False
number = 0

for i in range(60):
    if number < 5:
        output = test_outputs.output_ONBATT_46
        number+=1
    elif number < 10:
        output = test_outputs.output_ONLINE
        number += 1
    elif number < 15:
        output = test_outputs.output_COMMLOST
        number += 1
    elif number < 20:
        output = test_outputs.output_ONLINE
        number += 1
    elif number < 25:
        output = test_outputs.output_COMMLOST
        number += 1
    elif number < 30:
        output = test_outputs.output_ONBATT_87
        number += 1
    elif number < 35:
        output = test_outputs.output_COMMLOST
        number += 1
    elif number < 40:
        output = test_outputs.output_ONBATT_46
        number += 1
    elif number < 45:
        output = test_outputs.output_COMMLOST
        number += 1
    elif number < 50:
        output = test_outputs.output_ONBATT_17
        number += 1
    else:
        output = test_outputs.output_ONLINE
        number += 1

    status, battery, time_left, date, time, time_zone = APC_status.get_ups_status(output)

    if (status == "COMMLOST") & (comm_lost_send==False):
        subcejt = "APC: Lost communication"+str(number)
        msg = """WARNING: Communication with APC was lost.
        """+"\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
        comm_lost_send = True
        on_battery_mode_send = False
        battery_below_50_send = False
        battery_below_20_send = False
        online_send = False
        emailSender.sendMassage(subcejt, msg)

    elif status == "ONBATT":
        if  on_battery_mode_send == False:

            if comm_lost_send:
                msg = "Info: Communication has been restored."

            subcejt = "APC: Lost power source"+str(number)
            msg += """\r\nWARNING: The power source is off. APC has switched to battery mode.
            """ + "\r\nCurrent battery charge level is " + str(battery)+"""%.
            """ + "\r\nEstimated by APC time till battery runs out: " + str(time_left) +"""
            """+"\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
            on_battery_mode_send = True
            comm_lost_send = False
            online_send = False
            emailSender.sendMassage(subcejt, msg)
        elif (float(battery)<50) & (float(battery)>=20) & (battery_below_50_send==False):
            subcejt = "APC: Battery half empty"+str(number)
            msg = """ALERT: The battery charge level has dropped below 50%.
            """ + "\r\nCurrent battery charge level is " + str(battery) + """%.
            """ + "\r\nEstimated by APC time till battery runs out: " + str(time_left) + """
            """ + "\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
            battery_below_50_send = True
            emailSender.sendMassage(subcejt, msg)
        elif (float(battery)<20) & (battery_below_20_send==False):
            subcejt = "APC: BATTERY CRITICALLY LOW"+str(number)
            msg = """EMERGENCY: The battery charge level has dropped below 20%. Take the necessary actions to prevent system failure.
            """ + "\r\nCurrent battery charge level is " + str(battery) + """%.
            """ + "\r\nEstimated by APC time till battery runs out: " + str(time_left) + """
            """ + "\r\n\nInformation from \r\n"+"Date: "+str(date)+"\r\ntime: "+str(time)+"\r\ntime zone: "+str(time_zone)
            battery_below_20_send = True
            emailSender.sendMassage(subcejt, msg)

    elif (status == "ONLINE") & (online_send==False):
        subcejt = "APC: Power source active" + str(number)
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
        emailSender.sendMassage(subcejt, msg)
        online_send = True
