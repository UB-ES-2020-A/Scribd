from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Account(models.Model):
    username = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    date_registration = models.DateField()
    date_registration = models.DateField()
    subscribed = models.BooleanField()
    type = models.CharField(max_length=20)

    """def get_absolute_url(self):
        return reversed('blog_post_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args,**kwargs)"""

    class Meta:


        def __str__(self):
            return self.username







