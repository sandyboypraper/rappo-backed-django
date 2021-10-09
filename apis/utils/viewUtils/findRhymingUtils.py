from apis.const.findRhymeView import findRhymeRequestDataKeys
import json

def findRhymingDataReader(data):
    word, level_of_rhyme, is_add_to_db = 1,2,3
    for key in findRhymeRequestDataKeys:
        dataForKey = data[key.value]
        if key == findRhymeRequestDataKeys.WORD:
            word = dataForKey
        elif key == findRhymeRequestDataKeys.LEVEL_OF_RHYME:
            level_of_rhyme = dataForKey
        else:
            is_add_to_db = dataForKey or False
    
    return word, level_of_rhyme, is_add_to_db

def convertToJsonArray(word):
    json_array = [word]
    return json.dumps(json_array)