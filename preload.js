const { contextBridge, ipcRenderer } = require('electron');
const globals = require('./globals');


//List of callbacks
let gotConnectingCallback;
let gotTileInfoCallback;
let gotSummaryInfoCallback;
let gotTestCallback;
let gotActiveAlarmsCallback;
let gotDetailsCallback;
let gotIOCallback;
let gotCellInfoCallback;
let gotAlarmHistoryCallback;


let gotTest = (callback) => {
  console.log("gotTestCallback");
  gotTestCallback = callback;
}

let gotTileInfo = (callback) => {
  console.log("gotTileInfo");
  gotTileInfoCallback = callback;
}

let gotConnecting = (callback) => {
  console.log("gotConnecting");
  gotConnectingCallback = callback;
}

let gotSummaryInfo = (callback) => {
  console.log("gotSummaryInfo");
  gotSummaryInfoCallback = callback;
}

let gotActiveAlarms = (callback) => {
  console.log("gotActiveAlarms");
  gotActiveAlarmsCallback = callback;
}

let gotDetails = (callback) => {
  console.log("gotDetails");
  gotDetailsCallback = callback;
}

let gotIO = (callback) => {
  console.log("gotIO");
  gotIOCallback = callback;
}

let gotCellInfo = (callback) => {
  console.log("gotCellInfo");
  gotCellInfoCallback = callback;
}

let gotAlarmHistory = (callback) => {
  console.log("gotAlarmHistory");
  gotAlarmHistoryCallback = callback;
}

let getAlarmHistory = (BMSNumber) => {
  // console.log("getAlarmHistory");
  fetch(`http://127.0.0.1:5001/get_alarm_history/${BMSNumber}`).then((data)=>{
          return data.text();
      }
      ).then((text)=>{
        // console.log("data: ", text);
        var alarms = JSON.parse(text);
        // console.log("Cell Information: ", cellInfo.cell_info);
        gotAlarmHistoryCallback(alarms);
      }
      ).catch(e=>{
        console.log(e);
        gotConnectingCallback("Connecting...");
      }
      )
    
}

let getCellInfo = (BMSNumber) => {
  // console.log("getCellInfo");
  fetch(`http://127.0.0.1:5001/get_cell_info/${BMSNumber}`).then((data)=>{
          return data.text();
      }
      ).then((text)=>{
        // console.log("data: ", text);
        var cellInfo = JSON.parse(text);
        // console.log("Cell Information: ", cellInfo.cell_info);
        gotCellInfoCallback(cellInfo.cell_info);
      }
      ).catch(e=>{
        console.log(e);
        gotConnectingCallback("Connecting...");
      }
      )
    
}

let getIO = (BMSNumber) => {
  console.log("getIO");
  fetch(`http://127.0.0.1:5001/get_io/${BMSNumber}`).then((data)=>{
          return data.text();
      }
      ).then((text)=>{
        console.log("data: ", text);
        var io = JSON.parse(text);
        console.log("io: ", io.isFault);
        gotIOCallback(io);
      }
      ).catch(e=>{
        console.log(e);
        gotConnectingCallback("Connecting...");
      }
      )
    
}

let getDetails = (BMSNumber) => {
  console.log("getDetails");
  fetch(`http://127.0.0.1:5001/get_details/${BMSNumber}`).then((data)=>{
          return data.text();
      }
      ).then((text)=>{
        console.log("data: ", text);
        var details = JSON.parse(text);
        gotDetailsCallback(details);
      }
      ).catch(e=>{
        console.log(e);
        gotConnectingCallback("Connecting...");
      }
      )
    
}

let getActiveAlarms = (BMSNumber) => {
  console.log("getActiveAlarms");
  fetch(`http://127.0.0.1:5001/get_active_alarms/${BMSNumber}`).then((data)=>{
          return data.text();
      }
      ).then((text)=>{
        console.log("data: ", text);
        var alarms = JSON.parse(text);
        gotActiveAlarmsCallback(alarms);
      }
      ).catch(e=>{
        console.log(e);
        gotConnectingCallback("Connecting...");
      }
      )
    
}



let getSummaryInfo = (BMSNumber) => {
  console.log("getSummaryInfo");
  fetch(`http://127.0.0.1:5001/get_battery_summary/${BMSNumber}`).then((data)=>{
          return data.text();
      }
      ).then((text)=>{
        console.log("data: ", text);
        var summary = JSON.parse(text);
        gotSummaryInfoCallback(summary); 
      }
      ).catch(e=>{
        console.log(e);
        gotConnectingCallback("Connecting...");
      }
      )
    }


let getTileInfo = (bms) => {
  console.log("getTileInfo");
  fetch(`http://127.0.0.1:5001/get_tile_info/`).then((data)=>{      
          return data.text();
      }).then((text)=>{
        // console.log("data: ", text);
        var batteries = JSON.parse(text);

        
        gotTileInfoCallback(batteries); 
       
        
      }).catch(e=>{
        console.log(e);
        
        gotConnectingCallback("Connecting...");
      })
    }


//ping python script
let pingPython = () => {
    console.log("pingPython");
    fetch(`http://127.0.0.1:5001/get_info/654321`).then((data)=>{      
          return data.text();
      }).then((text)=>{
        console.log("data: ", text);
        var info = JSON.parse(text);
        console.log(`email : ${info.email} `)
      }).catch(e=>{
        console.log(e);
      })
  };

  contextBridge.exposeInMainWorld('electronAPI', {
    pingPython,
    gotTest,
    getTileInfo,
    gotTileInfo,
    gotConnecting,
    getSummaryInfo,
    gotSummaryInfo,
    getActiveAlarms,
    gotActiveAlarms,
    gotDetails,
    getDetails,
    getIO,
    gotIO,
    getCellInfo,
    gotCellInfo,
    getAlarmHistory,
    gotAlarmHistory
    
  })

