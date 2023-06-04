"""
    Main file that contains Bard class that synchoronously interacts with Google Bard API.
"""

from typing import Dict, Optional
import re

import httpx

from zaebal import config


class Bard:
    """
    Bard main class. Synchoronously interacts with Google Bard API.
    """

    def __init__(
        self,
        token: str,
        *,
        timeout: int = 20,
        proxies: Union[Dict[str, str], str, None] = None,
        lang: str = "en",
        client: Optional[httpx.Client] = None,
    ):
        """
        :param str token: Bard API token.
        :param int timeout: Timeout for api responses in seconds. Defaults to 20.
        :param Union[Dict[str, str], str, None] proxies: Proxies dict or single proxy string.
        Defaults to None.
        :param str lang: Language of your questions.
        This param will be used for translating from lang to English.
        :param Optional[httpx.Client] client: Httpx client. If not passed, creates new client.
        Default to None.
        :raises: ValueError if token is invalid.
        """
        if not token or token[-1] != ".":
            raise ValueError(
                "Token value must end with a single dot!"
            )
        self.token = token
        self.timeout = timeout
        self.proxies = proxies
        self.lang = lang
        if client is None:
            self.client = httpx.Client()
            self.client.cookies.set("__Secure-1PSID", self.token)
            self.client.headers = {

            }
        else:
            self.client = client
        self.lang = lang


    def _get_snlm0e(self) -> str:
        response = self.client.get(
            config.BARD_API_HOST, timeout=self.timeout, proxies=self.proxies,
        )
        response.raise_for_status()
        if SNlM0e := re.search(r"SNlM0e\":\"(.*)\""):
            return SNlM0e[1]
        else:
            raise ValueError(
                "SNlM0e value not found in response! Check token value."
            )
