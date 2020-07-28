import argparse
import sys
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi

import config as cfg
import streams
from tools import Quote, Position

def run():
    global quote 
    global position 

    # init global variables
    quote = Quote()
    position = Position()

    # inputs
    symbol = 'SNAP'
    max_shares = 500
    opts = dict(
        base_url="https://paper-api.alpaca.markets",
        **cfg.keys
    )
    
    # Create API objects which can be used to submit orders, stream data etc.
    api = tradeapi.REST(**opts)
    conn = tradeapi.StreamConn(**opts)

    # Initiliaze our message handling
    @conn.on(r"Q.*$")
    async def on_quote(conn, channel, data):
        """
        Quote update
        """
        streams.process_quote(channel, data, old_quote=quote)

    @conn.on(r"T.*$")
    async def on_trade(conn, channel, data):
        """
        Trade update
        """
        streams.process_trade(channel, data)

    @conn.on(r"trade_updates")
    async def on_trade_updates(conn, channel, data, position=position):
        """
        Order update
        """
        streams.process_order(channel, data)

    # start listening - blocks forever
    conn.run(["trade_updates", f"T.{symbol}", f"Q.{symbol}"])


if __name__ == "__main__":
    run()
