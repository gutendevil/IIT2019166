
flag = False
state = 0
def int_or_float(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

dict = {}
def sum(previous, key):
    temp = 0;
    temp1 = 0;
    temp2 = 0;
    for i in range(len(dict[key]), len(dict[key]) - 10, -1):
        if(len(i) == 3):
            temp += i[0];
            temp1 += i[1];
            temp2 += i[2];
        else:
            temp += i[0];

    return [temp, temp1, temp2]




def find_current_nature(name, val1, val2=0, val3=0):
    message = ""
    if(name == "RESP"):
        if(val1 != '0' and val1[0] != '['):
            if(int_or_float(val1) < 12):
                message += "respiratory rate is low.\n"
                state = -1
            elif(int_or_float(val1) > 27):
                message += "respiratory rate is critically high.\n"
                state = 1
                flag = True
            elif(int_or_float(val1) > 24):
                message += "respiratory rate is high.\n"
                state = 1
            else:
                state = 0
        else:
            state = 0
    elif(name == "CBP"):
        if(val1 != '0' and val2 != '0' and val3 != '0' and val1[0] != '['):
            if((int_or_float(val2) > 180) or (int_or_float(val3) > 120)):
                message += "Patient have Hypertensive Central Blood Pressure.\n"
                state = 1
                flag = True
            elif((int_or_float(val2) > 160) or (int_or_float(val3) > 90)):
                message += "Central Blood Pressure is high at stage2.\n"
                state = 1
            elif((int_or_float(val2) > 140) or (int_or_float(val3) > 80)):
                message += "Central Blood Pressure is high at stage1.\n"
                state = 1
            else:
                state = 0
        else:
            state = 0
    elif(name == "ABP"):
        if(val1 != '0' and val2 != '0' and val3 != '0' and val1[0] != '['):
            if ((int_or_float(val2) > 148) or (int_or_float(val3) > 94)):
                message += "Patient is in hypertensive arterial blood pressure.\n"
                state = 1
                flag = True
            elif ((int_or_float(val2) > 160) or (int_or_float(val3) > 88)):
                message += "Arterial Blood Pressure is high at stage2.\n"
                state = 1
            elif ((int_or_float(val2) > 140) or (int_or_float(val3) > 80)):
                message += "Arterial Blood Pressure is high at stage1.\n"
                state = 1
            else:
                state = 0
        else:
            state = 0
    elif(name == "NBP"):
        if (val1 != '0' and val2 != '0' and val3 != '0' and val1[0] != '['):
            if ((int_or_float(val2) > 160) or (int_or_float(val3) > 100)):
                message += "Patient have Stage-2 hypertensive non-invasive blood pressure.\n"
                state = 1
                flag = True
            elif ((int_or_float(val2) > 160) or (int_or_float(val3) > 88)):
                message += "Patient is in Stage-1 hypertensive non-invasive blood pressure.\n"
                state = 1
            elif ((int_or_float(val2) > 140) or (int_or_float(val3) > 80)):
                message += "Non-invasive blood pressure is higher than normal."
                state = 1
            elif (((int_or_float(val2) < 90) or (int_or_float(val3) < 60))):
                message += "Patient have Hypotensive non-invasive blood pressure."
                stage = -1
            else:
                state = 0
        else:
            state = 0
    elif (name == "SpO2"):
        if (val1 != '0' and val1[0] != '['):
            if (int_or_float(val1) < 85):
                message += "Patient is severly hypoxic"
                state = -1
                flag = True
            elif (int_or_float(val1) < 88):
                message += "Patient is hypoxic"
                state = -1
                flag = True
            elif (int_or_float(val1) < 93):
                message += "Oxygen level is below normal range."
                state = -1
            else:
                state = 0
        else:
            state = 0
    elif (name == "CO"):
        if(val1 != '0' and val1[0] != '['):
            if (int_or_float(val1) <= 2):
                message += "Cardiac output is critically low."
                state = -1
            else:
                state = 0
        else:
            state = 0
    elif (name == "PAP"):
        if(val1 != '0' and val3 != '0' and val2 != '0' and val1[0] != '['):
            if ((int_or_float(val1) > 25) or (int_or_float(val2) > 40) or (int_or_float(val3) > 18)):
                flag = True
                message += "Pulmonary artery Pressure is abnormally high.\n"
                state = 1
            else:
                state = 0
        else:
            state = 0
    elif (name == "LAP"):
        if(val1 != '0' and val1[0] != '['):
            if(int_or_float(val1) < 20):
                message += "LAP Score is extremely low.\n"
                state = -1
                flag = True
            elif (int_or_float(val1) < 40):
                message += "LAP Score is below normal.\n"
                state = -1
            elif (int_or_float(val1) > 120):
                message += "LAP Score is higher than normal range.\n"
                state = 1
            else:
                state = 0
        else:
            state = 0
    elif (name == "EtCO2"):
        if (val1 != '0' and val1[0] != '['):
            if(int_or_float(val1) > 50):
                message += "End tidal CO2 level is above critical range.\n"
                flag = True
                state = 1
            elif(int_or_float(val1) < 10):
                message += "End tidal CO2 level is below critical level.\n"
                flag = True
                state = -1
            elif (int_or_float(val1) > 45):
                message += "End tidal CO2 level is high in the patient.\n"
                state = 1
            elif (int_or_float(val1) < 35):
                message += "End tidal CO2 level is low in the patient.\n"
                state = -1
            else:
                state = 0
        else:
            state = 0
    elif (name == "AWRR"):
        if (val1 != '0' and val1[0] != '['):
            if(int_or_float(val1) < 9):
                message += "Airway Respiratory Rate is low in the patient.\n"
                flag = True
                state = -1
            elif (int_or_float(val1) > 30):
                message += "Airway Respiratory Rate is high in the patient.\n"
                flag = True
                state = 1
            else:
                state = 0
        else:
            state = 0
    elif (name == "PAWP"):
        if (val1 != '0' and val1[0] != '['):
            if(int_or_float(val1) < 4):
                message += "Pulmonary Artery wedge pressure is at critical level.\n"
                flag = True
                state = -1
            elif (int_or_float(val1) < 6):
                message += "Pulmonary Artery Wedge Pressure is below normal level.\n"
                state = -1
            elif (int_or_float(val1) > 18):
                message += "Pulmonary Artery wedge pressure is at critical level.\n"
                flag = True
                state = 1
            elif (int_or_float(val1) > 12):
                message += "Pulmonary Artery Wedge Pressure is aboe normal range.\n"
                state = 1
            else:
                state = 0
        else:
            state = 0
    elif (name == "IMCO2"):
        if (val1 != '0' and val1[0] != '['):
            if(int_or_float(val1) < 2):
                message += "Inspired minimum CO2 is below normal level.\n"
                state = -1
                flag = True



    if(flag == True):
        message += "Patient needs urgent care and medication."

def find_change_nature(name, previous, current, state, flag):
    message = ""
    status = 0
    if(current[0] != '0' and current[0] != '['):
        if(state == -1):
            if(sum(previous, name) > int_or_float(current[0])):
                status = -1
            elif(sum(previous, name) < int_or_float(current[0])):
                status = 1
        elif(state == 1):
            if (sum(previous, name) > int_or_float(current[0])):
                status = 1
            elif (sum(previous, name) < int_or_float(current[0])):
                status = -1

    return status