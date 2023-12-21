import pysherasync, asyncio, json

async def bitstamp_ob_subscription(loop):
    global loop 
    # This is your app key, currently set to https://www.bitstamp.net/websocket/ 
    appkey = "de504dc5763aeef9ff52"
    # Create an instance of PusherAsyncClient and pass it the appkey 
    pusherclient = pysherasync.PusherAsyncClient(appkey)
    # Connect to websocket 
    pushersocket = await pusherclient.connect()
    # Subscribe to channel 
    status = await pusherclient.subscribe(channel_name='prod-{}-trades'.format('BTCCLP'))
    print("Subscription Status: %s"%(status))
    while True:
        ## This is because re-connection logic is not implemented yet
        if not pushersocket.open:
            # on disconnections, reconnect
            print("Connection reconnecting")
            # re-connect
            pushersocket = await pusherclient.connect()
            # re-subscribe 
            status = await pusherclient.subscribe(channel_name='prod-{}-trades'.format('BTCCLP'))
            print("Subscription Status: %s"%(status))
        try:
            # wait for msg
            msg = await asyncio.wait_for(pushersocket.recv(), 5)
            # parse to json 
            msg = json.loads(msg)
            # print the msg 
            if msg:
                print(msg)        
        except asyncio.TimeoutError:
            print("asyncio timeout while waiting for ws msg")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bitstamp_ob_subscription(loop))
    loop.close()

