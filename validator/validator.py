
class ConfigValidator:
    def __init__(self, config, maker_balance, taker_balance):
        self.config = config
        self.maker_balance = maker_balance
        self.taker_balance = taker_balance
        self.validations = []
        self.suggestions = []
    
    def validate_all(self):
        """Executa todas as validações"""
        self._validate_balances()
        self._validate_order_amount()
        self._validate_profitability()
        self._validate_risk_parameters()
        
        return {
            'is_valid': all(v['status'] for v in self.validations),
            'validations': self.validations,
            'suggestions': self.suggestions
        }
    
    def _validate_balances(self):
        """Valida se os saldos são suficientes"""
        # Calcula o máximo teórico baseado nos fatores de configuração

        print(self.taker_balance.get('USDT', 0))
        print(self.maker_balance.get('USDT', 0))

        taker_max = self.taker_balance.get('USDT', 0) * (self.config.get('order_size_taker_balance_factor', 99.5) / 100)
        portfolio_total = self.maker_balance.get('USDT', 0) + self.taker_balance.get('USDT', 0)
        portfolio_max = portfolio_total * (self.config.get('order_size_portfolio_ratio_limit', 16.67) / 100)
        
        max_recommended = min(taker_max, portfolio_max)
        current_amount = self.config.get('order_amount', 0)
        
        is_valid = current_amount <= max_recommended
        self.validations.append({
            'name': 'Amount',
            'status': is_valid,
            'message': f"{'válido' if is_valid else 'inválido'}. "
                       f"Atual: {current_amount} USDT, Máx recomendado: {max_recommended:.2f} USDT, Saldo total(taker_max/saldo_total): {taker_max:.2f}/{portfolio_total:.2f} USDT."
        })
        
        if not is_valid:
            self.suggestions.append({
                'parameter': 'order_amount',
                'current_value': current_amount,
                'suggested_value': max_recommended,
                'reason': f"Valor atual excede o máximo recomendado baseado nos seus saldos ({(max_recommended):.2f} USDT)"
            })
    
    def _validate_order_amount(self):
        """Valida se o tamanho da ordem é apropriado"""

        order_amount = self.config.get('order_amount', 0)
        balance_available = self.maker_balance.get('USDT', 0)
        n_orders = self.config.get('n_orders', 0)

        is_too_large = order_amount > (balance_available / n_orders)

        
        self.validations.append({
            'name': 'Tamanho da ordem',
            'status': not is_too_large,
            'message': f"Tamanho da ordem {'adequado' if not is_too_large else 'muito grande'}: "
                      f"{order_amount} USDT."
        })
    
    def _validate_profitability(self):
        """Valida se a rentabilidade mínima é realista"""
        profitability = self.config.get('profitability_1', 0)
        is_low = profitability < 0.5  # Consideramos abaixo de 0.5% muito baixo
        
        self.validations.append({
            'name': 'Rentabilidade mínima',
            'status': not is_low,
            'message': f"Rentabilidade mínima {'adequada' if not is_low else 'muito baixa'}: "
                      f"{profitability}%"
        })
        
        if is_low:
            self.suggestions.append({
                'parameter': 'profitability_1',
                'current_value': profitability,
                'suggested_value': max(1.0, profitability),  # Sugere pelo menos 1%
                'reason': "Rentabilidade mínima muito baixa pode não cobrir taxas e oscilações"
            })
    
    def _validate_risk_parameters(self):
        """Valida parâmetros de risco"""
        # Valida slippage_buffer
        if self.config.get('slippage_buffer', 0) == 0:
            self.suggestions.append({
                'parameter': 'slippage_buffer',
                'current_value': 0,
                'suggested_value': 0.1,
                'reason': "Slippage buffer zero pode resultar em execuções a preços desfavoráveis"
            })
        
        # Valida order_size_taker_balance_factor
        if self.config.get('order_size_taker_balance_factor', 99.5) > 80:
            self.suggestions.append({
                'parameter': 'order_size_taker_balance_factor',
                'current_value': self.config.get('order_size_taker_balance_factor', 99.5),
                'suggested_value': 80,
                'reason': "Utilizar mais de 80% do saldo aumenta muito o risco"
            })