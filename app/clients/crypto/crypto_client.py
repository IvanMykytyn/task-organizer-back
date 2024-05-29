import hashlib

class CryptoClient:
    def value_to_unique_string(self, value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()