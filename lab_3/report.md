# Лабораторная 3

## Задание

Поднять kubernetes кластер локально (например minikube), в нём развернуть свой сервис, используя 2-3 ресурса kubernetes. В идеале разворачивать кодом из yaml файлов одной командой запуска. Показать работоспособность сервиса.

(сервис любой из своих не опенсорсных, вывод “hello world” в браузер тоже подойдёт)

## Ход работы

```
sudo pacman -Sy kubectl
```

```
sudo pacman -S minikube
```

```
kubectl apply -f /home/plioyee/sadhamster_project/deployment.yaml
```

```
kubectl apply -f /home/plioyee/sadhamster_project/html-configmap.yaml
```
```
kubectl apply -f /home/plioyee/sadhamster_project/nginx-service.yaml
```
```
kubectl rollout restart deployment/nginx-deployment
```

```
minikube ip
```

```
http://192.168.49.2:30007/
```

![image](https://github.com/user-attachments/assets/0aa62832-975d-4af9-b7d2-d587476c2321)
