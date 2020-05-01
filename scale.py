import pygatt
import time
import logging
import os
import pdb
import asyncio
import pandas as pd
import numpy  as np
import binascii

from binascii import hexlify
from pygatt.util import uuid16_to_uuid

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

ADRESS = '03:B3:EC:8D:F0:F1'
#03:B3:EC:8D:EF:16
UUID   = "0000ffb2-0000-1000-8000-00805f9b34fb"
#0000ffb2-0000-1000-8000-00805f9b34fb
HANDLE = b"0x0018"
HANDLE = b"0x18"

a = np.empty(1000,dtype='str')

VAR    = None
adapter= pygatt.GATTToolBackend()
#note each time /start is called make pd data series 

"""

import pandas as pd
from io import StringIO
from tabulate import tabulate

c = Chromosome Start End
chr1 3 6
chr1 5 7
chr1 8 9

df = pd.read_table(StringIO(c), sep="\s+", header=0)

print(tabulate(df, headers='keys', tablefmt='psql'))

+----+--------------+---------+-------+
|    | Chromosome   |   Start |   End |
|----+--------------+---------+-------|
|  0 | chr1         |       3 |     6 |
|  1 | chr1         |       5 |     7 |
|  2 | chr1         |       8 |     9 |
+----+--------------+---------+-------+
"""

def _parse(s):
    # # # # # # # # #
    # # #  # # #3# # #
    # # #   # # # # #
    sign = 1
    unit = None
    array = s.split('-')

    #number
    print(array)
    k = array[3] #first  2 bits
    n = array[4] #second 2 bits
    m = array[5] #sign
    print(f"k {k} , n {n}, m {m}")

    if m == '01':
        sign = -1

    i = int(k + n, 16)
    print(f"{k}+{n} = {i}")

    if array[6] == '33':
        sign = -1
        unit = 'oz'

    elif array[6] == '32':
        unit = 'oz'

    else:
        unit = 'g'
    return f"{i} {unit}"
    

class BLE:

    _VAR = None
    i    = 0
    DF     = pd.Series(data = a, dtype = str)

    def __init__(self, *args, **kwargs):
        adapter.start()
        logging.info("Started adapter")

    def start(self):
        try:
            self.device = adapter.connect(ADRESS, timeout = 10)
        except Exception as e:
            print(BLE.DF)
            logging.error(e)

        finally:
            logging.error("started")

    #@Client.client.on(events.NewMessage(pattern='/start'))
    async def _start(self, event):
        #self.start()
        self.device = adapter.connect(ADRESS, timeout = 5)
        await asyncio.sleep(1)
        logging.info("Connected device")
        await event.respond(f'Scale ')

    @staticmethod
    def handle_data(handle, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        try:
            #df = pd.Series()
            print(value)
            s = hexlify(value, '-').decode()
            s = _parse(s)
            BLE._VAR = s
            BLE.i   += 1
            BLE.DF[BLE.i] = BLE._VAR
            #DF[BLE.i] = s
            logging.info(s)
        except Exception as e:
            logging.error(f"handle_data: {e}")

    #async def _run(self):
    def _run(self):
        #try:
        logging.info("subscribed to uuid")
        UUID   = "0000ffb2-0000-1000-8000-00805f9b34fb"

        self.device = adapter.connect(ADRESS)
        #self.device.subscribe(UUID, callback=BLE.handle_data)
        
        for i in range(10):
            time.sleep(0.5)

            print("Read UUID %s: %s" % (UUID, binascii.hexlify(self.device.char_read(UUID))))
        #for uuid in self.device.discover_characteristics().keys():


        #for UUID in self.device.discover_characteristics().keys():
        #    print("Read UUID %s: %s" % (UUID, binascii.hexlify(self.device.char_read(UUID))))

        #await asyncio.sleep(0.5)
        #logging.info(f"BLE: {BLE._VAR}")
        #print(DF.to_markdown())
        #print(BLE.DF)
        #self.device.unsubscribe(UUID)
        #logging.info("unsubscribed")


if __name__ == '__main__':
    try:
        ble = BLE()
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(ble._run())
        ble._run()
        print(BLE.DF)
    

    except Exception as e:
        logging.error(e)
        print(BLE.DF)

    finally:
        logging.info("end")
        adapter.stop()


