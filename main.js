'use strict';

const {app, BrowserWindow, ipcMain} = require('electron');
const electronReload = require('electron-reload');
const path = require('path');
const globals = require('./globals')

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
}

app.whenReady().then(() => {
  ipcMain.on('set-title', handleSetTitle)
  createWindow()
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})


// Quit when all windows are closed.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  
  }
})
