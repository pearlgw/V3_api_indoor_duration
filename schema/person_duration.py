from pydantic import BaseModel
from datetime import datetime

class UpdateEndTimeRequest(BaseModel):
    end_time: datetime 