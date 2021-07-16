from django.db import models

class Voice(models.Model):
    v_title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.v_title

    class Meta:
        ordering = ['v_title']