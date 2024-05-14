import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr
from openAiFunctions.anotador import anotador

r = sr.Recognizer()


async def speech_recognition_interviewer(room,questions,texts_by_room,audio_data):
    try:
        text = speech_recognition(audio_data)
        if room:
            if room not in texts_by_room:
                texts_by_room[room] = {"Interviewer": [],"Interviewer_accumulated_text":"", "Interviewed": [],"Interviewed_accumulated_text":""}
            texts_by_room[room]["Interviewer_accumulated_text"] = texts_by_room[room]["Interviewer_accumulated_text"] + " " + text
            question = anotador(texts_by_room[room]["Interviewer_accumulated_text"], questions, os.getenv("OPENAI_API_KEY"))
            if question:
                texts_by_room[room]["Interviewer"].append(question[1])
                texts_by_room[room]["Interviewer_accumulated_text"] = ""
            else:
                return None
    except Exception as e:
        return
async def speech_recognition_interviewed(room,questions,texts_by_room,audio_data):
    try:
        text = speech_recognition(audio_data)
        if room:
            if room not in texts_by_room:
                texts_by_room[room] = {"Interviewer": [],"Interviewer_accumulated_text":"", "Interviewed": [],"Interviewed_accumulated_text":""}
            texts_by_room[room]["Interviewed_accumulated_text"] = texts_by_room[room]["Interviewed_accumulated_text"] + " " + text
            
    except Exception as e:
        return
def speech_recognition(audio_data):
    try:
        temp_audio_fd, temp_audio_path = tempfile.mkstemp()
        with os.fdopen(temp_audio_fd, 'wb') as temp_audio_file:
            temp_audio_file.write(audio_data)
        audio = AudioSegment.from_file(temp_audio_path)
        audio.export(temp_audio_path, format="wav")

        with sr.AudioFile(temp_audio_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='es-ES')
        os.remove(temp_audio_path)
        return text
    except Exception as e:
        return None
