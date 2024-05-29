from typing import Type

from app.data.sources.abstract_source_handler import SourceHandler
from app.data.sources.internal.source_handler import InternalSourceHandler
from app.data.sources.tick_tick.source_handler import TickTickSourceHandler


SOURCE_ID_TO_HANDLER: dict[str, Type[SourceHandler]] = {
    "tick_tick": TickTickSourceHandler,
    "internal": InternalSourceHandler,
}


def get_handler_class_by_source_id(source_id: str) -> Type[SourceHandler]:
    if source_id not in SOURCE_ID_TO_HANDLER:
        return SourceHandler
    return SOURCE_ID_TO_HANDLER[source_id]
