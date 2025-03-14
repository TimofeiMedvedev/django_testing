# Проект Django testing

## Описание проекта
Коллекция тестов для проектов YaNews и YaNote на pytest и unittest соответственно.
***
## Тесты на pytest для проекта YaNews
### test_routes.py:
- Главная страница доступна анонимному пользователю.
- Страница отдельной новости доступна анонимному пользователю.
- Страницы удаления и редактирования комментария доступны автору комментария.
- При попытке перейти на страницу редактирования или удаления комментария анонимный пользователь перенаправляется на страницу авторизации.
- Авторизованный пользователь не может зайти на страницы редактирования или удаления чужих комментариев (возвращается ошибка 404).
- Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны анонимным пользователям.

### test_content.py:
- Количество новостей на главной странице — не более 10.
- Новости отсортированы от самой свежей к самой старой. Свежие новости в начале списка.
- Комментарии на странице отдельной новости отсортированы в хронологическом порядке: старые в начале списка, новые — в конце.
- Анонимному пользователю недоступна форма для отправки комментария на странице отдельной новости, а авторизованному доступна.

### test_logic.py:
- Анонимный пользователь не может отправить комментарий.
- Авторизованный пользователь может отправить комментарий.
- Если комментарий содержит запрещённые слова, он не будет опубликован, а форма вернёт ошибку.
- Авторизованный пользователь может редактировать или удалять свои комментарии.
- Авторизованный пользователь не может редактировать или удалять чужие комментарии.

## Тесты на unittest для проекта YaNote
### test_routes.py:
- Главная страница доступна анонимному пользователю.
- Аутентифицированному пользователю доступна страница со списком заметок notes/, страница успешного добавления заметки done/, страница добавления новой заметки add/.
- Страницы отдельной заметки, удаления и редактирования заметки доступны только автору заметки. Если на эти страницы попытается зайти другой пользователь — вернётся ошибка 404.
- При попытке перейти на страницу списка заметок, страницу успешного добавления записи, страницу добавления заметки, отдельной заметки, редактирования или удаления заметки анонимный пользователь перенаправляется на страницу логина.
- Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям.

### test_content.py:
- Отдельная заметка передаётся на страницу со списком заметок в списке object_list в словаре context;
- В список заметок одного пользователя не попадают заметки другого пользователя;
- На страницы создания и редактирования заметки передаются формы.

### test_logic.py:
- Залогиненный пользователь может создать заметку, а анонимный — не может.
- Невозможно создать две заметки с одинаковым slug.
- Если при создании заметки не заполнен slug, то он формируется автоматически, с помощью функции pytils.translit.slugify.
- Пользователь может редактировать и удалять свои заметки, но не может редактировать или удалять чужие.

### Технологии
- Python 
- Django
- DRF
- Pytest
- Unittest
***
## Запуск проекта 
* Клонировать репозиторий:
```
git clone git@github.com:TimofeiMedvedev/django_testing.git
```
* Установите и активируйте виртуальное окружение
```
cd django_testing
python3 -m venv venv
source venv/bin/activate
```
* Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
* Выполнить миграции:
```
python3 ya_news/manage.py migrate
python3 ya_note/manage.py migrate
```
* Загрузить фикстуры DB для ya_news:
```
python3 ya_news/manage.py loaddata ya_news/news/fixtures/news.json
```
* Перейти в папку необходимого проекта. Запустить тесты для проектов:
```
# YaNews
cd ../ya_news
pytest

# YaNote
cd ../ya_note
pytest
```
