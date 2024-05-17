from audio_processing.Speech_recognition import speech_recognition_interviewer,speech_recognition_interviewed
import copy
from openAiFunctions.opciones import get_opcion
import os
import socketio

interviewers_texts_by_room = {}
interviewed_text_by_room = {}
def process_audio(data, questions,json_questions):
    userName = data.get('name')
    typeOfUser = data.get("typeOfUser")
    audio_data = data.get('audio')
    room = data.get('room')
    if interviewed_text_by_room.get(room) == None:
        interviewed_text_by_room[room] = {"Interviewed": [],"Interviewed_accumulated_text":""}
    if typeOfUser == "Interviewer":
        speech_recognition_interviewer(room,questions,interviewers_texts_by_room,audio_data,userName,interviewed_text_by_room)
    elif typeOfUser == "Interviewed":
        speech_recognition_interviewed(room,interviewed_text_by_room,typeOfUser,audio_data)
    if interviewers_texts_by_room.get(room) == None:
        return
    if interviewers_texts_by_room[room]["currentQuestion"] != False:
        interviewer_question = interviewers_texts_by_room[room]["currentQuestion"]
        interviewed_answer = interviewed_text_by_room[room]["Interviewed_accumulated_text"]
        question = json_questions["skills"][interviewer_question[0]]["dimensiones"][interviewer_question[1]]
        result = {}
        meetingType = str(room).split("_")[1]
        interview_id = str(room).split("_")[0]
        if interviewed_answer != "":
            if question["tipo"] != "radio":
                result = createSkill(json_questions,interviewer_question,interviewed_answer,interview_id)
            elif question["tipo"] == "radio":
                respuestas = question["respuestas"]
                formatted_lines = ["{}. {}".format(i, respuesta["nombre"]) for i, respuesta in enumerate(respuestas)]
                formatted_text = "\n".join(formatted_lines)
                index_answer = get_opcion(question["description"],interviewed_answer,formatted_text,os.getenv("OPENAI_API_KEY"))
                puntaje = 0
                if index_answer >= 0:
                    puntaje = question["respuestas"][index_answer]["puntaje"]
                result = createSkill(json_questions,interviewer_question,puntaje,interview_id)
            
            #GENERAR OTRA CONEXION SOCKET PARA ENVIAR LOS DATOS A LA API
            sio_client = socketio.Client()
            sio_client.connect(os.getenv("LEVELUP_SOCKETIO_URL"))
            sio_client.emit(os.getenv("LEVELUP_SOCKETIO_EVENT"), { "interview": result, "type": meetingType })
            sio_client.disconnect()

def createSkill(json_questions,interviewer_question,valor,interview_id):
    result = {
                "skills":[],
                "interviewed_id":interview_id
            }
    result["skills"].append(copy.deepcopy(json_questions["skills"][interviewer_question[0]]))
    result["skills"][0]["dimensiones"] = []
    result["skills"][0]["dimensiones"].append(json_questions["skills"][interviewer_question[0]]["dimensiones"][interviewer_question[1]])
    result["skills"][0]["dimensiones"][0]["valor"] = valor
    return result