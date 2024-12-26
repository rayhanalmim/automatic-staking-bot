from src.config.utils import send_transaction_with_retry

def increase_leverage(current_leverage, target_leverage):
    if current_leverage < target_leverage:
        def execute_increase():
            # Call Kamino API to adjust leverage
            print(f"Increasing leverage to {target_leverage}x")
            # Add transaction code here
        send_transaction_with_retry(execute_increase)
