import argparse
import json
import sys

import requests

from bot.client import FuturesClient, BinanceAPIError
from bot.logging_config import setup_logger
from bot.orders import (
    place_order,
    get_order,
    cancel_order,
    print_order_summary,
    print_order_response,
)

logger = setup_logger()


def cmd_place(args: argparse.Namespace) -> None:
    """Place a new futures order."""
    try:
        client = FuturesClient()

        # Print what we're about to do
        print_order_summary(
            order_type=args.type.upper(),
            side=args.side.upper(),
            symbol=args.symbol.upper(),
            quantity=args.quantity,
            price=args.price,
        )

        response = place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )

        print_order_response(response)
        print("✅ Order placed successfully!\n")
        print("Full response:")
        print(json.dumps(response, indent=2))

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"\n❌ Validation error: {e}")
        sys.exit(1)
    except BinanceAPIError as e:
        logger.error(f"Binance API error [{e.code}]: {e.message}")
        print(f"\n❌ Binance API error: {e.message}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        logger.error("Network error: Could not connect to Binance Futures Testnet.")
        print("\n❌ Network error: Could not reach testnet.binancefuture.com — check your internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        logger.error("Request timed out.")
        print("\n❌ Request timed out. Try again.")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


def cmd_status(args: argparse.Namespace) -> None:
    """Check status of an existing order."""
    try:
        client = FuturesClient()
        response = get_order(client, args.symbol, args.order_id)

        print("\n📋 Order Status:")
        print_order_response(response)
        print("Full response:")
        print(json.dumps(response, indent=2))

    except BinanceAPIError as e:
        logger.error(f"Binance API error [{e.code}]: {e.message}")
        print(f"\n❌ Binance API error: {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


def cmd_cancel(args: argparse.Namespace) -> None:
    """Cancel an open order."""
    try:
        client = FuturesClient()
        response = cancel_order(client, args.symbol, args.order_id)

        print(f"\n🚫 Order {args.order_id} cancelled successfully.")
        print(json.dumps(response, indent=2))

    except BinanceAPIError as e:
        logger.error(f"Binance API error [{e.code}]: {e.message}")
        print(f"\n❌ Binance API error: {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="futures-bot",
        description="Binance Futures Testnet trading bot — place MARKET and LIMIT orders via CLI.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── place ──
    place = subparsers.add_parser("place", help="Place a new futures order.")
    place.add_argument("--symbol",   required=True,  type=str,   help="Trading pair, e.g. BTCUSDT")
    place.add_argument("--side",     required=True,  type=str,   help="BUY or SELL")
    place.add_argument("--type",     required=True,  type=str,   help="MARKET or LIMIT")
    place.add_argument("--quantity", required=True,  type=float, help="Order quantity (in base asset)")
    place.add_argument("--price",    required=False, type=float, default=None, help="Limit price (required for LIMIT orders)")
    place.set_defaults(func=cmd_place)

    # ── status ──
    status = subparsers.add_parser("status", help="Check an existing order's status.")
    status.add_argument("--symbol",   required=True, type=str, help="Trading pair, e.g. BTCUSDT")
    status.add_argument("--order-id", required=True, type=int, dest="order_id", help="Binance order ID")
    status.set_defaults(func=cmd_status)

    # ── cancel ──
    cancel = subparsers.add_parser("cancel", help="Cancel an open order.")
    cancel.add_argument("--symbol",   required=True, type=str, help="Trading pair, e.g. BTCUSDT")
    cancel.add_argument("--order-id", required=True, type=int, dest="order_id", help="Binance order ID")
    cancel.set_defaults(func=cmd_cancel)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
