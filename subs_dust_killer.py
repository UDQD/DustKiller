# python 3.8.3
import csv
import datetime
import os
import json
import random
import threading
from paho.mqtt import client as mqtt_client
import json
from dustkiller import Room, Box, User, DustKiller
import asyncio


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped


class BoxConnect:
    def __init__(self, broker: str, port: int, name: str, password: str, topics: list, timer: int, is_debug: bool, dust_killer: DustKiller):
        # generate client ID with pub prefix randomly
        self.client_id = f'python-mqtt-{random.randint(0, 100)}'
        self.broker = broker
        self.port = port
        self.name = name
        self.password = password
        self.topics = topics
        self.timer = timer
        self.received_data_json = {}
        self.received_data_csv = {"time": "", "name": "", "value": ""}
        self.is_debug = is_debug
        self.dust_killer: DustKiller = dust_killer
        self.values = [
            [-1, self.dust_killer.dust_bag],
            [-1, self.dust_killer.battery_level],
            [True, self.dust_killer.need_clean_bug],
            ["", self.dust_killer.now_room],
        ]
        self.run_services()

    def run_services(self):
        self.timer_to_save()
        if not self.is_debug:
            self.client: mqtt_client = self.connect()
            self.subscribe()
            self.client.loop_forever()
        else:
            print('===')
            print("Connected to MQTT Broker!")
            self.emulate_connect()

    def connect(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.username_pw_set(self.name, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self):
        print('===')
        for topic in topics:
            self.client.subscribe(topic)
        self.client.on_message = self.on_message

    def on_message(self, msg):
        print(
            f"Received `{msg}` from `{msg.topic}` topic")
        for topic in self.topics:
            if msg.topic == topic:
                self.transform_data(msg.topic, msg.payload.decode())

    def transform_data(self, device_topic, payload):
        # get name of device
        device_name = device_topic.split("/")[-1]
        # json
        self.received_data_json[device_name] = payload
        self.received_data_json["time"] = str(datetime.datetime.now())
        # csv
        self.received_data_csv["time"] = str(datetime.datetime.now())
        self.received_data_csv["name"] = device_name
        self.received_data_csv["value"] = payload
        BoxSave.csv(self.received_data_csv)

    def timer_to_save(self):
        # restart timer
        BoxSave.json(self.received_data_json)
        threading.Timer(self.timer, self.timer_to_save).start()

    def emulate_message(self, payload, device_topic):

        print(
            f"Received `{payload}` from `{device_topic}` topic")
        for topic in self.topics:
            if topic == device_topic:
                self.transform_data(device_topic, payload)

    def emulate_connect(self):
        rnd_index = random.randint(0, len(self.topics)-1)
        value_device = [
            [-1, self.dust_killer.dust_bag],
            [-1, self.dust_killer.battery_level],
            [True, self.dust_killer.need_clean_bug],
            ["", self.dust_killer.now_room],
        ]
        if(self.values[rnd_index][0] != value_device[rnd_index][1]):

            self.emulate_message(
                device_topic=topics[rnd_index],
                payload=value_device[rnd_index][1])
            self.values[rnd_index][0] = value_device[rnd_index][1]

        threading.Timer(0, self.emulate_connect).start()


class BoxSave:

    @ staticmethod
    def json(dict: dict):
        NAME_JSON = 'data.json'
        print("Saved data to json..")
        print(dict)
        # save json
        dump = json.dumps(dict)
        with open(NAME_JSON, 'w') as file:
            file.write(dump)

    @ staticmethod
    def csv(dict: dict):
        NAME_CSV = 'data.csv'
        already_saved = os.path.isfile(NAME_CSV)
        # save csv
        if not already_saved:
            with open(NAME_CSV, 'w', encoding="utf8") as f:
                w = csv.DictWriter(f, dict.keys())
                w.writeheader()
                w.writerow(dict)
        else:
            with open(NAME_CSV, 'a', encoding="utf8") as f:
                w = csv.DictWriter(f, dict.keys())
                w.writerow(dict)


topics = [
    "/dustkiller/bag",
    "/dustkiller/battery",
    "/dustkiller/needclean",
    "/dustkiller/room",
]
living_room = Room("Жилая комната", Box(4, 4),)
kitchen = Room("Кухня", Box(2, 2), )
corridor = Room("Коридор", Box(1, 3),
                connected_rooms=[living_room, kitchen])
kitchen.connected_rooms = [corridor]
living_room.connected_rooms = [corridor]
rooms = [living_room, corridor, kitchen, ]

dimas = User("Дмитрий")

dustKiller = DustKiller(rooms)


@ background
def activate_dust():
    print("work")
    global dimas
    global dustKiller
    dimas.create_schedule(dustKiller, [12, 16, 18], start_now=True)
    dimas.activate_device(dustKiller)


def start_sub():
    print("work2")
    global topics
    global dustKiller
    box_saver = BoxConnect(broker='192.168.2.22',
                           port=1883,
                           name='user',
                           password='123123',
                           topics=topics,
                           timer=5,
                           is_debug=True, dust_killer=dustKiller)


if __name__ == '__main__':
    activate_dust()
    start_sub()
