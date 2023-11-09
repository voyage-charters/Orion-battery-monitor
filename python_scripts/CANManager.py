from PCANBasic import *
import os
import time
import threading
from MessageManager import *
import can #sudo apt install python3-can

IS_WINDOWS = platform.system() == 'Windows'
if IS_WINDOWS: 
    from msvcrt import getch
else:
    try:
        import getch	# pip install getch
    except ImportError:     
        GETCH_SUPPORTED = False

class ManageCan():

    # Timerinterval (ms) for reading 
    TimerInterval = 20

    def __init__(self):
        #Initiate CAN parameters
        self.isConnected = False
        self.isRunning = False
        self.MM = MessageManager()
        print("Can Manager has been initiated")


    def startCANDevice(self):
        if IS_WINDOWS:
            # Sets the PCANHandle (Hardware Channel)
            self.PcanHandle = PCAN_USBBUS1
            # Sets the desired connection mode (CAN = false / CAN-FD = true)   
            self.IsFD = False
            # Sets the bitrate for normal CAN devices
            self.Bitrate = PCAN_BAUD_500K
            # Shows if DLL was found
            self.m_DLLFound = False
            ## Starts the program
            print("This is a Windows system. ")
            #time.sleep(1)
            """
            Create an object starts the programm
            """
            self.ShowConfigurationHelp() ## Shows information about this sample
            #time.sleep(1)
            #self.ShowCurrentConfiguration() ## Shows the current parameters configuration
            #time.sleep(1)
            ## Checks if PCANBasic.dll is available, if not, the program terminates
            print("looking for PCANBasic library")
            try:
                self.m_objPCANBasic = PCANBasic()
                self.m_DLLFound = self.CheckForLibrary()
                print("Library found !! ")
                #time.sleep(1)
            except :
                print("Unable to find the library: PCANBasic.dll !")
                print("Press any key to close")
                self.getch()
                self.m_DLLFound = False
                return    

            print("Attempting to connect to PCAN Device")
            #time.sleep(1)
            ## Initialization of the selected channel
            stsResult = self.m_objPCANBasic.Initialize(self.PcanHandle,self.Bitrate)
            self.ShowStatus(stsResult)
            #time.sleep(1)
            connectAttempt = 0
            connectString = "Still trying to connect. Make sure the device is connected"
            if stsResult != PCAN_ERROR_OK:
                self.isConnected = False
                return False
            else:
                self.isConnected = True
                return True

            # while stsResult != PCAN_ERROR_OK:
            #     #self.ShowStatus(stsResult)
            #     connectStringTemp = connectString
            #     for x in range(0,connectAttempt):
            #         connectStringTemp = connectStringTemp + "."
            #     if connectAttempt == 10:
            #         connectAttempt = 0
            #     print(connectStringTemp)
            #     time.sleep(1)
            #     stsResult = self.m_objPCANBasic.Initialize(self.PcanHandle,self.Bitrate)
            #     connectAttempt += 1
            
            print("Connection successful. You can Read some CANBus data now")
        else:
            print("Starting SocketCan device")
            os.system('sudo ip link set can0 up type can bitrate 500000 restart-ms 1000')
            # os.system('sudo ifconfig can0 up')

            self.bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
            self.isConnected = True

    #Starts the timer repeater that reads the CANBus periodically
    def startCANBusRead(self): #initialize  and start the CANBus reading    
        self.m_objTimer = TimerRepeater("ReadMessages",(self.TimerInterval/1000), self.ReadCAN)
        self.start_reading()

    def start_reading(self): #Starts the Timer Repeater
        self.m_objTimer.start()
        self.isRunning = True
    
    def stop_reading(self): #Stops the Timer Repeater
        self.m_objTimer.stop()
        self.isRunning = False

    def get_running_state(self):
        return self.isRunning

    def __del__(self):
        if self.m_DLLFound:
            self.m_objPCANBasic.Uninitialize(PCAN_NONEBUS)

    def ReadCAN(self):
        # Check online status of all BMSs
        self.MM.BMS_Master_Combined.checkOnline()
        self.MM.BMS_Master.checkOnline()
        self.MM.BMS_Slave1.checkOnline()
        self.MM.BMS_Slave2.checkOnline()
        if IS_WINDOWS:
            #Read CANBus using PEAKCAN USB 
            # print("reading CANBus")
            self.ReadMessages()
        else:
            #Read CANBus using RS485 CAN HAT
            self.ReadMessage_RS485()
        #Update online status of BMS
        #self.MM.updateOnline()

    def ReadMessages(self):
        """
        Function for reading PCAN-Basic messages
        """
        stsResult = PCAN_ERROR_OK

        ## We read at least one time the queue looking for messages. If a message is found, we look again trying to 
        ## find more. If the queue is empty or an error occurr, we get out from the dowhile statement.
        while (not (stsResult & PCAN_ERROR_QRCVEMPTY)):

            stsResult = self.ReadMessage()
            if stsResult != PCAN_ERROR_OK and stsResult != PCAN_ERROR_QRCVEMPTY:
                self.ShowStatus(stsResult)
                return
    def BMSResetAll(self):

        """
        Sends a CANBus message that resets all ORION BMS devices on the network.
        Call to log the reset as well, given that the BMS is online. 
        
        """
        print("this resets all the BMSs")
        self.WriteMessages(0x7df,8,[0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],False)
        timeStamp = time.time()
        if self.MM.BMS_Master_Combined.isOnline:
            self.MM.BMS_Master_Combined.log_reset(timeStamp)
        if self.MM.BMS_Master.isOnline:
            self.MM.BMS_Master.log_reset(timeStamp)
        if self.MM.BMS_Slave1.isOnline:
            self.MM.BMS_Slave1.log_reset(timeStamp)
        if self.MM.BMS_Slave2.isOnline:
            self.MM.BMS_Slave2.log_reset(timeStamp)
        if self.MM.BMS_Slave3.isOnline: 
            self.MM.BMS_Slave3.log_reset(timeStamp)
        
        
    def ReadMessage_RS485(self):
        message = self.bus.recv(0.2)
        if message:
            try:
                # if message.arbitration_id == 947:    
                #     print(list(message.data))

                messageData = list(message.data)
                messageID = message.arbitration_id
                message.arbitration_id,message.dlc,messageData,message.timestamp
                itstimestamp = time.time()
                #print(message)
                self.MM.process_message(messageID,messageData,itstimestamp)
                # messageString =  "{}:ID={}:LEN={}".format("RX", message.arbitration_id, message.dlc)
                # for x in range(message.dlc):
                #     messageString += ":{:02x}".format(message.data[x])        
            #print exception if failed to parse the CAN message into the string.
            except Exception as e:
                print("Could not process RS485 CANBus message. Error : {}".format(e))
            

        


    def ReadMessage(self):
        """
        Function for reading CAN messages on normal CAN devices

        Returns:
            A TPCANStatus error code
        """
        ## We execute the "Read" function of the PCANBasic   
        stsResult = self.m_objPCANBasic.Read(self.PcanHandle)
        #print("message read")
        if stsResult[0] == PCAN_ERROR_OK:
            ## We show the received message
           
            self.ProcessMessageCan(stsResult[1],int(time.time()))
        elif stsResult[0] == PCAN_ERROR_QRCVEMPTY:
            #print("CANBus Queue is empty")
            t=1
        else:
            print("There seems to be a CANBus error. ERROR : {}".format(stsResult[0]))    
        return stsResult[0]
    def WriteMessages(self,ID,LEN,DATA,isExtended):
        '''
        Function for writing PCAN-Basic messages
        '''
        if IS_WINDOWS:
            
            stsResult = self.WriteMessage(ID,LEN,DATA,isExtended)
        else:
            self.WriteMessageSocketCAN(ID,LEN,DATA,isExtended)
            print("rpi writing")
            #write using r-pi
        ## Checks if the message was sent


    def WriteMessage(self,ID,LEN,DATA,isExtended):
        """
        Function for writing messages on CAN devices

        Returns:
            A TPCANStatus error code
        """
        ## Sends a CAN message with extended ID, and 8 data bytes
        #0x7df
        #data=[0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False)
        
        msgCanMessage = TPCANMsg()
        msgCanMessage.ID = ID
        msgCanMessage.LEN = LEN
        if isExtended:
            msgCanMessage.MSGTYPE = PCAN_MESSAGE_EXTENDED.value
        for i in range(8):
            msgCanMessage.DATA[i] = DATA[i]
        
        print("trying to send message")
        stsResult = self.m_objPCANBasic.Write(self.PcanHandle, msgCanMessage)
        
        if (stsResult != PCAN_ERROR_OK):
            self.ShowStatus(stsResult)
        else:
            print("Message was successfully SENT")
        return stsResult
        

    def WriteMessageSocketCAN(self,ID,LEN,DATA,isExtended):
        msg = can.Message(arbitration_id=ID, data=DATA, is_extended_id=False)
        self.bus.send(msg)
        print("writing with opencan")


    def ProcessMessageCan(self,msg,itstimestamp):
        """
            Processes a received CAN message
            
            Parameters:
                msg = The received PCAN-Basic CAN message
                itstimestamp = Timestamp of the message as TPCANTimestamp structure
            
            microsTimeStamp = itstimestamp.micros + 1000 * itstimestamp.millis + 0x100000000 * 1000 * itstimestamp.millis_overflow
            
            print("Type: " + self.GetTypeString(msg.MSGTYPE))
            print("ID: " + self.GetIdString(msg.ID, msg.MSGTYPE))
            print("Length: " + str(msg.LEN))
            print("Time: " + self.GetTimeString(microsTimeStamp))
            print("Data: " + self.GetDataString(msg.DATA,msg.MSGTYPE))
            print("----------------------------------------------------------")
        """

        #microsTimeStamp = itstimestamp.micros + 1000 * itstimestamp.millis + 0x100000000 * 1000 * itstimestamp.millis_overflow

        self.MM.process_message(msg.ID,self.GetDataInt(msg.DATA,msg.MSGTYPE),itstimestamp)

    def GetDataInt(self, data, msgtype):
        """
        Gets the data of a CAN message as a string

        Parameters:
            data = Array of bytes containing the data to parse
            msgtype = Type flags of the message the data belong

        Returns:
            A string with hexadecimal formatted data bytes of a CAN message
        """
        if (msgtype & PCAN_MESSAGE_RTR.value) == PCAN_MESSAGE_RTR.value:
            return "Remote Request"
        else:
            intTemp = []
            for x in data:
                intTemp.append(x)
            return intTemp

    def GetIdString(self, id, msgtype):
        """
        Gets the string representation of the ID of a CAN message

        Parameters:
            id = Id to be parsed
            msgtype = Type flags of the message the Id belong

        Returns:
            Hexadecimal representation of the ID of a CAN message
        """
        if (msgtype & PCAN_MESSAGE_EXTENDED.value) == PCAN_MESSAGE_EXTENDED.value:
            return '%.8Xh' %id
        else:
            return '%.3Xh' %id

    def GetTimeString(self, time):
        """
        Gets the string representation of the timestamp of a CAN message, in milliseconds

        Parameters:
            time = Timestamp in microseconds

        Returns:
            String representing the timestamp in milliseconds
        """
        fTime = time / 1000.0
        return '%.1f' %fTime

    def GetTypeString(self, msgtype):  
        """
        Gets the string representation of the type of a CAN message

        Parameters:
            msgtype = Type of a CAN message

        Returns:
            The type of the CAN message as string
        """
        if (msgtype & PCAN_MESSAGE_STATUS.value) == PCAN_MESSAGE_STATUS.value:
            return 'STATUS'
        
        if (msgtype & PCAN_MESSAGE_ERRFRAME.value) == PCAN_MESSAGE_ERRFRAME.value:
            return 'ERROR'        
        
        if (msgtype & PCAN_MESSAGE_EXTENDED.value) == PCAN_MESSAGE_EXTENDED.value:
            strTemp = 'EXT'
        else:
            strTemp = 'STD'

        if (msgtype & PCAN_MESSAGE_RTR.value) == PCAN_MESSAGE_RTR.value:
            strTemp += '/RTR'
        else:
            if (msgtype > PCAN_MESSAGE_EXTENDED.value):
                strTemp += ' ['
                if (msgtype & PCAN_MESSAGE_FD.value) == PCAN_MESSAGE_FD.value:
                    strTemp += ' FD'
                if (msgtype & PCAN_MESSAGE_BRS.value) == PCAN_MESSAGE_BRS.value:                    
                    strTemp += ' BRS'
                if (msgtype & PCAN_MESSAGE_ESI.value) == PCAN_MESSAGE_ESI.value:
                    strTemp += ' ESI'
                strTemp += ' ]'
                
        return strTemp

    def GetDataString(self, data, msgtype):
        """
        Gets the data of a CAN message as a string

        Parameters:
            data = Array of bytes containing the data to parse
            msgtype = Type flags of the message the data belong

        Returns:
            A string with hexadecimal formatted data bytes of a CAN message
        """
        if (msgtype & PCAN_MESSAGE_RTR.value) == PCAN_MESSAGE_RTR.value:
            return "Remote Request"
        else:
            strTemp = b""
            for x in data:
                strTemp += b'%.2X ' % x
            return str(strTemp).replace("'","",2).replace("b","",1)

    def ShowConfigurationHelp(self):
        """
        Shows/prints the configurable parameters for this sample and information about them
        """
        print("=========================================================================================")
        print("|                        PCAN-Basic ManualRead Example                                   |")
        print("=========================================================================================")
        print("Following parameters are to be adjusted before launching, according to the hardware used |")
        print("                                                                                         |")
        print("* PcanHandle: Numeric value that represents the handle of the PCAN-Basic channel to use. |")
        print("              See 'PCAN-Handle Definitions' within the documentation                     |")
        print("* IsFD: Boolean value that indicates the communication mode, CAN (false) or CAN-FD (true)|")
        print("* Bitrate: Numeric value that represents the BTR0/BR1 bitrate value to be used for CAN   |")
        print("           communication                                                                 |")
        print("* BitrateFD: String value that represents the nominal/data bitrate value to be used for  |")
        print("             CAN-FD communication                                                        |")
        print("=========================================================================================")
        print("")

    def ShowCurrentConfiguration(self):
        """
        Shows/prints the configured paramters
        """
        print("Parameter values used")
        print("----------------------")
        print("* PCANHandle: " + self.FormatChannelName(self.PcanHandle))
        print("* IsFD: " + str(self.IsFD))
        print("* Bitrate: " + self.ConvertBitrateToString(self.Bitrate))
        print("* BitrateFD: " + self.ConvertBytesToString(self.BitrateFD))
        print("")

    def FormatChannelName(self, handle, isFD=False):
        """
        Gets the formated text for a PCAN-Basic channel handle

        Parameters:
            handle = PCAN-Basic Handle to format
            isFD = If the channel is FD capable

        Returns:
            The formatted text for a channel
        """
        handleValue = handle.value
        if handleValue < 0x100:
            devDevice = TPCANDevice(handleValue >> 4)
            byChannel = handleValue & 0xF
        else:
            devDevice = TPCANDevice(handleValue >> 8)
            byChannel = handleValue & 0xFF

        if isFD:
           return ('%s:FD %s (%.2Xh)' % (self.GetDeviceName(devDevice.value), byChannel, handleValue))
        else:
           return ('%s %s (%.2Xh)' % (self.GetDeviceName(devDevice.value), byChannel, handleValue))

    def ConvertBitrateToString(self, bitrate):
        """
        Convert bitrate c_short value to readable string

        Parameters:
            bitrate = Bitrate to be converted

        Returns:
            A text with the converted bitrate
        """
        m_BAUDRATES = {PCAN_BAUD_1M.value:'1 MBit/sec', PCAN_BAUD_800K.value:'800 kBit/sec', PCAN_BAUD_500K.value:'500 kBit/sec', PCAN_BAUD_250K.value:'250 kBit/sec',
                       PCAN_BAUD_125K.value:'125 kBit/sec', PCAN_BAUD_100K.value:'100 kBit/sec', PCAN_BAUD_95K.value:'95,238 kBit/sec', PCAN_BAUD_83K.value:'83,333 kBit/sec',
                       PCAN_BAUD_50K.value:'50 kBit/sec', PCAN_BAUD_47K.value:'47,619 kBit/sec', PCAN_BAUD_33K.value:'33,333 kBit/sec', PCAN_BAUD_20K.value:'20 kBit/sec',
                       PCAN_BAUD_10K.value:'10 kBit/sec', PCAN_BAUD_5K.value:'5 kBit/sec'}
        return m_BAUDRATES[bitrate.value]

    def ConvertBytesToString(self, bytes):
        """
        Convert bytes value to string

        Parameters:
            bytes = Bytes to be converted

        Returns:
            Converted bytes value as string
        """
        return str(bytes).replace("'","",2).replace("b","",1)
   

    def ShowStatus(self,status):
        """
        Shows formatted status

        Parameters:
            status = Will be formatted
        """
        print("=========================================================================================")
        print(self.GetFormattedError(status))
        print("=========================================================================================")
    def GetFormattedError(self, error):
        """
        Help Function used to get an error as text

        Parameters:
            error = Error code to be translated

        Returns:
            A text with the translated error
        """
        ## Gets the text using the GetErrorText API function. If the function success, the translated error is returned.
        ## If it fails, a text describing the current error is returned.
        stsReturn = self.m_objPCANBasic.GetErrorText(error,0x09)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            message = str(stsReturn[1])
            return message.replace("'","",2).replace("b","",1)
            
    def CheckForLibrary(self):
        """
        Checks for availability of the PCANBasic library
        """
        ## Check for dll file
        try:
            self.m_objPCANBasic.Uninitialize(PCAN_NONEBUS)
            return True
        except :
            print("Unable to find the library: PCANBasic.dll !")
            print("Press any key to close")
            self.getch()
            return False 


## TimerClass
class TimerRepeater(object):

    """
    A simple timer implementation that repeats itself
    """

    ## Constructor
    def __init__(self, name, interval, target):
        """
        Creates a timer.

        Parameters:
            name = name of the thread
            interval = interval in second between execution of target
            target = function that is called every 'interval' seconds
        """
        # define thread and stopping thread event
        self._name = name
        self._thread = None
        self._event = None
        # initialize target
        self._target = target
        # initialize timer
        self._interval = interval

    # Runs the thread that emulates the timer
    #
    def _run(self):
        """
        Runs the thread that emulates the timer.

        Returns:
            None
        """
        while not self._event.wait(self._interval):
            self._target()

    # Starts the timer
    #
    def start(self):
        """
        Starts the timer

        Returns:
            None
        """
        # avoid multiple start calls
        if (self._thread == None):
            self._event = threading.Event()
            self._thread = threading.Thread(None, self._run, self._name)
            self._thread.start()

    # Stops the timer
    #
    def stop(self):
        """
        Stops the timer

        Returns:
            None
        """
        if (self._thread != None):
            self._event.set()
            self._thread = None

