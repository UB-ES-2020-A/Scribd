from django.db import models
from django_resized import ResizedImageField

from .user_models import User, providerProfile


##################################
####### MODELOS EBOOK ############
##################################
class Ebook(models.Model):
    TYPE_FILE = (
        ("pdf", "pdf"),
        ("epub", "epub"),
    )
    _type_files = dict(TYPE_FILE)

    CATEGORY_EBOOK = (
        ("Thriller", "Thriller"),
        ("Drama", "Drama"),
        ("Action", "Action"),
        ("Adventure", "Adventure"),
        ("Classics", "Classics"),
        ("Comic Book", "Comic Book"),
        ("Fantasy", "Fantasy"),
        ("Historical Fiction", "Historical Fiction"),
        ("Horror", "Horror"),
        ("Literary Fiction", "Literary Fiction"),
        ("Romance", "Romance"),
        ("Sci-Fi", "Sci-Fi"),
        ("Biography", "Biography"),
        ("Cookbook", "Cookbook"),
        ("Essay", "Essay"),
        ("History", "History"),
        ("Poetry", "Poetry"),
        ("Other", "Other"),
    )

    _category = dict(CATEGORY_EBOOK)

    ebook_number = models.CharField(max_length=8, unique=True,
                                    default="")  # IBAN?
    title = models.CharField(max_length=50, blank=False, default="")
    autor = models.CharField(max_length=50, blank=False, default="")
    description = models.TextField(default="")
    is_promot = models.BooleanField(default="False", blank=True, null=True)
    size = models.IntegerField(default=0)
    category = models.CharField(max_length=20,
                                choices=CATEGORY_EBOOK,
                                default="")
    media_type = models.CharField(max_length=5, choices=TYPE_FILE, default="")
    featured_photo = ResizedImageField(size=[350, 500],
                                       quality=100,
                                       upload_to="images",
                                       default="images/unknown.png")
    file = models.FileField(max_length=200,
                          default="readable_content/hp3.pdf",
                          blank=True,
                          null=True)
    count_downloads = models.PositiveIntegerField(default=0)
    publisher = models.ForeignKey(
        providerProfile,
        related_name="providers_key",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    follower = models.ManyToManyField(User,
                                      related_name="users_key",
                                      null=True,
                                      blank=True)

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
        return ("[**Promoted**]" if self.is_promot else "") + self.title

    class Meta:
        verbose_name = "Ebook"
        verbose_name_plural = "Ebooks"


class ViewedEbooks(models.Model):
    id_vr = models.AutoField(primary_key=True)
    ebook = models.ManyToManyField(Ebook, through="EbookInsertDate")

    class Meta:
        verbose_name = "ViewedEbooks"
        verbose_name_plural = "ViewedEbooks"


class EbookInsertDate(models.Model):
    viewedebooks = models.ForeignKey(ViewedEbooks, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]


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
    # comment_title = models.CharField(max_length=30, blank=False, default='comment')
    comment = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def get_human_stars(self):
        return self._d_stars[self.value_stars]

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


##################################
####### MODELOS Ticket ###########
##################################


class UserTickets(models.Model):
    id_uTicket = models.AutoField(primary_key=True)
    ticket_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    ticket_title = models.CharField(max_length=30, blank=False, default=" ")
    ticket_summary = models.CharField(max_length=300)
    ticket_date_added = models.DateTimeField(auto_now_add=True)
    ticket_solved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "UserTickets"
        verbose_name_plural = "UserTickets"


class DiscussionTickets(models.Model):
    userticket = models.ForeignKey(UserTickets,
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             default=None)
    discuss = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.userticket)


##################################
####### MODELOS PROFILE ##########
##################################


class UploadedResources(models.Model):
    # Available extensions
    VISIBILITY_CHOICES = (
        ("public", "public"),
        ("private", "private"),
    )
    _v_choices = dict(VISIBILITY_CHOICES)

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False, default="")
    user = models.ForeignKey(User, null=True,
                             on_delete=models.CASCADE)  # One to many
    visibility = models.CharField(max_length=10,
                                  choices=VISIBILITY_CHOICES,
                                  default="")
    featured_photo = models.ImageField(upload_to="images",
                                       default="images/unknown.png")
    file = models.FileField(upload_to="uploads", default="")


class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    ammount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)


##################################
####### MODELOS FORUM ############
##################################


class Forum(models.Model):
    ebook = models.ForeignKey(Ebook,
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             blank=True,
                             on_delete=models.CASCADE,
                             default=None)
    email = models.CharField(max_length=200, null=True)
    topic = models.CharField(unique=True, max_length=300)
    description = models.CharField(max_length=1000, blank=True)
    link = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.topic)


class Discussion(models.Model):
    forum = models.ForeignKey(Forum, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             blank=True,
                             on_delete=models.CASCADE,
                             default=None)
    discuss = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.forum)
