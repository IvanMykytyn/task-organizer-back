from typing import Type
from app.clients.credentials.base_credentials_handler import BaseCredentialsHandler
from app.clients.credentials.sources.tick_tick.handler import TickTickCredentialsHandler

SOURCE_ID_TO_CREDENTIALS_HANDLER: dict[str, Type[BaseCredentialsHandler]] = {
    "tick_tick": TickTickCredentialsHandler,
}


def get_credentials_class_by_source_id(source_id: str) -> Type[BaseCredentialsHandler]:
    if source_id not in SOURCE_ID_TO_CREDENTIALS_HANDLER:
        return BaseCredentialsHandler
    return SOURCE_ID_TO_CREDENTIALS_HANDLER[source_id]
