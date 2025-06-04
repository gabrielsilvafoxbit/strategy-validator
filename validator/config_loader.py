import yaml

def load_config(file_path):
    """Carrega o arquivo de configuração YAML"""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def validate_config_structure(config):
    """Valida a estrutura básica do arquivo de configuração"""
    required_fields = [
        'maker_market', 'taker_market', 
        'maker_market_trading_pair', 'taker_market_trading_pair',
        'n_orders', 'profitability_1', 'order_amount'
    ]
    
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise ValueError(f"Campos obrigatórios faltantes: {missing_fields}")