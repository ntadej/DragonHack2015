# coding: UTF-8
import sys
import time
import itertools
import numpy as np
from numpy.fft import fft
from collections import deque

import threading as th
import flask as fl
from flask import Flask, render_template, request, Response, redirect, url_for
from server import MuseServer
from search_yt_by_word import Search
from detect_movement import pravila


app = Flask(__name__)
calculatedBeat = 0
mainLock = th.RLock()
search = Search()
yt_id = ""

acc_data_num = 0
dq = deque()
headLock = th.RLock()


def serve():
    global calculatedBeat, yt_id

    t = 5

    while 1:
        server.acc_lock.acquire()
        tmp = list(zip(*server.acc_list))
        server.acc_list = []
        server.acc_lock.release()

        if tmp and tmp[0]:
            size = len(tmp[0])
            fs = [i / t for i in range(size // 2)]
            tmp = [np.array(x) - sum(x) / len(x) for x in tmp]
            acc_fft = [fft(x)[: size // 2] for x in tmp]
            imax = [sorted(enumerate(x), key=lambda k: abs(k[1]))[-1] for x in acc_fft]
            print(fs[imax[0][0]], fs[imax[0][0]] * 60)

            mainLock.acquire()
            calculatedBeat = fs[imax[0][0]] * 60
            local_beat = calculatedBeat
            mainLock.release()

            local_id = search.search_all(local_beat)

            yt_id = local_id

        acc_data_num = 0
        for i in range(10):
            server.acc_lock.acquire()
            tmp = list(zip(*server.acc_list))
            server.acc_lock.release()

            n2 = len(tmp)
            tmp = tmp[acc_data_num:]
            acc_data_num = n2
            podatki = pravila(tmp, duration=t/10)
            headLock.acquire()
            if "ndesno" in podatki:
                dq.append("ndesno")
            headLock.release()

            time.sleep(t / 10.0)


@app.route('/')
def index():
    global calculatedBeat

    mainLock.acquire()
    calculatedBeat = 0
    yt_id = ""
    search.clear()
    mainLock.release()

    return render_template('index.html')


@app.route('/headswipe')
def headswipe():
    def events():
        while 1:
            headLock.acquire()
            event = len(dq) or dq.pop()
            headLock.release()
            if event != 0:
                yield "event: headevent\ndata: %s\n\n" % (event)

            time.sleep(0.1)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


@app.route('/blink')
def blink():
    def events():
        while 1:
            server.blink_lock.acquire()
            event = len(server.blink_list) or server.blink_list
            server.blink_lock.release()
            if event != 0:
                yield "event: blinkevent\ndata: %s\n\n" % (event)

            time.sleep(0.05)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


@app.route('/jaw')
def jaw():
    def events():
        while 1:
            server.jaw_lock.acquire()
            event = len(server.jaw_list) or server.jaw_list
            server.jaw_lock.release()
            if event != 0:
                yield "event: jawclench\ndata: %s\n\n" % (event)

            time.sleep(0.05)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


@app.route('/bpm')
def bpm():
    def events():
        while 1:
            mainLock.acquire()
            tmpCalculatedBeat = calculatedBeat
            mainLock.release()
            if tmpCalculatedBeat != 0 and yt_id != "":
                yield "event: calculated\ndata: {\"bpm\": %d, \"yt_id\": \"%s\"}\n\n" % (tmpCalculatedBeat, yt_id)

            server.acc_lock.acquire()
            tmpMove = 0
            if server.acc_list and server.acc_list[-1]:
                tmpMove = server.acc_list[-1][0]
            server.acc_lock.release()
            if tmpMove != 0:
                yield "event: move\ndata: %d\n\n" % (tmpMove)

            #yield "event: test\ndata: %d\n\n" % (calculatedBeat)
            time.sleep(0.02)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


if __name__ == '__main__':
    server = MuseServer()
    server.start()

    ser = th.Thread(target=serve)
    ser.start()
    print("Starting local server")
    # serve()
    app.run("0.0.0.0", port=8080, threaded=True)

