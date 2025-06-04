import os
import json
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from typing import Dict, Optional, Any
from .base_exchange import BaseExchange

api_key = os.getenv('FOXBIT_API_KEY')
api_secret = os.getenv('FOXBIT_API_SECRET')
api_base_url = os.getenv('FOXBIT_API_URL')

class Foxbit(BaseExchange):
    def __init__(self):
        print(api_key, api_secret, api_base_url)
        super().__init__(api_key, api_secret, api_base_url)
        self.name = 'foxbit'
        
    def _sign_request(self, method: str, path: str, params: Optional[Dict] = None, body: Optional[Dict] = None) -> Dict[str, str]:
        """Implementa assinatura específica da Foxbit"""
        query_string = urlencode(params) if params else ''
        raw_body = json.dumps(body) if body else ''
        timestamp = str(int(time.time() * 1000))
        
        pre_hash = f"{timestamp}{method.upper()}{path}{query_string}{raw_body}"
        signature = hmac.new(
            self.api_secret.encode(),
            pre_hash.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return {
            'signature': signature,
            'timestamp': timestamp
        }
    
    def _request(self, method: str, path: str, params: Optional[Dict] = None, body: Optional[Dict] = None) -> Any:
        """Envia requisição para API Foxbit"""
        signed = self._sign_request(method, path, params, body)
        headers = {
            'X-FB-ACCESS-KEY': self.api_key,
            'X-FB-ACCESS-TIMESTAMP': signed['timestamp'],
            'X-FB-ACCESS-SIGNATURE': signed['signature'],
            'Content-Type': 'application/json',
        }
        
        url = f"{self.base_url}{path}"
        
        try:
            response = requests.request(
                method,
                url,
                params=params,
                json=body,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            error_msg = f"HTTP error occurred: {http_err}"
            if http_err.response:
                error_msg += f" - Response: {http_err.response.text}"
            raise Exception(error_msg)
        except Exception as err:
            raise Exception(f"An error occurred: {err}")
    
    def get_balances(self) -> Dict[str, float]:
        """Obtém saldos da conta na Foxbit"""
        response = self._request('GET', '/rest/v3/me')
        
        balances = {}
        for currency in response.get('currencies', []):
            symbol = currency['symbol'].upper()
            balances[symbol] = {
                'available': float(currency['available']),
                'total': float(currency['balance'])
            }
        
        return balances
    
    def get_ticker(self, trading_pair: str) -> Dict[str, float]:
        """Obtém cotações do par negociado"""
        # Foxbit usa o formato 'btcbrl' em vez de 'BTC-BRL'
        market_symbol = trading_pair.lower().replace('-', '')
        response = self._request('GET', f'/rest/v3/markets/{market_symbol}/ticker')
        
        return {
            'bid': float(response['bid']),
            'ask': float(response['ask']),
            'last': float(response['last_price'])
        }

        """Obtém ordens ativas"""
        market_symbol = trading_pair.lower().replace('-', '')
        params = {
            'market_symbol': market_symbol,
            'state': 'ACTIVE'
        }
        
        return self._request('GET', '/rest/v3/orders', params=params)