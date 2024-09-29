# Лабораторная 3

## Задание

Поднять kubernetes кластер локально (например minikube), в нём развернуть свой сервис, используя 2-3 ресурса kubernetes. В идеале разворачивать кодом из yaml файлов одной командой запуска. Показать работоспособность сервиса.

(сервис любой из своих не опенсорсных, вывод “hello world” в браузер тоже подойдёт)

## Ход работы


Для выполнения работы было необходимо установить kubectl и minikube.

```
sudo pacman -Sy kubectl

sudo pacman -S minikube
```

Было принято решение реализовать вывод html-страницы в браузере.

Сначала было необходимо создать ресурс `ConfigMap`, который используется для хранения конфигурационных данных, в нашем случае - html-файла.

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: html-configmap
data:
  index.html: |
    <html>
      <head>
        <meta charset="UTF-8">
        <title>It is a sad hamster</title>
        <style>
           body {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin: 0;
                font-family: 'Arial', sans-serif;
                background-color: #fc88a3;
                height: 100vh;
           }
           h1 {
                color: white;
           }
      </style>
      </head>
      <body>
        <h1>Wanna see a sad hamster?</h1>
        <h1> ʢٛ•ꇵٛ•ʡ </h1>
        <h1> Here it is (hihihaha в этот раз без картинки it's a prank)</h1>
      </body>
    </html>
```

Для `ConfigMap` было установлено имя `http-configmap`. В разделе `data` указаны имя html-файла — `index.html` и его содержимое — всё, что идет после `|` ))). 

При создании файла  ~~у нас возникли~~ могут возникать проблемы с несоблюдением разметки, поэтому важно помнить, что для каждого уровня вложенных тегов используется отступ в два пробела.

Далее было необходимо развернуть созданный `ConfigMap`.
```
kubectl apply -f /home/plioyee/sadhamster_project/html-configmap.yaml
```

Также был создан объект Deployment — он управляет запуском и обновлением подов.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 1
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.26.2
        ports:
        - containerPort: 80
        volumeMounts:
        - name: html-volume
          mountPath: /usr/share/nginx/html
      volumes:
      - name: html-volume
        configMap:
          name: html-configmap
```
Рассмотрим подробнее:
1. В начале файла определены API-версия, используемая для работы с объектами в kubernetes (в данном случае это `apps/v1`), а также типа объекта — `Deployment`.
2. В разделе  `metadata` указано имя ресурса, под которым он будет идентифицироваться в кластере - ` nginx-deployment`.
3. В разделе `spec` содержится основная конфигурация ресурса. Метка `app: nginx` указывает, что все поды с данной меткой будут управляться этим `Deployment`. Параметр `replicas: 1` показывает, что нужно запустить один под с контейнером nginx.
4. В разделе `templates` определяется, какие поды необходимо создавать. В данном случае в поде запускается контейнер nginx с образом `nginx:1.26.2`; для обрабоки http-запросов открывается порт 80.
5. Также в контейнер монтируется вольюм `html-volume`, который создан на основе `ConfigMap`, для хранения и загрузки HTML-файлов для nginx. Таким образом, вместо стандартных файлов, хранящихся в контейнере, nginx будет использовать файлы из `ConfigMap`.

Созданный `Deployment` был развернут.
```
kubectl apply -f /home/plioyee/sadhamster_project/deployment.yaml
```
Для того чтобы применить новые изменения (например, при изменении содержимого в `ConfigMap`) без изменения самого ресурса `Deployment`, под перезапускался.

```
kubectl rollout restart deployment/nginx-deployment
```

Далее был создан ресурс `Service` для доступа к nginx через внешний порт. 

```
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30007
```

Данный сервис открывает доступ снаружи через порт `30007`.

```
kubectl apply -f /home/plioyee/sadhamster_project/nginx-service.yaml
```


Чтобы проверить работоспособность сервиса, было необходимо узнать ip-адрес Minikube, где был запущен кластер.
```
minikube ip
```

При вводе `http://192.168.49.2:30007/` в браузере открывается наша красивая розовая html-страница. Успех!!

![image](https://github.com/user-attachments/assets/0aa62832-975d-4af9-b7d2-d587476c2321)
