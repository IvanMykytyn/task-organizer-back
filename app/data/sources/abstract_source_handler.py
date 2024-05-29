from abc import ABC, abstractmethod

from app.api.deps import SessionDep


class SourceHandler(ABC):

    @abstractmethod
    def get_tasks(self, session: SessionDep):
        pass