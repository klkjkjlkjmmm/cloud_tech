# Лабораторная работа 3 (со звездочкой)

## Задание

1. Создать helm chart на основе обычной 3 лабы
2. Задеплоить его в кластер
3. Поменять что-то в сервисе, задеплоить новую версию при помощи апгрейда релиза
4. В отчете приложить скрины всего процесса, все использованные файлы, а также привести три причины, по которым использовать хелм удобнее чем классический деплой через кубернетес манифесты

## Ход работы

Сначала было необходимо установить `helm` на нашу любимую Manjaro

```
sudo pacman -Sy helm
```

![image](https://github.com/user-attachments/assets/863c8983-5de0-4c7d-ba4d-31965a451052)

`helm` был установлен!!!

Далее был создан helm-chart.

```
apiVersion: v2
name: sadhamsterhelm
description: Helm Chart for sadhamster.com
type: application
version: 0.1.0
appVersion: "1.26.2"
```

После этого на основе лабораторной работы №3 был заполнен  `values.yaml`.

```
replicaCount: 1 

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.26.2"

service:
  type: NodePort
  port: 80
  targetPort: 80
  nodePort: 30008


volumes:
  name: html-volume2
  configMapName: configmap 
  mountPath: /usr/share/nginx/html


htmlConfigMapData: |
  <html><body><h1>HELLO WORLD !!11!1!1!1!1!!!!!!!!</h1></body></html>
```

Также в  `deployment.yaml`, `service.yaml` и `configMap.yaml ` была произведена замена значений на ссылки из `values.yaml`.

После этого было необходимо запустить релиз, но у нас снова возникли проблемы с пробелами в html-документе. ~Мы горько-горько плакали, а потом решили убрать отступы вообще))))~

Созданный `helm chart` был задеплоен в кластер. В браузере открылась html-страница с текстом.
![image](https://github.com/user-attachments/assets/a600dcac-b860-4ebb-a5d8-bdb0877aa9cc)

Далее было необходимо сделать какие-то изменения и задеплоить новую версию, поэтому было изменено содержимое html-файла.
```
htmlConfigMapData: |
  <html><body><h1>meow meow meow meow (we've been doing this upgrade for the millionth time and we're on the verge of tears rn)</h1></body></html>
```

С помощью команды 'helm upgrade` была задеплоена новая версия.
![image](https://github.com/user-attachments/assets/991a17d7-9893-45fb-a858-d7a764c97a1e)

Можно увидеть, что текст на страничке сменился.
![image](https://github.com/user-attachments/assets/8cd358a2-4847-4382-b3e5-02c459a3dbd7)

#### Почему helm использовать удобнее, чем кубернетес манифесты?

1. В helm-чартах можно создавать файлы-шаблоны с переменными и использовать их в манифестах, что позволяет легко управлять параметрами (например, количеством версий, используемыми портами, версиями) через `values.yaml` без необходимости вручную изменять каждый манифест.
2. Helm поддерживает версионирование, что позволяет легко апрейднуться на новую версию (`helm upgrade`) или откатиться на старую при необходимости (`helm rollback`) без ручного изменения манифестов.
3. Благодаря шаблонизации, Helm позволяет повторно использовать чарты. Также с помощью условных конструкций их можно настраивать динамически.



