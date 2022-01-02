
# load modules
import json
import asyncio
import time
import urllib.parse
from urllib import error, request


# definition
class Limiter:

    def __init__(self):

        self.ratelimit_reset = None
        self.ratelimit_remaining = None
        self.ratelimit_limit = None

    async def wait(self):
        now = self.unix_timestamp()
        if (self.ratelimit_reset is None) or (now > self.ratelimit_reset):
            self.ratelimit_reset = None
            self.ratelimit_remaining = None
            return
        if self.ratelimit_remaining == 0:
            sleepTime = self.ratelimit_reset - now
            await asyncio.sleep(sleepTime)
            self.ratelimit_remaining = self.ratelimit_limit
            self.ratelimit_reset = None

    def unix_timestamp(self):
        return round(time.time() / 1000)

    def setLimitData(self, remaining, reset, limit):
        self.ratelimit_remaining = remaining
        self.ratelimit_reset = reset
        self.ratelimit_limit = limit


async def get(
    request_url: str,
    max_retries: int = 20,
    sleep_wait: int = 5,
    user_agent: str = ''
):

    # init
    limiter = Limiter()

    # execute
    for i in range(max_retries):
        await limiter.wait()
        headers = {"User-Agent": urllib.parse.quote(user_agent)}
        req = request.Request(request_url, headers=headers)
        try:
            response = request.urlopen(req)
            remaining = response.headers.get("x-ratelimit-remaining")
            reset = response.headers.get("x-ratelimit-reset")
            limit = response.headers.get("x-ratelimit-limit")
            limiter.setLimitData(remaining, reset, limit)
        except error.HTTPError as e:
            if e.code == 401:
                # Not logged in
                raise e
            elif e.code == 404:
                # Not found
                raise e
            elif e.code == 422:
                # Invalid parameter
                raise e
            elif e.code == 429:
                # Too many requests
                await asyncio.sleep(sleep_wait)
                if i == (max_retries-1):
                    raise e
            else:
                raise e
        else:
            return json.load(response)
