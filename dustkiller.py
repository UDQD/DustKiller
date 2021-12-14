import datetime
import random
import threading
import datetime
import time


class Box:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Room:
    def __init__(self, name: str, box: Box, connected_rooms: list = [], square=0):
        self.name = name
        self.box: Box = box
        self.connected_rooms = connected_rooms
        self.square = square


class DustKiller:
    def __init__(self, rooms):
        self.voice = "Default"
        self.name = "Dustkiller3000"
        self.speed = 1
        self.x = 0
        self.y = 0
        self.now_room = "На зарядке"
        self.rooms = rooms
        self.start_now = False
        self.do_clean = False
        self.schedule = []
        self.battery_level = random.randint(0, 100)
        # self.dust_bag = 98.9
        self.dust_bag = 0
        self.need_clean_bug = False

    def start(self):
        if (self.battery_level < 15):
            self.log("Пожалуйста, поставь меня на зарядку")
            self.go_to_charge()
        else:
            self.log("Начал сканировать")

        self.scan_rooms()
        self.log("Начинаю проверять расписание")
        self.start_check_schedule()

    def scan_rooms(self):
        for room in self.rooms:
            self.now_room = room.name
            self.move_over_room(room)
            room.square = self.find_square(room)
            self.log(f'Площадь комнаты "{room.name}" = {room.square}')
            if(self.rooms[-1] != room):
                self.go_to_another_room()
        self.log("📱Сканирование завершено")

    def start_check_schedule(self):
        if(datetime.time.hour in self.schedule):
            self.start_clean()
        elif(self.start_now == True):
            self.start_clean()
            self.start_now = False
        else:
            self.log("Уборка на сейчас не запланирована.")
        threading.Timer(random.randint(0, 3),
                        self.start_check_schedule).start()

    def move_over_room(self, room: Room):
        self.move(0, 0)
        self.move(room.box.height, 0)
        self.move(room.box.width, room.box.height)
        self.move(room.box.width, 0)

    def go_to_another_room(self):
        self.log("🚶‍♀️Иду в другую комнату")

    def find_square(self, room: Room):
        return room.box.width * room.box.height

    def create_schedule(self, schedule, start_now):
        self.start_now = start_now
        self.schedule = schedule
        self.log("Расписание создано")

    def start_clean(self):
        self.log("♻ Начата уборка")
        for room in self.rooms:
            self.now_room = room.name
            self.move_over_room(room)
            self.log(f'♻ Комната "{room.name}" успешна очищена')
            if(self.rooms[-1] != room):
                self.go_to_another_room()
        self.log("♻ Уборка завершена")
        self.go_to_charge()

    def go_to_charge(self):
        self.now_room = "На зарядке"
        self.log("Иду на зарядку")
        self.log("⚡ Заряжаюсь")
        self.battery_level = 100
        self.log(f"Уровень батареи {self.battery_level}%")

    def move(self, x, y):
        self.x = x
        self.y = y
        time.sleep(random.randint(0, 2))
        self.check_battery()
        time.sleep(random.randint(0, 2))
        self.check_dust_bag()
        self.log(f"Я передвинулся на x: {self.x}, y: {self.y}")
        time.sleep(random.randint(0, 2))

    def check_battery(self):
        self.battery_level = self.battery_level-1
        if(self.battery_level < 15):
            self.go_to_charge()
        self.log(f"Уровень батареи {self.battery_level}%")

    def check_dust_bag(self):
        self.dust_bag = self.dust_bag+0.3
        self.log(f"Наполненность мешка с пылью {self.dust_bag}%")
        if(self.dust_bag > 90):
            self.need_clean_bug = True
            self.log("❌ ПОЖАЛУЙСТА, очистите мешок с пылью")
            self.log("❌ Иначе я не смогу работать")
            input()
            self.need_clean_bug = False
            self.dust_bag = 0
            self.log("✅ Мешок очищен, спасибо, продолжаю работать")

    def log(self, text):
        now = datetime.datetime.now()
        print(f'[{now.strftime("%H:%M:%S")}] {self.name}: {text}')


class User():
    def __init__(self, name):
        self.name = name

    def activate_device(self, device):
        print(f'{self.name}: Я активировал устройство {device.name}')
        device.start()

    def create_schedule(self, device, schedule, start_now=False):
        print(f'{self.name}: Задал расписание на {device.name}')
        device.create_schedule(schedule, start_now)


def start_dust_killer():
    living_room = Room("Жилая комната", Box(4, 4),)
    kitchen = Room("Кухня", Box(2, 2), )
    corridor = Room("Коридор", Box(1, 3),
                    connected_rooms=[living_room, kitchen])
    kitchen.connected_rooms = [corridor]
    living_room.connected_rooms = [corridor]
    rooms = [living_room, corridor, kitchen, ]

    dimas = User("Дмитрий")

    dustKiller = DustKiller(rooms)

    dimas.create_schedule(dustKiller, [12, 16, 18], start_now=True)
    dimas.activate_device(dustKiller)


# start_dust_killer()
