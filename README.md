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

### Enable I2C Interface

    sudo raspi-config
    Choose Interfacing Options -> I2C -> Yes.

Reboot Raspberry Pi

### Install bcm2835 
Open the terminal and run the commands below to install the bcm2835 library.

    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
    tar zxvf bcm2835-1.60.tar.gz 
    cd bcm2835-1.60/
    sudo ./configure
    sudo make
    sudo make check
    sudo make install
    # For more information, please refer to the official website: http://www.airspayce.com/mikem/bcm2835/


### Install wiringpy

    #Open the Raspberry Pi terminal and run the following command
    cd
    sudo apt-get install wiringpi
    #For Raspberry Pi systems after May 2019 (earlier than that can be executed without), an upgrade may be required:
    wget https://project-downloads.drogon.net/wiringpi-latest.deb
    sudo dpkg -i wiringpi-latest.deb
    gpio -v
    # Run gpio -v and version 2.52 will appear, if it doesn't it means there was an installation error

    # Bullseye branch system using the following command:
    git clone https://github.com/WiringPi/WiringPi
    cd WiringPi
    . /build
    sudo gpio -v
    # Run gpio -v and version 2.70 will appear, if it doesn't it means there was an installation error

### Install Python libraries

    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install python3-pil
    sudo apt-get install python3-numpy
    sudo pip3 install RPi.GPIO
    sudo pip3 install spidev 
    sudo pip3 install python-can

### Configure the device(dual SPI mode)

Insert the module into Raspberry Pi, and then modify the config.txt file:

    sudo nano /boot/config.txt

Add the following commands at the last line:

    dtparam=spi=on
    dtoverlay=spi1-3cs
    dtoverlay=mcp251xfd,spi0-0,interrupt=25
    dtoverlay=mcp251xfd,spi1-0,interrupt=24
     
For a more in-depth installation guide read the [Waveshare wiki](https://www.waveshare.com/wiki/2-CH_CAN_FD_HAT)

## Install NodeJS
    https://www.instructables.com/Install-Nodejs-and-Npm-on-Raspberry-Pi/

## Install Python3 packages
Run with sudo to install for all users otherwise it wont work at startup

    sudo pip3 install python-can --break-system-packages
    sudo pip3 install flask --break-system-packages
    sudo pip3 install flask-cors --break-system-packages

### Install NodeJS packages 

## Download Repo and build app

    git clone https://github.com/voyage-charters/Orion-battery-monitor
    cd Orion-battery-monitor
    - Check that the python app is running without error
    python python_scripts/main.py
    - Fix missing packages if needed and try again.
    - exit the pythong app(ctrl+c).
    - run the electron app 
    npm start 
    - Fix missing module errors if needed.
    - Check that it starts up properly and displays the batteries.
    - Exit the app(ctrl+c).
    - build the executable file 
    npm run make

## Run Electron app at startup

This method relies on running the executable file built in the previous step. 

Edit the desktop autostart file

    cd /etc/xdg/autostart/
    sudo touch display.desktop
    sudo nano /etc/xdg/autostart/display.desktop

Add the following lines

    [Desktop Entry]
    Name=OrionMonitor
    Exec=/home/voyage/Orion-battery-monitor/out/orion_battery_monitor-linux-arm64/orion_battery_monitor

Reboot the device to test. 

### (Optional) Autostart without build


## Configure a silent boot

### Edit the config.txt file

``` 
sudo nano /boot/config.txt
```
Disable rainbow splash screen

add "disable_splash=1"
add "loglevel=3"
### Edit the cmdline.txt file
All the configurations in this file are on one line so just make sure to append to the end of that line.
    sudo nano /boot/cmdline.txt
To disable the logo, add:
    logo.nologo
To remove the blinking curser, add:
    vt.global_cursor_default=0

## Change boot logo 
Copy an image with the name splash.png to your root folder. In this case the root folder is '/home/voyage/.' Proceed to replace the splash image in the default theme to your own image:

    cd /usr/share/plymouth/themes/pix
    - rename the original splash image.
    sudo mv splash.png splash_default.png
    - copy new splash.png to /home/voyage/
    cd /home/voyage/
    sudo cp splash.png /usr/share/plymouth/themes/pix


## Update the app 
The app can be updated by simply downloading the git repo again and building the app. No need to update the autostart files.

    cd Orion-battery-monitor
    git stash
    git pull 
    npm run make 



