"""Object and functions for working with Loans for Game Simulations."""


from dataclasses import dataclass
import logging

log: logging.Logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Loan:
    """Object to manage Loans in Game Simulations."""

    name: str
    balance: int
    monthly_payment: int
    partial_payment_allowed: bool = False

    def make_payment(self, *, payment: int) -> bool:
        """Make a Payment on a Loan."""
        log.info(f"Making a Payment on a Loan: {self.name}")
        log.info(f"self.partial_payment_allowed: {self.partial_payment_allowed}")
        log.info(f"payment: {payment}")
        log.info(f"self.balance: {self.balance}")
        if (
            (not self.partial_payment_allowed and payment != self.balance)
            or (payment % 1000) != 0
            or payment < 1000
            or payment > self.balance
        ):
            log.info(f"Not able to make payment on the loan")
            return False

        if payment == self.balance:
            log.info(
                f"Loan is being paid-off. This leaves a zero balance loan on player's books"
            )
        log.info(f"Able to make payment on the loan")
        self.balance -= payment
        log.info(f"New balance: {self.balance}")

        # Rule for Bank Loan, the only partially payable loan
        self.monthly_payment = int(self.balance * 0.10)
        return True

    def __str__(self):
        """Create string to be returned when str method is called."""
        return (
            f"Loan Name:             {self.name}"
            f"\n   Loan Balance:       {self.balance}"
            f"\n   Loan Payment:       {self.monthly_payment}"
            f"\n   Part. Pay. Allowed: {self.partial_payment_allowed}"
        )
