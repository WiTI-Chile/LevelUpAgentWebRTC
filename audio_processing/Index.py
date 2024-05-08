from audio_processing.Speech_recognition import speech_recognition_interviewer,speech_recognition_interviewed

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
        if interviewed_answer != "":
            option = get_opcion(question, interviewed_answer, question["opciones"], os.getenv("OPENAI_API_KEY"), [])
            await sio.emit('question', {'question': question, 'option': option}, room=room)
        print(question)