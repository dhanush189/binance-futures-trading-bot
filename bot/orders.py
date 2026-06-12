from bot.client import FuturesClient, BinanceAPIError
from bot.logging_config import setup_logger
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_symbol,
    validate_limit_requires_price,
)

logger = setup_logger()

FUTURES_ORDER_ENDPOINT = "/api/v3/order"

def place_order(
    client: FuturesClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict:
    """
    Validate inputs and place a MARKET or LIMIT futures order.
    Returns the full API response dict.
    """
    # Validate all inputs first
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    validate_limit_requires_price(order_type, price)

    if price is not None:
        price = validate_price(price)

    # Build request params
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    logger.info(
        f"Placing {order_type} {side} order | Symbol: {symbol} | Qty: {quantity}"
        + (f" | Price: {price}" if price else "")
    )
    logger.debug(f"Order request params: {params}")

    response = client.post(FUTURES_ORDER_ENDPOINT, params)

    logger.info(
        f"Order placed successfully | OrderId: {response.get('orderId')} "
        f"| Status: {response.get('status')} "
        f"| ExecutedQty: {response.get('executedQty')} "
        f"| AvgPrice: {response.get('avgPrice') or response.get('fills', [{}])[0].get('price', 'N/A')}"
    )
    logger.debug(f"Full order response: {response}")

    return response


def get_order(client: FuturesClient, symbol: str, order_id: int) -> dict:
    """Fetch status of an existing order by ID."""
    symbol = validate_symbol(symbol)
    logger.info(f"Fetching order | OrderId: {order_id} | Symbol: {symbol}")

    response = client.get(FUTURES_ORDER_ENDPOINT, {
        "symbol": symbol,
        "orderId": order_id,
    })

    logger.info(f"Order {order_id} status: {response.get('status')}")
    return response


def cancel_order(client: FuturesClient, symbol: str, order_id: int) -> dict:
    """Cancel an open order by ID."""
    symbol = validate_symbol(symbol)
    logger.info(f"Cancelling order | OrderId: {order_id} | Symbol: {symbol}")

    response = client.delete(FUTURES_ORDER_ENDPOINT, {
        "symbol": symbol,
        "orderId": order_id,
    })

    logger.info(f"Order {order_id} cancelled | Status: {response.get('status')}")
    return response


def print_order_summary(order_type: str, side: str, symbol: str, quantity: float, price: float | None) -> None:
    """Print a clean summary of the order being placed."""
    print("\n" + "─" * 45)
    print("  ORDER REQUEST SUMMARY")
    print("─" * 45)
    print(f"  Symbol    : {symbol}")
    print(f"  Side      : {side}")
    print(f"  Type      : {order_type}")
    print(f"  Quantity  : {quantity}")
    if price:
        print(f"  Price     : {price}")
    print("─" * 45)


def print_order_response(response: dict) -> None:
    """Print clean order response details."""
    print("\n  ORDER RESPONSE")
    print("─" * 45)
    print(f"  Order ID    : {response.get('orderId', 'N/A')}")
    print(f"  Status      : {response.get('status', 'N/A')}")
    print(f"  Executed Qty: {response.get('executedQty', 'N/A')}")
    avg = response.get('avgPrice') or (response.get('fills') or [{}])[0].get('price', 'N/A')
    print(f"  Avg Price   : {avg}")
    print(f"  Symbol      : {response.get('symbol', 'N/A')}")
    print(f"  Side        : {response.get('side', 'N/A')}")
    print(f"  Type        : {response.get('type', 'N/A')}")
    print("─" * 45 + "\n")
