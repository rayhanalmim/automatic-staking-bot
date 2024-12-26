from src.bot.increase_leverage import increase_leverage
from src.bot.decrease_leverage import decrease_leverage
from src.config.constants import TARGET_LEVERAGE, MIN_LEVERAGE, MAX_LEVERAGE

def monitor_leverage(current_leverage):
    if current_leverage < MIN_LEVERAGE:
        increase_leverage(current_leverage, TARGET_LEVERAGE)
    elif current_leverage > MAX_LEVERAGE:
        decrease_leverage(current_leverage, TARGET_LEVERAGE)
