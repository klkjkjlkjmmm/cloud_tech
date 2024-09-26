# Лабораторная №1

## Задание

Настроить nginx по заданному тз:
  1. Должен работать по https c сертификатом
  2. Настроить принудительное перенаправление HTTP-запросов (порт 80) на HTTPS (порт 443) для обеспечения безопасного соединения
  3. Использовать alias для создания псевдонимов путей к файлам или каталогам на сервере
  4. Настроить виртуальные хосты для обслуживания нескольких доменных имен на одном сервере
  5. Что угодно еще под требования проекта
**Результат:** Предположим, что у вас есть два пет проекта на одном сервере, которые должны быть доступны по https. Настроенный вами веб сервер умеет работать по https, относить нужный запрос к нужному проекту, переопределять пути исходя из требований пет проектов.
В качестве пет проектов можете использовать что-то свое, можете что-то опенсорсное, можете просто код из трех строчек как например здесь
Важно: В этой лабе прошу вас не углубляться в безопасность nginx, тк так будет интереснее делать лабу со звездочкой)

## Ход работы

~~Сначала мы долго пытались обновить линукс...очень долго...и очень страшно...~~

Были созданы два виртуальных хоста — sadhamster.com и happygiraffe.ru, информация о которых была добавлена в /etc/hosts
```

127.0.1.1  sadhamster.com
127.0.1.1  happygiraffe.ru

```
В конфигурационном файле Nginx'а была добавлена строка ```include /etc/nginx/sites-enabled/*.conf;```, которая отвечает за просмотр всех конфигурационых файлов в директории sites-enabled с расширением .conf, тем самым "показывая" Nginx'у, что доступные блоки server находятся в ней. 
Для каждого виртуального хоста были созданы простые HTML-страницы.
В директории sites-enabled хранятся все виртуальные хосты, которые есть на локальной машине. Директория sites-available хранит в себе те сайты, которые должны обслуживаться Nginx.

После этого были созданы символические ссылки на конфигурационные файлы виртуальных хостов из директории sites-enabled в sites-available.
```

sudo ln -s /etc/nginx/sites-available/sadhamster.com.conf /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/happygiraffe.ru.conf /etc/nginx/sites-enabled

```

Чтобы настроить соединение по HTTPS, для каждого хоста были созданы самоподписанные сертификаты.
```

mkdir /etc/nginx/ssl
cd /etc/nginx/ssl

#для первого хоста
openssl req -new -x509 -nodes -newkey rsa:4096 -keyout happygiraffe.key -out happygiraffe.crt -days 1095
chmod 400 happygiraffe.key #чтение только владельцем
chmod 444 happygiraffe.crt #чтение всеми пользователями

#для второго хоста
openssl req -new -x509 -nodes -newkey rsa:4096 -keyout sadhamster.key -out sadhamster.crt -days 1095
chmod 400 sadhamster.key 
chmod 444 sadhamster.crt

```
В конфигурационных файлах каждого хоста было настроено принудительное перенаправление HTTP-запросов (порт 80) на HTTPS (порт 443).
```

#для первого хоста
server {
  listen 80;
  server_name happygiraffe.ru www.happygiraffe.ru;
  return 301 https://happygiraffe.ru$request_uri;
}
server {
    listen 443 ssl;
    server_name happygiraffe.ru www.happygiraffe.ru;
    ssl_certificate /etc/nginx/ssl/happygiraffe.crt; #используем самоподписанный сертификат для доступа по HTTPS
    ssl_certificate_key /etc/nginx/ssl/happygiraffe.key;
    root /srv/www/happygiraffe.ru;
    index index.html;

    access_log /var/log/nginx/happygiraffe.ru.access.log; #храним логи получения успешного доступа к сайту
    error_log /var/log/nginx/happygiraffe.ru.error.log; #храним логи выпавших ошибок

    location / {
#        try_files $uri $uri/ =404;
        root /srv/www/happygiraffe.ru;
        index index.html index.htm;
   }
}

```
Аналогично был создан кофигурационный файл для второго виртуального хоста.
```

#для второго хоста
server {
  listen 80;
  server_name sadhamster.com www.sadhamster.com;
  return 301 https://sadhamster.com$request_uri;
}

server {
    listen 443 ssl;
    server_name sadhamster.com www.sadhamster.com;
    ssl_certificate /etc/nginx/ssl/sadhamster.crt;
    ssl_certificate_key /etc/nginx/ssl/sadhamster.key;
    root  /srv/www/sadhamster.com;
    index index.html;

    access_log /var/log/nginx/sadhamster.com.access.log;
    error_log /var/log/nginx/sadhamster.com.error.log;

    location /{
        root /srv/www/sadhamster.com;
        index index.html index.htm;
    }
}
```
Для создания псевдонимов путей к файлам или каталогам на сервере использовались алиасы.
```

# для первого хоста
location /static/ {
        alias /srv/www/happygiraffe.ru/images/;

# для второго хоста
location /hamster/{
	alias /srv/www/sadhamster.com/images/;

```

При открытии страницы sadhamster.com в браузере открывается простая html-страница. Можно увидеть, что соединение происходит по протоколу HTTPS.

![image](https://github.com/user-attachments/assets/a39158f6-2511-44b0-8ab9-bc456c2ef67d)

Если открыть картинку в новой вкладке, можно заметить, что для отображения пути использовался установленный алиас.

![image](https://github.com/user-attachments/assets/a66c5e08-aac6-4773-b00c-70746ef92876)

Аналогично с хостом happygiraffe.ru.

![image](https://github.com/user-attachments/assets/a15334f1-264b-460b-af99-613ee82971d6)

![image](https://github.com/user-attachments/assets/595299b1-cadf-417e-94f5-704690d69e4e)

