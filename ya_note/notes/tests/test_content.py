from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.models import Note

from .common import SLUG, URL_REVERSE, BaseTest

User = get_user_model()


class TestContent(BaseTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=SLUG,
            author=cls.author
        )

    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author_client, True),
            (self.not_author_client, False),
        )
        for user, status in users_statuses:
            with self.subTest(user=user):
                response = user.get(URL_REVERSE.list)
                object_list = response.context['object_list']
                self.assertIs((self.notes in object_list), status)

    def test_pages_contains_form(self):
        urls = (
            URL_REVERSE.add,
            URL_REVERSE.edit,
        )

        for name in urls:
            with self.subTest(name=name):
                response = self.author_client.get(name)
                self.assertIsInstance(response.context.get('form'), NoteForm)
