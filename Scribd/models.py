from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Account(models.Models):
    name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    username = models.CharField(max_length=15)
    subscribed = models.BooleanField()
    type = models.CharField(max_length=20)

    """def get_absolute_url(self):
        return reversed('blog_post_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args,**kwargs)"""

    class Meta:
        ordering = ['created on']







