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
#note each time /start is called make pd data series 

f = open('scale.csv')

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
        f.write(s+'\n')
        logging.info(s)
    except Exception as e:
        logging.error(f"handle_data: {e}")


def _run(device, UUID = ""):
    try:
        device.subscribe(UUID, callback = handle_data)
        for i in range(10):
            time.sleep(0.5)
    except Exception as e:
        logging.error(e)
    finally:
        device.unsubscribe(UUID)

def _scale():
    try:
        ADRESS = '03:B3:EC:8D:F0:F1'
        #ADRESS = '03:B3:EC:8D:EF:16'
        UUID   = "0000ffb2-0000-1000-8000-00805f9b34fb"
        #0000ffb2-0000-1000-8000-00805f9b34fb
        adapter= pygatt.GATTToolBackend()
        adapter.start()
        time.sleep(1)
        device = adapter.connect(ADRESS, timeout = 10)
        #for uuid in self.device.discover_characteristics().keys():
        _run(device, UUID = UUID)

    except Exception as e:
        logging.error(e)

    finally:
        adapter.stop()
        f.close()




if __name__ == '__main__':
    _scale()

