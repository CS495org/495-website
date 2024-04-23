from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import CustomUser, Show, Movie
from django.contrib.auth.forms import AuthenticationForm
from .forms import (RegistrationForm, UserPasswordResetForm, UserSetPasswordForm,
                            UserPasswordChangeForm, FavMoviesForm, FavShowsForm)
from accounts.models import CustomUser, Movie, Show
from django.urls import reverse


class RegistrationFormTestCase(TestCase):
    def test_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test1234',
            'password2': 'test1234',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test1234',
            'password2': 'differentpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class LoginFormTestCase(TestCase):
    def test_login_form_valid(self):
        form_data = {'username': 'testuser', 'password': 'test1234'}
        form = AuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {'username': 'testuser', 'password': 'wrongpassword'}
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

class UserPasswordResetFormTestCase(TestCase):
    def test_password_reset_form_valid(self):
        form_data = {'email': 'test@example.com'}
        form = UserPasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_reset_form_invalid(self):
        form_data = {'email': 'invalidemail'}
        form = UserPasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class UserSetPasswordFormTestCase(TestCase):
    def test_set_password_form_valid(self):
        form_data = {'new_password1': 'newpassword123', 'new_password2': 'newpassword123'}
        form = UserSetPasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_set_password_form_invalid(self):
        form_data = {'new_password1': 'newpassword123', 'new_password2': 'differentpassword'}
        form = UserSetPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors)

class UserPasswordChangeFormTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser',
                                                   email='test@example.com',
                                                   password='oldpassword')

    def test_password_change_form_valid(self):
        form_data = {
            'old_password': 'oldpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
            }

        form = UserPasswordChangeForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_change_form_invalid(self):
        form_data = {'old_password': 'wrongpassword',
                     'new_password1': 'newpassword123',
                     'new_password2': 'newpassword123'}
        form = UserPasswordChangeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)

class FavMoviesFormTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser',
                                                   email='test@example.com',
                                                   password='test1234')

        self.movie = Movie.objects.create(title='Test Movie')

    def test_fav_movies_form_valid(self):
        form_data = {'fav_movies': [self.movie.id]}
        form = FavMoviesForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_fav_movies_form_invalid(self):
        form_data = {'fav_movies': ['invalid_id']}
        form = FavMoviesForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fav_movies', form.errors)

class FavShowsFormTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser',
                                                   email='test@example.com',
                                                   password='test1234')

        self.show = Show.objects.create(title='Test Show')

    def test_fav_shows_form_valid(self):
        form_data = {'fav_shows': [self.show.id]}
        form = FavShowsForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_fav_shows_form_invalid(self):
        form_data = {'fav_shows': ['invalid_id']}
        form = FavShowsForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fav_shows', form.errors)



class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        self.show = Show.objects.create(title='Test Show', vote_count=100)
        self.movie = Movie.objects.create(title='Test Movie')

        self.client.login(username='testuser', password='12345')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('all_shows', response.context)
        self.assertIn('all_movies', response.context)
        self.assertIn('top_ten_shows', response.context)

    def test_redirect_by_user_id(self):
        response = self.client.get(reverse('redirect_by_user_id'))
        self.assertEqual(response.status_code, 302)