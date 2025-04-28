from threading import Lock

class ModelManager:
    _models = {}
    _locks = {}

    @classmethod
    def get_model(cls, name):
        if name not in cls._models:
            if name not in cls._locks:
                cls._locks[name] = Lock()
            with cls._locks[name]:
                if name not in cls._models:
                    # Model yükleme işlemi (örnek: transformers ile)
                    # from transformers import AutoModelForCausalLM, AutoTokenizer
                    # model = AutoModelForCausalLM.from_pretrained(name)
                    # tokenizer = AutoTokenizer.from_pretrained(name)
                    # cls._models[name] = (model, tokenizer)
                    cls._models[name] = f"DUMMY_MODEL_{name}"
        return cls._models[name]