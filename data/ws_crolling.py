import csv

import pyupbit
import uuid
import json
import asyncio
import websockets
import traceback


def get_all_ticker():
    """데이터 수신할 TICKER 목록

    :return: krw_ticker: str[]
    """
    krw_ticker = pyupbit.get_tickers(fiat="KRW-BTC")
    return krw_ticker


async def connect_socket():
    """UPBIT 소켓 연결

    :return: None
    """
    while True:
        try:
            async with websockets.connect('wss://api.upbit.com/websocket/v1', ping_timeout=30,
                                          ping_interval=None, max_queue=10000) as websocket:
                subscribe_fmt = [
                    {'ticket': str(uuid.uuid4())[:6]},
                    {
                        'type': 'ticker',
                        'codes': get_all_ticker(),
                        'isOnlyRealtime': True
                    },
                ]
                subscribe_data = json.dumps(subscribe_fmt)
                await websocket.send(subscribe_data)

                while True:
                    try:
                        data = await websocket.recv()
                        data = json.loads(data)

                        if 'code' not in data:
                            print('[Data Error]', data)
                            continue

                        ticker = data['code'].split('-')[1]

                        with open('./UPBIT_HISTORY.csv', 'a', newline='') as file:
                            writer = csv.DictWriter(file, fieldnames=data.keys())
                            writer.writerow(data)

                        print(ticker, data)

                    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                        try:
                            pong = await websocket.ping()
                            await asyncio.wait_for(pong, timeout=30)
                        except:
                            await asyncio.sleep(30)
                            break
                    except:
                        traceback.print_exc()
        except:
            await asyncio.sleep(30)


async def run():
    """
    :return:
    """
    await asyncio.wait([
        asyncio.create_task(connect_socket()),
    ])


if __name__ == '__main__':
    asyncio.run(run())
