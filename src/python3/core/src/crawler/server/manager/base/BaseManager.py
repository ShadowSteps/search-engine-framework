from core.src.crawler.server.repository.Repository import Repository
from interfaces.src.crawler.server.data.ISearchEngineContext import ISearchEngineContext


class BaseManager:
    def __init__(self, context: ISearchEngineContext) -> None:
        self.context = context
        self.repository = Repository(context)