from apis.utils.phoneticAlgo import phoneticsOf, phoneticsOf_array
from apis.const.WordView import WordViewRequestDataKeys
import json

def convertTitlesToVoices(title_for_show, titles_for_algo):
    voices = []
    if len(titles_for_algo) == 0:
        voices = [phoneticsOf(title_for_show)]
    else:
        voices = phoneticsOf_array(titles_for_algo)
    return voices

def wordViewDataReader(data):
    titles_for_algo, category_names, title_for_show = 1,2,3
    for key in WordViewRequestDataKeys:
        dataForKey = data[key.value]
        if key == WordViewRequestDataKeys.CATEGORY_NAMES:
            if dataForKey != "":
                category_names = json.loads(dataForKey)
            else:
                category_names = ""
        elif key == WordViewRequestDataKeys.TITLES_FOR_ALGO:
            titles_for_algo = json.loads(dataForKey)
        else:
            title_for_show = dataForKey
    return titles_for_algo, category_names, title_for_show
