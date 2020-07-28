class Quote:
    """
    We use Quote objects to represent the bid/ask spread. When we encounter a
    'level change', a move of exactly 1 penny, we may attempt to make one
    trade. Whether or not the trade is successfully filled, we do not submit
    another trade until we see another level change.

    Note: Only moves of 1 penny are considered eligible because larger moves
    could potentially indicate some newsworthy event for the stock, which this
    algorithm is not tuned to trade.
    """

    def __init__(self):
        self.bid = 0
        self.ask = 0
        self.bid_size = 0
        self.ask_size = 0

    def update(self, data):
        """
        Overwrite current quotes with new data from the exchange
        """
        # extract price data
        self.bid_price = data.bidprice
        self.ask_price = data.askprice
        self.bid_size = data.bidsize
        self.ask_size = data.asksize
        self.timestamp = data.timestamp
        # calculate indicators
        self.spread = self.ask_price - self.bid_price
        self.midprice = self.calc_mp()
        self.vwmp = self.calc_vwmp()

    def calc_mp(self):
        """
        Calculate plain midprice
        """
        return (self.ask_price + self.bid_price) / 2

    def calc_vwmp(self):
        """
        Calculate volume weighted midprice
        """
        total_quantity = self.bid_size + self.ask_size
        weighted_bid = self.bid_price * self.ask_size
        weighted_ask = self.ask_price * self.bid_size
        return (weighted_bid + weighted_ask) / total_quantity 


class Position:
    """
    The position object is used to track how many shares we have. We need to
    keep track of this so our position size doesn't inflate beyond the level
    we're willing to trade with. Because orders may sometimes be partially
    filled, we need to keep track of how many shares are "pending" a buy or
    sell as well as how many have been filled into our account.
    """

    def __init__(self):
        self.open_orders = {}
        self.pending_buy_shares = 0
        self.pending_sell_shares = 0
        self.total_shares = 0

    def update_pending_buy_shares(self, quantity):
        self.pending_buy_shares += quantity

    def update_pending_sell_shares(self, quantity):
        self.pending_sell_shares += quantity

    def update_total_shares(self, quantity):
        self.total_shares += quantity

    def update_filled_amount(self, order_id, new_amount, side):
        old_amount = self.open_orders[order_id]['filled']
        if new_amount > old_amount:
            if side == "buy":
                self.update_pending_buy_shares(old_amount - new_amount)
                self.update_total_shares(new_amount - old_amount)
            else:
                self.update_pending_sell_shares(old_amount - new_amount)
                self.update_total_shares(old_amount - new_amount)
            self.open_orders[order_id]['filled'] = new_amount

    def remove_pending_order(self, order_id, side):
        """
        In case of cancellation or complete fill
        """
        old_amount = self.open_orders[order_id]['filled']
        total_amount = self.open_orders[order_id]['quantity']
        if side == "buy":
            self.update_pending_buy_shares(old_amount - total_amount)
        else:
            self.update_pending_sell_shares(old_amount - total_amount)
        del self.open_orders[order_id]

    def register_pending_order(self, order_id, qty, side)
        self.open_orders[order_id] = {
            'filled': 0, 
            'quantity': qty,
            'side': side
        }


