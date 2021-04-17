from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Word, Voice, Category
from .serializers import WordSerializer, VoiceSerializer
from .rhymeAlgo import rhymeOf
from .utils import filterMatchedVoices

from django.db import utils

import json
import logging
import sys

logger = logging.getLogger(__name__)
IntegrityError = utils.IntegrityError

# This is the api for adding and getting all words.
@api_view(['GET' , 'POST'])
def word(request):
    if request.method == 'GET':
        words = Word.objects.all()
        word_serializer = WordSerializer(words , many = True)
        return Response(word_serializer.data)
    elif request.method == 'POST':
        try:
            word_request_data = request.data
            v_title = rhymeOf(word_request_data["title_algo"])
            v_display_name = word_request_data["title"]
            category_name = word_request_data["category"]
            voice = Voice.objects.get_or_create(v_title = v_title)[0]
            category = Category.objects.get_or_create(category_title = category_name)[0]
            Word.objects.create(title = word_request_data["title_algo"].lower(), voice = voice, category = category, show_title=v_display_name)
            return Response(data = {"status" : 200}, status = status.HTTP_201_CREATED)
        except IntegrityError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("wordPostAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500, "message" : "duplicate words not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("wordPostAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def lyrics(request):
    try:
        lyrics_request_data = request.data
        splitBySpace = set(lyrics_request_data["lyrics"].split(" "))
        words = []
        for word in splitBySpace:
            if len(word) >= 4:
                v_title = rhymeOf(word)
                try:
                    words.append(Word(title = word.lower(), voice = Voice.objects.get_or_create(v_title = v_title)[0]))
                except Exception:
                    pass
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

@api_view(['POST'])
def findRhymings(request):
    try:
        word = request.data["word"]
        level = request.data["level"]
        voice_of_word = rhymeOf(word)
        voice_obj = Voice.objects.get_or_create(v_title = voice_of_word)[0]
        try:
            Word.objects.create(title = word, voice = voice_obj)
        except:
            pass
        all_voices = VoiceSerializer(Voice.objects.all(), many = True).data
        all_matched_voices = filterMatchedVoices(voices = all_voices, voice = voice_of_word, level = level)
        final_word_list = []
        for voice_item in all_matched_voices:
            words_list = Word.objects.filter(voice = voice_item["id"])
            word_serializer = WordSerializer(words_list, many = True)
            final_word_list.append(word_serializer.data)
        return Response(data = {"status" : 200, "rhymes_list" : final_word_list}, status = status.HTTP_200_OK)
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("FindRhymeAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def recycleWords(request):
    try:
        all_words = WordSerializer(Word.objects.all(), many = True).data
        for word in all_words:
            v_title_of_word = rhymeOf(word["title"])
            voice = Voice.objects.get_or_create(v_title = v_title_of_word)[0]
            Word.objects.filter(id=word["id"]).update(voice = voice)
        return Response(data = {"status" : 200}, status = status.HTTP_200_OK)
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("RecycleAPI: %s at %s", e, str(exc_tb.tb_lineno))
            return Response(data = {"status" : 500}, status=status.HTTP_400_BAD_REQUEST)