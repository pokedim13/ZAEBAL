"""
    Main file that contains Bard class that synchoronously interacts with Google Bard API.
"""

from typing import Dict, Optional, Union, Any, Set
import re
import json

import httpx

from zaebal import config
from zaebal.base_classes.base_bard import BaseBard
from zaebal.models import BardError, BardAnswer, BardAnswerChoice


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
        super().__init__(token=token, timeout=timeout, proxies=proxies, lang=lang)

    def ask(self, prompt: str) -> Union[BardAnswer, BardError]:
        """
        Asks Bard with prompt.
        :param str prompt: User prompt text
        :return: Bard answer or error
        :rtype: Union[BardAnswer, BardError]
        """
        params = {
            "bl": "boq_assistant-bard-web-server_20230530.14_p0",
            "_reqid": str(self._reqid),
            "rt": "c",
        }
        prompt_struct = [
            [prompt],
            None,
            [self.conversation_id, self.response_id, self.choice_id],
        ]
        if not getattr(self, "SNlM0e", None):
            self.SNlM0e = self._get_snlm0e()
        data = {
            "f.req": json.dumps([None, json.dumps(prompt_struct)]),
            "at": self.SNlM0e,
        }
        response = self._execute_api_method(
            "POST",
            "_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
            params=params,
            data=data,
        )
        chat_data = json.loads(response.content.splitlines()[3])[0][2]
        if not chat_data:
            return BardError(content=response.content, status_code=response.status_code)

        json_chat_data = json.loads(chat_data)
        answer = BardAnswer(
            content=json_chat_data[0][0],
            conversation_id=json_chat_data[1][0],
            response_id=json_chat_data[1][1],
            factualityQueries=json_chat_data[3],
            textQuery=json_chat_data[2][0] if json_chat_data[2] is not None else "",
            choices=[BardAnswerChoice(id=i[0], content=i[1]) for i in json_chat_data[4]],
            images=self._extract_images_from_chat_data(json_chat_data),
        )
        self.conversation_id = answer.conversation_id
        self.response_id = answer.response_id
        self.choice_id = self.choices[0].id
        self._reqid += 1000
        return answer



    def _get_snlm0e(self) -> str:
        """
        Requests Bard for SNlM0e identificator and returns it.
        :return: SNlM0e identificator
        :rtype: str
        """
        response = self.client.get(
            config.BARD_API_HOST,
            timeout=self.timeout,
            follow_redirects=True,
        )
        response.raise_for_status()
        if SNlM0e := re.search(r"SNlM0e\":\"(.*)\"", response.content):
            return SNlM0e[1]
        else:
            raise ValueError("SNlM0e value not found in response! Check token value.")

    def _execute_api_method(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """
        Executes Bard API method.
        :param str method: HTTP method
        :param str endpoint: API endpoint to send request
        :param Optional[Dict[str, Any]] data: POST request data.
        :param Optional[Dict[str, Any]] params: GET params in url.
        :return: API response
        :rtype: httpx.Response
        """
        return self.client.request(
            method,
            config.BARD_API_HOST + endpoint,
            data=data,
            params=params,
            timeout=self.timeout,
        )


    @staticmethod
    def _extract_images_from_chat_data(chat_data: Dict[str, Any]) -> Set[str]:
        """
        Extracts set of images from chat data and returns it.
        :param Dict[str, Any] chat_data: Chat data from Bard answer response.
        :return: set of image urls
        :rtype: Set[str]
        """
        images = set()
        if len(chat_data) >= 3 and len(chat_data[4][0]) >= 4 and chat_data[4][0][4]:
            for img in chat_data[4][0][4]:
                images.add(img[0][0][0])
        return images
