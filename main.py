from dustkiller import Room, Box, User, DustKiller
from fastapi import FastAPI
import uvicorn
# from parse import get_input_data
from random import randint as rnd
import asyncio
# from ML import Model


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped
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


@background
def activate_dust():
    print("work")
    global dimas
    global dustKiller
    dimas.create_schedule(dustKiller, [12, 16, 18], start_now=True)
    dimas.activate_device(dustKiller)
activate_dust()
app = FastAPI()




@app.get("/")
async def root():
    return {"status":"ok"}

@app.get("/params")
async def get_params():
    return {
                    'voice':dustKiller.voice,
                    'name':dustKiller.name,
                    'speed':dustKiller.speed,
                    'x':dustKiller.x,
                    'y':dustKiller.y,
                    'now_room':dustKiller.now_room,
                    # 'rooms':dustKiller.rooms,
                    'start_now':dustKiller.start_now,
                    'do_clean':dustKiller.do_clean,
                    'schedule':dustKiller.schedule,
                    'battery_level':dustKiller.battery_level,
                    'dust_bag':dustKiller.dust_bag,
                    'need_clean_bug':dustKiller.need_clean_bug
                    }
@app.get("/go_to_charge")
async def run_task_1():
    dustKiller.go_to_charge()
    return {"status":"ok"}

@app.get("/scan_rooms")
async def run_task_2():
    dustKiller.scan_rooms()
    return {"status":"ok"}

@app.get("/start_clean")
async def start_clean():
    dustKiller.start_clean()
    return {"status":"ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
