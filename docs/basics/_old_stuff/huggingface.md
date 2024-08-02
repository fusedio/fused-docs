# HuggingFace

HuggingFace is the community platform to build AI and ML. Use it with Fused to interface with models, datasets, and applications.

Three things to keep in mind when working with HuggingFace on Fused:
1. Set cache directories
2. Use `@fused.cache` to ensure you download models only once.
3. Authenticate with a token.

```python
@fused.udf
def udf(bbox: fused.types.Bbox=None, n: int=10):
    
    import os
    
    import requests
    import torch
    from transformers import AutoImageProcessor, AutoModel
    from huggingface_hub import hf_hub_download
    import huggingface_hub


    # Set HF and Torch cache directories to Fused filesystem
    os.environ['HF_HOME'] = os.environ['HF_HUB_CACHE'] = '/mnt/cache/hf'
    os.environ['TORCH_WHERE'] = os.environ['TORCH_HOME'] = '/mnt/cache/my_username/tmp/'
    
    # Use strategic caching to only download model files once
    @fused.cache
    def download_model_and_processor():
        processor = AutoImageProcessor.from_pretrained('facebook/dinov2-base')
        model = AutoModel.from_pretrained('facebook/dinov2-base')
        return processor, model

    processor, model = download_model_and_processor()

    # Authenticate to HF hub with token
    huggingface_hub.login(token='hf_...')
    
```