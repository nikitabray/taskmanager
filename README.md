# Web-приложение для контроля списка задач

### Установка

Для поднятия сервера вам потребуется [docker](https://www.docker.com) и [docker-compose](https://docs.docker.com/compose/install/).

Скопируйте репозиторий и перейдите в созданную папку с проектом. 
Создайте необходимые образы, выполнив «сборку»
```console
user@host:~$ docker-compose build
```
Далее, попробуйте поднять сервер. 
```console
user@host:~$ docker-compose up
```

Обычно, при первом запуске, postgresql инициализирует необходимую ему директорию дольше, чем запускается сервер Django. 

Поэтому, если в консоли написано что-то подобное тексту на скриншоте ниже, то дождитесь сообщения database system is ready to accept connections, остановите выполнение команды и запустите заново.  
![alt text](https://i.ibb.co/jLyVmMb/Screenshot-2021-06-20-at-20-57-21.png "Ошибка подключения к Postgresql")

В случае успешного выполнения команды, вы увидите что-то подобное  
![alt text](https://i.ibb.co/31gZx37/Screenshot-2021-06-20-at-21-01-51.png "Сервер успешно запущен")

Теперь сервер доступен вам по адресу 0.0.0.0:8000  
![alt text](https://i.ibb.co/m8BRDQr/Screenshot-2021-06-20-at-22-52-58.png "Главная страничка в браузере")  
Для начального заполнения приложения данными, я рекомендую сначала перейти в импорт из CVS, что находится справа на верхнем блоке навигации, и выбрать файл csv/example.csv из директории проекта. Он содержит в себе 30 случайно сгенерированных задач, 3 категории и 7 тэгов. Также вы можете сгенерировать данные, перейдя по соответствующей ссылке в меню навигации, после чего экспортировать все задачи в CSV. Не рекомендуется вводить слишком большое значение, т.к. генерация занимает некоторое время. 200-1000 нормальные значения.

Приложение поддерживает фильтрацию задач по категориям/тэгам. Для этого нажмите на интересущую вас категорию/тэг в соответствующем списке из меню навигации. 

Для задач/категорий/тэгов доступно удаление всех записей. Ссылка находится сверху на каждой из соответствующих страниц. 




### TODO

- [x] Написать базовый функционал.
- [ ] Использовать NginX + gunicorn для размещения приложения.
- [ ] Добавить мануал на английском.
- [ ] Базовая документация
- [ ] Выводить нормальную пагинацию.
- [ ] Оптимиизация. Каждя страница списка грузится дольше, чем должно быть, т.к. запрашивается весь список для пагинатора.
- [ ] Сделать красивый фронтенд. 
- [ ] Использовать другие средства для автоматического запуска makemigrations и migrate.
- [ ] Добавить возможность интерпретации архивированнной строки с данными об истории изменений в объект HistoricalTask.
- [ ] Поддержка тэгов историей изменений.