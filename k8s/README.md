# Kubernetes Deployment

## MCP Server

```sh
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Notlar

- `configmap.yaml` ortam değişkenlerini, `secret.yaml` ise hassas bilgileri içerir.
- Veritabanı için production ortamında persistent volume kullanınız.
- Redis ve Chroma vektör store ayrı olarak deploy edilmelidir.