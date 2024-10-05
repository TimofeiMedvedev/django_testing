from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'


def test_anonymous_user_cant_create_comment(client, detail_url, form_data):
    object_count_before = Comment.objects.count()
    client.post(detail_url, data=form_data)
    assert object_count_before == Comment.objects.count()


def test_user_can_create_comment(
        reader_client,
        news,
        form_data,
        reader,
        detail_url):
    Comment.objects.all().delete
    response = reader_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == reader


@pytest.mark.parametrize(
    'bad_words_list',
    (BAD_WORDS)
)
def test_user_cant_use_bad_words(reader_client, detail_url, bad_words_list):
    bad_words_data = {'text': f'Какой-то текст, {bad_words_list}, еще текст'}
    response = reader_client.post(detail_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
        author_client,
        delete_url,
        detail_url):
    response = author_client.delete(delete_url)
    assertRedirects(
        response,
        detail_url + '#comments'
    )
    assert Comment.objects.count() == 0
    assert not Comment.objects.exists()


def test_user_cant_delete_comment_of_another_user(reader_client, delete_url):
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
        author_client,
        form_data,
        news,
        edit_url,
        comment):
    form_data['text'] = NEW_COMMENT_TEXT
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, reverse(
        'news:detail',
        args=(news.id,)) + '#comments')
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
        reader_client,
        author,
        comment,
        form_data,
        edit_url,
        news):
    form_data['text'] = NEW_COMMENT_TEXT
    response = reader_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author
