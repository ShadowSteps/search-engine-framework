from requests import Response

from core.src.crawler.client.utils.communication.exception.FailedRequestException import FailedRequestException


class BaseCommunicator:
    GET_NEXT_JOB_PATH = '/job/next'
    FINISH_JOB_PATH = '/job/register'

    def __init__(self, base_api_url: str, crawler_id: str) -> None:
        super().__init__()
        self.crawler_id = crawler_id
        self.base_url = base_api_url
        self.http_headers = {
            'AUTH_TOKEN': self.crawler_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def validate_response(self, response: Response):
        if response.status_code != 200:
            raise FailedRequestException('Server returned not-ok status: ' + response.status_code)
        try:
            response_json = response.json()
        except Exception:
            raise FailedRequestException('Server returned not-ok response: ' + response.raw)
        if 'is_successful' not in response_json:
            raise FailedRequestException('Response does not contain is_successful flag!')
        if not response_json['is_successful']:
            raise FailedRequestException('Response delivers not successful flag!')
        return response_json
