# Create your tests here.

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings, Client
from django.urls import reverse

from Scribd.models import Ebook, UploadedResources, Payments, UserTickets, Forum
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
        self.client.login(username=self.user.username, password="xTu<3D\R")
        followers = self.book.follower.count()
        self.client.post(
            reverse("ebook_custom_detail", kwargs={"pk": self.book.id}),
            data={"follow": ""},
        )
        new_followers = self.book.follower.count()
        self.assertTrue(followers < new_followers)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_follow_book_not_authenticated(self):

        followers = self.book.follower.count()
        a = self.client.post(
            reverse("ebook_custom_detail", kwargs={"pk": self.book.id}),
            data={"follow": ""},
        )
        new_followers = self.book.follower.count()
        self.assertTrue(followers == new_followers)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_forum(self):
        self.client.login(username=self.user.username, password="xTu<3D\R")
        topic = "test"
        description = "test"
        forums = self.book.forum_set.count()
        self.client.post(
            reverse("ebook_custom_detail", kwargs={"pk": self.book.id}),
            data={
                "topic": topic,
                "description": description,
                "create_forum": ""
            },
        )

        new_forums = self.book.forum_set.count()
        self.assertTrue(forums < new_forums)
        self.assertTrue(self.book.forum_set.all()[new_forums -
                                                  1].user == self.user)
        self.assertTrue(self.book.forum_set.all()[new_forums -
                                                  1].topic == topic)
        self.assertTrue(
            self.book.forum_set.all()[new_forums -
                                      1].description == description)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_forum_not_authenticated(self):
        forums = self.book.forum_set.count()
        self.client.post(
            reverse("ebook_custom_detail", kwargs={"pk": self.book.id}),
            data={
                "topic": "test",
                "description": "test",
                "create_forum": ""
            },
        )

        new_forums = self.book.forum_set.count()
        self.assertTrue(forums == new_forums)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_review(self):
        self.client.login(username=self.user.username, password="xTu<3D\R")
        comment = "test"
        value_stars = "Five stars"
        reviews = self.book.review_set.count()
        self.client.post(
            reverse("ebook_custom_detail", kwargs={"pk": self.book.id}),
            data={
                "comment": comment,
                "value_stars": value_stars,
                "review": ""
            },
        )

        new_reviews = self.book.review_set.count()

        self.assertTrue(reviews < new_reviews)
        self.assertTrue(self.book.review_set.all()[new_reviews -
                                                   1].user == self.user)
        self.assertTrue(self.book.review_set.all()[new_reviews -
                                                   1].comment == comment)
        self.assertTrue(
            self.book.review_set.all()[new_reviews -
                                       1].value_stars == value_stars)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_review_not_authenticated(self):
        comment = "test"
        value_stars = "Five stars"
        reviews = self.book.review_set.count()
        self.client.post(
            reverse("ebook_custom_detail", kwargs={"pk": self.book.id}),
            data={
                "comment": comment,
                "value_stars": value_stars,
                "review": ""
            },
        )

        new_reviews = self.book.review_set.count()
        self.assertTrue(reviews == new_reviews)


class TicketDetailTesting(TestCase):
    def setUp(self) -> None:
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

        self.ticket = UserTickets.objects.create(
            ticket_summary='test',
            ticket_title='test',
            ticket_user=self.user
        )

        self.ticket.save()
        self.user.save()



    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_ticketdetail_page_url(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')
        response = self.client.get("/ticket/"+str(self.ticket.id_uTicket)+"/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/ticketdetail.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_ticketdetail_page_view_name(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')
        response = self.client.get(
            reverse("ticket_detail",kwargs={'pk': self.ticket.id_uTicket}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/ticketdetail.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_ticketdetail_page_url_not_authenticated(self):

        response = self.client.get("/ticket/"+str(self.ticket.id_uTicket)+"/")
        self.assertEqual(response.status_code, 302)


    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_ticketdetail_page_view_not_authenticated_name(self):
        response = self.client.get(
            reverse("ticket_detail", kwargs={'pk': self.ticket.id_uTicket}))
        self.assertEqual(response.status_code, 302)




    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_message(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')

        comment = 'test'
        comments = self.ticket.discussiontickets_set.count()
        response = self.client.post(reverse("ticket_detail", kwargs={'pk': self.ticket.id_uTicket}),data={'discuss':comment})

        new_comments = self.ticket.discussiontickets_set.count()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(comments < new_comments)
        self.assertTrue(self.ticket.discussiontickets_set.all()[new_comments-1].user == self.user)
        self.assertTrue(self.ticket.discussiontickets_set.all()[new_comments-1].discuss == comment)


    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")

    def test_create_message_not_authenticated(self):

        comment = 'test'
        comments = self.ticket.discussiontickets_set.count()
        self.client.post(reverse("ticket_detail", kwargs={'pk': self.ticket.id_uTicket}),
                                    data={'discuss': comment})

        new_comments = self.ticket.discussiontickets_set.count()

        self.assertTrue(comments == new_comments)


class ForumDetailTesting(TestCase):
    def setUp(self) -> None:
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
        userprofile.bio = ("Soy un usuario de prueba",)
        userprofile.subs_type = ("Free Trial",)
        userprofile.nbooks_by_subs = ("10",)
        userprofile.card_titular = "Pepito 123"

        self.book = Ebook.objects.create(
            ebook_number="74564",
            title="Don Quijote",
            autor="Miguel de Cervantes",
            description="",
            is_promot=False,
            size=2,
            media_type="pdf",
        )

        self.forum = Forum.objects.create(
            ebook=self.book,
            user=self.user,
            email=self.user.email,
            topic='test',
            description='test',
            link='test',
        )

        self.forum.save()
        self.book.save()

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_forumdetail_page_url(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')
        response = self.client.get("/ebookdetail/" + str(self.book.id)+"/forum/"+str(self.forum.id)+"/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/forumdetail.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_forumdetail_page_view_name(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')
        response = self.client.get(
            reverse("forumdetail", kwargs={'book_k': self.book.id,'forum_k':self.forum.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/forumdetail.html")


    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_forum_message(self):
        self.client.login(username=self.user.username, password='xTu<3D\R')

        comment = 'test'
        comments = self.forum.discussion_set.count()
        response = self.client.post(reverse("forumdetail", kwargs={'book_k': self.book.id,'forum_k':self.forum.id}),
                                    data={'discuss': comment})

        new_comments = self.forum.discussion_set.count()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(comments < new_comments)
        self.assertTrue(self.forum.discussion_set.all()[new_comments - 1].user == self.user)
        self.assertTrue(self.forum.discussion_set.all()[new_comments - 1].discuss == comment)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_forum_message_not_authenticated(self):
        comment = 'test'
        comments = self.forum.discussion_set.count()
        self.client.post(reverse("forumdetail", kwargs={'book_k': self.book.id, 'forum_k': self.forum.id}),
                                    data={'discuss': comment})
        new_comments = self.forum.discussion_set.count()

        self.assertTrue(comments == new_comments)




class SupportPageTesting(TestCase):
    def setUp(self) -> None:
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
    def test_supportpage_page_url(self):
        self.client.login(username=self.user.username, password="xTu<3D\R")
        response = self.client.get("/tickets/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/support_page.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_supportpage_page_view_name(self):
        self.client.login(username=self.user.username, password="xTu<3D\R")
        response = self.client.get(reverse("support_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/support_page.html")

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_supportpage_page_url_not_authenticated(self):

        response = self.client.get("/tickets/")
        self.assertEqual(response.status_code, 302)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_supportpage_page_view_not_authenticated_name(self):

        response = self.client.get(reverse("support_page"))
        self.assertEqual(response.status_code, 302)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_ticket(self):
        self.client.login(username=self.user.username, password="xTu<3D\R")
        ticket_title = "test"
        ticket_summary = "test"
        tickets = UserTickets.objects.count()
        response = self.client.post(
            reverse("support_page"),
            data={
                "ticket_title": ticket_title,
                "ticket_summary": ticket_summary
            },
        )

        new_tickets = UserTickets.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(tickets < new_tickets)
        self.assertTrue(UserTickets.objects.all()[new_tickets -
                                                  1].ticket_user == self.user)
        self.assertTrue(
            UserTickets.objects.all()[new_tickets -
                                      1].ticket_title == ticket_title)
        self.assertTrue(
            UserTickets.objects.all()[new_tickets -
                                      1].ticket_summary == ticket_summary)

    @override_settings(STATICFILES_STORAGE=
                       "django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_create_ticket_not_authenticated(self):

        ticket_title = "test"
        ticket_summary = "test"
        tickets = UserTickets.objects.count()
        self.client.post(
            reverse("support_page"),
            data={
                "ticket_title": ticket_title,
                "ticket_summary": ticket_summary
            },
        )

        new_tickets = UserTickets.objects.count()

        self.assertTrue(tickets == new_tickets)


class page404Testing(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test404(self):
        response = self.client.get("/randomlink/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name="scribd/404.html")