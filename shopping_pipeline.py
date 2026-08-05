"""
shopping_pipeline.py
======================
Level 3: Online Shopping Assistant, rebuilt on the shared Agent base class.
"""

import logging
from dataclasses import dataclass, field

import config
from base_agent import Agent
from data_loader import load_products

logger = logging.getLogger("Shopping")


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------
@dataclass
class ShoppingSharedState:
    cart: list = field(default_factory=list)
    cart_total: float = 0.0
    total_discount: float = 0.0
    tax_amount: float = 0.0
    payable: float = 0.0
    payment_method: str = ""


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------
class ProductAgent(Agent):
    def process(self, state: ShoppingSharedState):
        state.cart = load_products(config.PRODUCTS_CSV)
        return state


class CartAgent(Agent):
    required_keys = ["cart"]

    def process(self, state: ShoppingSharedState):
        for item in state.cart:
            item.subtotal = round(item.price * item.qty, 2)
        state.cart_total = round(sum(item.subtotal for item in state.cart), 2)
        return state


class DiscountAgent(Agent):
    required_keys = ["cart"]

    def process(self, state: ShoppingSharedState):
        total_discount = 0.0
        for item in state.cart:
            item_discount = (
                item.subtotal * config.BULK_DISCOUNT_RATE
                if item.qty >= config.BULK_QTY_THRESHOLD else 0
            )
            item.discount = round(item_discount, 2)
            total_discount += item_discount

        if state.cart_total > config.CART_DISCOUNT_THRESHOLD:
            total_discount += state.cart_total * config.CART_DISCOUNT_RATE

        state.total_discount = round(total_discount, 2)
        return state


class ShoppingTaxAgent(Agent):
    required_keys = ["cart"]

    def process(self, state: ShoppingSharedState):
        taxable = state.cart_total - state.total_discount
        state.tax_amount = round(taxable * config.TAX_RATE, 2)
        return state


class PaymentAgent(Agent):
    required_keys = ["cart"]

    def process(self, state: ShoppingSharedState):
        state.payable = round(
            state.cart_total - state.total_discount + state.tax_amount, 2
        )
        state.payment_method = (
            "Credit Card" if state.payable > config.CARD_PAYMENT_THRESHOLD else "UPI"
        )
        return state


class InvoiceAgent(Agent):
    required_keys = ["cart"]

    def process(self, state: ShoppingSharedState):
        logger.info("=" * 50)
        logger.info("INVOICE")
        logger.info("=" * 50)
        for item in state.cart:
            logger.info(
                f"{item.item} x{item.qty} = ₹{item.subtotal} "
                f"(-₹{item.discount} discount)"
            )
        logger.info(f"Cart Total: ₹{state.cart_total}")
        logger.info(f"Discount: -₹{state.total_discount}")
        logger.info(f"Tax: +₹{state.tax_amount}")
        logger.info(f"Payable: ₹{state.payable} via {state.payment_method}")
        return state


# ---------------------------------------------------------------------------
# Pipeline builder
# ---------------------------------------------------------------------------
def build_shopping_pipeline():
    from supervisor import Supervisor
    return Supervisor(
        agents=[
            ProductAgent(),
            CartAgent(),
            DiscountAgent(),
            ShoppingTaxAgent(),
            PaymentAgent(),
            InvoiceAgent(),
        ],
        state_factory=ShoppingSharedState,
        name="Shopping Assistant",
    )
