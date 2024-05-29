


from app.clients.credentials.credentials_factory import get_credentials_class_by_source_id
from app.clients.crypto.crypto_client import CryptoClient
from infisical_client import GetSecretOptions
from app.core.config import settings


class CredentialsHandler:
    def __init__(self) -> None:
        self.crypto = CryptoClient()
    
    def get_credentials(self, user_email: str, source_id: str):
        handler_class = get_credentials_class_by_source_id(source_id=source_id)
        handler = handler_class(source_id)
        
        hashed_email = self.crypto.value_to_unique_string(value=user_email)
        path = f'/users/{hashed_email}'
        secret = handler.secrets_client.getSecret(options=GetSecretOptions(
            environment=settings.INFISICAL_ENV, 
            project_id=settings.INFISICAL_PROJECT, 
            secret_name=handler.secret_name, 
            path=path))
        return handler.get_credentials(secret)