from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from account.models import User , Profile


class SpecialTestCase(TestCase):
    def casual_template_test(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,f'{self.login_url}?next={self.url}')

        self.user = User.objects.create_user(phone_number='09123456789')
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)
        self.assertTemplateUsed(self.response,self.template)


class TestProfileView(SpecialTestCase):
    def setUp(self) -> None:
        self.login_url = reverse('account:login-page')
        self.url = reverse('account:profile-page')
        self.template = 'profile.html'


    def test_get_method_profile(self):
        super().casual_template_test()
        profile = Profile.objects.get(user=self.user)

        self.assertEqual(self.response.context['user'],self.user)
        self.assertEqual(self.response.context['profile'],profile)


class TestProfileSideBarView(SpecialTestCase):
    def setUp(self) -> None:
        self.login_url = reverse('account:login-page')
        self.url = reverse('account:profile-sidebar')
        self.template = 'layout/profile-sidebar.html'


    def test_get_method_profile(self):
        super().casual_template_test()
        profile = Profile.objects.get(user=self.user)

        self.assertEqual(self.response.context['user'],self.user)
        self.assertEqual(self.response.context['profile'],profile)


class TestProfileAddInfoView(SpecialTestCase):
    def setUp(self) -> None:
        self.login_url = reverse('account:login-page')
        self.url = reverse('account:profile-add-info-page')
        self.success_url = reverse('account:profile-page')
        self.template = 'profile-additional-info.html'
        self.test_user = User.objects.create_user(phone_number='09123456788')


    def test_get_method_profile(self):
        super().casual_template_test()
        profile = Profile.objects.get(user=self.user)

        self.assertEqual(self.response.context['profile'],profile)

    def test_post_method_logout_user(self):
        response = self.client.post(self.url)
        self.assertRedirects(response,f'{self.login_url}?next={self.url}')

    def test_post_method_no_profile(self):
        self.client.force_login(self.test_user)
        Profile.objects.filter(user=self.test_user).delete()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code,404)
        self.assertTemplateUsed(response,'404.html')

    def test_post_method_empty_data(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertRedirects(response,self.url)

    def test_post_method_wrong_data(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url,data={'email':'1'})
        self.assertRedirects(response,self.url)

    def test_post_method_right_data(self):
        self.client.force_login(self.test_user)
        profile_data = {
            'full_name' : 'e',
            'email' : 'test@gmail.com',
            'address' : 'e',
            'postalcode' : '1',
            'birth_date' : '2021-1-1',
            'recive_newsletter': '1',
            'recive_events': '1',
        }

        response = self.client.post(self.url,data=profile_data)
        new_email = Profile.objects.get(user=self.test_user).email

        self.assertRedirects(response,self.success_url)
        self.assertEqual(new_email,'test@gmail.com')

