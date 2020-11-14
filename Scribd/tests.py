# Create your tests here.
from django.test import TestCase
from Scribd.models import Ebook
from Scribd.user_model import User

from django.contrib.auth import get_user_model


class EbookTestCase(TestCase):
    def setUp(self):
        Ebook.objects.create(ebook_number="74564",title="Don Quijote", autor="Miguel de Cervantes", description="", is_promot=False,size=2,media_type="pdf")

    def test_ebook_search(self):
        quijote = Ebook.objects.get(title="Don Quijote")
        print(quijote.autor)
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
            user_type='provider',
            subs_type='Free Trial',
            card_titular='',
            card_number='',
            card_expiration='',
            card_cvv='',
            password='xTu<3D\R'
        )

        self.assertEqual(user.email, 'pepito123@gmail.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
