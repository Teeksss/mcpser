# Performans İyileştirmeleri

Bu bölümde MCP Server için model yükleme optimizasyonu, önbellekleme ve fallback (yedekleme) mekanizmaları dahil olmak üzere performans artırıcı geliştirmeler ele alınır.

---

## 1. Model Yükleme Optimizasyonu

### Amaç
- Her model yalnızca bir kez belleğe yüklensin (singleton).
- Model yükleme sırasında bekleme yaşanmasın.
- Modelin yüklenip yüklenmediği kolayca kontrol edilebilsin.

### Uygulama

#### a) Singleton Model Yükleyici

```python name=src/services/intelligence/model_manager.py
from threading import Lock

class ModelManager:
    _instances = {}
    _lock = Lock()

    def __init__(self):
        self.models = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register("phi3", provider="transformers", model_name="microsoft/phi-3-mini-4k-instruct", device="cpu")
        # Diğer modeller...

    def register(self, key: str, provider: str, model_name: str, api_key: str = None, device: str = "cpu", **kwargs):
        with self._lock:
            if key not in self.models:
                self.models[key] = LLMClient(
                    provider=provider,
                    model_name=model_name,
                    api_key=api_key,
                    device=device,
                    **kwargs
                )

    def get(self, key: str) -> LLMClient:
        if key not in self.models:
            raise ValueError(f"Model {key} kayıtlı değil.")
        return self.models[key]

    def generate(self, key: str, prompt: str, **kwargs) -> str:
        client = self.get(key)
        return client.generate(prompt, **kwargs)

mm = ModelManager()
```

#### b) Model Sıcaklığı ve Durumu

```python name=src/services/intelligence/model_status.py
from datetime import datetime

class ModelStatus:
    def __init__(self):
        self.status = {}
    
    def set_loaded(self, model_name):
        self.status[model_name] = {
            "loaded_at": datetime.utcnow(),
            "last_request": datetime.utcnow()
        }
    
    def update_last_request(self, model_name):
        if model_name in self.status:
            self.status[model_name]["last_request"] = datetime.utcnow()
    
    def get_status(self, model_name):
        return self.status.get(model_name, None)
```

Model yükleme sırasında ve her istekte ilgili fonksiyonlar çağrılır.

---

## 2. Cache/Fallback Mekanizması

### a) Kısa Süreli Sonuç Cache’i

**Redis** veya basit Python LRU cache ile cevaplar kısa süreli saklanabilir.

```python name=src/services/intelligence/response_cache.py
from functools import lru_cache

@lru_cache(maxsize=256)
def cached_generate(model_key, prompt, max_tokens=128, temperature=0.7, top_p=0.95):
    return mm.generate(model_key, prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p)
```

API endpoint’inde kullanılabilir:

```python name=src/api/v1/endpoints/llm.py
@router.post("/generate")
def generate_llm(req: LLMRequest):
    try:
        result = cached_generate(
            req.model_key,
            req.prompt,
            req.max_tokens,
            req.temperature,
            req.top_p
        )
        return {"result": result}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
```

### b) Fallback (Yedek Model) Desteği

Ana model başarısız olursa yedek model ile yanıt dönecek yapı:

```python name=src/services/intelligence/model_manager.py
def generate_with_fallback(self, key: str, prompt: str, fallback_key: str = None, **kwargs) -> str:
    try:
        return self.generate(key, prompt, **kwargs)
    except Exception:
        if fallback_key:
            return self.generate(fallback_key, prompt, **kwargs)
        raise
```

API’de opsiyonel fallback_key parametresi ile kullanılabilir.

---

## 3. Asenkron Model Çalıştırma (async inference)

Büyük veya uzun süren model çağrıları için arka planda çalıştırma:

```python name=src/services/intelligence/async_runner.py
import asyncio

async def async_generate(model_key, prompt, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, mm.generate, model_key, prompt, **kwargs)
```

FastAPI endpoint’inizde `async def` ile çağrılır.

---

## 4. Prometheus ile Model Performans Ölçümü

Her model çağrısı için süre ve başarı metriği toplayın.

```python name=src/services/metrics_service.py
from prometheus_client import Summary

INFERENCE_TIME = Summary("inference_time_seconds", "LLM inference response time", ['model'])

def timed_inference(model_key, prompt, **kwargs):
    with INFERENCE_TIME.labels(model_key).time():
        return mm.generate(model_key, prompt, **kwargs)
```

---

> Bu geliştirmeler sayesinde MCP Server daha verimli, ölçeklenebilir ve hatalara karşı dirençli çalışacaktır.  
> Diğer başlıklar için de benzer ayrıntılı teknik dökümantasyon ve örnek kodlar hazırlanabilir.