import pytest
from django.conf import settings
from django.urls import reverse
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, all_news):
    url = reverse('news:home',)
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, all_news):
    url = reverse('news:home',)
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, id_for_args, comments):
    url = reverse('news:detail', args=id_for_args)
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comments.created for comments in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, id_for_args):
    url = reverse('news:detail', args=id_for_args)
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(reader_client, id_for_args):
    url = reverse('news:detail', args=id_for_args)
    response = reader_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
