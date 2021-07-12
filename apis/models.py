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
    title_algo = models.CharField(max_length=30, unique=True)
    voice = models.ForeignKey(Voice, on_delete = models.SET_NULL, default=1, null=True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null=True)
    title_show = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.title_show
    
    def save(self, *args, **kwargs):
        if not self.title_show:
            self.title_show = self.title_algo
        super(Word, self).save(*args, **kwargs)

    class Meta:
        ordering = ['title_show']

