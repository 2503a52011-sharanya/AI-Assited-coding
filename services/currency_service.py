from config.constants import CURRENCIES

class CurrencyService:
    @staticmethod
    def get_rate_to_inr(currency: str) -> float:
        curr = CURRENCIES.get(currency.upper(), CURRENCIES["INR"])
        return curr["rate_to_inr"]

    @staticmethod
    def convert(amount: float, from_curr: str, to_curr: str) -> float:
        if from_curr == to_curr:
            return round(amount, 2)
        # Convert to INR first
        in_inr = amount * CurrencyService.get_rate_to_inr(from_curr)
        # Convert to target
        target_rate = CurrencyService.get_rate_to_inr(to_curr)
        return round(in_inr / target_rate, 2)

    @staticmethod
    def format_currency(amount: float, currency: str = "INR") -> str:
        curr_info = CURRENCIES.get(currency.upper(), CURRENCIES["INR"])
        sym = curr_info["symbol"]
        return f"{sym}{amount:,.0f}" if amount >= 100 else f"{sym}{amount:,.2f}"

currency_service = CurrencyService()
