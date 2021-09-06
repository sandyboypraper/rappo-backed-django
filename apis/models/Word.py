from django.db import models
from .Voice import *
from .Category import *

class Word(models.Model):
    titles_for_algo = models.CharField(max_length=300, unique=True)
    voices = models.ManyToManyField(Voice)
    category_names = models.ManyToManyField(Category)
    title_for_show = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.title_for_show
    
    def save(self, *args, **kwargs):
        if not self.title_for_show or self.title_for_show == "":
            print("YES")
            self.title_for_show = "NULL"
        else:
            print("NO")
        super(Word, self).save(*args, **kwargs)

    class Meta:
        ordering = ['title_for_show']