# Solar Data Receiver
MQTT listener designed to receive and store incoming NodeRenogy data from a solar stationary node. A timestamp is also appended to the incoming data before it is saved. 

## Dependencies
### System-level Dependencies (remember to update and upgrade first!):

**MQTT**
- To install MQTT on a Raspberry Pi, follow the [tutorial linked here](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/).

**Python3**
- `sudo apt install python3`

**Python3-pip**
- `sudo apt install python3-pip`
 
### Python Dependencies:

**Paho MQTT**
- `pip install paho-mqtt`

## Running the code
This application is intended to run as a background service. This means that systemctl should handle executing the code on boot. To check in on the status of the program, run:

`sudo systemctl status mqtt_solar_receive.service`

The output logs of the mqtt_solar_receive service is located in the logs/ directory. A new log file is generated when the service is reset and will be labelled with the current date. An example log file may be named: `mqtt_solar_receive-20221220.log`

## Viewing the saved data
This application is designed to only save data from the following set of topics:
 - NodeRenogy/ccrisolar1/device
 - NodeRenogy/ccrisolar2/device
 - NodeRenogy/ccrisolar1/state
 - NodeRenogy/ccrisolar2/state

Be sure that your NodeRenogy instance is publishing MQTT data over those topics mentioned above, otherwise, it will not be saved.

To view the saved JSON data, check out the data/ directory. There should be seperate JSON files for each device (ccrisolar1 or ccrisolar2) and data source (either state or device). There are also sample data files. The naming convention for each file is as follows:
 - `deviceName + '-' + dataSource + '-data.json'`

For example, if you are looking for the state data from ccrisolar2, expect to find that data in `ccrisolar2-state-data.json`

As mentioned in the [NodeRenogy repo](https://github.com/mickwheelz/NodeRenogy#publishing-to-mqtt), the `<topic>/device` and `<topic>/state` subtopics contain different information about the solar charge controller. Keep this in mind when reading over the JSON data files.
