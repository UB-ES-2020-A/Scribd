from django.test import TestCase, Client
from django.urls import reverse
from .urls import urlpatterns
from .models import Ebook
from .user_models import User
import json


class TestViews(TestCase):

    def setUp(self):
        pass

    def test_mainpage_GET(self):
        c = Client()
        response = c.get(reverse('index'))
        print(response)
        self.assertEquals(response.status_code, 200)
