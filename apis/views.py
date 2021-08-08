from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from apis.models.Category import *
from apis.models.Voice import *
from apis.models.Word import *

from .serializers import WordSerializer, VoiceSerializer
from apis.utils.phoneticAlgo import phoneticsOf, phoneticsOf_array
from apis.utils.rhymeFilterAndSort import filterMatchedVoices

from apis.const.RhymeType import RhymeType

from django.db import utils

import json
import logging
import sys

logger = logging.getLogger(__name__)
IntegrityError = utils.IntegrityError

# This is the api for adding and getting all words.
# add word request packat = {title_show, titles_algo, category}.
# title_algo is an array.
@api_view(['GET' , 'POST'])
def word(request):
    if request.method == 'GET':
        words = Word.objects.all()
        word_serializer = WordSerializer(words , many = True)
        return Response(word_serializer.data)
    elif request.method == 'POST':
        try:
            word_request_data = request.data

            # Only for show
            title_show = word_request_data["title_show"]
            
            # important for algorithm
            v_titles_algo = []
            titles_algo = json.loads(word_request_data['titles_algo'])

            if len(titles_algo) == 0:
                v_titles_algo = [phoneticsOf(title_show)]
            else:
                v_titles_algo = phoneticsOf_array(titles_algo)

            category_name = word_request_data["category"]
            category = Category.objects.get_or_create(category_title = category_name)[0]

            new_word_obj = Word(titles_algo = word_request_data['titles_algo'], category = category, title_show = title_show)

            for v_title_algo in v_titles_algo:
                voice = Voice.objects.get_or_create(v_title = v_title_algo)[0]
                new_word_obj.voices.add(voice)
            
            new_word_obj.save()
            return Response(data = {"status" : 200}, status = status.HTTP_201_CREATED)
        except IntegrityError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("wordPostAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500, "message" : "duplicate words not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("wordPostAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500}, status=status.HTTP_400_BAD_REQUEST)

#process-lyrics API
#request packat = {lyrics, split-by}
@api_view(['POST'])
def lyrics(request):
    try:
        lyrics_request_data = request.data
        splitBy = lyrics_request_data["split-by"] or " "
        splited = set(lyrics_request_data["lyrics"].split(splitBy))
        words = []
        for word in splited:
            print(word)
            if len(word) >= 4:
                v_title_algo = phoneticsOf(word)
                try:
                    words.append(Word(title_algo = word.lower(), voice = Voice.objects.get_or_create(v_title = v_title_algo)[0], title_show = word.lower()))
                except Exception:
                    pass
        print(words)
        Word.objects.bulk_create(words, ignore_conflicts=True)
        return Response(data = {"status" : 200}, status = status.HTTP_201_CREATED)
    except IntegrityError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("LyricsAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500, "message" : "duplicate words not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("LyricsAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500}, status=status.HTTP_400_BAD_REQUEST)

#find-rhymes API
#request packat {word, is_add_to_db, rhyme_type, level}
#is_add_to_db - are you willing to add that word into database?
#rhyme_type - 1/2 | 1-RHYME_BY_LAST | 2-RHYME_BY_SUBSTRING
@api_view(['POST'])
def findRhymings(request):
    try:
        word = request.data["word"]
        level = request.data["level"]
        is_add_to_db = request.data["is_add_to_db"] or False

        # introduce enum here
        rhyme_type = RhymeType(request.data["rhyme_type"]) or RhymeType.RHYME_BY_LAST

        voice_of_word = phoneticsOf(word)
        voice_obj = Voice.objects.get_or_create(v_title = voice_of_word)[0]

        if is_add_to_db:
            try:
                Word.objects.create(title_algo = word, voice = voice_obj)
            except:
                pass
        
        all_voices = VoiceSerializer(Voice.objects.all(), many = True).data
        all_matched_voices = filterMatchedVoices(voices = all_voices, voice = voice_of_word, level = level, rhyme_type = rhyme_type)
        final_word_list = []
        for voice_item in all_matched_voices:
            words_list = Word.objects.filter(voice = voice_item["id"])
            word_serializer = WordSerializer(words_list, many = True)
            word_serializer_only_title_show = map(lambda obj : {
                "title_show" : obj["title_show"],
                "id" : obj["id"]
            }, word_serializer.data)
            final_word_list.append(word_serializer_only_title_show)
        return Response(data = {"status" : 200, "rhymes_list" : final_word_list}, status = status.HTTP_200_OK)
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("FindRhymeAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500}, status=status.HTTP_400_BAD_REQUEST)

#recycle-words API
#it recycle all the words for updated rhyming algorithm
@api_view(['POST'])
def recycleWords(request):
    try:
        all_words = WordSerializer(Word.objects.all(), many = True).data
        for word in all_words:
            v_title_of_word = phoneticsOf(word["title_algo"])
            voice = Voice.objects.get_or_create(v_title = v_title_of_word)[0]
            Word.objects.filter(id=word["id"]).update(voice = voice)
        return Response(data = {"status" : 200}, status = status.HTTP_200_OK)
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("RecycleAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500}, status=status.HTTP_400_BAD_REQUEST)

#delete-words API
#request packat - {words(array)}
@api_view(['POST'])
def deleteWords(request):
    try:
        words = request.data['words']
        count = 0
        for word in words:
            word_object = Word.objects.filter(title_show = word)
            print(word_object)
            if word_object.exists():
                count = count + word_object.delete()[0]

        return Response(data = {"status" : 200, "count" : count}, status=status.HTTP_200_OK)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("DeleteAPI: %s at %s", e, str(exc_tb.tb_lineno))
        return Response(data = {"status" : 500}, status=status.HTTP_400_BAD_REQUEST)
