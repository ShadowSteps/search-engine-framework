from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker, Session

from .set.CrawlerSet import CrawlerSet
from .set.JobSet import JobSet
from easy_search.interfaces.server.job.data.ISearchEngineContext import ISearchEngineContext
from easy_search.interfaces.server.job.data.set.ICrawlerSet import ICrawlerSet
from easy_search.interfaces.server.job.data.set.IJobSet import IJobSet


class SearchEngineContext(ISearchEngineContext):

    def job_set(self) -> IJobSet:
        return self.job_set_instance

    def crawler_set(self) -> ICrawlerSet:
        return self.crawler_set_instance

    def save(self) -> None:
        self.current_session.flush()

    def start_transaction(self) -> None:
        pass

    def rollback(self) -> None:
        self.current_session.rollback()

    def commit(self) -> None:
        self.current_session.commit()

    def __init__(self, database_connection: str):
        self.engine = create_engine(database_connection)
        self.session_manager = sessionmaker(bind=self.engine)
        self.current_session = self.session_manager()
        self.job_set_instance = JobSet(self.current_session)
        self.crawler_set_instance = CrawlerSet(self.current_session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.current_session.close()
