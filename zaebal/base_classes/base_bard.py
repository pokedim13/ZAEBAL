"""
    Abstract BaseBard class for Bard and AsyncBard classes.
"""
from typing import Dict, Union
from httpx._client import BaseClient


class BaseBard:
    """
    Abstract BaseBard class for Bard and AsyncBard classes.
    :param str token: Bard API token from __Secure_1PSID cookie.
    :param int timeout: Timeout for Bard API requests in seconds. Defaults to 20.
    :param Union[Dict[str, str], str, None] proxies: Proxies dict or single proxy for Bard API requests.
    Defaults to None.
    :param str lang: Language of question text for translating. Defaults to en.
    :param BaseClient client: Sync or async httpx client for requests to Bard API.
    """
    client: BaseClient

    def __init__(
        self,
        token: str,
        *,
        timeout: int = 20,
        proxies: Union[Dict[str, str], str, None] = None,
        lang: str = "en",
    ):
        if not token or token[-1] != ".":
            raise ValueError("Token value must end with a single dot!")
        self.token = token
        self.timeout = timeout
        self.proxies = proxies
        self.lang = lang
        self.client.cookies.set("__Secure-1PSID", token)
        self.client.headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Host": "bard.google.com",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "X-Same-Domain": "1",
        }
        self.choice_id = ""
        self.conversation_id = ""
        self.response_id = ""

    def ask(self, *args, **kwargs):
        raise NotImplementedError(
            "ask() method is not implemented in derived class."
        )

    def _execute_api_method(self, *args, **kwargs):
        raise NotImplementedError(
            "_execute_api_method() is not implemented in the derived class."
        )

    def _get_snlm0e(self, *args, **kwargs):
        raise NotImplementedError(
            "_get_snlm0e() is not implemented in the derived class."
        )
