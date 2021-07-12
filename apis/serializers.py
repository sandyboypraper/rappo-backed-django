from rest_framework import serializers
from .models import Word,Voice

class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ['title_algo', 'title_show', 'id']

class VoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Voice
        fields = ['v_title', 'id']