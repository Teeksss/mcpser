# MCP Server

Kurumsal ve genişletilebilir Multi-Model RAG + LLM platformu.

## Özellikler

- JWT Authentication & RBAC
- Rate Limiting
- Model cache ve fallback desteği
- Singleton model yönetimi
- Prometheus ile monitoring
- Kullanıcı, rol ve tenant yönetimi API
- Çoklu vektör backend desteği ve multi-tenancy (her tenant’a izole vektör-store)
- Modern frontend (React + Ant Design)
- Docker/Kubernetes ile kolay deployment

## Hızlı Kurulum

```bash
git clone <repo-url>
cd <repo>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -c "from src.models.database import init_db; init_db()"
uvicorn src.main:app --reload
```

## Docker

```bash
docker-compose up --build
```

## Kubernetes

```bash
kubectl apply -f k8s/
```

## Yol Haritası

Daha fazla bilgi için [ROADMAP.md](ROADMAP.md) dosyasına bakın.