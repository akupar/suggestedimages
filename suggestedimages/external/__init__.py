import requests_cache
requests_cache.install_cache()

from .yso import YSO


by_language = {
    'fi': [
        YSO('fi')
    ]
}
