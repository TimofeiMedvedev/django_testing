from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .common import URL_REVERSE, BaseTest

User = get_user_model()


class TestNoteCreation(BaseTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }

    def creates_notes(self):
        self.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='note-slug',
            author=self.author,
        )
        return self.notes

    def test_user_can_create_note(self):
        Note.objects.all().delete
        response = self.author_client.post(
            URL_REVERSE.add,
            data=self.form_data
        )
        self.assertRedirects(response, URL_REVERSE.success)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        object_count_before = Note.objects.count()
        response = self.client.post(URL_REVERSE.add, data=self.form_data)
        self.expected_url = f'{URL_REVERSE.login}?next={URL_REVERSE.add}'
        self.assertRedirects(response, self.expected_url)
        self.assertEqual(Note.objects.count(), object_count_before)

    def test_not_unique_slug(self):
        note = self.creates_notes()
        self.form_data['slug'] = note.slug
        response = self.author_client.post(
            URL_REVERSE.add,
            data=self.form_data
        )
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=(note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        response = self.author_client.post(
            URL_REVERSE.add,
            data=self.form_data)
        self.assertRedirects(response, URL_REVERSE.success)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        note = self.creates_notes()
        self.response = self.author_client.post(
            URL_REVERSE.edit,
            self.form_data
        )
        self.assertRedirects(self.response, URL_REVERSE.success)
        note.refresh_from_db()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_other_user_cant_edit_note(self):
        note = self.creates_notes()
        response = self.not_author_client.post(
            URL_REVERSE.edit,
            self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=note.id)
        self.assertEqual(note.title, note_from_db.title)
        self.assertEqual(note.text, note_from_db.text)
        self.assertEqual(note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        self.creates_notes()
        response = self.author_client.post(URL_REVERSE.delete)
        self.assertRedirects(response, URL_REVERSE.success)
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        self.creates_notes()
        response = self.not_author_client.post(URL_REVERSE.delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
