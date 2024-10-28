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

Далее был создан `Chart.yaml`

```
apiVersion: v2
name: sadhamsterhelm
description: Helm Chart for sadhamster.com
type: application
version: 0.1.0
appVersion: "1.26.2"
```

После этого на основе лабораторной работы №3 был заполнен  `values.yaml `

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

После этого было необходимо запустить релиз, но у нас снова возникли проблемы с пробелами в html-документе. Мы горько-горько плакали, а потом решили убрать отступы вообще))))

