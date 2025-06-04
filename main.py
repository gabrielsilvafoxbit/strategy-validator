from validator.config_loader import load_config, validate_config_structure
from validator.exchange_connector import ExchangeConnector
from validator.validator import ConfigValidator
from validator.optimizer import ConfigOptimizer

config_path = "strategy/xemm-v2.yml"

def main():
    # Carrega configuração
    config = load_config(config_path)
    validate_config_structure(config)
    
    # Conecta às exchanges
    maker = ExchangeConnector(config['maker_market'])
    taker = ExchangeConnector(config['taker_market'])
    
    # Obtém saldos
    maker_balance = maker.get_balances()
    taker_balance = taker.get_balances()
    
    # Valida configuração
    validator = ConfigValidator(config, maker_balance, taker_balance)
    validation_result = validator.validate_all()
    
    # Otimiza configuração
    optimizer = ConfigOptimizer(config, maker, taker)
    optimization_suggestions = optimizer.optimize_config()
    
    # Combina todas as sugestões
    all_suggestions = validation_result['suggestions'] + optimization_suggestions
    
    # Exibe resultados
    print("\n====================================")

    print(f"\nMaker Balance({config["maker_market"]}): ", maker_balance)
    print(f"Taker Balance({config["taker_market"]}): ", taker_balance)

    print("\n====================================")

    print("\n=== Resultados da Validação ===")
    for validation in validation_result['validations']:
        status = "✔" if validation['status'] else "✖"
        print(f"{status} {validation['name']}: {validation['message']}")
    
    if all_suggestions:
        print("\n=== Sugestões de Otimização ===")
        for suggestion in all_suggestions:
            print(f"\nParâmetro: {suggestion['parameter']}")
            print(f"Valor atual: {suggestion['current_value']}")
            print(f"Sugestão: {suggestion['suggested_value']}")
            print(f"Motivo: {suggestion['reason']}")
    else:
        print("\nConfiguração já otimizada. Nenhuma sugestão no momento.")
    
    print(f"\nValidação {'bem-sucedida' if validation_result['is_valid'] else 'com problemas'}")

if __name__ == "__main__":
    main()