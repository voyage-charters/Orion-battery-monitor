

const dayOfTheWeek = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
const monthShort = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec"];
let BMSID = 0;
const pageIndexes  = {
    Home: 'Home',
    Summary : 'Summary',
    Details : 'Details',
}
let pageIndex = pageIndexes.Home;


window.addEventListener("load", () => {
    //callbacks
    window.electronAPI.gotTileInfo(gotTileInfo);    
    window.electronAPI.gotTest(gotTest);
    window.electronAPI.gotSummaryInfo(gotSummaryInfo);
    window.electronAPI.gotConnecting(gotConnecting);
    

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

   

  }, 5000);



function testfunction(){
    console.log("test function");
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
    mainInfo.innerHTML = "";
    // add back button in mainInfo
    mainInfo.innerHTML += `
        <button type="button" id="" class="btn btn-warning" onclick="pageIndex = pageIndexes.Home; manageInfo()" style="width:100px">Back</button>
    `;

    mainInfo.innerHTML += getInfoRow("Status", [statusString], statusColor);
    var batteryPowerStr = getPowerString(battery.power);
    mainInfo.innerHTML += getInfoRow("Battery Summary", [`${battery.instantVoltage} V`,`${battery.packCurrent}`,batteryPowerStr]);
    mainInfo.innerHTML += getInfoRow("State Of Charge (SOC)", [`${battery.packSOC} %`]);
    // Cell Voltages
    
    // Details
    mainInfo.innerHTML += getInfoRow("Details", [],"white","testfunction()");
}

function getInfoRow(infoName, infoValues, valueColor = "white", infoFuntion = null){
    console.log(infoValues)
    // Info Name
    var infoRow = ` 
    <div class="info-row rounded  " onclick=${infoFuntion}>
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

    // infoRow = `
    // <div class="info-row rounded ">
    //     <div class="container">
    //         <div class="row">
    //             <div class="col-md-8 info_name">
    //                 ${infoName}
    //             </div>
    //             <div class="col-md-4 ">
    //                 <div class="row justify-content-end"> 
    //                     <div class="col-md-4 info_value rounded" style="color:red">
    //                         FAULT
    //                     </div>
    //                 </div>
    //             </div>  
    //         </div>  
    //     </div> 
    // </div>
    // `;
    return infoRow;
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
    // console.log(`page index: ${pageIndex}`);
    if (pageIndex == pageIndexes.Home){
        // console.log("home page");
        // console.log("getting tile info");
        window.electronAPI.getTileInfo();
    } else if (pageIndex == pageIndexes.Summary){
        window.electronAPI.getSummaryInfo(BMSID);
        console.log("summary page");
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
        batteryPowerStr = (power/1000).toFixed(1) + " kw";
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
                    <div class="col-2 bat-inf">${battery.power}</div>
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
    pageIndex = pageIndexes.Summary;
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



