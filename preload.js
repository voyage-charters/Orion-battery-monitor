const { contextBridge, ipcRenderer } = require('electron');
const globals = require('./globals');


//List of callbacks
let gotConnectingCallback;
let gotTileInfoCallback;
let gotSummaryInfoCallback;
let gotTestCallback;


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
    
  })

