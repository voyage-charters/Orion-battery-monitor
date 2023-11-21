'use strict';

const {app, BrowserWindow, ipcMain} = require('electron');
const electronReload = require('electron-reload');
const path = require('path');
const globals = require('./globals')
const { spawn } = require("child_process");
var pyshell =  require('python-shell');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.





// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
function handleSetTitle (event, title) {
  
  const webContents = event.sender;
  const win = BrowserWindow.fromWebContents(webContents);
  console.log(`The thing is now done in main.js with title = ${title}`  );
  
  // win.setTitle(title);
}
function runPythonScript (){
  console.log("runPythonScript");
  let python = spawn('python', [path.join(app.getAppPath(), '..', 'python_scripts/main.py')])
  // let py = spawn('python', ['./python_scripts/main.py']);
  // py.stdout.on('data', data => console.log('data : ', data.toString()))
}



function createWindow () {

  const mainWindow = new BrowserWindow({
    autoHideMenuBar: true,
    // frame: false,
    icon: __dirname + './assets/images/voyage-logo-color-dark.ico',
    webPreferences: {
      // devTools: true,
      
      nodeIntegration: true,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
  }
  });
  mainWindow.maximize();
  mainWindow.loadFile('index.html')
  mainWindow.webContents.on('did-finish-load', () => {
    const pythonProcess = spawn('python', [path.join(app.getAppPath(), 'python_scripts/main.py')])
    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python script output: ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
      console.error(`Error from Python script: ${data}`);
    });
  });
}



app.whenReady().then(() => {
  ipcMain.handle('set-title', handleSetTitle)
  ipcMain.handle('start-python',runPythonScript)
  createWindow()
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('before-quit', () => {
  // Terminate the Python process before quitting the app
  if (pythonProcess) {
    pythonProcess.kill();
  }
});


// Quit when all windows are closed.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  
  }
})

