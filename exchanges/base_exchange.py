import os
import abc
from typing import Dict, Optional, Any

class BaseExchange(abc.ABC):
    def __init__(self, api_key: str = None, api_secret: str = None, api_base_url: str = None):
        self.api_key = api_key or os.getenv(f"{self.__class__.__name__.upper()}_API_KEY")
        self.api_secret = api_secret or os.getenv(f"{self.__class__.__name__.upper()}_API_SECRET")
        self.base_url = api_base_url or os.getenv(f"{self.__class__.__name__.upper()}_API_URL")
        
    @abc.abstractmethod
    def get_balances(self) -> Dict[str, float]:
        """Obtém saldos da exchange"""
        pass
    
    @abc.abstractmethod
    def get_ticker(self, trading_pair: str) -> Dict[str, float]:
        """Obtém preços atuais do par negociado"""
        pass
    
    @abc.abstractmethod
    def _sign_request(self, method: str, path: str, params: Optional[Dict] = None, body: Optional[Dict] = None) -> Dict[str, str]:
        """Assina a requisição conforme padrão da exchange"""
        pass
    
    @abc.abstractmethod
    def _request(self, method: str, path: str, params: Optional[Dict] = None, body: Optional[Dict] = None) -> Any:
        """Envia requisição para a API"""
        pass