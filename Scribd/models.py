from django.contrib.auth.models import User
from django.db import models

from Scribd.user_model import User


class Ebook(models.Model):
    TYPE_FILE = (
        ("pdf", "pdf"),
        ("epub", "epub"),
    )
    _type_files = dict(TYPE_FILE)

    CATEGORY_EBOOK = (
        ("Thriller", "Thriller"),
        ("Drama", "Drama"),
    )
    _category = dict(CATEGORY_EBOOK)

    ebook_number = models.CharField(max_length=8, unique=True, default='')  # IBAN?
    title = models.CharField(max_length=50, blank=False, default='')
    autor = models.CharField(max_length=50, blank=False, default='')
    description = models.TextField(default='')
    is_promot = models.BooleanField(default='False', blank=True, null=True)
    size = models.IntegerField(default=0)
    category = models.CharField(max_length=8, choices=CATEGORY_EBOOK, default='')
    media_type = models.CharField(max_length=5, choices=TYPE_FILE, default='')
    featured_photo = models.ImageField(upload_to="static/images/", default='static/images/unknown.png')
    url = models.URLField(max_length=200, default='static/ebooks/unknown.png', blank=True, null=True)
    count_downloads = models.PositiveIntegerField(default=0)

    def get_ebook_media_type(self):
        return self._type_files[self.media_type]

    def get_category(self):
        return self._category[self.category]

    def get_ebook_number(self):
        return self.ebook_number

    def get_autor(self):
        return self.autor

    def get_url(self):
        return self.url

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ebook'
        verbose_name_plural = 'Ebooks'

class ViewedEbooks(models.Model):
    id_vr = models.AutoField(primary_key=True)
    ebook = models.ManyToManyField(Ebook, through='EbookInsertDate')

class userTickets(models.Model):
    id_uTicket = models.AutoField(primary_key=True)
    ticket_title = models.CharField(max_length=30, blank=False, default='Ticket')
    ticket_summary = models.CharField(max_length=300)
    ticket_date_added = models.DateTimeField(auto_now_add=True)
    ticket_solved = models.BooleanField(default=False)


class EbookInsertDate(models.Model):
    viewed_ebooks = models.ForeignKey(ViewedEbooks, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']


class Review(models.Model):
    STARS = (
        ("One star", 1),
        ("Two stars", 2),
        ("Three stars", 3),
        ("Four stars", 4),
        ("Five stars", 5),
    )
    _d_stars = dict(STARS)
    id = models.AutoField(primary_key=True)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    value_stars = models.CharField(max_length=12, choices=STARS)
    comment = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def get_human_stars(self):
        return self._d_stars[self.value_stars]
