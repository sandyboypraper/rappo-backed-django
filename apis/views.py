from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Word
from .serializers import WordSerializer

# This is the api for adding and getting all words.
@api_view(['GET' , 'POST'])
def word(request):

    if request.method == 'GET':

        words = Word.objects.all()
        word_serializer = WordSerializer(words , many = True)
        return Response(word_serializer.data)

    elif request.method == 'POST':

        word_serializer = WordSerializer(data = request.data)
        if word_serializer.is_valid():
            #No need to create new object and then add keys by keys 
            word_serializer.save()
            return Response(word_serializer.data, status=status.HTTP_201_CREATED)
        return Response(word_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


