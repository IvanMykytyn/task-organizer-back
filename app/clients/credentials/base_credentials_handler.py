
import logging
from app.core.config import settings
from infisical_client import ClientSettings, InfisicalClient

SECRET_NAME_KEY_IN_DB = "secret_name"

logger = logging.getLogger(__name__)

class SourceNotFoundException(Exception):
    def __init__(self, source_id: str):
        message = f"Source '{source_id}' was not found"
        super().__init__(message)
        

class BaseCredentialsHandler:
    def __init__(self, source_id: str):
        self.source_id = source_id
        self.secret_name = f'{source_id.upper()}_CREDS'
        self.secrets_client = InfisicalClient(ClientSettings(access_token=settings.INFISICAL_TOKEN))


    def get_credentials(self, secret: dict) -> str | dict | None:
        """
        Gets credentials from infisical
        """
        return secret
            

