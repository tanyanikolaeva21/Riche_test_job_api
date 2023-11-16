# Тестовое задание по api 

 

## Описание задания

 

Задание разделено на 2 пункта.

Основная задача состоит в том , чтоб достать данные с сайта
 
Retail CRM -> После чего очистить их -> Отправить на запись в базу данных чрез API

Метод который нужно использовать для получения данных 

https://docs.retailcrm.ru/Developers/API/APIVersions/APIv5#get--api-v5-orders

Метод куда нужно записывать 

http://94.&&&.143.164:8000/site/add_site_items/

Документация к принимающему API

http://94.&&&.143.164:8000/docs


Вторая часть состоит в том что у метода orders (retailcrm) есть пагинация 
Суть задачи состоит в том чтоб выгрузить сразу большой объём данных ( условно за месяц ) и так же передать и в базу

Успешным выполнением запроса считается response от принимающего Api


{
  "status": true,
  "message": "Создано - 7 повторения - 0 за 00:00:00.007"
}


Весь получившийся код передавать по средствам удаленного репозитория (GitHub , GitLab ) на выбор

 

## Как запустить проект: 

 

Клонировать репозиторий и перейти в него в командной строке: 

 

``` 

git clone git@github.com:tanyanikolaeva21/Riche_test_job_api.git

``` 

 

``` 

cd Riche_test_job_api

``` 

 

Cоздать и активировать виртуальное окружение: 

 

``` 

python -m venv env 

``` 

Для Windows:

``` 

source venv/Scripts/activate 

``` 

Для Linux:

``` 

source env/bin/activate

``` 

для получения данных с api источника запустить файл get_data.py

``` 

для отправки полученных данных на принимающий api запустить файл send_data.py

``` 

## Credits

- Николаева Татьяна - https://github.com/tanyanikolaeva21
