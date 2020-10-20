from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# comentario de prueba
class ebook(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1024)
    autor = models.CharField(max_length=1024)
    size = models.IntegerField()
    media_type= models.CharField(max_length=16)
    count_downloads = models.IntegerField()

    class Meta:
        verbose_name = 'Ebooks'
        verbose_name_plural = 'Ebooks'

    def __str__(self):
        return self.title
