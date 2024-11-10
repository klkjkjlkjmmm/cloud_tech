# Лабораторная 5

## Задание

Сделать мониторинг сервиса, поднятого в кубере (использовать, например, prometheus и grafana). 
Показать хотя бы два рабочих графика, которые будут отражать состояние системы. Приложить скриншоты всего процесса настройки.

## Ход работы

Сначала мы долго пытались начать делать лабу.

1. установить репозиторий хелм-чартов
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
![image](https://github.com/user-attachments/assets/0381e653-ed78-418d-88e4-13163f9dbd73)

2. установить Prometheus и Grafana с использованием чарта kube-prometheus-stack
тут мы поняли что сначала стоило бы включить миникуб

![image](https://github.com/user-attachments/assets/91408bfe-548c-4958-b605-20c50663256d)


3. после установки нужно сделать переадресацию портов для доступа к интерфейсам графаны и прометеуса

```
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```
![image](https://github.com/user-attachments/assets/f24d1021-53b2-4d7b-aa21-d6bbcae55d8b)

```
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

![image](https://github.com/user-attachments/assets/33ee61cb-6bad-42c2-b562-e443986ba2d8)


4. настройка графана
потом нужно было настроить графану; так как мы устанавливали через куб-прометеус-стак, то пароль был не админ-админ, а админ-prom operator (петь как smooth operator от sade)
![image](https://github.com/user-attachments/assets/8f5e8569-e4e2-4343-bb3f-d240059cfae5)

5. 

