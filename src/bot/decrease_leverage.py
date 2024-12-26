from src.config.utils import send_transaction_with_retry

def decrease_leverage(current_leverage, target_leverage):
    if current_leverage > target_leverage:
        def execute_decrease():
            # Call Kamino and Lulo APIs to pay down debt
            print(f"Decreasing leverage to {target_leverage}x")
            # Add transaction code here
        send_transaction_with_retry(execute_decrease)
