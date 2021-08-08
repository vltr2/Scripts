#!/usr/bin/env python3

# IBM System X 3650 M4 Fan Speed Control
# This script for setting fans using IPMI tool based on temps returned from IPMI Tool Query
# Can be called with a cron job or use watch to monitor with the following:
# ipmitool -H[IMM IP] -U[USER] -P[PASSWORD] sdr list | grep CPU | ~/scripts/ipmifans.py
# The first 4 channels returned are the 2 CPU temps and CPU VRMs.  
# Fan speed based on highest of these temps
# IPMI Command to control fans:
# Zone 1: raw 0x3a 0x07 0x01 0xXX 0x01
# Zone 2: raw 0x3a 0x07 0x02 0xXX 0x01
# Fan Speeds max @ FF
# 
# Before running this script put each zone into "acoustic mode" by setting speed to 0x00
# This ought to be needed only once.  It prevents the IMM from taking back control of fan 
# speed.  If fans ramp up after commanding slow, run it again.  This mode should be able
# to be disabled by running raw 0x3a 0x07 0x01[or2] 0x00 0x00

import sys
import os

ipmi_string = "ipmitool -H[IMM IP] -U[USER] -P[PASSWORD] raw 0x3a 0x07 "

index = 0
max_temp = 0
speed_out = "0x12"

try:
    for line in sys.stdin:
        out = line.split()
        # print("Line: " + repr(out))
        index += 1
        if int(out[4]) > max_temp:
            max_temp = int(out[4])

        # print("Max: " + repr(max_temp))
        if index >= 4:
            break

except:
    print("failure")

if max_temp < 30:
    speed_out = "0x10"
elif max_temp < 35:
    speed_out = "0x12"
elif max_temp < 40: 
    speed_out = "0x16"
elif max_temp < 45:
    speed_out = "0x1D"
elif max_temp < 50:
    speed_out = "0x24"
elif max_temp < 60:
    speed_out = "0x50"
elif max_temp < 70:
    speed_out = "0x8B"
elif max_temp < 80:
    speed_out = "0xB4"
elif max_temp < 90:
    speed_out = "0xDD"
else:
    speed_out = "0xFF"

os.system(ipmi_string + " 0x01 " + speed_out + " 0x01")
os.system(ipmi_string + " 0x02 " + speed_out + " 0x01")

print("Max Temp: " + repr(max_temp))
print("Set Fans to " + speed_out)

