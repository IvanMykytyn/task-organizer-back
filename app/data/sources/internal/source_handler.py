

from app.api.deps import SessionDep
from app.crud import get_items
from app.data.models import Task
from app.data.sources.abstract_source_handler import SourceHandler


SOURCE_ID = 'internal'


class InternalSourceHandler(SourceHandler):
    def __init__(self, user_id: str, user_email: str) -> None:
        self.user_id = user_id
        self.user_email = user_email
        self.source_id = SOURCE_ID
    
    def get_tasks(self, session: SessionDep, q: str):
        items = get_items(session=session, owner_id=self.user_id)
        tasks = []
        for item in items:
            if q:
                if not (q.lower() in (item.title.lower() + item.description.lower())):
                    continue
            tasks.append(Task(**dict(item), url="", source=self.source_id))
        return tasks