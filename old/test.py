#### code snippts from official alpaca api for python
#### //link 

import alpaca_trade_api as tradeapi
import logging
from pprint import pprint

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
    datefmt="%m-%d %H:%M",
)

api = tradeapi.REST(
    key_id="PKL805CHIPIN8UDATO1N",
    secret_key="BEscMquBc6qg5K9F3dWEfBVRdPs5d1ILaNxYpdlt",
    api_version="v2",
    base_url="https://paper-api.alpaca.markets",
)
account = api.get_account()
open_pos = api.list_positions()

print('-'*50)
print('-'*50)
print('-'*50)
print(account.status)
print(open_pos)
print('-'*50)
print('-'*50)
print('-'*50)

conn = tradeapi.StreamConn(
    key_id="PKL805CHIPIN8UDATO1N",
    secret_key="BEscMquBc6qg5K9F3dWEfBVRdPs5d1ILaNxYpdlt",
    base_url="https://paper-api.alpaca.markets",
)

@conn.on(r'.*')
async def on_data(conn, channel, data):
    print('-'*50, 'New Message')
    print(channel)
    pprint(data)


# A.SPY will work, because it only goes to Polygon
conn.run(['trade_updates', 'Q.AAPL', 'T.AAPL'])
# conn.run(['trade_updates', 'AM.AAPL', 'A.AAPL', 'status' 'T.AAPL'])


# @conn.on(r"^trade_updates$")
# async def on_account_updates(conn, channel, account):
#     print("account", account)


# @conn.on(r"^status$")
# async def on_status(conn, channel, data):
#     print("polygon status update", data)


# @conn.on(r"^AM$")
# async def on_minute_bars(conn, channel, bar):
#     print("bars", bar)


# @conn.on(r"^A$")
# async def on_second_bars(conn, channel, bar):
#     print("bars", bar)


# @conn.on(r"Q$")
# async def on_quote(conn, channel, data):
#     print("Quote received")
#     # Quote update received
#     print(data)


# @conn.on(r"T$")
# async def on_trade(conn, channel, data):
#     print("Trade received")
#     print(data)


# # blocks forever
# qc = "Q.SNAP"
# tc = "T.SNAP"
# conn.run(["trade_updates", tc, qc])
