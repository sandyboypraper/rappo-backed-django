from apis.models.Voice import *

def convertVoicesToObjs(voices):
    voices_objects = []
    for voice in voices:
        voice_object = Voice.objects.get_or_create(v_title = voice)[0]
        voices_objects.append(voice_object)
    return voices_objects