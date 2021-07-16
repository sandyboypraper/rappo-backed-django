from django.db import models

class Category(models.Model):
    category_title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.category_title
    
    class Meta:
        ordering = ['category_title']