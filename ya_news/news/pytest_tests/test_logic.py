from http import HTTPStatus

import pytest
from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, id_for_args, form_data):
    url = reverse('news:detail', args=id_for_args)
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        reader_client,
        id_for_args,
        form_data,
        news,
        reader):
    url = reverse('news:detail', args=id_for_args)
    response = reader_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == reader


@pytest.mark.django_db
def test_user_cant_use_bad_words(id_for_args, reader_client):
    url = reverse('news:detail', args=id_for_args)
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = reader_client.post(url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, comment, id_for_args):
    url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(url)
    assertRedirects(
        response,
        reverse('news:detail', args=id_for_args) + '#comments'
    )
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(reader_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    response = reader_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
        author_client,
        comment,
        form_data,
        id_for_args):
    form_data['text'] = 'Обновлённый комментарий'
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, reverse(
        'news:detail',
        args=id_for_args) + '#comments')


def test_user_cant_edit_comment_of_another_user(
        reader_client,
        comment,
        form_data,
        comment_text):
    form_data['text'] = 'Обновлённый комментарий'
    url = reverse('news:edit', args=(comment.id,))
    response = reader_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
