import time
import logging
from config.settings import DEMO_MODE_PAYMENTS, PAYMENT_API_KEY
from utils.helpers import generate_reference_id

logger = logging.getLogger(__name__)


class PaymentService:
    @staticmethod
    def initiate_transaction(amount: float, booking_reference: str, method: str = "DEMO_UPI") -> dict:
        """Initiates a payment order."""
        payment_ref = generate_reference_id("PAY")
        
        # If live payment credentials were provided, Razorpay/Stripe client logic would trigger here
        if not DEMO_MODE_PAYMENTS:
            logger.info("Initializing live payment gateway integration...")
            # e.g., razorpay_client.order.create(...)

        return {
            "payment_reference": payment_ref,
            "booking_reference": booking_reference,
            "amount": amount,
            "currency": "INR",
            "method": method,
            "status": "INITIATED",
            "is_demo": DEMO_MODE_PAYMENTS
        }

    @staticmethod
    def process_payment(payment_ref: str, amount: float, method: str = "UPI / NetBanking") -> dict:
        """Processes transaction and simulates immediate verification in Demo Mode."""
        # Simulated payment network latency
        time.sleep(0.3)
        
        return {
            "payment_reference": payment_ref,
            "amount": amount,
            "currency": "INR",
            "payment_method": method,
            "status": "SUCCESS",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "is_demo": DEMO_MODE_PAYMENTS
        }
