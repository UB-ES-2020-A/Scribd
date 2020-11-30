from django.test import Client, TestCase, override_settings
from django.urls import reverse


class MyTest(TestCase):

    def setUpTestingViews(self):
        self.client = Client()

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_get_base(self):
        response = self.client.get(reverse('base'))

        # 200, OK
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'scribd/base.html')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_get_ebooks(self):
        response = self.client.get(reverse('ebooks'))

        # 200, OK
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'scribd/mainpage.html')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_get_users(self):
        response = self.client.get(reverse('users'))

        # 200, OK
        self.assertEquals(response.status_code, 200)


    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_get_ebooks(self):
        response = self.client.get(reverse('ebooks'))

        # 200, OK
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'scribd/mainpage.html')
