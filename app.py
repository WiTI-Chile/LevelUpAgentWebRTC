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



app = web.Application()
sio.attach(app)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def room_join(sid, data):
    email = data.get('email')
    room = data.get('room')
    nombre = data.get('nombre')
    typeOfUser = data.get('typeOfUser')

    await sio.enter_room(sid, room)
    await sio.emit('user_joined', {'email': email, 'id': sid}, room=room)
    await sio.emit('room_join', data, room=sid)
    print(f'{nombre} se ha unido a la sala {room}')

@sio.event
async def data(sid, data):
    try:
        await process_audio(sio,sid,data,questions,json_questions)
    except Exception as e:
        return

@sio.event
async def user_call(sid, data):
    to = data.get('to')
    offer = data.get('offer')
    await sio.emit('incomming_call', {'from': sid, 'offer': offer}, room=to)

@sio.event
async def call_accepted(sid, data):
    to = data.get('to')
    ans = data.get('ans')
    await sio.emit('call_accepted', {'from': sid, 'ans': ans}, room=to)

@sio.event
async def peer_nego_needed(sid, data):
    to = data.get('to')
    offer = data.get('offer')
    await sio.emit('peer_nego_needed', {'from': sid, 'offer': offer}, room=to)

@sio.event
async def peer_nego_done(sid, data):
    to = data.get('to')
    ans = data.get('ans')
    await sio.emit('peer_nego_final', {'from': sid, 'ans': ans}, room=to)

@sio.event
async def end_call(sid, data):
    to = data.get('to')
    await sio.emit('end_call', {'from': sid}, room=to)

@sio.event
async def user_toggleCamera(sid, data):
    to = data.get('to')
    await sio.emit('user_toggleCamera', {'from': sid}, room=to)
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8000)