from django.urls import path
from .views import *

urlpatterns = [
    path('words/', word),
    path('process-lyrics/', lyrics),
    path('find-rhymes/', findRhymings),
    path('recycle-words/', recycleWords),
    path('delete-words/', deleteWords)
]