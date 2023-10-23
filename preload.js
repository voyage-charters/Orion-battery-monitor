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
let gotStartCanBusCallback;
let gotStartCanReadCallback;


let gotTest = (callback) => {
  console.log("gotTestCallback");
  gotTestCallback = callback;
}



let gotConnecting = (callback) => {
  console.log("gotConnecting");
  gotConnectingCallback = callback;
}










// ##########################################################
// ################### Alarm History ########################
// ##########################################################


let getAlarmHistory = (BMSNumber) => {
  // console.log("getAlarmHistory");
  fetch(`http://127.0.0.1:5001/get_alarm_history/${BMSNumber}`).then((data) => {
    return data.text();
  }
  ).then((text) => {
    // console.log("data: ", text);
    var alarms = JSON.parse(text);
    // console.log("Cell Information: ", cellInfo.cell_info);
    gotAlarmHistoryCallback(alarms);
  }
  ).catch(e => {
    console.log(e);
    gotConnectingCallback("Connecting...");
  }
  )

}
let gotAlarmHistory = (callback) => {
  console.log("gotAlarmHistory");
  gotAlarmHistoryCallback = callback;
}

// ##########################################################
// ################### Cell Info ############################
// ##########################################################

let getCellInfo = (BMSNumber) => {
  // console.log("getCellInfo");
  fetch(`http://127.0.0.1:5001/get_cell_info/${BMSNumber}`).then((data) => {
    return data.text();
  }
  ).then((text) => {
    // console.log("data: ", text);
    var cellInfo = JSON.parse(text);
    // console.log("Cell Information: ", cellInfo.cell_info);
    gotCellInfoCallback(cellInfo.cell_info);
  }
  ).catch(e => {
    console.log(e);
    gotConnectingCallback("Connecting...");
  }
  )

}
let gotCellInfo = (callback) => {
  console.log("gotCellInfo");
  gotCellInfoCallback = callback;
}

// ##########################################################
// ################### IO ###################################
// ##########################################################

let getIO = (BMSNumber) => {
  console.log("getIO");
  fetch(`http://127.0.0.1:5001/get_io/${BMSNumber}`).then((data) => {
    return data.text();
  }
  ).then((text) => {
    console.log("data: ", text);
    var io = JSON.parse(text);
    console.log("io: ", io.isFault);
    gotIOCallback(io);
  }
  ).catch(e => {
    console.log(e);
    gotConnectingCallback("Connecting...");
  }
  )

}
let gotIO = (callback) => {
  console.log("gotIO");
  gotIOCallback = callback;
}

// ##########################################################
// ####################  Details ############################
// ##########################################################

let getDetails = (BMSNumber) => {
  console.log("getDetails");
  fetch(`http://127.0.0.1:5001/get_details/${BMSNumber}`).then((data) => {
    return data.text();
  }
  ).then((text) => {
    console.log("data: ", text);
    var details = JSON.parse(text);
    gotDetailsCallback(details);
  }
  ).catch(e => {
    console.log(e);
    gotConnectingCallback("Connecting...");
  }
  )

}
let gotDetails = (callback) => {
  console.log("gotDetails");
  gotDetailsCallback = callback;
}

// ##########################################################
// ####################  Active Alarms ######################
// ##########################################################

let getActiveAlarms = (BMSNumber) => {
  console.log("getActiveAlarms");
  fetch(`http://127.0.0.1:5001/get_active_alarms/${BMSNumber}`).then((data) => {
    return data.text();
  }
  ).then((text) => {
    console.log("data: ", text);
    var alarms = JSON.parse(text);
    gotActiveAlarmsCallback(alarms);
  }
  ).catch(e => {
    console.log(e);
    gotConnectingCallback("Connecting...");
  }
  )

}
let gotActiveAlarms = (callback) => {
  console.log("gotActiveAlarms");
  gotActiveAlarmsCallback = callback;
}


// ##########################################################
// ####################  Summary Info #######################
// ##########################################################


let getSummaryInfo = (BMSNumber) => {
  console.log("getSummaryInfo");
  fetch(`http://127.0.0.1:5001/get_battery_summary/${BMSNumber}`).then((data) => {
    return data.text();
  }
  ).then((text) => {
    console.log("data: ", text);
    var summary = JSON.parse(text);
    gotSummaryInfoCallback(summary);
  }
  ).catch(e => {
    console.log(e);
    gotConnectingCallback("Connecting...");
  }
  )
}
let gotSummaryInfo = (callback) => {
  console.log("gotSummaryInfo");
  gotSummaryInfoCallback = callback;
}

// ##########################################################
// ####################  Tile Info ##########################
// ##########################################################


let getTileInfo = (bms) => {
  console.log("getTileInfo");
  fetch(`http://127.0.0.1:5001/get_tile_info/`).then((data) => {
    return data.text();
  }).then((text) => {
    // console.log("data: ", text);
    var batteries = JSON.parse(text);


    gotTileInfoCallback(batteries);


  }).catch(e => {
    console.log(e);

    gotConnectingCallback("Connecting...");
  })
}

let gotTileInfo = (callback) => {
  console.log("gotTileInfo");
  gotTileInfoCallback = callback;
}

// ##########################################################
// ####################  Ping Test ##########################
// ##########################################################

//ping python script
let pingPython = () => {
  console.log("pingPython");
  fetch(`http://127.0.0.1:5001/get_info/654321`).then((data) => {
    return data.text();
  }).then((text) => {
    console.log("data: ", text);
    var info = JSON.parse(text);
    console.log(`email : ${info.email} `)
  }).catch(e => {
    console.log(e);
  })
};

// ##########################################################
// ####################  Start CanBus Device#################
// ##########################################################

let startCanBus = () => {
  console.log("startCanBus");
  fetch(`http://127.0.0.1:5001/start_canBus`).then((data) => {
    return data.text();
  }).then((text) => {
    console.log("data: ", text);
    var info = JSON.parse(text);
    gotStartCanBusCallback(info);
  }).catch(e => {
    console.log(e);
  })
};
let gotStartCanBus = (callback) => {
  console.log("gotStartCanBus");
  gotStartCanBusCallback = callback;
}

// ##########################################################
// ####################  Start CanRead Device################
// ##########################################################

let startCanRead = () => {
  console.log("startCanRead");
  fetch(`http://127.0.0.1:5001/start_canBus_read`).then((data) => {
    return data.text();
  }).then((text) => {
    console.log("data: ", text);
    var info = JSON.parse(text);
    gotStartCanReadCallback(info);
  }).catch(e => {
    console.log(e);
  })
}
let gotStartCanRead = (callback) => {
  console.log("gotStartCanRead");
  gotStartCanReadCallback = callback;
}

// ##########################################################
// ####################  Send Reset Command #################
// ##########################################################

let sendResetCommand = () => {
  console.log("sendResetCommand");
  fetch(`http://127.0.0.1:5001/reset_bms`).then((data) => {
    return data.text();
  }).then((text) => {
    console.log("Reset: ", text);
    // var info = JSON.parse(text);
    // gotStartCanReadCallback(info);
  })
}




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
  gotAlarmHistory,
  startCanBus,
  gotStartCanBus,
  startCanRead,
  gotStartCanRead,
  sendResetCommand,


})

