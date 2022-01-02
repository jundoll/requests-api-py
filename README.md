# requests-api-py

## How to
### Install
```console
$ pip install git+https://github.com/jundoll/requests-api-py.git
```

### Use (sample)
```python
import requests_api as request
import asyncio

# get a result of request URI (from https://sampleapis.com/)
request_uri = 'https://api.sampleapis.com/coffee/hot'
response_dict = asyncio.run(request.get(request_uri))
```
