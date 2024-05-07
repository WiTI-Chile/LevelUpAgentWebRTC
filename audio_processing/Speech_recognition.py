import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr
from openAiFunctions.anotador import anotador

r = sr.Recognizer()

texts_by_room = {}
async def speech_recognition(sio,sid,data,questions):
    try:
        audio_data = data.get('audio')
        typeOfUser = data.get('typeOfUser')
        # Crear un archivo temporal para guardar el stream de audio
        temp_audio_fd, temp_audio_path = tempfile.mkstemp()
        with os.fdopen(temp_audio_fd, 'wb') as temp_audio_file:
            temp_audio_file.write(audio_data)

        # Convertir el audio a formato WAV
        audio = AudioSegment.from_file(temp_audio_path)
        audio.export(temp_audio_path, format="wav")

        # Procesar el audio con speech_recognition
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='es-ES')

        # Obtener la sala a la que pertenece el usuario
        rooms = sio.rooms(sid)
        room = rooms[0] if rooms else None

        if room:
            # Si la sala no está en el diccionario, agregarla
            if room not in texts_by_room:
                texts_by_room[room] = {"Interviewer": [], "Interviewed": []}
            # Almacenar el texto con el identificador del socket en el array de la sala
            texts_by_room[room][typeOfUser].append(text)
            last_index = len(texts_by_room[room][typeOfUser]) - 1
            # ENVIAR EL TEXTO AL ANOTADOR
            # SI NO SE DETECTA UNA PREGUNTA SE CONCATENA EL TEXTO ACTUAL CON EL ANTERIOR
            question = anotador(texts_by_room[room][typeOfUser][last_index], questions, os.getenv("OPENAI_API_KEY"))
            if not question:
                # concatenar el texto actual con el anterior
                concatenated_text = ""
                for i in range (3):
                    concatenated_text = texts_by_room[room][typeOfUser][last_index-(i+1)] + concatenated_text
                    question = anotador(concatenated_text, questions, os.getenv("OPENAI_API_KEY"))
                    if question:
                        break
            if question:
                print(question)
            print(texts_by_room)
        os.remove(temp_audio_path)
    except Exception as e:
        return
