import socketio
from aiohttp import web
from audio_processing.Index import process_audio
import os
from openAiFunctions.estructura import json_to_dataframe
from dotenv import load_dotenv
import json
load_dotenv()

texts_by_room = {}
questions = ""
json_questions = {}
with open("questions.json", "r",encoding="UTF-8") as f:
    questions = str(f.read())
    json_questions = json.loads(questions)
questions = json_to_dataframe(questions,os.getenv("OPENAI_API_KEY"))

sio = socketio.AsyncServer(cors_allowed_origins='*')


users_connected = {}
app = web.Application()
sio.attach(app)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
        

@sio.event
async def data(sid, data):
    try:
        process_audio(data,questions,json_questions)
    except Exception as e:
        return

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8000)