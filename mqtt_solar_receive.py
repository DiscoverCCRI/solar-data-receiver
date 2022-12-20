from network import Network
import logging
import json
from datetime import datetime
import os.path

### To enable debug logging, uncomment the line below
logging.basicConfig(level=logging.DEBUG)

VALID_DATA_SOURCES = ['device', 'state']
VALID_DEVICE_NAMES = ['ccrisolar1', 'ccrisolar2']

# Define callback function for MQTT message callback
def on_message(client, userdata, message):
    """Callback function for receiving messages."""
    msg = "{} {}".format(message.topic, message.payload.decode("utf-8"))

    # Capture the message in the global Network Class queue
    network.mqtt.msg_queue.append(msg)


def outputToJSON(dataToAdd, fileName):
    jsonData = []
    dataDir = './data/'
    dataDirExists = os.path.isdir(dataDir)

    if dataDirExists:
        try:
            # Open the existing file
            jsonFile = open(dataDir+fileName, "r+")
            jsonData = json.load(jsonFile)

        except FileNotFoundError:
            print(f"[+] Creating {dataDir+fileName}...")
            jsonFile = open(dataDir+fileName, "w")
    
    # At this point it can be assumed that the data file exists, so we can read from and add to it.
    jsonData.append(dataToAdd)

    jsonFile.seek(0)
    json.dump(jsonData, jsonFile, indent=4, separators=(',',': '))
    jsonFile.truncate()
    jsonFile.close()


class DataReceiver:
    # TODO: Secure MQTT can help with security.
    def __init__(self, hostname, client, topic):
        self.hostname = hostname
        self.client = client
        self.topic = topic


    def receive_and_store(self):
        # Declare global network for on_message to access the message queue
        global network

        # Initialize network instance for mqtt
        network = Network(self.hostname, self.client)
        network.mqtt.client.on_message = on_message

        logging.debug("[+] Request to connect to MQTT Broker...")
        network.connect()
        
        while True:
            # Retrieve incoming messages, store message contents into
            # topic/payload variables.
            received_msg = network.receive(self.topic).split(" ")
            received_topic = received_msg[0]
            received_payload = " ".join(received_msg[1:])
            logging.debug(f"[+] Topic: {received_topic}")
            logging.debug(f"[+] Payload: {received_payload}")

            try:
                # Use topic to find/create appropriate file to save data
                device_name = received_topic.split("/")[1]
                data_source = received_topic.split("/")[2]

                # Since this is running on 1883, we want to validate the incoming message topics
                # as an extra precaution
                if device_name not in VALID_DEVICE_NAMES:
                    raise Exception("[-] Invalid device name in topic, skipping...\n")

                if data_source not in VALID_DATA_SOURCES:
                    raise Exception("[-] Invalid data source in topic, skipping...\n")

                file_name = device_name + '-' + data_source + '-data.json'

                # Convert received payload into a dictionary
                json_payload = json.loads(received_payload)
                json_payload["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Insert the data into a file
                logging.debug(f"[+] Data to be inserted into {file_name}: {json_payload}\n")
                outputToJSON(json_payload, file_name)
            
            except Exception as error_message:
                logging.debug(error_message)
                continue
