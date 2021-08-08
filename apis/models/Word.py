from django.db import models
from .Voice import *
from .Category import *

class Word(models.Model):
    titles_algo = models.CharField(max_length=30, unique=True)
    voices = models.ManyToManyField(Voice)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null=True)
    title_show = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.title_show
    
    def save(self, *args, **kwargs):
        if not self.title_show or self.title_show == "":
            print("YES")
            self.title_show = self.title_algo
        else:
            print("NO")
        super(Word, self).save(*args, **kwargs)

    class Meta:
        ordering = ['title_show']