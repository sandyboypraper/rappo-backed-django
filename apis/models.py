from django.db import models

class Voice(models.Model):
    v_title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.v_title

    class Meta:
        ordering = ['v_title']


class Category(models.Model):
    category_title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.category_title
    
    class Meta:
        ordering = ['category_title']



class Word(models.Model):
    title = models.CharField(max_length=30, unique=True)
    voice = models.ForeignKey(Voice, on_delete = models.SET_NULL, default=1, null=True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null=True)
    show_title = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

