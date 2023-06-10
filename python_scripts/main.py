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


def ping():
	return  "pong"

app = Flask(__name__)

@app.route("/ping")
@cross_origin()
def pingPython():    
    return ping()

@app.route('/get_tile_info/')
def get_current_user():
    BMSList = [CM.MM.BMS_Master_Combined ,CM.MM.BMS_Master, CM.MM.BMS_Slave1, CM.MM.BMS_Slave2]
    retobj = {}
    for selBMS in BMSList:
        BMSName=selBMS.BMSName
        retobj[BMSName] = {
            "BMSName":selBMS.BMSName,
            "instantVoltage":selBMS.instantVoltage,
            "packSOC":selBMS.packSOC,
            "isFault" : selBMS.isFault,
            "isOnline" : selBMS.isOnline,
            "packCurrent" : selBMS.packCurrent,
            "power" : selBMS.instantVoltage*selBMS.packCurrent,
            "relayState" : selBMS.relayState,
            "BMSNumber" : selBMS.get_unit_number(),
        }     
    print(retobj)  
    return jsonify(retobj)

# get battery summary with BMSNumber as an input
@app.route('/get_battery_summary/<BMSNumber>')
def get_battery_summary(BMSNumber):
    print("BMSNumber",BMSNumber)
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
    
    retobj = {
        "BMSName":BMS.BMSName,
        "instantVoltage":BMS.instantVoltage,
        "packSOC":BMS.packSOC,
        "isFault" : BMS.isFault,
        "isOnline" : BMS.isOnline,
        "packCurrent" : BMS.packCurrent,
        "power" : BMS.instantVoltage*BMS.packCurrent,
        "relayState" : BMS.relayState,
        "BMSNumber" : BMS.get_unit_number(),
    }
    # print(retobj)
    return jsonify(retobj)


          
     


   

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)