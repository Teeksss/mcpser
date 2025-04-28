# Detaylı MCP Server Kurulum Parametreleri

Aşağıda hem backend hem frontend (web arayüzü) için ortam değişkenleri ve yapılandırma parametreleri detaylı olarak açıklanmıştır.

---

## 1. Ortam Değişkenleri (`.env`)

Aşağıdaki parametreler `.env` dosyasında tanımlanmalıdır.  
`.env.example` dosyasındaki şablon üzerinden kendi değerlerinizi belirleyiniz.

| Parametre           | Açıklama                                                                 | Örnek                           |
|---------------------|--------------------------------------------------------------------------|---------------------------------|
| VECTOR_BACKEND      | Vektör veritabanı türü: chromadb, faiss, pinecone, weaviate, elasticsearch| chromadb                       |
| OPENAI_API_KEY      | (Opsiyonel) OpenAI tabanlı LLM için API anahtarı                        | sk-...                          |
| DATABASE_URL        | SQLAlchemy için veritabanı bağlantı dizesi                              | sqlite:///./mcp.db              |
| PINECONE_API_KEY    | (Opsiyonel, Pinecone kullanılıyorsa) Pinecone API anahtarı              | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx|
| WEAVIATE_HOST       | (Opsiyonel, Weaviate kullanılıyorsa) Weaviate sunucu adresi             | http://localhost:8080           |
| ELASTIC_URL         | (Opsiyonel, Elasticsearch kullanılıyorsa) Elasticsearch adresi           | http://localhost:9200           |

---

## 2. Backend Başlatma Parametreleri

Backend FastAPI uygulaması için, sunucuya göre aşağıdaki parametrelerle başlatabilirsiniz:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Varsayılan parametreler:
- `--host 0.0.0.0`: Tüm arayüzlerden erişim.
- `--port 8000`: API portu.
- `--reload`: Otomatik yeniden başlatma (geliştirme için).

---

## 3. Frontend (React) Ortam Parametreleri

Web arayüzü API'ya hangi adresten ulaşacağını belirlemek için `.env` veya `.env.local` dosyası oluşturabilirsiniz:

| Parametre        | Açıklama                                      | Örnek                    |
|------------------|-----------------------------------------------|--------------------------|
| REACT_APP_API_URL| API'nın tam adresi                            | http://localhost:8000    |

Örneğin `web/.env` dosyası:
```
REACT_APP_API_URL=http://localhost:8000
```

---

## 4. Gelişmiş Kurulum (Ekstra Parametreler)

Aşağıdaki parametreler/ayarlar isteğe bağlıdır:

| Parametre         | Açıklama                                      | Örnek           |
|-------------------|-----------------------------------------------|-----------------|
| LOG_LEVEL         | Log seviyesini belirler (INFO, DEBUG, ERROR)  | INFO            |
| ADMIN_USERNAME    | Varsayılan admin kullanıcı adı                | admin           |
| ADMIN_PASSWORD    | Varsayılan admin şifresi                      | 123456          |
| MAX_UPLOAD_SIZE   | Yüklenebilecek dosyanın maksimum boyutu (MB)  | 20              |
| OCR_LANGUAGES     | Varsayılan OCR dilleri                        | eng+tur         |

> Not: Bazı parametreler kodda doğrudan sabit olabilir, değiştirmek için ilgili Python dosyalarını kontrol edin.

---

## 5. Örnek `.env` Dosyası

```
VECTOR_BACKEND=chromadb
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///./mcp.db
PINECONE_API_KEY=
WEAVIATE_HOST=
ELASTIC_URL=
LOG_LEVEL=INFO
ADMIN_USERNAME=admin
ADMIN_PASSWORD=123456
MAX_UPLOAD_SIZE=20
OCR_LANGUAGES=eng+tur
```

---

## 6. Kurulumdan Sonra

- `.env` içeriğinizi doldurduğunuzdan ve gereksiz bilgileri dışarıya paylaşmadığınızdan emin olun.
- Tesseract yüklü olmalı (OCR için).
- Gelişmiş vektör store (Pinecone, Weaviate, ElasticSearch) için ilgili parametreleri doldurun ve bağımlılıkları yükleyin.

---