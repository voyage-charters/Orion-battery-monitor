# Orion-battery-monitor

## Install Raspberry Pi OS (64-bit) 

## Update Raspberry Pi firmware
```
sudo rpi-update
```
## Update Raspberry Pi OS
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get autoremove
sudo apt-get autoclean
sudo apt-get clean
```
## Install WAVESHARE 2-CH_CAN_FD_HAT

### Enable I2C
```
sudo raspi-config
``` 
Choose Interfacing Options -> I2C -> Yes.

### Install bcm2835 drivers
install wiringpy

Run in dual SPI mode
copy following to /boot/config.txt
    dtparam=spi=on
    dtoverlay=spi1-3cs
    dtoverlay=mcp251xfd,spi0-0,interrupt=25
    dtoverlay=mcp251xfd,spi1-0,interrupt=24
     
For a more in-depth installation guide read the [Waveshare wiki](https://www.waveshare.com/wiki/2-CH_CAN_FD_HAT)

## Install NodeJS
    https://www.instructables.com/Install-Nodejs-and-Npm-on-Raspberry-Pi/
## Install NodeJS packages 

## Install Python3 packages
Run with sudo to install for all users otherwise it wont work at startup
``` 
sudo pip3 install python-can --break-system-packages
sudo pip3 install flask --break-system-packages
sudo pip3 install flask-cors --break-system-packages
``` 

## Configure a silent boot

### Edit the config.txt file

``` 
sudo nano /boot/config.txt
```
Disable rainbow splash screen

add "disable_splash=1"
add "loglevel=3"
## Disable Logo
sudo nano /boot/cmdline.txt
add "logo.nologo" 
## Mute kernel logs
sudo nano /boot/config.txt
add "loglevel=3"
## Remove blinking curser
    sudo nano /boot/cmdline.txt
    - add "vt.global_cursor_default=0"
## Change boot logo 
    cd /usr/share/plymouth/themes/pix
    sudo mv splash.png splash_default.png

    - copy new splash.png to /home/voyage/
    cd /home/voyage/
    sudo cp splash.png /usr/share/plymouth/themes/pix

## Download Repo and build app
    git clone https://github.com/voyage-charters/Orion-battery-monitor
    cd Orion-battery-monitor
    - Check that the python app is running without error
    python python_scripts/main.py
    - Fix missing packages if needed
    - exit the pythong app
    - run the electron app 
    npm start 
    - Fix missing module errors if needed 
    - Check that it starts up properly and displays the batteries
    - Exit the app
    - build the executable file 
    npm run make


## Run Electron app at startup 

######### DONT NEED THIS ############   
Run python script at startup
    edit /etc/rc.local
    - add following line before exit 0
    bash -c '/usr/bin/python3 /home/voyage/Orion-battery-monitor/python_scripts/main.py > /home/voyage/mylog.log 2>&1' &
######### DONT NEED THIS ############

## Update the app 
    cd Orion-battery-monitor
    git stash
    git pull 
    npm run make 



