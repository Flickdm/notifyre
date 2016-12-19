# notipyre

The purpose of this project is to create a open-source notification system for those with hearing loss that can be built cheaply with little linux experience.

This project is still under development and is subject to change.

Purchase List:
 * Android (Android is currently being developed, Iphone support soon)
 * Raspberry Pi 3 ~ $35 (may attempt this with pi zero + bluetooth module)
 * RGB LED Strip  ~ $13
 * Custom equipment (with writeup)

Prerequisites:
 * Basic Linux (Eventually this could be an image)
 * Python knowledge

 ##Installation

 install bluez
 ```
 sudo apt-get install bluetooth bluez
 ```

 install pyBluez
 ```
 sudo apt-get install bluez python-bluez
 ```

 ##Setup your Raspberry Pi

 Make your device discoverable
 ```
 sudo hciconfig hci0 piscan
 ```
 Configure your device name
 ```
 sudo hciconfig hci0 name 'Device Name'
 ```
