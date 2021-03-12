from django.db import models

class Voice(models.Model):
    v_title = models.CharField(max_length=30)

    def __str__(self):
        return self.v_title

    class Meta:
        ordering = ['v_title']


class Word(models.Model):
    title = models.CharField(max_length=30)
    voice = models.ForeignKey(Voice, on_delete = models.CASCADE, default=1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']