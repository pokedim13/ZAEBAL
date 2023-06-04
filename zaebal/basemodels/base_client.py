import string
import random
import httpx

from typing import Dict, Optional, Union
from httpx._client import BaseClient

class BaseBot:

    client: BaseClient

    def __init__(self,
                session_id: str,
                proxy: dict = None,
                timeout: int = 20,):
        headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
        self._reqid = int("".join(random.choices(string.digits, k=4)))
        self.proxy = proxy
        self.conversation_id = ""
        self.response_id = ""
        self.choice_id = ""
        self.session_id = session_id
        self.client.headers = headers
        self.client.cookies.set("__Secure-1PSID", session_id)
        self.timeout = timeout

    def execute_api_method(self):
        raise NotImplementedError("execute_api_method is not implemented in the inheritor of the class")




# Пример создания экземляра
class AsyncBot(BaseBot):
    def __init__(self, session_id: str, proxy: dict = None, timeout: int = 20):
        self.client = httpx.AsyncClient()
        super().__init__(session_id, proxy, timeout)



class BaseBard:

    client: BaseClient

    def __init__(self,
                token: str,
                *,
                timeout: int = 20,
                proxies: Union[Dict[str, str], str, None] = None,
                lang: str = "en",):
        if not token or token[-1] != ".":
            raise ValueError(
                "Token value must end with a single dot!"
            )
        self.token = token
        self.timeout = timeout
        self.proxies = proxies
        self.lang = lang

    def execute_api_method(self):
        raise NotImplementedError("execute_api_method is not implemented in the inheritor of the class")

