class ConfigOptimizer:
    def __init__(self, config, maker_connector, taker_connector):
        self.config = config
        self.maker = maker_connector
        self.taker = taker_connector
    
    def optimize_config(self):
        """Retorna sugestões de otimização baseadas no mercado atual"""
        suggestions = []
        
        # Obtém preços atuais
        maker_ticker = self.maker.get_current_ticker(self.config['maker_market_trading_pair'])
        taker_ticker = self.taker.get_current_ticker(self.config['taker_market_trading_pair'])
        
        # Calcula rentabilidade real
        buy_profit = (maker_ticker['bid'] / taker_ticker['ask'] - 1) * 100
        sell_profit = (taker_ticker['bid'] / maker_ticker['ask'] - 1) * 100
        current_profit = max(buy_profit, sell_profit)
        
        # Sugere ajuste de rentabilidade mínima se necessário
        if current_profit < self.config['profitability_1']:
            suggestions.append({
                'parameter': 'profitability_1',
                'current_value': self.config['profitability_1'],
                'suggested_value': current_profit * 0.8,  # 10% abaixo do atual
                'reason': f"Rentabilidade atual do mercado ({current_profit:.2f}%) abaixo do mínimo configurado"
            })
        
        # Sugere ativar ajuste de ordens se inativo
        if not self.config.get('adjust_order_enabled', False):
            suggestions.append({
                'parameter': 'adjust_order_enabled',
                'current_value': False,
                'suggested_value': True,
                'reason': "Ajuste automático de ordens pode melhorar a taxa de execução"
            })
        
        # Sugere aumentar número de ordens se apenas 1
        if self.config.get('n_orders', 1) == 1:
            suggestions.append({
                'parameter': 'n_orders',
                'current_value': 1,
                'suggested_value': 2,
                'reason': "Múltiplas ordens podem capturar mais oportunidades de arbitragem"
            })
        
        if self.config.get('order_size_taker_balance_factor', 99.5) < 95:
            suggestions.append({
                'parameter': 'order_size_taker_balance_factor',
                'current_value': self.config.get('order_size_taker_balance_factor', 99.5),
                'suggested_value': 95,
                'reason': "Sem taxas, pode usar mais do saldo disponível"
            })
        
        if self.config.get('order_size_taker_balance_factor', 99.5) > 80:
            suggestions.append({
                'parameter': 'order_size_taker_balance_factor',
                'current_value': self.config.get('order_size_taker_balance_factor', 99.5),
                'suggested_value': 80,
                'reason': "Utilizar mais de 80% do saldo aumenta muito o risco"
            })
    
        return suggestions