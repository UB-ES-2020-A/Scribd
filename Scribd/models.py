from django.contrib.auth.models import User
from django.db import models

from Scribd.user_model import User, Provider


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
    featured_photo = models.ImageField(upload_to="images", default='images/unknown.png')
    url = models.URLField(max_length=200, default='https://es-scribd-staging.herokuapp.com/media/ebooks/unknown.pdf', blank=True, null=True)
    count_downloads = models.PositiveIntegerField(default=0)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'user_type': 'Provider'})

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
    class Meta:
        verbose_name = 'ViewedEbooks'
        verbose_name_plural = 'ViewedEbooks'


class UserTickets(models.Model):
    id_uTicket = models.AutoField(primary_key=True)
    ticket_title = models.CharField(max_length=30, blank=False, default='Ticket')
    ticket_summary = models.CharField(max_length=300)
    ticket_date_added = models.DateTimeField(auto_now_add=True)
    ticket_solved = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'UserTickets'
        verbose_name_plural = 'UserTickets'


class EbookInsertDate(models.Model):
    viewed_ebooks = models.ForeignKey(ViewedEbooks, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'EbookInsertDate'
        verbose_name_plural = 'EbookInsertDates'
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

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class UploadedResources(models.Model):
    # Available extensions
    VISIBILITY_CHOICES = (
        ("public", "public"),
        ("private", "private"),
    )
    _v_choices = dict(VISIBILITY_CHOICES)

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False, default='')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # One to many
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='')
    featured_photo = models.ImageField(upload_to="images", default='images/unknown.png')
    file = models.FileField(upload_to='uploads', default='')


class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    ammount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
