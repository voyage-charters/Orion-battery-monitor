import sys
from flask import Flask
from flask_cors import cross_origin
from flask import jsonify
import platform

# import CanBus manager classes
from CANManager import ManageCan
from CANManager import BMSUnit

CM = ManageCan()
IS_WINDOWS = platform.system() == 'Windows'

def getBMS(BMSNumber):
    if BMSNumber == "0":
        BMS = CM.MM.BMS_Master_Combined
    elif BMSNumber == "1":
        BMS = CM.MM.BMS_Master
    elif BMSNumber == "2":
        BMS = CM.MM.BMS_Slave1
    elif BMSNumber == "3":
        BMS = CM.MM.BMS_Slave2
    else:
        BMS = CM.MM.BMS_Master_Combined
    return BMS

def ping():
	return  "pong"

app = Flask(__name__)

@app.route("/ping")
@cross_origin()
def pingPython():    
    return ping()

# Return CANBus connection status 
@app.route("/get_canBus_status")
def get_canBus_status():
    retobj = {
        "isConnected": CM.isConnected,
        "isWindows": IS_WINDOWS,
    }
    return jsonify(retobj)

# Start CANBus connection
@app.route("/start_canBus")
def start_canBus():
    print("Starting CANBus")
    CM.startCANDevice()
    retobj = {
        "isConnected": CM.isConnected,
        "isWindows": IS_WINDOWS,
    }
    return jsonify(retobj)

#start CANBus Read
@app.route("/start_canBus_read")
def start_canBus_read():
    print("Starting CANBus Read")
    CM.startCANBusRead()
    retobj = {
        "isRunning": CM.isRunning,
    }
    return jsonify(retobj)


@app.route('/get_tile_info/')
def get_current_user():
    BMSList = [CM.MM.BMS_Master_Combined ,CM.MM.BMS_Master, CM.MM.BMS_Slave1, CM.MM.BMS_Slave2]
    retobj = {}
    for BMS in BMSList:
        BMSName=BMS.BMSName
        retobj[BMSName] = {
            "BMSName":BMS.BMSName,
            "instantVoltage":"%0.1f" % (BMS.instantVoltage,),
            "packSOC":"%0.0f" % (BMS.packSOC,),
            "isFault" : BMS.isFault,
            "isOnline" : BMS.isOnline,
            "packCurrent" : "%0.1f" % (BMS.packCurrent,),
            "power" : "%0.0f" % (BMS.instantVoltage*BMS.packCurrent,),
            "relayState" : BMS.relayState,
            "BMSNumber" : BMS.get_unit_number(),
        }     
    # print(retobj)  
    return jsonify(retobj)

# get battery summary with BMSNumber as an input
@app.route('/get_battery_summary/<BMSNumber>')
def get_battery_summary(BMSNumber):
    print("BMSNumber",BMSNumber)
    BMS = getBMS(BMSNumber)
    
    retobj = {
        "BMSName":BMS.BMSName,
        "instantVoltage": "%0.1f" % (BMS.instantVoltage,),
        "packSOC": "%0.0f" % (BMS.packSOC,),
        "isFault" : BMS.isFault,
        "isOnline" : BMS.isOnline,
        "packCurrent" : "%0.1f" % (BMS.packCurrent,),
        "power" : "%0.0f" % (BMS.instantVoltage*BMS.packCurrent,),
        "relayState" : BMS.relayState,
        "BMSNumber" : BMS.get_unit_number(),
        "highCellVoltage" : "%0.2f" % (BMS.highCellVoltage,),
        "lowCellVoltage" : "%0.2f" % (BMS.lowCellVoltage,),
        "activeAlarms" : BMS.get_active_alarms(),


    }
    # print(retobj)
    return jsonify(retobj)

# get active alarms with BMSNumber as an input
@app.route('/get_active_alarms/<BMSNumber>')
def get_active_alarms(BMSNumber):
    BMS = getBMS(BMSNumber)
    retobj = {
        "activeAlarms" : BMS.get_active_alarms(),
    }
    return jsonify(retobj)
          
# get details with BMSNumber as an input
@app.route('/get_details/<BMSNumber>')
def get_details(BMSNumber):
    BMS = getBMS(BMSNumber)
    retobj = {
        "BMSName":BMS.BMSName,
        "highCellVoltage" : "%0.2f" % (BMS.highCellVoltage,),
        "lowCellVoltage" : "%0.2f" % (BMS.lowCellVoltage,),
        "highCellId" : BMS.highCellId,
        "lowCellId" : BMS.lowCellId,
        "highTemp" : "%0.2f" % (BMS.highTemp,),
        "lowTemp" : "%0.2f" % (BMS.lowTemp,),
        "heatSinkTemp" : "%0.2f" % (BMS.heatSinkTemp,),
        "packDCL" : "%0.2f" % (BMS.packDCL,),
        "packCCL" : "%0.2f" % (BMS.packCCL,),


    }
    return jsonify(retobj)


# get IO with BMSNumber as an input
@app.route('/get_io/<BMSNumber>')
def get_io(BMSNumber):
    BMS = getBMS(BMSNumber)
    retobj = {
        "isFault" : BMS.isFault,
        "isOnline" : BMS.isOnline,
        "relayState" : BMS.relayState,
        "isCharging" : BMS.chargeSafety,
        "isBalancing" : BMS.isBalancing,
        "allowDischarge" : BMS.allowDischarge,
        "allowCharge" : BMS.allowCharge,
    }
    return jsonify(retobj)

# get cell information with BMSNumber as an input
@app.route('/get_cell_info/<BMSNumber>')
def get_cell_info(BMSNumber):
    BMS = getBMS(BMSNumber)
    retobj = {
        "cell_info": BMS.cell_info,
    }
    # print(retobj)
    return jsonify(retobj)

#get alarms history with BMSNumber as an input
@app.route('/get_alarm_history/<BMSNumber>')
def get_alarm_history(BMSNumber):
    BMS = getBMS(BMSNumber)
    retobj = {
        "alarmHistory": BMS.get_alarm_history(),
    }
    return jsonify(retobj)

#Reset all BMSs
@app.route('/reset_bms')
def send_reset_bms():
    # log reset
    print("Resetting BMSs")
    CM.BMSResetAll()
    retobj = {
        "resetBMS": "OK",
    }
    return jsonify(retobj)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)