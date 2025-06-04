from exchanges.base_exchange import BaseExchange
from exchanges.foxbit import Foxbit

class ExchangeConnector:
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name.lower()
        self.exchange = None
        if self.exchange_name == 'foxbit':
            self.exchange = Foxbit()
        elif self.exchange_name == 'binance':
            self.exchange = Foxbit()
        else:
            raise ValueError(f"Exchange não suportada: {self.exchange_name}")
        # Aqui você implementaria a conexão real com a API da exchange
        # Esta é uma implementação mock para demonstração
        
    def get_balances(self):
        return self.exchange.get_balances()
    
    def get_current_ticker(self, trading_pair):
        """Retorna preços atuais (mock)"""
        if self.exchange_name == 'foxbit' and trading_pair == 'USDT-BRL':
            return {'bid': 5.20, 'ask': 5.25}
        elif self.exchange_name == 'binance' and trading_pair == 'USDT-BRL':
            return {'bid': 5.18, 'ask': 5.22}
        elif self.exchange_name == 'okx' and trading_pair == 'USDT-BRL':
            return {'bid': 5.16, 'ask': 5.19}
        elif self.exchange_name == 'kucoin' and trading_pair == 'USDT-BRL':
            return {'bid': 5.14, 'ask': 5.17}
        else:
            raise ValueError("Par de negociação não suportado")