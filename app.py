import socketio
from aiohttp import web
import os
import speech_recognition as sr
import tempfile
from pydub import AudioSegment

# Crear un servidor Socket.IO con política CORS
sio = socketio.AsyncServer(cors_allowed_origins='*')
r = sr.Recognizer()


# Crear una aplicación web para el servidor
app = web.Application()
sio.attach(app)

# Definir el evento de conexión
@sio.event
def connect(sid, environ):
    print('connect ', sid)

# Definir el evento de desconexión
@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def room_join(sid, data):
    email = data.get('email')
    room = data.get('room')
    nombre = data.get('nombre')
    rol = data.get('rol')

    await sio.enter_room(sid, room)
    await sio.emit('user_joined', {'email': email, 'id': sid}, room=room)
    await sio.emit('room_join', data, room=sid)
    print(f'{nombre} se ha unido a la sala {room}')

texts_by_room = {}

@sio.event
async def data(sid, audio_stream):
    # Crear un archivo temporal para guardar el stream de audio
    temp_audio_fd, temp_audio_path = tempfile.mkstemp()
    with os.fdopen(temp_audio_fd, 'wb') as temp_audio_file:
        temp_audio_file.write(audio_stream)

    # Convertir el audio a formato WAV
    audio = AudioSegment.from_file(temp_audio_path)
    audio.export(temp_audio_path, format="wav")

    # Procesar el audio con speech_recognition
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='es-ES')

    # Borrar el archivo temporal
    #os.remove(temp_audio_path)

    # Obtener la sala a la que pertenece el usuario
    rooms = sio.rooms(sid)
    room = rooms[0] if rooms else None

    if room:
        # Si la sala no está en el diccionario, agregarla
        if room not in texts_by_room:
            texts_by_room[room] = []

        # Almacenar el texto con el identificador del socket en el array de la sala
        texts_by_room[room].append({sid: text})
        print(f'[{room}] {sid}: {text}')

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
# Si este archivo se ejecuta directamente, iniciar el servidor
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8000)