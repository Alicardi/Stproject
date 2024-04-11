# Проект Saint Tropez

## Описание

Этот проект написан на языке Python и представляет собой сайт солярием Saint Tropez.  
На сайте несколько страниц со своим функционалом.  
На данный момент пользователь может зарегистрироваться/авторизироваться, просмотреть товары и информацию о соляриях.  
Сайт написан с использованием Django, Python, HTML, CSS и JS.

## Установка

Для начала работы с проектом выполните следующие шаги:

1. Убедитесь, что на вашем компьютере установлен [Python](https://www.python.org/downloads/). Если его нет, скачайте и установите Python с [официального сайта Python](https://www.python.org/downloads/).
2. Склонируйте репозиторий проекта на свой локальный компьютер.
3. Создайте виртуальное окружение. Для этого выполните следующие команды в терминале:

   ```
   python -m venv venv
   ```


3. Активируйте виртуальное окружение:

    - В Windows (cmd):
    ```
    venv\Scripts\activate
    ```

    - В macOS и Linux:
    ```
    source venv/bin/activate
    ```

## Установка библиотек 

``` 
pip install django
pip install Pillow
```

## Запуск

После установки зависимостей вы можете запустить проект. Для этого выполните следующие команды:

```
python manage.py runserver
```

После этого проект будет доступен по адресу http://127.0.0.1:8000/ в вашем веб-браузере.



