# Лабораторная 5

## Задание

Сделать мониторинг сервиса, поднятого в кубере (использовать, например, prometheus и grafana). 
Показать хотя бы два рабочих графика, которые будут отражать состояние системы. Приложить скриншоты всего процесса настройки.

## Ход работы

Сначала мы долго пытались начать делать лабу.

1. сначала мы установили nginx-ingress

```
helm repo add nginx-stable https://helm.nginx.com/stable
helm repo update
helm install my-nginx nginx-stable/nginx-ingress
```


2. добавим чтобы следить
```
controller:
  metrics:
    enabled: true
    service:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "10254"
```
3. прометеус
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
4. сервис монитор
```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: nginx-servicemonitor
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: ingress-nginx
  namespaceSelector:
    matchNames:
    - default
  endpoints:
  - port: metrics
    interval: 30s
```

```
kubectl apply -f nginx-servicemonitor.yaml
```



5. графана
```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```
```
helm install grafana grafana/grafana
```

```
kubectl get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

```
kubectl port-forward service/grafana 3000:80
```


    

