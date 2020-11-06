# Create your tests here.
from django.test import TestCase
from Scribd.models import Ebook

class EbookTestCase(TestCase):
    def setUp(self):
        Ebook.objects.create(title="Don Quijote", autor="Miguel de Cervantes", description="", is_promot=False,size=2,media_type="pdf")

    def test_ebook_can_create(self):
        quijote = Ebook.objects.get(title="Don Quijote")
        self.assertEqual(quijote.autor, 'Miguel de Cervantes')
        self.assertEqual(quijote.is_promot, False)
