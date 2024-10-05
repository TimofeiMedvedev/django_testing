from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.models import Note

from .common import SLUG, URL_REVERSE, BaseTest

User = get_user_model()


class TestRoutes(BaseTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=SLUG,
            author=cls.author
        )

    def test_pages_availability_for_all(self):
        user_statuses = (
            (URL_REVERSE.home, self.client, HTTPStatus.OK),
            (URL_REVERSE.login, self.client, HTTPStatus.OK),
            (URL_REVERSE.logout, self.client, HTTPStatus.OK),
            (URL_REVERSE.login, self.client, HTTPStatus.OK),
            (URL_REVERSE.signup, self.client, HTTPStatus.OK),
            (URL_REVERSE.add, self.not_author_client, HTTPStatus.OK),
            (URL_REVERSE.success, self.not_author_client, HTTPStatus.OK),
            (URL_REVERSE.list, self.not_author_client, HTTPStatus.OK),
            (URL_REVERSE.detail, self.author_client, HTTPStatus.OK),
            (URL_REVERSE.edit, self.author_client, HTTPStatus.OK),
            (URL_REVERSE.delete, self.author_client, HTTPStatus.OK),
            (URL_REVERSE.detail, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_REVERSE.edit, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_REVERSE.delete, self.not_author_client, HTTPStatus.NOT_FOUND),
        )

        for url, user, status in user_statuses:
            with self.subTest(url=url, user=user, status=status):
                response = user.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            (URL_REVERSE.detail),
            (URL_REVERSE.edit),
            (URL_REVERSE.delete),
            (URL_REVERSE.add),
            (URL_REVERSE.success),
            (URL_REVERSE.list),
        )

        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{URL_REVERSE.login}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
