from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple
from uuid import UUID

from easy_search.interfaces.server.index.communication.request.SearchQuery import SearchQuery
from easy_search.interfaces.server.job.communication.request.JobResult import JobResult
from ...server.BaseServer import BaseServer
from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.server.IRestServer import IRestServer


class BaseHTTPRestServer(BaseServer, IRestServer):
    @abstractmethod
    def run_dev(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None:
        raise NotImplementedError

    __metaclass__ = ABCMeta
    JOB_REGISTER_PATH = "/job/register"
    JOB_FETCH_PATH = "/job/next"
    DOCUMENT_ADD = "/index/add"
    DOCUMENT_DELETE = "/index/remove"
    DOCUMENT_SEARCH = "/index/search"
    DOCUMENT_GET = "/index/fetch"

    FORBIDDEN = 403
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SUCCESS = 200

    def authenticate(self, headers: dict) -> Optional[UUID]:
        token = headers.get("AUTH_TOKEN", None)
        if token is None:
            return token
        try:
            return UUID(token, version=4)
        except Exception:
            return None

    def manage_response(self, response: BaseResponse) -> Tuple[str, int]:
        if response.is_successful:
            return self.serializer.serialize(response), self.SUCCESS
        elif response.error is not None:
            return self.serializer.serialize(response), response.error.code
        else:
            return self.serializer.serialize(response), self.INTERNAL_SERVER_ERROR

    def register_job(self, headers: dict, request: dict) -> Tuple[str, int]:
        crawler_id = self.authenticate(headers)
        if crawler_id is None:
            return "Token not provided!", self.FORBIDDEN
        if "job_id" not in request:
            return "Job id is not provided!", self.BAD_REQUEST
        job_id_string = request["job_id"]
        try:
            UUID(job_id_string, version=4)
        except Exception:
            return "Job id is not valid!", self.BAD_REQUEST
        job_result = self.serializer.deserialize(request, JobResult)
        response = self.job_scheduler.finish_job(crawler_id, job_result)
        return self.manage_response(response)

    def get_next_free(self, headers: dict):
        crawler_id = self.authenticate(headers)
        if crawler_id is None:
            return "Token not provided!", self.FORBIDDEN
        plugins = headers.get("ACCEPT_PLUGINS", "")
        if plugins == "":
            return "Plugin list not provided!", self.BAD_REQUEST
        response = self.job_scheduler.get_next_job(crawler_id, plugins.split(","))
        return self.manage_response(response)

    def add_document(self, headers: dict, request: dict):
        crawler_id = self.authenticate(headers)
        if crawler_id is None:
            return "Token not provided!",  self.FORBIDDEN
        if "unique_id" not in request:
            return "Document id is not provided!", self.BAD_REQUEST
        document = self.serializer.deserialize(request, self.index_type)
        response = self.documents.add(document)
        return self.manage_response(response)

    def delete_document(self, headers: dict, doc_id: str):
        crawler_id = self.authenticate(headers)
        if crawler_id is None:
            return "Token not provided!",  self.FORBIDDEN
        response = self.documents.delete(doc_id)
        return self.manage_response(response)

    def search(self, headers: dict, request: dict):
        crawler_id = self.authenticate(headers)
        if crawler_id is None:
            return "Token not provided!", self.FORBIDDEN
        query = self.serializer.deserialize(request, SearchQuery)
        response = self.documents.search(query)
        return self.manage_response(response)

    def fetch(self, headers: dict, doc_id: str):
        crawler_id = self.authenticate(headers)
        if crawler_id is None:
            return "Token not provided!", self.FORBIDDEN
        response = self.documents.get(doc_id)
        return self.manage_response(response)
