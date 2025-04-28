# MCP Server Dosya Bütünlüğü ve Proje İncelemesi

Bu belge, MCP Server projesinin güncel dosya bütünlüğünü ve mimarisini özetler. Proje, kurumsal düzeyde güvenli, çok kiracılı (multi-tenant), vektör tabanlı arama ve modern yönetim paneli özellikleriyle tasarlanmıştır.

---

## 1. Kök Dizini

```plaintext
.
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── k8s/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── secret.yaml
│   └── README.md
├── requirements.txt
├── README.md
├── ROADMAP.md
├── docs/
│   ├── security_overview.md
│   └── grafana_dashboard_example.json
├── tests/
│   └── test_auth.py
├── src/
│   ├── main.py
│   ├── core/
│   │   ├── security.py
│   │   ├── rbac.py
│   │   └── tenant_context.py
│   ├── services/
│   │   ├── cache.py
│   │   ├── model_manager.py
│   │   ├── metrics_service.py
│   │   ├── vector_store.py
│   │   ├── async_runner.py
│   │   ├── audit_log.py
│   │   └── logger.py
│   ├── models/
│   │   ├── user.py
│   │   ├── tenant.py
│   │   ├── core.py
│   │   └── database.py
│   └── api/
│       └── v1/
│           └── endpoints/
│               ├── auth.py
│               ├── user_admin.py
│               ├── pipeline.py
│               ├── metrics.py
│               ├── tenant.py
│               ├── vector.py
│               └── audit.py
└── web/
    └── src/
        ├── api.js
        ├── App.jsx
        └── components/
            ├── AdminDashboard.jsx
            ├── TenantSwitcher.jsx
            ├── TenantAdminPanel.jsx
            └── AuditLogView.jsx
```

---

## 2. Ana Bileşenler ve Sorumlulukları

### Backend (src/)
- **core/**: Güvenlik, RBAC ve tenant context yönetimi.
- **services/**: Model yönetimi, cache, loglama, monitoring, vektör store (multi-backend ve multi-tenancy), audit log.
- **models/**: SQLAlchemy modelleri, kullanıcı, tenant ve temel DB kurulumları.
- **api/v1/endpoints/**: REST API endpoint’leri (auth, kullanıcı, tenant, vektör, pipeline, log, metrikler).

### Frontend (web/src/)
- **components/**: Yönetim panelleri (admin, tenant, audit), tenant seçici, kullanıcı yönetimi.
- **api.js**: Tüm frontend API çağrıları için merkezi axios client.
- **App.jsx**: Uygulama ana çatı ve sayfa yönlendirme.

### Deployment
- **Dockerfile, docker-compose.yml**: Geliştirici ve prod ortamları için hazır container yapılandırması.
- **k8s/**: Tüm servisler için Kubernetes manifestleri.

### İzleme, Loglama ve Test
- **Prometheus ve Grafana**: Monitoring endpoint ve dashboard örnekleri.
- **services/logger.py, services/audit_log.py**: Uygulama ve kullanıcı hareket logları.
- **tests/**: Unit ve API testi altyapısı.

---

## 3. Multi-Tenancy ve Vektör Yönetimi

- Her tenant, izole bir vektör-store’a ve doküman havuzuna sahip.
- API ve frontend, tenant context’i ile çalışacak şekilde tasarlandı.
- Metadata/attribute bazlı sorgu, bulk ekleme/silme ve çoklu backend desteği mevcut.

---

## 4. Güvenlik ve Kullanıcı Yönetimi

- JWT authentication, refresh token, RBAC (rol tabanlı yetki).
- Rate limiting (slowapi).
- Parola sıfırlama, kullanıcı ve rol yönetimi.
- Audit log: Tüm önemli işlemler kayıt altına alınmakta.

---

## 5. Monitoring, Loglama ve Test

- Prometheus endpoint’i ve örnek Grafana dashboard’u ile canlı izleme.
- Rotating file ve stdout loglama.
- Testler için pytest ve API testleri.

---

## 6. Frontend

- Modern React + Ant Design arayüz; tenant ve kullanıcı yönetimi, audit log görüntüleme.
- Tüm API’lerle tam uyumlu.

---

## 7. Dağıtım ve DevOps

- Docker ve Kubernetes manifestleri (volume, config, secret).
- GitHub Actions ile CI/CD pipeline örneği.

---

## Sonuç

Bu dosya bütünlüğü ile MCP Server projesi;
- Güvenlik, yönetim, izleme ve ölçeklenebilirlik açısından kurumsal gereksinimleri karşılar.
- Kolayca genişletilebilir ve özelleştirilebilir.
- Hem geliştirici dostu hem de üretim ortamına hazırdır.

> Belirli bir dosya veya modülün içeriğini ayrıntılı görmek için dosya adı belirtmeniz yeterlidir.