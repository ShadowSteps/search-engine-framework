from ..common.JobDescription import JobDescription
from .BaseResponse import BaseResponse


class JobInformation(BaseResponse):
    def __init__(self, job_desc: JobDescription = None):
        result = job_desc is not None
        super().__init__(result)
        self.job_desc = job_desc