from mqtt_client import MQTTClient
import time

"""Network Class for MQTT Communication between client and server."""


class Network:
    def __init__(self, hostname: str, user: str):
        """Constructor method."""
        self.hostname = hostname
        self.user = user
        self.mqtt = MQTTClient(self.hostname, self.user)

    def disconnect(self):
        """Close the network connection."""
        self.mqtt.loop_stop()
        self.mqtt.disconnect()

    def connect(self, port=1883):
        """Connect to the network interface."""
        self.mqtt.connect(port)
        self.mqtt.loop_start()

    def receive(self, user=None) -> str:
        """Receive a message and return the string."""
        if user is None:
            user = self.user
        self.mqtt.subscribe(user)
        print("Waiting for a message...")
        
        # This is a funny way to say while true.
        cmd_received = False
        while not cmd_received:
            time.sleep(0.1)  # Delay to throttle tight loop
            if len(self.mqtt.msg_queue) > 0:
                # Grab the message from the queue
                incoming_msg = self.mqtt.msg_queue.pop()
                return incoming_msg

    def send(self, receiver: str, msg: str):
        """Send a message, return true if successful."""
        self.mqtt.publish(receiver, msg, qos=2)
