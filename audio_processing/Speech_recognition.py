import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr
from openAiFunctions.anotador import anotador

r = sr.Recognizer()


def speech_recognition_interviewer(room,questions,interviewers_texts_by_room,audio_data,userName,interviewed_text_by_room):
    try:
        text = speech_recognition(audio_data)
        if room:
            if room not in interviewers_texts_by_room:
                interviewers_texts_by_room[room] = {f"{userName}":{"Interviewer": [],"Interviewer_accumulated_text":""},"currentQuestion":False}
            interviewers_texts_by_room[room][userName]["Interviewer_accumulated_text"] = interviewers_texts_by_room[room][userName]["Interviewer_accumulated_text"] + " " + text
            question = anotador(interviewers_texts_by_room[room][userName]["Interviewer_accumulated_text"], questions, os.getenv("OPENAI_API_KEY"))
            if question:
                interviewers_texts_by_room[room][userName]["Interviewer"].append(question[1])
                interviewers_texts_by_room[room]["currentQuestion"] = question[1]
                interviewers_texts_by_room[room][userName]["Interviewer_accumulated_text"] = ""
                if interviewers_texts_by_room[room]["currentQuestion"] != False and question[1] != interviewers_texts_by_room[room]["currentQuestion"]:
                    interviewed_text_by_room[room]["Interviewed"].append(interviewed_text_by_room[room]["Interviewed_accumulated_text"])
                    interviewed_text_by_room[room]["Interviewed_accumulated_text"] = ""
            else:
                return None
    except Exception as e:
        return
def speech_recognition_interviewed(room,interviewed_text_by_room,audio_data):
    try:
        text = speech_recognition(audio_data)
        if room:
            if room not in interviewed_text_by_room:
                interviewed_text_by_room[room] = {"Interviewed": [],"Interviewed_accumulated_text":""}
            interviewed_text_by_room[room]["Interviewed_accumulated_text"] = interviewed_text_by_room[room]["Interviewed_accumulated_text"] + " " + text
            
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
