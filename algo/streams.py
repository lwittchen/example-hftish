import logging
import alpaca_trade_api as tradeapi 
from tools import Quote, Position

logger = logging.getLogger('__streams__')

def process_quote(channel: str, data: tradeapi.entity.Quote, old_quote: Quote):
    """
    Update quotes object with new prices
    """
    logger.info('Update Quote')
    old_quote.update(data=data)
    breakpoint()


def process_trade(channel: str, data: tradeapi.entity.Trade):
    """
    ...
    """
    if (
        data.size > 100
        and data.price == quote.ask
        and quote.bid_size > (quote.ask_size * 1.5)
    ):
        # post buy order
        try:
            o = api.submit_order(
                symbol=symbol,
                qty="100",
                side="buy",
                type="limit",
                time_in_force="day",
                limit_price=str(quote.ask),
            )
            # Approximate an IOC order by immediately cancelling
            api.cancel_order(o.id)
            position.register_pending_order(100)
            print("Buy at", quote.ask, flush=True)
        except Exception as e:
            print(e)
    elif (
        data.size > 100
        and data.price == quote.bid
        and quote.ask_size > (quote.bid_size * 1.5)
    ):
        # post sell order



def process_order(channel: str, data: tradeapi.entity.Entity, position: Position):
    """
    Process order response from Alpaca. 
    """
    event = data.event
    logger.info(f'Process Order Information - {event}')
    if event == "fill":
        if data.order["side"] == "buy":
            position.update_total_shares(int(data.order["filled_qty"]))
        else:
            position.update_total_shares(-1 * int(data.order["filled_qty"]))
        position.remove_pending_order(data.order["id"], data.order["side"])
    elif event == "partial_fill":
        position.update_filled_amount(
            data.order["id"], int(data.order["filled_qty"]), data.order["side"]
        )
    elif event == "canceled" or event == "rejected":
        position.remove_pending_order(data.order["id"], data.order["side"])