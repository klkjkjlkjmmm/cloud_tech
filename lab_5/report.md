# Лабораторная 5

## Задание

Сделать мониторинг сервиса, поднятого в кубере (использовать, например, prometheus и grafana). 
Показать хотя бы два рабочих графика, которые будут отражать состояние системы. Приложить скриншоты всего процесса настройки.

## Ход работы

Сначала мы долго пытались начать делать лабу. Потом мы несколько раз переделывали ее, потому что нам казалось, что стоит начать с листого листа.

Для мониторинга был выбран сервис `ingress-nginx`.


### Установка всего необходимого

Сначала было необходимо задеплоить `ingress-nginx`. Для этого использовалась команда `helm`.
```
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

С помощью `helm` был запущен `Prometheus`.

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

### Настройка всего необходимого

Далее было необходимо установить параметры, отвечающие за экспорт метрик:
1. `--set controller.metrics.enabled=true` включает метрики для контроллера `nginx ingress`;
2. `--set controller.metrics.serviceMonitor.enabled=true` включает `ServiceMonitor` для `nginx ingress`, который используется для сбора метрик с подов;
3. `--set controller.metrics.serviceMonitor.additionalLabels.release="prometheus"` добавляет метку `prometheus` (она должна совпадать с названием релиза `Prometheus`)
```
helm upgrade ingress-nginx ingress-nginx/ingress-nginx \
--namespace ingress-nginx \
--set controller.metrics.enabled=true \
--set controller.metrics.serviceMonitor.enabled=true \
--set controller.metrics.serviceMonitor.additionalLabels.release="prometheus"
```

Из-за того, что `Prometheus` и `nginx ingress` запущены в разных пространствах имен, необходимо настроить `Prometheus` так, чтобы он смог обнаружить `ServiceMonitor` из другого пространства имен.

```
helm upgrade prometheus prometheus-community/kube-prometheus-stack \
--namespace prometheus  \
--set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
--set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

### Подключение к Prometheus

Откроем страницу `Prometheus` в браузере, перед этим совершив переброс портов.
```
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n prometheus 9090:9090
```
Страница успешно открылась и мы можем увидеть метрики, которые собирает `Prometheus`. Ура-ура!

![image](https://github.com/user-attachments/assets/7e889837-3bbb-4623-a9de-c9b2c810fa7a)

### Подключение Grafana

Аналогично, перебросим порты для `Grafana`.
```
kubectl port-forward svc/prometheus-grafana  3000:80 -n prometheus
```
По адресу `localhost:3000` нас ждал красивый интерфейс `Grafana`.
![image](https://github.com/user-attachments/assets/d442bd81-3e3d-4660-b7dc-d040852a4b4a)

Осталось совсем немного - необходимо указать `Prometheus` в источниках данных, а также импортировать дэшборд (мы использовали вот [этот](https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/grafana/dashboards/nginx.json)).

![image](https://github.com/user-attachments/assets/586111e0-9281-45ba-a095-3cfc7e896f6b)

Здесь можно увидеть много интересных графиков, например:

`Average Memory Usage` - показывает среднее количество используемой памяти

![image](https://github.com/user-attachments/assets/2149e31b-918c-42e3-bc13-e10e87d15293)

`Average CPU Usage` - показывает среднее использование CPU

![image](https://github.com/user-attachments/assets/6690b3d1-8116-4bca-93a7-44a3a8d83215)


