from rest_framework import serializers
from apis.models.Voice import *
from apis.models.Category import *
from apis.models.Word import *


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ['titles_for_algo', 'title_for_show', 'id']

class VoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Voice
        fields = ['v_title', 'id']