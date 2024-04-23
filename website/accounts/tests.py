from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, LoginForm
from .models import Movie, Show, TopRatedShow, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm
from django.contrib.auth.models import User


class SignUpViewTestCase(TestCase):
    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_signup_view_post(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test1234',
            'password2': 'test1234',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))



class LoginViewTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser',
                                             email='test@example.com',
                                             password='test1234')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_view_post_valid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'test1234',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_view_post_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Invalid username or password')


class MovieModelTestCase(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            id='1234567890123456789012345678901234567890',
            title='Test Movie',
            overview='This is a test movie',
            poster_path='/path/to/poster.jpg',
            backdrop_path='/path/to/backdrop.jpg',
            air_date='2023-01-01',
            genres='Action, Comedy',
            vote_count=100,
            vote_average=8.5,
            images_loaded=True
        )

    def test_movie_str(self):
        self.assertEqual(str(self.movie), 'Test Movie')

    def test_movie_to_dict(self):
        movie_dict = self.movie.to_dict()
        self.assertEqual(movie_dict['title'], 'Test Movie')
        self.assertEqual(movie_dict['overview'], 'This is a test movie')
        self.assertEqual(movie_dict['id'], '1234567890123456789012345678901234567890')
        self.assertEqual(movie_dict['poster_path'], '/path/to/poster.jpg')

class ShowModelTestCase(TestCase):
    def setUp(self):
        self.show = Show.objects.create(
            id='1234567890123456789012345678901234567890',
            title='Test Show',
            overview='This is a test show',
            poster_path='/path/to/poster.jpg',
            backdrop_path='/path/to/backdrop.jpg',
            air_date='2023-01-01',
            genres='Drama, Thriller',
            vote_count=200,
            vote_average=9.0,
            images_loaded=False
        )

    def test_show_str(self):
        self.assertEqual(str(self.show), 'Test Show')

    def test_show_to_dict(self):
        show_dict = self.show.to_dict()
        self.assertEqual(show_dict['title'], 'Test Show')
        self.assertEqual(show_dict['overview'], 'This is a test show')
        self.assertEqual(show_dict['id'], '1234567890123456789012345678901234567890')
        self.assertEqual(show_dict['poster_path'], '/path/to/poster.jpg')

class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser',
                                                   email='test@example.com',
                                                   password='test1234')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_add_movie(self):
        movie_id = '1234567890123456789012345678901234567890'
        self.user.add_movie(movie_id)
        self.assertTrue(self.user.fav_movies.filter(id=movie_id).exists())

    def test_add_show(self):
        show_id = '1234567890123456789012345678901234567890'
        self.user.add_show(show_id)
        self.assertTrue(self.user.fav_shows.filter(id=show_id).exists())

    def test_add_top(self):
        top_id = '1234567890123456789012345678901234567890'
        self.user.add_top(top_id)
        self.assertTrue(self.user.fav_top_rated.filter(id=top_id).exists())

    def test_add_comp_show(self):
        show_id = '1234567890123456789012345678901234567890'
        self.user.add_comp_show(show_id)
        self.assertTrue(self.user.comp_shows.filter(id=show_id).exists())

    def test_add_comp_top(self):
        top_id = '1234567890123456789012345678901234567890'
        self.user.add_comp_top(top_id)
        self.assertTrue(self.user.comp_top_rated.filter(id=top_id).exists())




class CustomUserCreationFormTestCase(TestCase):
    def test_clean_username(self):

        existing_user = User.objects.create_user(username='testuser',
                                                 email='test@example.com',
                                                 password='test1234')
        form_data = {
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
            }

        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['This username is already taken.'])

    def test_clean_username_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
            }

        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())



class CustomUserChangeFormTestCase(TestCase):
    def test_form_fields(self):
        form = CustomUserChangeForm()
        self.assertEqual(form.Meta.model, User)
        self.assertEqual(form.Meta.fields, ('username', 'email'))

class LoginFormTestCase(TestCase):
    def test_form_fields(self):
        form = LoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Username')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Password')
