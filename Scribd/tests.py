# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase

from Scribd.models import Ebook


class EbookTestCase(TestCase):
    def setUp(self):
        Ebook.objects.create(ebook_number="74564", title="Don Quijote", autor="Miguel de Cervantes", description="",
                             is_promot=False, size=2, media_type="pdf")

    def test_ebook_search(self):
        quijote = Ebook.objects.get(title="Don Quijote")
        self.assertEqual(quijote.autor, 'Miguel de Cervantes')
        self.assertEqual(quijote.is_promot, False)

    def delete_book(self):
        quijote = Ebook.objects.get(title="Don Quijote")
        quijote.delete()
        self.assertEqual(quijote, '')


class UserTestCase(TestCase):

    def test_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='pepito123@gmail.com',
            username='pepito123',
            first_name='Pepito',
            last_name='123',
            subs_type='Free Trial',
            password='xTu<3D\R'
        )

        self.assertEqual(user.email, 'pepito123@gmail.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
