from apis.models import Word
from apis.serializers import WordSerializer

def copyTitleAlgoToTileShow():
    words_query_set = Word.objects.all()
    words = WordSerializer(words_query_set , many = True)
    for word in words.data:
        if word["title_show"] == "":
            word_from_db = Word.objects.get(id = word["id"])
            word_from_db.title_show = word["title_algo"]
            word_from_db.save()
