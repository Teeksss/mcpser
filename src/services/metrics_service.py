from prometheus_client import Summary

INFERENCE_TIME = Summary("inference_time_seconds", "LLM inference response time", ['model'])

def timed_inference(model_key, prompt, **kwargs):
    with INFERENCE_TIME.labels(model_key).time():
        return mm.generate(model_key, prompt, **kwargs)