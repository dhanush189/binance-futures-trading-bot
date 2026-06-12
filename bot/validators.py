from bot.logging_config import setup_logger

logger = setup_logger()

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_side(side: str) -> str:
    """Validate order side is BUY or SELL."""
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be BUY or SELL.")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type is MARKET or LIMIT."""
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be MARKET or LIMIT.")
    return order_type


def validate_quantity(quantity: float) -> float:
    """Quantity must be a positive number."""
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0, got {quantity}.")
    return quantity


def validate_price(price: float) -> float:
    """Price must be a positive number."""
    if price <= 0:
        raise ValueError(f"Price must be greater than 0, got {price}.")
    return price


def validate_symbol(symbol: str) -> str:
    """Normalize symbol to uppercase."""
    return symbol.upper().strip()


def validate_limit_requires_price(order_type: str, price: float | None) -> None:
    """LIMIT orders must have a price."""
    if order_type == "LIMIT" and price is None:
        raise ValueError("LIMIT orders require --price to be specified.")
