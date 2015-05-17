from liblo import ServerThread, ServerError, make_method

import sys
import time

import threading as th
from copy import deepcopy

import numpy as np
from numpy.fft import fft
from collections import deque

#from detect_movement import *

class MuseServer(ServerThread):

    acc_lock = None
    acc_list = None

    blink_lock = None
    blink_list = None

    jaw_lock = None
    jaw_list = None

    # listen for messages on port 5001

    def __init__(self):
        self.acc_lock = th.RLock()
        self.acc_list = []

        self.blink_lock = th.RLock()
        self.blink_list = deque()

        self.jaw_lock = th.RLock()
        self.jaw_list = deque()

        ServerThread.__init__(self, 5001)

    # receive accelrometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):

        self.acc_lock.acquire()
        self.acc_list.append(args)
        self.acc_lock.release()

        acc_x, acc_y, acc_z = args

        #print ("%s %f %f %f" % (path, acc_x, acc_y, acc_z))

    # receive blink data
    @make_method('/muse/elements/blink', 'i')
    def blink_callback(self, path, args):

        if args[0]:
            self.blink_lock.acquire()
            self.blink_list.append(time.time())
            self.blink_lock.release()

    # receive blink data
    @make_method('/muse/elements/jaw_clench', 'i')
    def jaw_callback(self, path, args):

        if args[0]:
            self.jaw_lock.acquire()
            self.jaw_list.append(time.time())
            self.jaw_lock.release()

    @make_method(None, None)
    def fallback(self, path, args, types, src):
        pass


if __name__ == "__main__":

    try:
        server = MuseServer()

    except ServerError as err:

        print(str(err))

        sys.exit()

    server.start()

    t = 0.5

    while 1:
        server.acc_lock.acquire()
        tmp = list(zip(*server.acc_list))
        server.acc_list = []
        server.acc_lock.release()

        if tmp:
            size = len(tmp[0])
            fs = [i / t for i in range(size // 2)]
            tmp = [np.array(x) - sum(x) / len(x) for x in tmp]
            acc_fft = [fft(x)[: size // 2] for x in tmp]
            imax = [sorted(enumerate(x), key=lambda k: abs(k[1]))[-1] for x in acc_fft]
            print(fs[imax[0][0]], fs[imax[0][0]] * 60)
            print(pravila(tmp, duration=t, debug=True))

        time.sleep(t)
