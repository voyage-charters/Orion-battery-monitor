
from enum import Enum
from datetime import datetime
import time
import csv
import os.path
import platform

IS_WINDOWS = platform.system() == 'Windows'


class BitOrder(Enum):
    LSB = 0
    MSB = 1

class BMSOrder(Enum):
    Combined = 0
    Master = 1
    Slave1 = 2
    Slave2 = 3
    Slave3 = 4

class ByteOrder(Enum):
    LittleEndian = "little"
    BigEndian = "big"




        

class BMSUnit():
    
    
    #threshold for BMS offline trigger.(seconds)
    offlineTimeDelta = 10

    def __init__(self,unitType : int ):
        self.cell_info = []
        self.BMSErrorLogPath = ""
        self.BMSName = ""
        self.erorLogHeader = ["DateTime","Log Description","Action"]
        self.prevOnlineStatus = True
        self.instantVoltage  = 0
        self.packCurrent     = 0
        self.packSOC         = 0
        self.packDCL         = 0
        self.packCCL         = 0
        self.targetMaxVoltage = 0
        self.targetMinVoltage = 0
        self.relayState      = False
        self.isFault         = False
        self.chargeSafety    = False
        self.allowCharge     = False
        self.allowDischarge  = False
        self.faultList       = []
        self.highCellVoltage : int = 0
        self.highCellId      = 0
        self.lowCellVoltage  = 0
        self.lowCellId       = 0
        self.isBalancing     = False
        self.highTemp        = 0
        self.lowTemp         = 0
        self.heatSinkTemp    = 0
        self.lastOnline      = None,
        self.isOnline         = False
        self.activeFaults    =[]
        self.activeHistoricAlarms = []

    
        for i in range(1,45,1):
                   self.cell_info.append({'Broadcast_Cell_ID':i,'Broadcast_Cell_Intant_Voltage': 0.0, 'Broadcast_Cell_Resistance': 0.0,'Broadcast_Cell_Open_Voltage' : 0.0})
    

        self.lastOnline = time.time()
        self.unitType           = unitType          ,
        pre_path = os.path.dirname(os.path.realpath(__file__))
        
        #set BMS Name 
        if IS_WINDOWS:
            if self.unitType[0] == BMSOrder.Combined :
                self.BMSErrorLogPath = pre_path+"\error_logs\Orion_Combined_Error_Log.csv"
                self.BMSName = "Master Combined"         
            elif self.unitType[0] == BMSOrder.Master :            
                self.BMSErrorLogPath = pre_path+"\error_logs\Orion_Master_Error_Log.csv"
                self.BMSName = "Master BMS"
            elif self.unitType[0] == BMSOrder.Slave1 :        
                self.BMSErrorLogPath = pre_path+"\error_logs\Orion_Slave1_Error_Log.csv"
                self.BMSName = "Slave1 BMS"
            elif self.unitType[0] == BMSOrder.Slave2 :
                self.BMSErrorLogPath = pre_path+"\error_logs\Orion_Slave2_Error_Log.csv"
                self.BMSName = "Slave2 BMS"
            elif self.unitType[0] == BMSOrder.Slave3 :          
                self.BMSErrorLogPath = pre_path+"\error_logs\Orion_Slave3_Error_Log.csv"
                self.BMSName = "Slave3 BMS"
        else:
            if self.unitType[0] == BMSOrder.Combined :
                self.BMSErrorLogPath = pre_path+"/error_logs/Orion_Combined_Error_Log.csv"
                self.BMSName = "Master Combined"         
            elif self.unitType[0] == BMSOrder.Master :            
                self.BMSErrorLogPath = pre_path+"/error_logs/Orion_Master_Error_Log.csv"
                self.BMSName = "Master BMS"
            elif self.unitType[0] == BMSOrder.Slave1 :        
                self.BMSErrorLogPath = pre_path+"/error_logs/Orion_Slave1_Error_Log.csv"
                self.BMSName = "Slave1 BMS"
            elif self.unitType[0] == BMSOrder.Slave2 :
                self.BMSErrorLogPath = pre_path+"/error_logs/Orion_Slave2_Error_Log.csv"
                self.BMSName = "Slave2 BMS"
            elif self.unitType[0] == BMSOrder.Slave3 :          
                self.BMSErrorLogPath = pre_path+"/error_logs/Orion_Slave3_Error_Log.csv"
                self.BMSName = "Slave3 BMS"   
        #print(self.BMSErrorLogPath) 
        #check if error log exists, create one if not
    
        if not os.path.exists(self.BMSErrorLogPath):
            print("log does not exist.")
            print("Creating log file at {}".format(self.BMSErrorLogPath))
            with open(self.BMSErrorLogPath,'w',newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.erorLogHeader)

        for i in range(1,45,1):
            self.cell_info.append({'Broadcast_Cell_ID':i,'Broadcast_Cell_Intant_Voltage': 0.0, 'Broadcast_Cell_Resistance': 0.0,'Broadcast_Cell_Open_Voltage' : 0.0}),
        self.faultList = {
        "DTC P0A1F : Internal Cell Communication"   :   False,  
        "DTC P0A12 : Cell Balancing Stuck Off"      :   False,      
        "DTC P0A80 : Weak Cell"                     :   False,                    
        "DTC P0AFA : Low Cell Voltage"              :   False,             
        "DTC P0A04 : Cell Open Wiring"              :   False,             
        "DTC P0AC0 : Current Sensor"                :   False,               
        "DTC P0A0D : Cell Voltage Over 5V"          :   False,         
        "DTC P0A0F : Cell Bank"                     :   False,                    
        "DTC P0A02 : Weak Pack"                     :   False,                    
        "DTC P0A81 : Fan Monitor"                   :   False,                        
        "DTC P0A9C : Thermistor"                    :   False,                   
        "DTC U0100 : CAN Communication"             :   False,            
        "DTC P0560 : Redundant Power Supply"        :   False,       
        "DTC P0AA6 : High Voltage Isolation"        :   False,       
        "DTC P0A05 : Invalid Input Supply Voltage"  :   False, 
        "DTC P0A06 : ChargeEnable Relay"            :   False,           
        "DTC P0A07 : DischargeEnable Relay"         :   False,        
        "DTC P0A08 : Charger Safety Relay"          :   False,         
        "DTC P0A09 : Internal Hardware"             :   False,            
        "DTC P0A0A : Internal Heatsink Thermistor"  :   False, 
        "DTC P0A0B : Internal Logic"                :   False,               
        "DTC P0A0C : Highest Cell Voltage Too High" :   False,
        "DTC P0A0E : Lowest Cell Voltage Too Low"   :   False,  
        "DTC P0A10 : Pack Too Hot"                  :   False,                 
    }
    
    def get_active_historic_alarms (self):
        
        with open(self.BMSErrorLogPath) as file:
            csv_reader = csv.reader(file,delimiter=',',)
            line_count = 0
            #print("Printing list for {} with csv path :  {}".format(self.BMSName, self.BMSErrorLogPath))
            for row in csv_reader:
                    #check for valid number of columns in row
                    if len(row) > 2:
                        if line_count == 0:
                            #skip the header row
                            #print (f'Column names are {", ".join(row)}')
                            line_count += 1
                        else:
                            

                            listItem = [row[0],row[1] ,row[2]]
                            
                                #print(listItem)
                            line_count += 1

    def checkOnline(self): #Compare last message time to current time

            #get time difference in seconds
            if self.lastOnline == 0:
                return
            else:

   
                timeDelta = (datetime.fromtimestamp(time.time()) - datetime.fromtimestamp(self.lastOnline)).total_seconds()
                
                #
                if timeDelta > self.offlineTimeDelta:
                    #log comms failure. '''' REMOVED ''''
                    # if self.prevOnlineStatus:
                    #     with open(self.BMSErrorLogPath,'a') as file: #Write to CSV file
                    #         writer = csv.writer(file)
                    #         errorDesc = self.BMSName+" Communication failure"
                    #         errorData = [datetime.fromtimestamp(self.lastOnline),errorDesc,"Raised"]
                    #         writer.writerow(errorData)  
                    self.isOnline = False
                    self.prevOnlineStatus = False
                    #self.packCurrent =0
                    #self.packSOC = 0
                    #print("Previous online status set to {}".format(self.prevOnlineStatus))
                else:
                    #log comms failure. '''' REMOVED ''''
                    # if not self.prevOnlineStatus:
                        # with open(self.BMSErrorLogPath,'a', newline='') as file: #Write to CSV file
                        #     writer = csv.writer(file)
                        #     errorDesc = self.BMSName+" Communication failure"
                        #     errorData = [datetime.fromtimestamp(self.lastOnline),errorDesc,"Cleared"]
                        #     writer.writerow(errorData)
                    self.isOnline = True
                    self.prevOnlineStatus = True

            

             
            
    def set_val(self,name,value,timeStamp):
        #Grab and store BMS Unit values
 
        
        self.lastOnline = timeStamp
        # self.checkOnline()
        if name == 'Pack_Current':
            if (value == -600) and (self.isFault):
                self.packCurrent = 0
            else:
                self.packCurrent = value
            #print("PACK Current = {}".format(value))  
        elif name == 'Inst_Voltage'   :                      
            self.instantVoltage    = value  
        elif name == 'Pack_SOC'   :                          
            self.packSOC        = value            
        # elif name == 'Relay_State'    :   
        #     self.relayState        = value                    
        elif name == 'Pack_DCL'   :
            self.packDCL        = value                         
        elif name == 'Pack_CCL'   : 
            self.packCCL        = value                    
        elif name == 'High_Temperature'   :                  
            self.highTemp       = value
        elif name == 'Low_Temperature'    :                                   
            self.lowTemp        = value
        elif name == 'Balancing_Active'  :                         
            self.isBalancing    = value
        elif name == 'MultiPurpose_Enable'   :            
            self.relayState     = value
        elif name == 'Charge Enable Inverted'    :                   
            self.allowCharge    = value
        elif name == 'Discharge Enable Inverted'    :                   
            self.allowDischarge    = value
        elif name == 'Low_Cell_Voltage':
            self.lowCellVoltage = value
        elif name == 'Low_Cell_ID':
            self.lowCellId = value
        elif name == 'High_Cell_Voltage':
            self.highCellVoltage = value
        elif name == 'High_Cell_ID':
            self.highCellId = value
        elif name == 'Low_Temperature':
            self.lowTemp = value -273
        elif name == 'High_Temperature':
            self.highTemp = value -273
        
           
        #BMS fault handling
        
        #get fault list keys
        faultKeys = list(self.faultList.keys())

            

        if name in faultKeys:#Check if msg name is a fault code
            #if self.BMSName == "Master BMS":
                #print(self.activeFaults)
                #print("setting {} to {}".format(name,value))
            # prevVal = self.faultList[name]
            # if prevVal:
            #     #if pervious value = True and current = False, delete from list
            #     if not value:
            #         if name in self.activeFaults:
            #             self.activeFaults.remove(name)
            # else:
            #     #if pervious value = False and current = True, append to list
            #     if value:
            #         self.activeFaults.append(name)
            # #print(self.activeFaults)
            # self.faultList[name] = value #set fault status of  specific code
            # #print("active faults {}".format(self.activeFaults))
  


                
            if value:  
        
                if name not in self.activeFaults: #Only add fault to list if not already there
                
                    self.activeFaults.append(name)
                    print("writing {} to file".format(name))
                    with open(self.BMSErrorLogPath,'a', newline='') as file: #Write to CSV file
                        print('Appending fault to {}'.format(self.BMSErrorLogPath))
                        writer = csv.writer(file)
                        errorData = [datetime.fromtimestamp(timeStamp),name,"Raised"]
                        writer.writerow(errorData)
                        
            else:
                if self.isOnline:#Only clear faults if BMS is Online

                    if (name in self.activeFaults): #Clear Fault from active fault list

                        self.activeFaults.remove(name)
                        with open(self.BMSErrorLogPath,'a', newline='') as file: #Write to CSV file
                            
                            writer = csv.writer(file)
                            errorData = [datetime.fromtimestamp(timeStamp),name,"Cleared"]
                            writer.writerow(errorData)
                
        

        if len(self.activeFaults) > 0:
            #check if any faults active
            self.isFault = True
        else:
            self.isFault = False
             
        #clear isfault if none of the faults are present anymore
        # if self.isFault:
        #     isFaultCheck = False
        #     for key in faultKeys:
        #         isFaultCheck = isFaultCheck & self.faultList[key]
    


    def get_unit_number(self):
        return self.unitType[0].value
    def get_active_alarms(self):
        activeAlarmList = []
     
        
        if len(self.activeFaults) == 0:
            # activeAlarmList = [['No active alarms','']]
            activeAlarmList = []
        else:
            
            for alarm in self.activeFaults:
                human_alarm = [alarm,"Active"]
                activeAlarmList.append(human_alarm)

        return activeAlarmList

    def Extract(lst):
        return [item[0] for item in lst]

    def get_alarm_history(self):
        #return a list of historic alarms with raised timestamp (newest first)
        errorList = []
        errorListTemp = []
        #print("returning list of alarms")
        with open(self.BMSErrorLogPath) as file:
            csv_reader = csv.reader(file,delimiter=',',)
            try:
                line_count = 0
                #print("Printing list for {} with csv path :  {}".format(self.BMSName, self.BMSErrorLogPath))
                for row in csv_reader:
                        #check for valid number of columns in row
                        if len(row) > 2:
                            if line_count == 0:
                                #skip the header row
                                #print (f'Column names are {", ".join(row)}')
                                line_count += 1
                            else:
                                

                                listItem = [row[0],row[1] ,row[2]]
                                errorList.append(listItem)
                                    #print(listItem)
                                line_count += 1
                #print("There are {} items in the list".format(line_count))
                
                errorList.reverse()
                #print(errorList)
                return errorList
            except Exception as e:
                print("could not read from CSV because {}".format(e))
                return errorList

    def log_reset(self, timeStamp):
        print("resetting {} bms")
        with open(self.BMSErrorLogPath,'a', newline='') as file: #Write to CSV file
            writer = csv.writer(file)
            resetData = [datetime.fromtimestamp(timeStamp),"BMS Reset by operator","N/A"]
            writer.writerow(resetData)        


class CombinedBMSUnit(BMSUnit):

    def __init__(self,unitType):
        BMSUnit.__init__(self,unitType)

        self.parallelActiveStrings = 0

    def set_val_combined(self,name,value,timeStamp):

        self.set_val(name,value,timeStamp)
        if name == 'Parallel_Active_Strings':
            self.parallelActiveStrings = value
        elif name == 'Parallel_Combined_Charger_Safety_Inverted':
            if value:
                self.chargeSafety = False
            else:
                self.chargeSafety = True
        elif name == 'Parallel_Combined_Charge_Enable_Inverted':
            self.allowCharge = value
            
        elif name == 'Parallel_Combined_Faults_Present':
            self.isFault = value
        elif name == 'Parallel_CCL':
      
            self.packCCL = value
        elif name == 'Parallel_DCL':
            self.packDCL = value
        elif name == 'Low_Cell_Voltage':
            self.lowCellVoltage = value
        elif name == 'High_Cell_Voltage':
            self.highCellVoltage = value
        elif name == 'Low_Temperature':
            self.lowTemp = value-273
        elif name == 'High_Temperature':
            self.highTemp = value-273
            
            




    #parallel strings connected
    #parallel allow charge
    #parallel allow discharge
    



class CANMessage:

    def __init__(self, 
    name, 
    id,
    startBit,
    len=8,
    bitOrder=BitOrder.MSB,
    byteOrder=ByteOrder.BigEndian,
    factor=1,
    BMSNumber=BMSOrder.Slave3,
    value=None, 
    timeStamp =None,
    isSigned = False,
    
    ):
        self.name       = name      #Message name as a string   
        self.id         = id        #Message ID
        self.startBit  = startBit   #Message startBit in message
        self.len        = len       #Length of message in bits(default = 8)
        self.bitOrder   = bitOrder  #bit order of Byte, either 0 = LSB or 1 = MSB(default)
        self.byteOrder  = byteOrder #byte order of message, either 0 = LittleEndian, 1 = BigEndian(default)
        self.factor     = factor    #Multiplication factor of message
        self.BMSNumber = BMSNumber
        self.value      = value     
        self.timeStamp  = timeStamp
        self.isSigned   = isSigned
        

    def set_val(self,data,timeStamp):
        #get the byte position of the message [0 --> 7]
        bytePos = int(self.startBit / 8)



        try:
            if self.len == 1:
                bitPos = self.startBit - 8*bytePos
                bitState = bool(int(data[bytePos])&(1<<bitPos))
                self.value = bitState

                
       
            else:
                # get the number of bytes for the message
                byteNum = int(self.len / 8)
                if byteNum == 1:
                    self.value = data[bytePos]*self.factor
                else:
                    valueInts = data[bytePos:byteNum+bytePos]
                    ValueBytes = bytes(valueInts)
                    if self.byteOrder == ByteOrder.BigEndian:
                        self.value = int.from_bytes(ValueBytes,"big",signed=self.isSigned)*self.factor
                    else:
                        self.value = int.from_bytes(ValueBytes,"little",signed=self.isSigned)*self.factor

               

   
            
            self.timeStamp = timeStamp

          
            return self.value
        except:
            print('There was an error')

class MessageManager():

    cell_broadcast_ids = [0xe3,0xe4,0xe5,0xe6]
    id_list = [0x3b1,0x3b2,0x3b3]
    id_read =[]
    msg_list = []

    #Message list coming from the Master BMS
    CANMsg_All = [
    # CANMessage('Broadcast_Cell_ID',             0xe3,0,8,BitOrder.MSB,ByteOrder.BigEndian,1),  
    # CANMessage('Broadcast_Cell_Intant_Voltage', 0xe3,8,16,BitOrder.MSB,ByteOrder.BigEndian,0.1),    #Units in mV
    # CANMessage('Broadcast_Cell_Resistance',     0xe3,24,16,BitOrder.MSB,ByteOrder.BigEndian,0.01),  #Units in mOhm 
    # CANMessage('Broadcast_Cell_Open_Voltage',   0xe3,40,16,BitOrder.MSB,ByteOrder.BigEndian,0.1),   #Units in mV
        #Master Unit messages
    CANMessage('Pack_Current',                              0x3b1,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.1,BMSOrder.Master,isSigned=True),
    CANMessage('Inst_Voltage',                              0x3b1,16,16,BitOrder.MSB,ByteOrder.BigEndian,0.1,BMSOrder.Master),
    CANMessage('Pack_SOC',                                  0x3b1,32,8,BitOrder.MSB,ByteOrder.BigEndian,0.5,BMSOrder.Master),
    CANMessage('Relay_State',                               0x3b1,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('Pack_DCL',                                  0x3b2,0,16,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('Pack_CCL',                                  0x3b2,16,16,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('High_Temperature',                          0x3b2,32,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('Low_Temperature',                           0x3b2,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    
    CANMessage('DTC P0A1F : Internal Cell Communication',   0x3b3,0,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A12 : Cell Balancing Stuck Off',      0x3b3,1,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0A80 : Weak Cell',                     0x3b3,2,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0AFA : Low Cell Voltage',              0x3b3,3,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0A04 : Cell Open Wiring',              0x3b3,4,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0AC0 : Current Sensor',                0x3b3,5,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0A0D : Cell Voltage Over 5V',          0x3b3,6,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0A0F : Cell Bank',                     0x3b3,7,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0A02 : Weak Pack',                     0x3b3,8,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0A81 : Fan Monitor',                   0x3b3,9,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0A9C : Thermistor',                    0x3b3,10,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC U0100 : CAN Communication',             0x3b3,11,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0560 : Redundant Power Supply',        0x3b3,12,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0AA6 : High Voltage Isolation',        0x3b3,13,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('DTC P0A05 : Invalid Input Supply Voltage',  0x3b3,14,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),  
    CANMessage('DTC P0A06 : ChargeEnable Relay',            0x3b3,15,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A07 : DischargeEnable Relay',         0x3b3,16,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A08 : Charger Safety Relay',          0x3b3,17,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A09 : Internal Hardware',             0x3b3,18,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A0A : Internal Heatsink Thermistor',  0x3b3,19,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A0B : Internal Logic',                0x3b3,20,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A0C : Highest Cell Voltage Too High', 0x3b3,21,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A0E : Lowest Cell Voltage Too Low',   0x3b3,22,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('DTC P0A10 : Pack Too Hot',                  0x3b3,23,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('Balancing_Active',                          0x3b3,24,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('MultiPurpose_Enable',                       0x3b3,25,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master), 
    CANMessage('Charge Enable Inverted',                    0x3b3,26,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),
    CANMessage('Discharge Enable Inverted',                 0x3b3,27,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Master),

    CANMessage('Low_Cell_Voltage',                          0x3b4,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Master),
    CANMessage('Low_Cell_ID',                               0x3b4,16,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Master),
    CANMessage('High_Cell_Voltage',                         0x3b4,24,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Master),
    CANMessage('High_Cell_ID',                              0x3b4,42,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Master),

        #Slave1 Unit messages
    CANMessage('Pack_Current',                              0x4b1,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.1,BMSOrder.Slave1,isSigned=True),
    CANMessage('Inst_Voltage',                              0x4b1,16,16,BitOrder.MSB,ByteOrder.BigEndian,0.1,BMSOrder.Slave1),
    CANMessage('Pack_SOC',                                  0x4b1,32,8,BitOrder.MSB,ByteOrder.BigEndian,0.5,BMSOrder.Slave1),
    CANMessage('Relay_State',                               0x4b1,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('Pack_DCL',                                  0x4b2,0,16,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('Pack_CCL',                                  0x4b2,16,16,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('High_Temperature',                          0x4b2,32,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('Low_Temperature',                           0x4b2,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A1F : Internal Cell Communication',   0x4b3,0,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A12 : Cell Balancing Stuck Off',      0x4b3,1,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A80 : Weak Cell',                     0x4b3,2,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0AFA : Low Cell Voltage',              0x4b3,3,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A04 : Cell Open Wiring',              0x4b3,4,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0AC0 : Current Sensor',                0x4b3,5,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A0D : Cell Voltage Over 5V',          0x4b3,6,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A0F : Cell Bank',                     0x4b3,7,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A02 : Weak Pack',                     0x4b3,8,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A81 : Fan Monitor',                   0x4b3,9,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A9C : Thermistor',                    0x4b3,10,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC U0100 : CAN Communication',             0x4b3,11,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0560 : Redundant Power Supply',        0x4b3,12,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0AA6 : High Voltage Isolation',        0x4b3,13,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('DTC P0A05 : Invalid Input Supply Voltage',  0x4b3,14,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),  
    CANMessage('DTC P0A06 : ChargeEnable Relay',            0x4b3,15,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A07 : DischargeEnable Relay',         0x4b3,16,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A08 : Charger Safety Relay',          0x4b3,17,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A09 : Internal Hardware',             0x4b3,18,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A0A : Internal Heatsink Thermistor',  0x4b3,19,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A0B : Internal Logic',                0x4b3,20,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A0C : Highest Cell Voltage Too High', 0x4b3,21,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A0E : Lowest Cell Voltage Too Low',   0x4b3,22,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('DTC P0A10 : Pack Too Hot',                  0x4b3,23,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('Balancing_Active',                          0x4b3,24,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('MultiPurpose_Enable',                       0x4b3,25,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1), 
    CANMessage('Charge Enable Inverted',                    0x4b3,26,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('Discharge Enable Inverted',                 0x4b3,27,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave1),
    CANMessage('Low_Cell_Voltage',                          0x4b4,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Slave1),
    CANMessage('Low_Cell_ID',                               0x4b4,16,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Slave1),
    CANMessage('High_Cell_Voltage',                         0x4b4,24,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Slave1),
    CANMessage('High_Cell_ID',                              0x4b4,42,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Slave1),
        #Slave2 Unit messages
    CANMessage('Pack_Current',                              0x5b1,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.1,BMSOrder.Slave2,isSigned=True),
    CANMessage('Inst_Voltage',                              0x5b1,16,16,BitOrder.MSB,ByteOrder.BigEndian,0.1,BMSOrder.Slave2),
    CANMessage('Pack_SOC',                                  0x5b1,32,8,BitOrder.MSB,ByteOrder.BigEndian,0.5,BMSOrder.Slave2),
    CANMessage('Relay_State',                               0x5b1,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('Pack_DCL',                                  0x5b2,0,16,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('Pack_CCL',                                  0x5b2,16,16,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('High_Temperature',                          0x5b2,32,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('Low_Temperature',                           0x5b2,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A1F : Internal Cell Communication',   0x5b3,0,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A12 : Cell Balancing Stuck Off',      0x5b3,1,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A80 : Weak Cell',                     0x5b3,2,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0AFA : Low Cell Voltage',              0x5b3,3,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A04 : Cell Open Wiring',              0x5b3,4,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0AC0 : Current Sensor',                0x5b3,5,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A0D : Cell Voltage Over 5V',          0x5b3,6,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A0F : Cell Bank',                     0x5b3,7,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A02 : Weak Pack',                     0x5b3,8,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A81 : Fan Monitor',                   0x5b3,9,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A9C : Thermistor',                    0x5b3,10,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC U0100 : CAN Communication',             0x5b3,11,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0560 : Redundant Power Supply',        0x5b3,12,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0AA6 : High Voltage Isolation',        0x5b3,13,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('DTC P0A05 : Invalid Input Supply Voltage',  0x5b3,14,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),  
    CANMessage('DTC P0A06 : ChargeEnable Relay',            0x5b3,15,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A07 : DischargeEnable Relay',         0x5b3,16,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A08 : Charger Safety Relay',          0x5b3,17,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A09 : Internal Hardware',             0x5b3,18,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A0A : Internal Heatsink Thermistor',  0x5b3,19,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A0B : Internal Logic',                0x5b3,20,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A0C : Highest Cell Voltage Too High', 0x5b3,21,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A0E : Lowest Cell Voltage Too Low',   0x5b3,22,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('DTC P0A10 : Pack Too Hot',                  0x5b3,23,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('Balancing_Active',                          0x5b3,24,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('MultiPurpose_Enable',                       0x5b3,25,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2), 
    CANMessage('Charge Enable Inverted',                    0x5b3,26,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('Discharge Enable Inverted',                 0x5b3,27,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave2),
    CANMessage('Low_Cell_Voltage',                          0x5b4,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Slave2),
    CANMessage('Low_Cell_ID',                               0x5b4,16,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Slave2),
    CANMessage('High_Cell_Voltage',                         0x5b4,24,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Slave2),
    CANMessage('High_Cell_ID',                              0x5b4,42,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Slave2),
        #Slave2 Unit messages
    CANMessage('Pack_Current',                              0x6b1,0,16,BitOrder.MSB,ByteOrder.BigEndian,0.1,BMSOrder.Slave3),
    CANMessage('Inst_Voltage',                              0x6b1,16,16,BitOrder.MSB,ByteOrder.BigEndian,0.1,BMSOrder.Slave3),
    CANMessage('Pack_SOC',                                  0x6b1,32,8,BitOrder.MSB,ByteOrder.BigEndian,0.5,BMSOrder.Slave3),
    CANMessage('Relay_State',                               0x6b1,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('Pack_DCL',                                  0x6b2,0,16,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('Pack_CCL',                                  0x6b2,16,16,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('High_Temperature',                          0x6b2,32,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('Low_Temperature',                           0x6b2,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A1F : Internal Cell Communication',   0x6b3,0,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A12 : Cell Balancing Stuck Off',      0x6b3,1,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A80 : Weak Cell',                     0x6b3,2,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0AFA : Low Cell Voltage',              0x6b3,3,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A04 : Cell Open Wiring',              0x6b3,4,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0AC0 : Current Sensor',                0x6b3,5,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A0D : Cell Voltage Over 5V',          0x6b3,6,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A0F : Cell Bank',                     0x6b3,7,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A02 : Weak Pack',                     0x6b3,8,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A81 : Fan Monitor',                   0x6b3,9,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A9C : Thermistor',                    0x6b3,10,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC U0100 : CAN Communication',             0x6b3,11,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0560 : Redundant Power Supply',        0x6b3,12,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0AA6 : High Voltage Isolation',        0x6b3,13,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('DTC P0A05 : Invalid Input Supply Voltage',  0x6b3,14,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),  
    CANMessage('DTC P0A06 : ChargeEnable Relay',            0x6b3,15,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A07 : DischargeEnable Relay',         0x6b3,16,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A08 : Charger Safety Relay',          0x6b3,17,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A09 : Internal Hardware',             0x6b3,18,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A0A : Internal Heatsink Thermistor',  0x6b3,19,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A0B : Internal Logic',                0x6b3,20,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A0C : Highest Cell Voltage Too High', 0x6b3,21,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A0E : Lowest Cell Voltage Too Low',   0x6b3,22,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('DTC P0A10 : Pack Too Hot',                  0x6b3,23,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('Balancing_Active',                          0x6b3,24,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('MultiPurpose_Enable',                       0x6b3,25,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3), 
    CANMessage('Charge Enable Inverted',                    0x6b3,26,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('Discharge Enable Inverted',                 0x6b3,27,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Slave3),
    CANMessage('Low_Cell_Voltage',                          0x6b4,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Slave3),
    CANMessage('Low_Cell_ID',                               0x6b4,16,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Slave3),
    CANMessage('High_Cell_Voltage',                         0x6b4,24,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Slave3),
    CANMessage('High_Cell_ID',                              0x6b4,42,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Slave3),

#Master combined BMS

    CANMessage('Inst_Voltage',                              0x356,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.01,BMSOrder.Combined),
    CANMessage('Pack_Current',                              0x356,16,16,BitOrder.MSB,ByteOrder.LittleEndian,0.1,BMSOrder.Combined,isSigned=True),
    
    CANMessage('Pack_SOC',                                  0x355,0,16,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Combined),
    CANMessage('Relay_State',                               0x3b1,40,8,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Combined),

    CANMessage('Parallel_Target_Max_DC_PackV',              0x351,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.1,BMSOrder.Combined),
    CANMessage('Parallel_CCL',                              0x351,16,16,BitOrder.MSB,ByteOrder.LittleEndian,0.1,BMSOrder.Combined),
    CANMessage('Parallel_DCL',                              0x351,32,16,BitOrder.MSB,ByteOrder.LittleEndian,0.1,BMSOrder.Combined),
    CANMessage('Parallel_Target_Min_DC_PackV',              0x351,48,16,BitOrder.MSB,ByteOrder.LittleEndian,0.1,BMSOrder.Combined),

    CANMessage('Parallel_Active_Strings',                   0x372,0,8,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Combined),

    CANMessage('Low_Cell_Voltage',                          0x373,0,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Combined),
    CANMessage('High_Cell_Voltage',                         0x373,16,16,BitOrder.MSB,ByteOrder.LittleEndian,0.001,BMSOrder.Combined),
    CANMessage('Low_Temperature',                           0x373,32,16,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Combined),
    CANMessage('High_Temperature',                          0x373,48,16,BitOrder.MSB,ByteOrder.LittleEndian,1,BMSOrder.Combined),

    CANMessage('Parallel_Combined_Charger_Safety_Inverted', 0x3b3,29,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Combined), 
    CANMessage('Parallel_Combined_Charge_Enable_Inverted',  0x3b3,30,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Combined), 
    CANMessage('Parallel_Combined_Faults_Present',          0x3b3,31,1,BitOrder.MSB,ByteOrder.BigEndian,1,BMSOrder.Combined), 
    #parallel bus voltage
    #parallel current
    #parallel charge anable
    #parallel dcl
    #parallel ccl
    #parallel high temp
    #parallel low temp
    #parallel high cell 
    #parallel low cell

    ]    
    WHITELIST_IDs = []#List of message IDs that we want. 

    cell_info       = {0xe3:[],0xe4:[],0xe5:[],0xe6:[]}
    cell_broadcast_ids = [0xe3,0xe4,0xe5,0xe6] 

    BMS_Master_Combined = CombinedBMSUnit(unitType=BMSOrder.Combined)
    #BMS_Master_Combined = BMSUnit(unitType=BMSOrder.Combined)
    BMS_Master = BMSUnit(unitType=BMSOrder.Master)
    BMS_Slave1 = BMSUnit(unitType=BMSOrder.Slave1)
    BMS_Slave2 = BMSUnit(unitType=BMSOrder.Slave2)
    BMS_Slave3 = BMSUnit(unitType=BMSOrder.Slave3)

    def updateOnline(self): #update online status of all BMS Units
        self.BMS_Master.checkOnline()
        self.BMS_Slave1.checkOnline()
        self.BMS_Slave2.checkOnline()
        self.BMS_Slave3.checkOnline()

    

    def __init__(self) -> None:
        #populate the whitelists
        self.populate_whitelist()

    def populate_whitelist(self):  
        #The for loop seems to have a problem if a list of CANMessages are appended to another list.
        #The whilelist will have to be once long list with all the needed message IDS
        for message in self.CANMsg_All:   
            if message.id not in self.WHITELIST_IDs:
                self.WHITELIST_IDs.append(message.id)
        print(self.WHITELIST_IDs)
            #Create an ampty list for master to slave3 
        for u in range(0,4,1):
            for i in range(1,45,1):
                self.cell_info[0xe3+u].append({'Broadcast_Cell_ID':i,'Broadcast_Cell_Intant_Voltage': 0.0, 'Broadcast_Cell_Resistance': 0.0,'Broadcast_Cell_Open_Voltage' : 0.0})

        
    def process_message(self,messageId,messageData,messageTime):
        if messageId in self.cell_broadcast_ids:
            self.process_cell_broadcast(messageId,messageData,messageTime)
        elif messageId in self.WHITELIST_IDs:
            for msg in self.CANMsg_All:
                if messageId == msg.id:
                    #Set CANBus message data
                    msg.set_val(messageData,messageTime)
                    #populate BMS data
                    if msg.BMSNumber == BMSOrder.Combined:
                        self.BMS_Master_Combined.set_val_combined(msg.name,msg.value,messageTime)
                    elif msg.BMSNumber == BMSOrder.Master:
                        self.BMS_Master.set_val(msg.name,msg.value,messageTime)
                    elif msg.BMSNumber == BMSOrder.Slave1:
                        self.BMS_Slave1.set_val(msg.name,msg.value,messageTime)
                    elif msg.BMSNumber == BMSOrder.Slave2:
                        self.BMS_Slave2.set_val(msg.name,msg.value,messageTime)
                    elif msg.BMSNumber == BMSOrder.Slave3:
                        self.BMS_Slave3.set_val(msg.name,msg.value,messageTime)
    
                    #print(msg.id)
                    #print(msg.name)
                    #print(msg.value)


    def process_cell_broadcast(self,messageId,messageData,messageTime):
    
        #Extract the cell ID
        cellId          = messageData[0]
        #Extract instant voltage in mV
        valueInts       = messageData[1:3]
        ValueBytes      = bytes(valueInts)
        cellInstVoltage = int.from_bytes(ValueBytes,"big")*0.1
        #Extract Cell resistance in mOhm
        valueInts       = messageData[3:5]
        ValueBytes      = bytes(valueInts)
        cellResistance  = int.from_bytes(ValueBytes,"big")*0.01
        #Extract Cell Open Voltage in mV
        valueInts       = messageData[5:7]
        ValueBytes      = bytes(valueInts)
        cellOpenVoltage = int.from_bytes(ValueBytes,"big")*0.1
        #Append cell info list for master unit
        if messageId == 0xe3:
            self.BMS_Master.lastOnline=messageTime
            self.BMS_Master.cell_info[cellId - 1]['Broadcast_Cell_ID']              = cellId
            self.BMS_Master.cell_info[cellId - 1]['Broadcast_Cell_Intant_Voltage']  = cellInstVoltage
            self.BMS_Master.cell_info[cellId - 1]['Broadcast_Cell_Resistance']      = cellResistance
            self.BMS_Master.cell_info[cellId - 1]['Broadcast_Cell_Open_Voltage']    = cellOpenVoltage
        elif messageId == 0xe4:
            self.BMS_Slave1.cell_info[cellId - 1]['Broadcast_Cell_ID']              = cellId
            self.BMS_Slave1.cell_info[cellId - 1]['Broadcast_Cell_Intant_Voltage']  = cellInstVoltage
            self.BMS_Slave1.cell_info[cellId - 1]['Broadcast_Cell_Resistance']      = cellResistance
            self.BMS_Slave1.cell_info[cellId - 1]['Broadcast_Cell_Open_Voltage']    = cellOpenVoltage
        elif messageId == 0xe5:
            self.BMS_Slave2.cell_info[cellId - 1]['Broadcast_Cell_ID']              = cellId
            self.BMS_Slave2.cell_info[cellId - 1]['Broadcast_Cell_Intant_Voltage']  = cellInstVoltage
            self.BMS_Slave2.cell_info[cellId - 1]['Broadcast_Cell_Resistance']      = cellResistance
            self.BMS_Slave2.cell_info[cellId - 1]['Broadcast_Cell_Open_Voltage']    = cellOpenVoltage
        elif messageId == 0xe6:
            self.BMS_Slave3.cell_info[cellId - 1]['Broadcast_Cell_ID']              = cellId
            self.BMS_Slave2.cell_info[cellId - 1]['Broadcast_Cell_Intant_Voltage']  = cellInstVoltage
            self.BMS_Slave2.cell_info[cellId - 1]['Broadcast_Cell_Resistance']      = cellResistance
            self.BMS_Slave2.cell_info[cellId - 1]['Broadcast_Cell_Open_Voltage']    = cellOpenVoltage

