from dustkiller import *
from subs_dust_killer import dustKiller
from fastapi import FastAPI
import uvicorn
# from parse import get_input_data
from random import randint as rnd
# from ML import Model

app = FastAPI()

def make_json():
    global dustKiller
    all_params = {
                    'voise':dustKiller.voice,
                    'name':dustKiller.name,
                    'speed':dustKiller.speed,
                    'x':dustKiller.x,
                    'y':dustKiller.y,
                    'now_room':dustKiller.now_room,
                    'rooms':dustKiller.rooms,
                    'start_now':dustKiller.start_now,
                    'do_clean':dustKiller.do_clean,
                    'schedule':dustKiller.schedule,
                    'battery_level':dustKiller.battery_level,
                    'dust_bag':dustKiller.dust_bag,
                    'need_clean_bug':dustKiller.need_clean_bug
                    }
    return all_params

@app.get("/")
async def root():
    return make_json()

@app.get("/page_1")
async def root_2():
    # return str(model.nn.predict(get_input_data())) #"qwdqwdqwdqdwqd"#{"Hello": "W1"}
    return "this is pythonwdwdw"

if __name__ == "__main__":
    # model = Model()
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
