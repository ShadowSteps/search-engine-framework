import datetime
from uuid import UUID

from easy_search.interfaces.base.enum.JobType import JobType


class JobData(object):
    def __init__(self, job_type: JobType, target: str, locked: bool, creator_crawler_id: UUID, plugin: str,
                 repeat: int = None, repeat_after: datetime = None) -> None:
        self.repeat_after = repeat_after
        self.repeat = repeat
        self.type = job_type
        self.target = target
        self.locked = locked
        self.creator_id = creator_crawler_id
        self.executor_id = None
        self.date_executed = None
        self.plugin_type = plugin

    def set_executor_crawler_id(self, crawler_id: UUID, date_executed: datetime) -> None:
        self.executor_id = crawler_id
        self.date_executed = date_executed
