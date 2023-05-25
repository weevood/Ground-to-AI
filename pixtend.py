#!/usr/bin/env python3
# coding=utf-8

from __future__ import print_function

from datetime import *
from gpiozero import DigitalOutputDevice

# Import PiXtend V2 class
from pixtendv2l import PiXtendV2L
import time as t
import sys
import socket

# Import constants and functions
import influxdb_client
from utils.constants import *
from utils.send import *
from utils.log import *

# -----------------------------------------------------------------
# Print Art and Slogan
# -----------------------------------------------------------------
strSlogan1 = "PiXtend Python Library v2 (PPLv2)"
print("")
print("    ____     _    _  __   __                      __")
print("   / __ \\   (_)  | |/ /  / /_  ___    ____   ____/ /")
print("  / /_/ /  / /   |   /  / __/ / _ \\  / __ \\ / __  / ")
print(" / ____/  / /   /   |  / /_  /  __/ / / / // /_/ /  ")
print("/_/      /_/   /_/|_|  \\__/  \\___/ /_/ /_/ \\__,_/   ")
print("")
print(strSlogan1)
print("")

# -----------------------------------------------------------------
# Create instance - SPI communication starts automatically
# -----------------------------------------------------------------
# PiXtend V2 -L- with DAC, Analog Output active, default/factory setting
p = PiXtendV2L(com_interval=0.1)

# PiXtend V2 -L- with CAN-Bus active, physical jumper set from AO to CAN,
# the DAC device in the PPLv2 has to be disabled. Comment out the above line
# and comment in the line below to be able to use the CAN-Bus along side or
# from within Python. This requires PPLv2 Version 0.1.4 or later.
# p = PiXtendV2L(disable_dac=True)

# -----------------------------------------------------
# Main Program
# -----------------------------------------------------
name = 'pixtend'
deviceName = socket.gethostname()

if p is not None:
    print("Running Main Program - Hit Ctrl + C to exit")
    send('✅ PPLv2 script ({}) start running...'.format(deviceName))
    log(TSDB_BUCKETS['EV'], deviceName, influxdb_client.Point('boolean').tag('script', name).field('run', True))

    while True:
        try:

            # Check if SPI communication is running and the received data is correct
            if p.crc_header_in_error is False and p.crc_data_in_error is False:

                cycle_counter += 1
                now = datetime.now().time()

                if not is_config:
                    is_config = True
                    print("The value False = OFF and the value True = ON")
                    print("")

                # Clear the text on screen
                str_text = "                                               \n"
                for i in range(0, 43, 1):
                    str_text += "                                               \n"
                str_text += " "

                # Print text to console
                print(str_text, end="\r")
                # Reset cursor
                for i in range(0, 44, 1):
                    sys.stdout.write("\x1b[A")

                # Print the info text to console
                # str_text += " \n"
                str_text += "PiXtend V2 -L- Info:\n"
                str_text += "Firmware:    {0}\n".format(p.firmware)
                str_text += "Hardware:    {0}\n".format(p.hardware)
                str_text += "Model:       {0}\n".format(chr(p.model_in))
                str_text += " \n"
                str_text += "Local variables:\n"
                str_text += "Cycle No.:             {0}\n".format(cycle_counter)
                str_text += "Date (now):            {0}\n".format(date.today())
                str_text += "Time (now):            {0}\n".format(now)
                str_text += "GPIO0 (humidity):      {0}\n".format(p.humid0)
                str_text += "GPIO0 (temperature):   {0}\n".format(p.temp0)
                str_text += " \n"

                # Print text to console
                print(str_text, end="\r")

                # Reset cursor
                for i in range(0, 44, 1):
                    sys.stdout.write("\x1b[A")

                if cycle_counter > 10:
                    cycle_counter = 0
                    try:
                        log(TSDB_BUCKETS['SE'], deviceName, influxdb_client.Point('climate').tag('room', 'technical').field('temperature', p.temp0))
                        log(TSDB_BUCKETS['SE'], deviceName, influxdb_client.Point('climate').tag('room', 'technical').field('humidity', p.humid0))
                    except Exception as e:
                        print(e)

                # --- START OF MAIN ---

                # --- END OF MAIN ---

            else:
                send("Communication error, the data from the microcontroller is not correct!\nLeaving the application.\n\nPlease check that the Raspberry Pi can communicate with the microcontroller on the PiXtend V2 -L- board.")

                t.sleep(0.25)
                p.close()
                p = None

            # Wait some time, SPI communication will continue in the background
            t.sleep(0.25)

        # Catch errors and if an error is caught, leave the program
        except IOError as e:
            # Print out the caught error and leave program
            send("🚫 {} - I/O error({0}): {1}".format(deviceName, e.errno, e.strerror))
            p.close()
            t.sleep(0.25)
            del p
            p = None
            break

        except ValueError as ve:
            # Print out the caught error and leave program
            send("🚫 {} - Value error({0}): {1}".format(deviceName, ve.errno, ve.strerror))
            p.close()
            t.sleep(0.25)
            del p
            p = None
            break

        except RuntimeError as re:
            # Print out the caught error and leave program
            send("🚫 {} - Runtime error({0}): {1}".format(deviceName, re.errno, re.strerror))
            p.close()
            t.sleep(0.25)
            del p
            p = None
            break

        except KeyboardInterrupt:
            # Keyboard interrupt caught, Ctrl + C, now clean up and leave program
            for i in range(0, 45, 1):
                print("")
            print(strSlogan1 + " finished.")
            send('🚫 PiXtend PPLv2 leaving the application.')
        
            p.digital_out0 = p.OFF
            p.digital_out1 = p.OFF
            p.digital_out2 = p.OFF
            p.digital_out3 = p.OFF
            p.digital_out4 = p.OFF
            p.digital_out5 = p.OFF
            p.digital_out6 = p.OFF
            p.digital_out7 = p.OFF
            p.digital_out8 = p.OFF
            p.digital_out9 = p.OFF
            p.digital_out10 = p.OFF
            p.digital_out11 = p.OFF
            p.relay0 = p.OFF
            p.relay1 = p.OFF
            p.relay2 = p.OFF
            p.relay3 = p.OFF
            t.sleep(0.25)

            p.close()
            t.sleep(0.25)
            del p
            p = None
            
            send('🛑 Exiting pplv2 script.')
            log(TSDB_BUCKETS['EV'], deviceName, influxdb_client.Point('boolean').tag('script', name).field('run', False))
            sys.exit(0)  # Exit the application
