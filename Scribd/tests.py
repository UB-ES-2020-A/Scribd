# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase

from Scribd.models import Ebook, UploadedResources
from Scribd.user_model import User


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


class UploadFilesTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            email='pepito123@gmail.com',
            username='pepito123',
            first_name='Pepito',
            last_name='123',
            subs_type='Free Trial',
            password='xTu<3D\R'
        )
        uf = UploadedResources.objects.create(title='MyStory', user=user, visibility='public',
                             featured_photo='images/HP3.jpg', file='uploads/LoremIpsum.pdf')

    def test_uploadedFile_search(self):
        uf = UploadedResources.objects.get(title='MyStory')
        self.assertEqual(uf.user.username, 'pepito123')
        self.assertEqual(uf.visibility, 'public')
        self.assertEqual(uf.featured_photo, 'images/HP3.jpg')
        self.assertEqual(uf.file, 'uploads/LoremIpsum.pdf')

    def delete_uploadedFile(self):
        uf = UploadedResources.objects.get(title='MyStory')
        uf.delete()
        self.assertEqual(uf, '')