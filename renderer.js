

const dayOfTheWeek = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
const monthShort = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec"];
let BMSID = 0;
const pageIndexes  = {
    Home: 'Home',
    Summary : 'Summary',
    Details : 'Details',
    activeAlarms : 'activeAlarms',
    alarmHistory : 'alarmHistory',  
    IO : 'IO',
    CellInfo : 'CellInfo',
}
let pageIndex = [pageIndexes.Home];


window.addEventListener("load", () => {
    //callbacks
    window.electronAPI.gotTileInfo(gotTileInfo);    
    window.electronAPI.gotTest(gotTest);
    window.electronAPI.gotSummaryInfo(gotSummaryInfo);
    window.electronAPI.gotConnecting(gotConnecting);
    window.electronAPI.gotActiveAlarms(gotActiveAlarms);
    // Got details
    window.electronAPI.gotDetails(gotDetails);
    // Got IO
    window.electronAPI.gotIO(gotIO);
    // Got cell info
    window.electronAPI.gotCellInfo(gotCellInfo);
    // Got alarm history
    window.electronAPI.gotAlarmHistory(gotAlarmHistory);
    


    

    // Initial call to get tile info
    window.electronAPI.getTileInfo();

    // getBatteryTile(batteryMaster);
    // getBatteryTile(batterySlave);
    // getBatteryTile(batterySlave2); 
});

const btnshowSidebar = document.getElementById("openbtn");
const btnHideSidebar = document.getElementById("closebtn");
const mainInfo = document.getElementById("main-info");


var pageRefresh = setInterval(function() {
    // window.electronAPI.getTileInfo();
    // Run manage info periodically
    manageInfo();

   

  }, 20000);



function testfunction(){
    console.log("test function");
}

const gotCellInfo = (cellInfo) => {
    let cellsPerRow = 11;
    let cellCount = 1;
    // console.log(`Cell information : ${cellInfo.cellInfo[0]}`);
    addHeader("Cell Info");
    let tableString = "";

    tableString += `
    <table class="table table-bordered cell-table">
        <caption>Cell Voltages</caption>
        <thead>
            <tr>
                <th scope="col"></th> `;
    for (let i = 1; i <= cellsPerRow; i++){
        tableString += `
                <th scope="col">${i}</th>`;
    }
    tableString += `
            </tr>
        </thead>
        <tbody>`;
    for (let i = 0; i < 4; i++){
        tableString += `
            <tr>
                <th scope="row">${i+1}</th>`;
            for (let j = 0; j < cellsPerRow; j++){
                tableString += `
                    <td>${Number(cellInfo[cellCount-1].Broadcast_Cell_Intant_Voltage).toFixed(3) }</td>`;
                cellCount++;
            }
        tableString += `
            </tr>`;
    }
    tableString +=`
        </tbody>
    </table>`;
    
    console.log(tableString);
    mainInfo.innerHTML += tableString;

        



    // add cell info
    
    // Add a row with 3 options for instant voltage, open voltage and Resistance

    // Create a grid with 11 cells in a row and 4 rows

    

}
const gotIO = (IO) => {
    console.log("gotIO");
    console.log(IO);
    var statusColor= "white";
    let dispString = "";
    
    addHeader("IO");
    // add IO info
    // isFault
    // if (IO.isFault){
    //     statusColor = "red";
    //     dispString = "FAULT";
    // }else{
    //     statusColor = "green";
    //     dispString = "OK";
    // }
    // mainInfo.innerHTML += getInfoRow("Faults present", [`${dispString}`], null, statusColor);
    // // isOnline
    // if (IO.isOnline){
    //     statusColor = "green";
    //     dispString = "ONLINE";
    // }else{
    //     statusColor = "red";
    //     dispString = "OFFLINE";
    // }
    // mainInfo.innerHTML += getInfoRow("Online", [`${dispString}`], null, statusColor);
    // relayState
    if (IO.relayState){
        statusColor = "green";
        dispString = "CLOSED";
    }else{
        statusColor = "red";
        dispString = "OPEN";
    }
    mainInfo.innerHTML += getInfoRow("Relay State", [`${dispString}`], null, statusColor);
    // allowCharge
    if (IO.allowCharge){
        statusColor = "green";
        dispString = "YES";
    }else{
        statusColor = "red";
        dispString = "NO";
    }
    mainInfo.innerHTML += getInfoRow("Allow Charge", [`${dispString}`], null, statusColor);
    // allowDischarge
    if (IO.allowDischarge){
        statusColor = "green";
        dispString = "YES";
    }else{
        statusColor = "red";
        dispString = "NO";

    }
    mainInfo.innerHTML += getInfoRow("Allow Discharge", [`${dispString}`], null, statusColor);
    // isBalancing
    if (IO.isBalancing){
        statusColor = "white";
        dispString = "YES";
    }else{
        statusColor = "white";
        dispString = "NO";
    }
    mainInfo.innerHTML += getInfoRow("Balancing", [`${dispString}`], null, statusColor);

}


const gotDetails = (battery) => {
    console.log("gotDetails");
    // console.log(details);
    addHeader("Battery Details");
    // add details info
    mainInfo.innerHTML += getInfoRow("BMS Name", [`${battery.BMSName}`]);
    // high cell voltage and cell number
    mainInfo.innerHTML += getInfoRow("High Cell Voltage", [`${battery.highCellVoltage} V`,`Cell ${battery.highCellId}`]);
    // low cell voltage and cell number
    mainInfo.innerHTML += getInfoRow("Low Cell Voltage", [`${battery.lowCellVoltage} V`,`Cell ${battery.lowCellId}`]);
    // packDCL
    mainInfo.innerHTML += getInfoRow("Pack DCL", [`${battery.packDCL} A`]);
    // packCCL
    mainInfo.innerHTML += getInfoRow("Pack CCL", [`${battery.packCCL} A`]);
    // high temp
    mainInfo.innerHTML += getInfoRow("High Temperature", [`${battery.highTemp} °C`]);
    // low temp
    mainInfo.innerHTML += getInfoRow("Low Temperature", [`${battery.lowTemp} °C`]);
    // Heat Sink Temp
    mainInfo.innerHTML += getInfoRow("Heat Sink Temperature", [`${battery.heatSinkTemp} °C`]);



}





const gotActiveAlarms = (alarms) => {
    console.log(` list of active alarms ${alarms.activeAlarms}`);
    addHeader("Active Alarms");
    // add alarm info
    
}


const gotTest = (test) => {
    console.log("gotTest");
    console.log(test);
}

const gotConnecting = (connecting) => {
    console.log("gotConnecting");
    mainInfo.innerHTML = "";
    mainInfo.innerHTML = `
        <div class="row align-items-center" style="width:80%; text-align: center; margin-left:auto;margin-right:auto;margin-top:100px">
            <h1>${connecting}</h1>
            
        </div>
    `;
}

const gotSummaryInfo = (battery) => {
    console.log("gotSummaryInfo");
    console.log(battery);
    var statusColor= "red";
    let statusString = "OFFLINE";
    let batteryStatus = getStatusString(battery);
    statusString = batteryStatus[0];
    statusColor = batteryStatus[1];
    addHeader("Battery Summary");

    mainInfo.innerHTML += getInfoRow("Status", [statusString],null, statusColor);
    var batteryPowerStr = getPowerString(battery.power);
    mainInfo.innerHTML += getInfoRow("Battery Summary", [`${battery.instantVoltage} V`,`${battery.packCurrent}`,batteryPowerStr]);
    mainInfo.innerHTML += getInfoRow("State Of Charge (SOC)", [`${battery.packSOC} %`]);
    // Details
    mainInfo.innerHTML += getInfoRow("Details", [">"],pageIndexes.Details);
    mainInfo.innerHTML += getInfoRow("Active Alarms", [`${battery.activeAlarms.length}`,">"], pageIndexes.activeAlarms);
    mainInfo.innerHTML += getInfoRow("Alarms History", [">"], pageIndexes.alarmHistory);
    mainInfo.innerHTML += getInfoRow("IO", [">"], pageIndexes.IO);
    // Cell Voltages
    mainInfo.innerHTML += getInfoRow("Cell Info", [`${battery.highCellVoltage}`,`${battery.lowCellVoltage}`,">"], pageIndexes.CellInfo, "white");
    
    
}

function addHeader(headerText){
    // add back button in mainInfo
    mainInfo.innerHTML = `
        <div class="info-row rounded  " >
            <button type="button" id="" class="btn btn-light" onclick="pageIndex.shift(); manageInfo()" style="width:100px">Back</button>
        </div>
    `;
}

function getInfoRow(infoName, infoValues,  page = null, valueColor = "white"){
    console.log(infoValues)
    // Info Name
    var infoRow = ` 
    <div class="info-row rounded  " onclick="setPageIndex('${page}')">
        <div class="container">
            <div class="row">
                <div class="col-md-6 info_name">
                    ${infoName}
                </div>
                <div class="col-md-6 ">
                    <div class="row justify-content-end">  `;
    // Info Values
    for (const value in infoValues){
        infoRow += `
        <div class="col-md-auto info-value rounded align-self-center" style="color:${valueColor}">
            <span class="align-middle">${infoValues[value]}</span>
        </div>
        `;
    }
    // Closing divs
    infoRow += `
                    </div>
                </div>  
            </div>  
        </div> 
    </div>
    `;


    return infoRow;
}

function setPageIndex(page){
    // if not null, then add page to pageIndex
    console.log(`page: ${page}`);
    if (page != 'null'){
        // log type of page
        // console.log(`page type: ${typeof page}`);

        pageIndex.unshift(page);
    }
    manageInfo();

}

    


const gotTileInfo = (batteries) => {
    console.log("gotTileInfo");
    console.log(batteries);
    //list through batteries in battery tile info
    // console.log(`batteryTileInfo: ${typeof batteries}`);
    mainInfo.innerHTML = "";
    for (const battery in batteries){
        var batteryInfo = batteries[battery];
        // console.log(`battery power : ${batteryInfo.BMSName}`)
        getBatteryTile(batteryInfo);
        // console.log(`battery: ${batteryInfo.BMSName}`);
        }
    //add a button to end of mainInfo
    mainInfo.innerHTML += `
        <button type="button" id="" class="btn btn-warning" onclick="testfunction()" style="width:100px">Reset</button>
    `;

}

function manageInfo(){
    console.log("manage info");
    console.log(`pageIndex: ${pageIndex}`);
    // console.log(`page index: ${pageIndex}`);
    if (pageIndex[0] == pageIndexes.Home){
        // console.log("home page");
        // console.log("getting tile info");
        window.electronAPI.getTileInfo();
    } else if (pageIndex[0] == pageIndexes.Summary){
        window.electronAPI.getSummaryInfo(BMSID);
        console.log("summary page");
    } else if (pageIndex[0] == pageIndexes.Details){
        console.log("details page");
        window.electronAPI.getDetails(BMSID);
    } else if (pageIndex[0] == pageIndexes.activeAlarms){
        console.log("activeAlarms page");
        // get active alarms list
        window.electronAPI.getActiveAlarms(BMSID);
    }
    else if (pageIndex[0] == pageIndexes.alarmHistory){
        console.log("alarmHistory page");
    }
    else if (pageIndex[0] == pageIndexes.IO){
        console.log("IO page");
        window.electronAPI.getIO(BMSID);
    }
    else if (pageIndex[0] == pageIndexes.CellInfo){
        console.log("CellInfo page");
        window.electronAPI.getCellInfo(BMSID);
    }
    else {
        console.log("unknown page");
        pageIndex = [pageIndexes.Home];
    }


}
function getStatusString(battery){
    if (battery.isOnline) {
        if (battery.isFault){
            statusString = "FAULT";
            statusColor = "red";
        } else if (!battery.relayState){
            statusString = "RELAY\nOPEN";
            statusColor = "red";
        } else {
            statusString = "OK";
            statusColor = "green";
        }
    } else {
        statusString = "OFFLINE";
        statusColor = "red";
    }
    // return statusString and statusColor
    return [statusString, statusColor];
}

function getPowerString(power){
    // if abs of batteryPower is less than 1000, then batteryPower is in watts
    let batteryPowerStr = "";
    if (Math.abs(power) < 1000){
        batteryPowerStr =power  + " w";
    }else {
        // batteryPower is in kw to 1 decimal place
        batteryPowerStr = (power/1000).toFixed(2) + " kw";
    }
    return batteryPowerStr;
}


function getBatteryTile(battery){
    // const batteryPower = battery.voltage * battery.amps;
    
    var batteryStatus = getStatusString(battery);;
    var batteryDraw;
    var statusColor= "red";
    let statusString = "OFFLINE";
    statusString = batteryStatus[0];
    statusColor = batteryStatus[1];
    //absolute value of batteryPower
    
   
    var batteryPowerStr = getPowerString(battery.power);
    
    if (battery.power < -50){
        //discharging
        batteryDraw = "discharging";
    } else if ((battery.power >= -50) && (battery.power <= 50)){
        // idle
        batteryDraw = "idle";
    } else {
        // charging
        batteryDraw = "charging";
    }



    


    if (battery.status == "OK"){
        statusColor = "green";
    } else {
        statusColor = "red";
    }
    
    mainInfo.innerHTML += `
        <div class="battery-tile row rounded align-items-center border border-1 border-dark scan-tile mx-auto" onclick="loadBatterySummary(${battery.BMSNumber})">
            <!-- <div class="col-2  " style="">
                <img src="assets\images\batery_icon.png" onerror="this.src='assets/images/icons8-person-80.png';" class="rounded" style="">
            </div> -->
            <div class="col-10" >
                <div style="color:#e6e6e6"> ${battery.BMSName}</div>
                <!-- <p class=" " style="text-align: left;  margin-bottom:2;"> </p> -->
                <!-- <hr class="divider"/> -->
                <div class="row align-items-start">
                    <!-- Voltage -->
                    <div class="col-2 bat-inf">${battery.instantVoltage} V</div>
                    <!-- Current -->
                    <div class="col-2 bat-inf">${battery.packCurrent} A</div>
                    <!-- Power -->
                    <div class="col-2 bat-inf">${batteryPowerStr}</div>
                    <!-- SOC -->
                    <div class="col-6 bat-inf">${battery.packSOC}% ${batteryDraw}</div>
                </div>
            </div>
            <div class="col-2 " style="text-align: center; border-left: 1px solid;" >
                <div>STATUS</div>
                <div style="color:${statusColor};">${statusString}</div>
            </div>
        </div>
    `;



}


function loadBatterySummary(BMSNumber){
    pageIndex.unshift(pageIndexes.Summary);
    // pageIndex = pageIndexes.Summary;
    BMSID = BMSNumber;
    console.log(`loading battery summary for ${BMSNumber}`);
    window.electronAPI.getSummaryInfo(BMSID);
}

function getBatterySummary(bms){
    console.log(`getting battery summary for ${bms}`);
    window.electronAPI.getBatterySummary(bms);
}

btnshowSidebar.addEventListener('click', () => {
    console.log("showing the sidebar")
    document.getElementById("mySidebar").style.width = "180px";
    // document.getElementById("content").style.marginLeft = "250px";
});
btnHideSidebar.addEventListener('click', () => {
    document.getElementById("mySidebar").style.width = "0";
    // document.getElementById("content").style.marginLeft = "0";
});



