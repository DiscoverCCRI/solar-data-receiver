from mqtt_solar_receive import DataReceiver

def main():
    # Init vars
    hostname = "localhost"
    client = "supervisor"
    topic = "NodeRenogy/+/+"

    print("--------------------------")
    print("|   Start Data Receive   |")
    print("--------------------------")
    run_data_receive(hostname, client, topic)


def run_data_receive(hostname, client, topic):
    data_receiver = DataReceiver(hostname, client, topic)
    data_receiver.receive_and_store()


if __name__ == "__main__":
    main()