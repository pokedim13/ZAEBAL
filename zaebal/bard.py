"""
    Main file that contains Bard class that synchoronously interacts with Google Bard API.
"""

from typing import Dict, Optional, Union, Any
import re

import httpx

from zaebal import config
from zaebal.base_classes.base_bard import BaseBard


class Bard(BaseBard):
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
    ):
        """
        :param str token: Bard API token.
        :param int timeout: Timeout for api responses in seconds. Defaults to 20.
        :param Union[Dict[str, str], str, None] proxies: Proxies dict or single proxy string.
        Defaults to None.
        :param str lang: Language of your questions.
        This param will be used for translating from lang to English.
        :raises: ValueError if token is invalid.
        """
        self.client = httpx.Client()
        super(self).__init__(token=token, timeout=timeout, proxies=proxies, lang=lang)


    def ask(self, prompt: str) -> BardAnswer:
        ...

    def _get_snlm0e(self) -> str:
        """
        Requests Bard for SNlM0e identificator and returns it.
        :return: SNlM0e identificator
        :rtype: str
        """
        response = self.client.get(
            config.BARD_API_HOST,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        response.raise_for_status()
        if SNlM0e := re.search(r"SNlM0e\":\"(.*)\""):
            return SNlM0e[1]
        else:
            raise ValueError("SNlM0e value not found in response! Check token value.")

    def _execute_api_method(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.client.request(
            method,
            config.BARD_API_HOST + endpoint,
            data=data,
            params=params,
            timeout=self.timeout,
            proxies=self.proxies,
        )
