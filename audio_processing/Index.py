from audio_processing.Speech_recognition import speech_recognition_interviewer,speech_recognition_interviewed
import copy
from openAiFunctions.opciones import get_opcion
import os

texts_by_room = {}
async def process_audio(sio,sid, data, questions,json_questions):
    typeOfUser = data.get('typeOfUser')
    audio_data = data.get('audio')
    rooms = sio.rooms(sid)
    room = rooms[0] if rooms else None
    if typeOfUser == "Interviewer":
        await speech_recognition_interviewer(room,questions,texts_by_room,audio_data)
    elif typeOfUser == "Interviewed":
        await speech_recognition_interviewed(room,questions,texts_by_room,typeOfUser,audio_data)
    if len(texts_by_room[room]["Interviewer"]) > 0 and texts_by_room[room]["Interviewer_accumulated_text"] == "":
        interviewer_question = texts_by_room[room]["Interviewer"][len(texts_by_room[room]["Interviewer"]) - 1]
        interviewed_answer = texts_by_room[room]["Interviewed_accumulated_text"]
        question = json_questions["skills"][interviewer_question[0]]["dimensiones"][interviewer_question[1]]
        result = {}
        if interviewed_answer != "":
            if question["tipo"] != "radio":
                result = createSkill(json_questions,interviewer_question,interviewed_answer)
            elif question["tipo"] == "radio":
                respuestas = question["respuestas"]
                formatted_lines = ["{}. {}".format(i, respuesta["nombre"]) for i, respuesta in enumerate(respuestas)]
                formatted_text = "\n".join(formatted_lines)
                index_answer = get_opcion(question["description"],interviewed_answer,formatted_text,os.getenv("OPENAI_API_KEY"))
                puntaje = 0
                if index_answer >= 0:
                    puntaje = question["respuestas"][index_answer]["puntaje"]
                result = createSkill(json_questions,interviewer_question,puntaje)
            sio.emit(os.getenv("LEVELUP_SOCKETIO_EVENT"), { "interview": result, "type": "meetingType" })

def createSkill(json_questions,interviewer_question,valor):
    result = {
                "skills":[],
                "interviewed_id":"idInterviewed"
            }
    result["skills"].append(copy.deepcopy(json_questions["skills"][interviewer_question[0]]))
    result["skills"][0]["dimensiones"] = []
    result["skills"][0]["dimensiones"].append(json_questions["skills"][interviewer_question[0]]["dimensiones"][interviewer_question[1]])
    result["skills"][0]["dimensiones"][0]["valor"] = valor
    return result