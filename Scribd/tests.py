# Create your tests here.

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings, Client
from django.urls import reverse

from Scribd.models import Ebook, UploadedResources, Payments
from Scribd.user_models import User, userProfile


class EbookTestCase(TestCase):
    def setUp(self):
        Ebook.objects.create(
            ebook_number="74564",
            title="Don Quijote",
            autor="Miguel de Cervantes",
            description="",
            is_promot=False,
            size=2,
            media_type="pdf",
        )

    def test_ebook_search(self):
        quijote = Ebook.objects.get(title="Don Quijote")
        self.assertEqual(quijote.autor, "Miguel de Cervantes")
        self.assertEqual(quijote.is_promot, False)

    def delete_book(self):
        quijote = Ebook.objects.get(title="Don Quijote")
        quijote.delete()
        self.assertEqual(quijote, "")


class UserSimpleTestCase(TestCase):
    def test_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="pepito123@gmail.com",
            username="pepito123",
            first_name="Pepito",
            last_name="123",
            password="xTu<3D\R",
        )

        self.assertEqual(user.email, "pepito123@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)


class UserTestCase(TestCase):
    def setUpTestingViews(self):
        self.client = Client()

    def test_user(self):
        user = User.objects.create_user(
            email="pepito123@gmail.com",
            username="pepito123",
            first_name="Pepito",
            last_name="123",
            password="xTu<3D\R",
        )
        userprofile = userProfile.objects.create(user=user)
        userprofile.bio = ("Soy un usuario de prueba", )
        userprofile.subs_type = ("Free Trial", )
        userprofile.nbooks_by_subs = ("10", )
        userprofile.card_titular = "Pepito 123"

        self.assertEqual(user.email, "pepito123@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.user_profile.bio, "Soy un usuario de prueba")
        self.assertTrue(user.user_profile.nbooks_by_subs, "10")


class PaymentTestCase(TestCase):
    def test_payment(self):
        user = User.objects.create_user(
            email="pepito123@gmail.com",
            username="pepito123",
            first_name="Pepito",
            last_name="123",
            password="xTu<3D\R",
        )
        p = Payments.objects.create(user=user, ammount=100.0)
        self.assertEqual(p.user.email, "pepito123@gmail.com")
        self.assertTrue(p.ammount == 100.0)


class UploadFilesTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email="pepito123@gmail.com",
            username="pepito123",
            first_name="Pepito",
            last_name="123",
            password="xTu<3D\R",
        )
        uf = UploadedResources.objects.create(
            title="MyStory",
            user=user,
            visibility="public",
            featured_photo="images/HP3.jpg",
            file="uploads/LoremIpsum.pdf",
        )

    def test_uploadedFile_search(self):
        uf = UploadedResources.objects.get(title="MyStory")
        self.assertEqual(uf.user.username, "pepito123")
        self.assertEqual(uf.visibility, "public")
        self.assertEqual(uf.featured_photo, "images/HP3.jpg")
        self.assertEqual(uf.file, "uploads/LoremIpsum.pdf")

    def delete_uploadedFile(self):
        uf = UploadedResources.objects.get(title="MyStory")
        uf.delete()
        self.assertEqual(uf, "")


class MyTest(TestCase):
    def setUpTestingViews(self):
        self.client = Client()

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_get_base(self):
        response = self.client.get(reverse("base"))

        # 200, OK
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "scribd/base.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_get_ebooks(self):
        response = self.client.get(reverse("ebooks"))

        # 200, OK
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "scribd/mainpage.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_get_users(self):
        response = self.client.get(reverse("users"))

        # 200, OK
        self.assertEquals(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_get_ebooks(self):
        response = self.client.get(reverse("ebooks"))

        # 200, OK
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "scribd/mainpage.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_get_ebooks(self):
        response = self.client.get(reverse("ebooks"))

        # 200, OK
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "scribd/mainpage.html")


class LoginTesting(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="pepito123@gmail.com",
            username="pepito123",
            first_name="Pepito",
            last_name="123",
            password="xTu<3D\R",
        )
        self.user.set_password("xTu<3D\R")
        userprofile = userProfile.objects.create(user=self.user)
        userprofile.bio = ("Soy un usuario de prueba", )
        userprofile.subs_type = ("Free Trial", )
        userprofile.nbooks_by_subs = ("10", )
        userprofile.card_titular = "Pepito 123"

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_wrong_login(self):
        response = self.client.post(
            "/accounts/login/",
            data={
                "username": self.user.username,
                "password": "randompassword"
            },
        )
        self.assertEquals(response.status_code, 302)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_correct_login(self):
        self.client.login(username=self.user.username, password="xTu<3D\R")
        response = self.client.get(reverse("index"))
        self.assertEquals(response.context["user"].is_active, True)


class SignupTesting(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = "pepito123@gmail.com"
        self.username = "pepito123"
        self.first_name = "Pepito"
        self.last_name = "123"

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_signup_page_url(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="registration/signup.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_signup_page_view_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="registration/signup.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_correct_password(self):
        password = "xTu<3D\R"
        response = self.client.post(
            reverse("signup"),
            data={
                "username": self.username,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": password,
                "password2": password,
            },
        )
        self.assertEqual(response.status_code, 302)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_wrong_password(self):
        password = "xTu<3D\R"
        response = self.client.post(
            reverse("signup"),
            data={
                "username": self.username,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": password,
                "password2": "otherinput",
            },
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_short_password(self):
        password = "as33"
        response = self.client.post(
            reverse("signup"),
            data={
                "username": self.username,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": password,
                "password2": password,
            },
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_similar_to_user_name(self):
        password = self.username + "123"
        response = self.client.post(
            reverse("signup"),
            data={
                "username": self.username,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": password,
                "password2": password,
            },
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_too_common(self):
        password = "123456789"
        response = self.client.post(
            reverse("signup"),
            data={
                "username": self.username,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": password,
                "password2": password,
            },
        )
        self.assertEqual(response.status_code, 200)


class EbookDetailsTesting(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.book = Ebook.objects.create(
            ebook_number="74564",
            title="Don Quijote",
            autor="Miguel de Cervantes",
            description="",
            is_promot=False,
            size=2,
            media_type="pdf",
        )

        self.user = User.objects.create_user(
            email="pepito123@gmail.com",
            username="pepito123",
            first_name="Pepito",
            last_name="123",
            password="xTu<3D\R",
        )
        self.user.set_password("xTu<3D\R")
        userprofile = userProfile.objects.create(user=self.user)
        userprofile.bio = ("Soy un usuario de prueba", )
        userprofile.subs_type = ("Free Trial", )
        userprofile.nbooks_by_subs = ("10", )
        userprofile.card_titular = "Pepito 123"

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_ebookdetails_page_url(self):
        response = self.client.get("/ebookdetail/" + str(self.book.id) + "/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/ebook_details.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_signup_page_view_name(self):
        response = self.client.get(
            reverse("ebook_custom_detail", kwargs={"pk": self.book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/ebook_details.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_follow_book(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')
        followers = self.book.follower.count()
        self.client.post(reverse('ebook_custom_detail',kwargs={'pk':self.book.id}),data={'follow':''})
        new_followers = self.book.follower.count()
        self.assertTrue(followers < new_followers)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_follow_book_not_authenticated(self):

        followers = self.book.follower.count()
        a = self.client.post(reverse('ebook_custom_detail',kwargs={'pk':self.book.id}),data={'follow':''})
        new_followers = self.book.follower.count()
        self.assertTrue(followers == new_followers)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_forum(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')
        topic = 'test'
        description = 'test'
        forums = self.book.forum_set.count()
        self.client.post(reverse('ebook_custom_detail', kwargs={'pk': self.book.id}),data={'topic':topic,'description':description,'create_forum':''})

        new_forums= self.book.forum_set.count()
        self.assertTrue(forums < new_forums)
        self.assertTrue(self.book.forum_set.all()[new_forums-1].user == self.user)
        self.assertTrue(self.book.forum_set.all()[new_forums-1].topic == topic)
        self.assertTrue(self.book.forum_set.all()[new_forums-1].description == description)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_forum_not_authenticated(self):
        forums = self.book.forum_set.count()
        self.client.post(reverse('ebook_custom_detail', kwargs={'pk': self.book.id}),
                         data={'topic': 'test', 'description': 'test', 'create_forum': ''})

        new_forums = self.book.forum_set.count()
        self.assertTrue(forums == new_forums)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_review(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')
        comment = 'test'
        value_stars = 'Five stars'
        reviews = self.book.review_set.count()
        self.client.post(reverse('ebook_custom_detail', kwargs={'pk': self.book.id}),data={'comment':comment,'value_stars':value_stars,'review':''})

        new_reviews= self.book.review_set.count()

        self.assertTrue(reviews < new_reviews)
        self.assertTrue(self.book.review_set.all()[new_reviews-1].user == self.user)
        self.assertTrue(self.book.review_set.all()[new_reviews-1].comment == comment)
        self.assertTrue(self.book.review_set.all()[new_reviews-1].value_stars == value_stars)


    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_review_not_authenticated(self):
        comment = 'test'
        value_stars = 'Five stars'
        reviews = self.book.review_set.count()
        self.client.post(reverse('ebook_custom_detail', kwargs={'pk': self.book.id}),
                         data={'comment': comment, 'value_stars': value_stars, 'review': ''})

        new_reviews = self.book.review_set.count()
        self.assertTrue(reviews == new_reviews)
