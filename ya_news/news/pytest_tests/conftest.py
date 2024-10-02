import pytest
from django.test.client import Client
from news.models import Comment, News
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'


@pytest.fixture
def new_comment_text():
    return NEW_COMMENT_TEXT


@pytest.fixture
def comment_text():
    return COMMENT_TEXT


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXT
    )
    return comment


@pytest.fixture
def id_for_args(news):
    return (news.id,)


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comments(news, author):
    now = timezone.now()
    for index in range(10):
        comments = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comments.created = now + timedelta(days=index)
        comments.save()
    return comments


@pytest.fixture
def form_data():
    return {
        'text': COMMENT_TEXT,
    }
